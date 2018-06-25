#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)
#
# This file is part of libSigNetSim.
#
# libSigNetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libSigNetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libSigNetSim.  If not, see <http://www.gnu.org/licenses/>.

"""

	This file ...

"""
from __future__ import print_function

from libsignetsim.model.math.CFE import CFE
from libsignetsim.model.math.ODE import ODE
from libsignetsim.model.math.MathSubmodel import MathSubmodel
from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger, SympyEqual
from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from libsignetsim.model.math.container.ListOfConservationLaws import ListOfConservationLaws
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

from sympy import solve, pprint, pretty


class MathSlowModel(MathSubmodel):
	""" Sbml model class """

	def __init__(self, sbml_model=None, reduced_model=None):
		""" Constructor of model class """

		MathSubmodel.__init__(self, parent_model=reduced_model)

		self.sbmlModel = sbml_model
		self.reducedModel = reduced_model

		self.fastLaws = []
		self.fastLaws_vars = []

		self.fastStoichiometryMatrix = MathStoichiometryMatrix(sbml_model)
		self.slowStoichiometryMatrix = MathStoichiometryMatrix(sbml_model)
		self.fastConservationLaws = ListOfConservationLaws(sbml_model)
		self.DEBUG = False

	def copyEquations(self):

		for cfe in self.reducedModel.listOfCFEs:
			t_var = self.listOfVariables.getBySymbol(cfe.getVariable().symbol.getSymbol())
			t_cfe_formula = MathFormula(self)
			t_cfe_formula.setInternalMathFormula(cfe.getDefinition().getDeveloppedInternalMathFormula())
			t_cfe = CFE(self)
			t_cfe.new(t_var, t_cfe_formula)
			self.listOfCFEs.append(t_cfe)

		for ode in self.reducedModel.listOfODEs:
			original_variable = self.sbmlModel.listOfVariables.getBySymbol(ode.getVariable().symbol.getSymbol())
			if original_variable.isRateRuled():
				t_var = self.listOfVariables.getBySymbol(ode.getVariable().symbol.getSymbol())
				t_ode_formula = MathFormula(self)
				t_ode_formula.setInternalMathFormula(ode.getDefinition().getDeveloppedInternalMathFormula())
				t_ode = ODE(self)
				t_ode.new(t_var, t_ode_formula)
				self.listOfODEs.append(t_ode)

	def findFastReactions(self):
		""" Finds the fast reactions and build the fast stoichiometry matrix """

		for reaction in self.sbmlModel.listOfReactions:
			if reaction.fast:
				self.fastLaws.append(reaction.kineticLaw.getDefinition().getDeveloppedInternalMathFormula())

				for reactant in reaction.listOfReactants:
					self.fastLaws_vars.append(reactant.getSpecies().symbol.getDeveloppedInternalMathFormula())

				for product in reaction.listOfProducts:
					self.fastLaws_vars.append(product.getSpecies().symbol.getDeveloppedInternalMathFormula())

	def findVelocities(self, subs={}, include_fast_reaction=True, include_slow_reaction=True):

		matrix_velocities = None
		for reaction in self.sbmlModel.listOfReactions:
			velocities = reaction.kineticLaw.getRawVelocities(
				subs=subs,
				include_fast_reaction=include_fast_reaction,
				include_slow_reaction=include_slow_reaction
			)

			if matrix_velocities is None:
				matrix_velocities = velocities
			else:
				matrix_velocities = matrix_velocities.col_join(velocities)

		return matrix_velocities

	def __findKeptVariables(self):

		original_variables = [var.symbol.getSymbol() for var in self.reducedModel.variablesOdes]
		kept_variables = []
		for i, var in enumerate(self.sbmlModel.variablesOdes):
			if var.symbol.getSymbol() in original_variables:
				kept_variables.append(i)

		return kept_variables

	def __buildStoichiometryMatrices(self, kept_variables):

		self.fastStoichiometryMatrix.build(including_slow_reactions=False)
		self.slowStoichiometryMatrix.build(including_fast_reactions=False)
		self.findFastReactions()

		fast_matrix = self.fastStoichiometryMatrix.stoichiometryMatrix
		slow_matrix = self.slowStoichiometryMatrix.stoichiometryMatrix

		return (fast_matrix[kept_variables, :], slow_matrix[kept_variables, :])

	def __buildODEs(self, slow_system, slow_variables, subs):

		for i, symbol in enumerate(slow_variables):
			variable = self.listOfVariables.getBySymbol(symbol)

			t_definition = MathFormula(self)
			t_definition.setInternalMathFormula(unevaluatedSubs(sum(slow_system[i, :]), subs))

			ode = ODE(self)
			ode.new(variable, t_definition)
			self.listOfODEs.append(ode)

	def __buildCFEs(self, fast_laws, fast_vars, subs):

		for law in fast_laws:

			law = unevaluatedSubs(law, subs)
			intersect = set(fast_vars).intersection(set(law.atoms(SympySymbol)))
			if len(intersect) > 0:
				var = list(intersect)[0]

				if self.DEBUG:
					print(pretty(law))
					print(pretty(var))

				res = solve(law, var)

				t_var = self.listOfVariables.getBySymbol(var)
				t_cfe = MathFormula(self)
				t_cfe.setInternalMathFormula(res[0])

				cfe = CFE(self)
				cfe.new(t_var, t_cfe)

				self.listOfCFEs.append(cfe)
				self.listOfVariables.changeVariableType(t_var, MathVariable.VAR_ASS)

		self.listOfCFEs.developCFEs()

	def __classifyVariables(self, kept_variables):

		slow_variables = []
		fast_variables = []
		for var in kept_variables:
			variable = self.sbmlModel.variablesOdes[var]
			if variable.isSpecies() and not variable.isOnlyInFastReactions():
				slow_variables.append(variable.symbol.getSymbol())
			else:
				fast_variables.append(variable.symbol.getSymbol())

		return slow_variables, fast_variables

	def build(self):

		if self.DEBUG:
			print(">> Building slow model")

		self.copyVariables()
		self.copyEquations()

		kept_variables = self.__findKeptVariables()
		if self.DEBUG:
			print("> Variables kept in the reduced model : %s" % str(kept_variables))

		fast_matrix, slow_matrix = self.__buildStoichiometryMatrices(kept_variables)

		fast_velocities = self.findVelocities(include_slow_reaction=False)
		slow_velocities = self.findVelocities(include_fast_reaction=False)

		fast_system = fast_matrix * fast_velocities
		slow_system = slow_matrix * slow_velocities

		if self.DEBUG:
			print("> Fast system matrix")
			pprint(fast_system)
			print("\n")

			print("> Slow system matrix")
			pprint(slow_system)
			print("\n")

		subs = self.reducedModel.listOfCFEs.getSubs()
		slow_variables, fast_variables = self.__classifyVariables(kept_variables)

		self.__buildODEs(slow_system, slow_variables, subs)
		self.__buildCFEs(self.fastLaws, fast_variables, subs)

		# Computing new initial values
		system_vars = self.fastLaws_vars

		subs = {}
		for var, math_formula in list(self.sbmlModel.listOfInitialConditions.items()):
			variable = self.sbmlModel.listOfVariables.getBySymbol(var)
			if var not in system_vars or variable.boundaryCondition:
				subs.update({var: math_formula.getDeveloppedInternalMathFormula()})

		if self.DEBUG:
			print("> Known initial values : %s" % pretty(subs))

		system = []

		# Solving the initial values using the fast conservation laws, and the fast laws.
		for cons_law in self.fastConservationLaws.getRawFormulas(self.fastStoichiometryMatrix):
			formula = unevaluatedSubs(cons_law, subs)
			if formula not in [True, False]:
				system.append(formula)

		for fast_law in self.fastLaws:
			formula = SympyEqual(unevaluatedSubs(fast_law, subs), SympyInteger(0))
			if formula not in [True, False]:
				system.append(formula)

		if self.DEBUG:
			print(system)
			print(system_vars)

		res = solve(system, system_vars)

		if self.DEBUG:
			print(res)

		for var, value in list(res.items()):
			math_formula = MathFormula(self)
			math_formula.setInternalMathFormula(unevaluatedSubs(value, subs))

			self.listOfInitialConditions.update({var: math_formula})

		self.setUpToDate(True)
