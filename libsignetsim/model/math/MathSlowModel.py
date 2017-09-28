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

from libsignetsim.model.math.DAE import DAE
from libsignetsim.model.math.CFE import CFE
from libsignetsim.model.math.ODE import ODE
from libsignetsim.model.math.MathSubmodel import MathSubmodel
from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyZero, SympyInteger, SympyEqual, SympyUnequal, SympyTrue, SympyDerivative
from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from libsignetsim.model.math.container.ListOfConservationLaws import ListOfConservationLaws

from sympy import solve, eye, pprint, Lambda, flatten, expand


class MathSlowModel(MathSubmodel):
	""" Sbml model class """

	def __init__ (self, sbml_model=None, reduced_model=None):
		""" Constructor of model class """

		MathSubmodel.__init__(self, parent_model=reduced_model)

		# self.parentModel = parent_model
		self.sbmlModel = sbml_model
		self.reducedModel = reduced_model

		self.fastLaws = []
		self.fastLaws_vars = []

		self.fastStoichiometryMatrix = MathStoichiometryMatrix(sbml_model)
		self.slowStoichiometryMatrix = MathStoichiometryMatrix(sbml_model)

		# Function returning a boolean if the value is not zero
		self.notZeroFilter = Lambda(
			SympySymbol('x'),
			SympyUnequal(
				SympySymbol('x'),
				SympyInteger(0)
			)
		)

		# Function returning a boolean if the value is zero
		self.ZeroFilter = Lambda(
			SympySymbol('x'),
			SympyEqual(
				SympySymbol('x'),
				SympyInteger(0)
			)
		)

	def copyEquations(self):

		for cfe in self.reducedModel.listOfCFEs:
			t_var = self.listOfVariables.getBySymbol(cfe.getVariable().symbol.getSymbol())
			t_cfe_formula = MathFormula(self)
			t_cfe_formula.setInternalMathFormula(cfe.getDefinition().getDeveloppedInternalMathFormula())
			t_cfe = CFE(self)
			t_cfe.new(t_var, t_cfe_formula)
			self.listOfCFEs.append(t_cfe)

	def findFastReactions(self):
		""" Finds the fast reactions and build the fast stoichiometry matrix """

		for reaction in self.sbmlModel.listOfReactions.values():
			if reaction.fast:
				self.fastLaws.append(reaction.kineticLaw.getDefinition().getDeveloppedInternalMathFormula())

				for reactant in reaction.listOfReactants.values():
					self.fastLaws_vars.append(reactant.getSpecies().symbol.getDeveloppedInternalMathFormula())

				for product in reaction.listOfProducts.values():
					self.fastLaws_vars.append(product.getSpecies().symbol.getDeveloppedInternalMathFormula())

	def findVelocities(self, subs={}, include_fast_reaction=True, include_slow_reaction=True):

		matrix_velocities = None
		for reaction in self.sbmlModel.listOfReactions.values():
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


	def build(self):

		DEBUG = False

		self.copyVariables()
		self.copyEquations()
		self.fastStoichiometryMatrix.build(including_slow_reactions=False)
		self.slowStoichiometryMatrix.build(including_fast_reactions=False)
		self.findFastReactions()

		fast_matrix = self.fastStoichiometryMatrix.rawStoichiometryMatrix.transpose()
		slow_matrix = self.slowStoichiometryMatrix.rawStoichiometryMatrix.transpose()
		fast_velocities = self.findVelocities(include_slow_reaction=False)
		slow_velocities = self.findVelocities(include_fast_reaction=False)
		subs = self.reducedModel.listOfCFEs.getSubs()

		kept_variables = []
		for i, var in enumerate(self.sbmlModel.variablesOdes):
			if (var.symbol.getSymbol() in [var2.symbol.getSymbol() for var2 in self.reducedModel.variablesOdes]):# and not var.boundaryCondition):

				if DEBUG:
					print "%s : %s" % (var.symbol.getSymbol(), str(var.boundaryCondition))
				kept_variables.append(i)

		if DEBUG:
			print [var.symbol.getSymbol() for var in self.sbmlModel.variablesOdes]
			print [var.symbol.getSymbol() for var in self.reducedModel.variablesOdes]
			print kept_variables


		# if DEBUG:
		# 	print "> Fast stoichiometry matrix"
		# 	pprint(fast_matrix)
		# 	print "\n"
		#
		#
		# 	print "> Slow stoichiometry matrix"
		# 	pprint(slow_matrix)
		# 	print "\n"

		fast_matrix = fast_matrix[kept_variables,:]
		slow_matrix = slow_matrix[kept_variables,:]

		if DEBUG:
			print "> Fast stoichiometry matrix"
			pprint(fast_matrix)
			print "\n"


			print "> Slow stoichiometry matrix"
			pprint(slow_matrix)
			print "\n"

		fast_system = fast_matrix * fast_velocities
		slow_system = slow_matrix * slow_velocities
		full_system = fast_system + slow_system



		if DEBUG:
			print "> Fast system matrix"
			pprint(fast_system)
			print "\n"

			print "> Slow system matrix"
			pprint(slow_system)
			print "\n"

			print "> Full system matrix"
			pprint(full_system)
			print "\n"

		nullspace = fast_matrix.transpose().nullspace()

		matrix_nullspace = None
		for sol in nullspace:
			if matrix_nullspace is None:
				matrix_nullspace = sol
			else:
				matrix_nullspace = matrix_nullspace.row_join(sol)

		if DEBUG:
			pprint(matrix_nullspace)

		reduced_slow_system = matrix_nullspace.transpose() * slow_system




		slow_variables = []
		for i in range(reduced_slow_system.shape[0]):
			t_symbol = self.sbmlModel.variablesOdes[kept_variables[i]].symbol.getSymbol()
			slow_variables.append(t_symbol)

			if DEBUG:
				pprint(SympyEqual(
					SympyDerivative(t_symbol,SympySymbol("t")),
					sum(reduced_slow_system[i,:]).subs(subs)
				))

			t_var = self.listOfVariables.getBySymbol(t_symbol)

			t_definition = MathFormula(self)
			t_definition.setInternalMathFormula(sum(reduced_slow_system[i,:]).subs(subs))

			ode = ODE(self)
			ode.new(t_var, t_definition)
			self.listOfODEs.append(ode)

		# print "\n"
		# print slow_variables
		fast_vars = []
		# for i in range(fast_matrix.shape[0]):
		# 	if not all(fast_matrix[i,:].applyfunc(self.ZeroFilter)):
		# 		fast_vars.append(self.parentModel.variablesOdes[kept_variables[i]].symbol.getSymbol())
		for i, var in enumerate(self.sbmlModel.variablesOdes):
			if var.symbol.getSymbol() not in slow_variables and i in kept_variables:
				fast_vars.append(var.symbol.getSymbol())


		# print fast_vars
		# print subs
		formulas = {}
		for law in self.fastLaws:
			# print law
			# print fast_vars
			law = law.subs(subs)
			intersect = set(fast_vars).intersection(set(law.atoms(SympySymbol)))
			if len(intersect) > 0:
				var = list(intersect)[0]
				res = solve(law, var)
				formulas.update({var: res[0]})

				if DEBUG:
					pprint(SympyEqual(var, formulas[var]))

				t_var = self.listOfVariables.getBySymbol(var)
				t_cfe = MathFormula(self)
				t_cfe.setInternalMathFormula(res[0])
				cfe = CFE(self)
				cfe.new(t_var, t_cfe)
				self.listOfCFEs.append(cfe)
				self.listOfVariables.changeVariableType(t_var, MathVariable.VAR_ASS)


		# print self.listOfCFEs
		self.listOfCFEs.developCFEs()



		vars = self.fastLaws_vars

		subs = {}

		for var, math_formula in self.sbmlModel.solvedInitialConditions.items():
			if var not in vars:
				subs.update({var: math_formula.getDeveloppedInternalMathFormula()})


		#
		system = []
		#
		for cons_law in self.sbmlModel.listOfConservationLaws:
			formula = cons_law.getFormula().subs(subs)
			# formula = cons_law.getFormula()
			if formula not in [True, False]:
				system.append(formula)
		#
		for fast_law in self.fastLaws:

			system.append(SympyEqual(fast_law, SympyInteger(0)))
			# system.append(SympyEqual(expand(fast_law.subs(self.reducedModel.listOfCFEs.getSubs())), SympyInteger(0)))

		if DEBUG:
			print system
			print vars

		if True not in system:
			res = solve(system, vars)

			if DEBUG:
				print res

			for var, value in res.items():
				math_formula = MathFormula(self)
				math_formula.setInternalMathFormula(value.subs(subs))
				self.solvedInitialConditions.update({var: math_formula})













		self.setUpToDate(True)

	def prettyPrint(self):

		print "\n> Full system : "
		print self.listOfCFEs
		print self.listOfDAEs
		print self.listOfODEs
		print "-----------------------------"

	# 
	# def build(self, treated_variables=[]):
	# 
	# 	self.fastStoichiometryMatrix.build(including_slow_reactions=False)
	# 	self.slowStoichiometryMatrix.build(including_fast_reactions=False)
	# 	self.findFastReactions()
	# 	# print [var.getSbmlId() for var in self.parentModel.variablesOdes]
	# 	fast_matrix = self.fastStoichiometryMatrix.rawStoichiometryMatrix.transpose()
	# 	slow_matrix = self.slowStoichiometryMatrix.rawStoichiometryMatrix.transpose()
	# 	fast_velocities = self.findVelocities(include_slow_reaction=False)
	# 	slow_velocities = self.findVelocities(include_fast_reaction=False)
	# 
	# 	# print "> Fast stoichiometry matrix"
	# 	# pprint(fast_matrix)
	# 	# print "\n"
	# 	#
	# 	#
	# 	# print "> Slow stoichiometry matrix"
	# 	# pprint(slow_matrix)
	# 	# print "\n"
	# 	#
	# 	# print "> Fast velocities"
	# 	# pprint(fast_velocities.transpose())
	# 	# print "\n"
	# 	#
	# 	# print "> Slow velocities"
	# 	# pprint(slow_velocities.transpose())
	# 	# print "\n"
	# 
	# 	fast_system = fast_matrix * fast_velocities
	# 	slow_system = slow_matrix * slow_velocities
	# 	full_system = fast_system + slow_system
	# 
	# 
	# 	# print "> Fast system matrix"
	# 	# pprint(fast_system)
	# 	# print "\n"
	# 	#
	# 	# print "> Slow system matrix"
	# 	# pprint(slow_system)
	# 	# print "\n"
	# 	#
	# 	# print "> Full system matrix"
	# 	# pprint(full_system)
	# 	# print "\n"
	# 
	# 	# reduced_fast_stoichiometry = None
	# 	# for i in range(fast_matrix.shape[1]):
	# 	# 	reaction = fast_matrix[:,i]
	# 	# 	if any(reaction.applyfunc(self.notZeroFilter)):
	# 	# 		if reduced_fast_stoichiometry is None:
	# 	# 			reduced_fast_stoichiometry = reaction
	# 	# 		else:
	# 	# 			reduced_fast_stoichiometry = reduced_fast_stoichiometry.row_join(reaction)
	# 	#
	# 	# pprint(reduced_fast_stoichiometry)
	# 
	# 
	# 
	# 	nullspace = fast_matrix.transpose().nullspace()
	# 
	# 	matrix_nullspace = None
	# 	for sol in nullspace:
	# 		# pprint(sol)
	# 		# print sol.applyfunc(self.notZeroFilter)
	# 		#
	# 		# print flatten(sol.applyfunc(self.notZeroFilter))
	# 		# if flatten(sol.applyfunc(self.notZeroFilter)).count(True) > 1:
	# 		# if sum(sol.applyfunc(self.notZeroFilter)) > 1:
	# 			if matrix_nullspace is None:
	# 				matrix_nullspace = sol
	# 			else:
	# 				matrix_nullspace = matrix_nullspace.row_join(sol)
	# 
	# 	#
	# 	# print "> Raw fast nullspace matrix"
	# 	# pprint(nullspace)
	# 	# print "\n"
	# 	#
	# 	# print "> Fast nullspace matrix"
	# 	# pprint(matrix_nullspace)
	# 	# print "\n"
	# 
	# 
	# 	print "> Nullspace * fast system matrix"
	# 	reduced_fast_system = matrix_nullspace.transpose() * fast_system
	# 	# pprint(reduced_fast_system)
	# 	for i in range(reduced_fast_system.shape[0]):
	# 		# print "\n\n> Species %s" % self.parentModel.variablesOdes[i].getSbmlId()
	# 		pprint(SympyEqual(self.parentModel.variablesOdes[i].symbol.getSymbol(), sum(reduced_fast_system[i, :])))
	# 	# # print "\n"
	# 
	# 	print "> Nullspace * slow system matrix"
	# 	reduced_slow_system = matrix_nullspace.transpose() * slow_system
	# 	# pprint(reduced_slow_system)
	# 	for i in range(reduced_slow_system.shape[0]):
	# 		# print "\n\n> Species %s" % self.parentModel.variablesOdes[i].getSbmlId()
	# 
	# 		pprint(SympyEqual(self.parentModel.variablesOdes[i].symbol.getSymbol(), sum(reduced_slow_system[i,:])))
	# 	print "\n"
	# 
	# 
	# 
	# 
	# def buildFromReduced(self, treated_variables=[]):
	# 
	# 	self.fastStoichiometryMatrix.build(including_slow_reactions=False)
	# 	self.slowStoichiometryMatrix.build(including_fast_reactions=False)
	# 	self.findFastReactions()
	# 	# print [var.getSbmlId() for var in self.parentModel.variablesOdes]
	# 	fast_matrix = self.fastStoichiometryMatrix.rawStoichiometryMatrix.transpose()
	# 	slow_matrix = self.slowStoichiometryMatrix.rawStoichiometryMatrix.transpose()
	# 	subs = self.reducedModel.listOfCFEs.getSubs()
	# 	fast_velocities = self.findVelocities(include_slow_reaction=False)
	# 	slow_velocities = self.findVelocities(include_fast_reaction=False)
	# 
	# 	kept_variables = []
	# 	for i, var in enumerate(self.parentModel.variablesOdes):
	# 		if var.symbol.getSymbol() in [var.symbol.getSymbol() for var in self.reducedModel.variablesOdes]:
	# 			kept_variables.append(i)
	# 	# print kept_variables
	# 
	# 	# print "> Fast stoichiometry matrix"
	# 	fast_matrix = fast_matrix[kept_variables,:]
	# 	# pprint(fast_matrix)
	# 	# print "\n"
	# 	#
	# 	#
	# 	# print "> Slow stoichiometry matrix"
	# 	slow_matrix = slow_matrix[kept_variables,:]
	# 	# pprint(slow_matrix)
	# 	# print "\n"
	# 	#
	# 	# print "> Fast velocities"
	# 	# pprint(fast_velocities)
	# 	# print "\n"
	# 	#
	# 	# print "> Slow velocities"
	# 	# pprint(slow_velocities)
	# 	# print "\n"
	# 
	# 	fast_system = fast_matrix * fast_velocities
	# 	slow_system = slow_matrix * slow_velocities
	# 	full_system = fast_system + slow_system
	# 
	# 
	# 	# print "> Fast system matrix"
	# 	# pprint(fast_system)
	# 	# print "\n"
	# 	#
	# 	# print "> Slow system matrix"
	# 	# pprint(slow_system)
	# 	# print "\n"
	# 	#
	# 	# print "> Full system matrix"
	# 	# pprint(full_system)
	# 	# print "\n"
	# 
	# 	# reduced_fast_stoichiometry = None
	# 	# for i in range(fast_matrix.shape[1]):
	# 	# 	reaction = fast_matrix[:,i]
	# 	# 	if any(reaction.applyfunc(self.notZeroFilter)):
	# 	# 		if reduced_fast_stoichiometry is None:
	# 	# 			reduced_fast_stoichiometry = reaction
	# 	# 		else:
	# 	# 			reduced_fast_stoichiometry = reduced_fast_stoichiometry.row_join(reaction)
	# 	#
	# 	# pprint(reduced_fast_stoichiometry)
	# 
	# 
	# 
	# 	nullspace = fast_matrix.transpose().nullspace()
	# 	# pprint(nullspace)
	# 	matrix_nullspace = None
	# 	for sol in nullspace:
	# 		if matrix_nullspace is None:
	# 			matrix_nullspace = sol
	# 		else:
	# 			matrix_nullspace = matrix_nullspace.row_join(sol)
	# 
	# 	# print "> Fast nullspace matrix"
	# 	# pprint(matrix_nullspace)
	# 	# print "\n"
	# 	#
	# 	#
	# 	# print "> Nullspace * fast system matrix"
	# 	# reduced_fast_system = matrix_nullspace.transpose() * fast_system
	# 	# # pprint(reduced_fast_system)
	# 	# for i in range(reduced_fast_system.shape[0]):
	# 	# 	# print "\n\n> Species %s" % self.parentModel.variablesOdes[i].getSbmlId()
	# 	# 	pprint(SympyEqual(self.parentModel.variablesOdes[kept_variables[i]].symbol.getSymbol(), sum(reduced_fast_system[i, :])))
	# 	# # # print "\n"
	# 
	# 	# print "> Nullspace * slow system matrix"
	# 	reduced_slow_system = matrix_nullspace.transpose() * slow_system
	# 	# pprint(reduced_slow_system)
	# 	for i in range(reduced_slow_system.shape[0]):
	# 		# print "\n\n> Species %s" % self.parentModel.variablesOdes[i].getSbmlId()
	# 
	# 		pprint(SympyEqual(
	# 			SympyDerivative(self.parentModel.variablesOdes[kept_variables[i]].symbol.getSymbol(),SympySymbol("t")),
	# 			sum(reduced_slow_system[i,:])
	# 		))
	# 	print "\n"
	# 
	# 	fast_vars = []
	# 	# print fast_matrix.shape
	# 	for i in range(fast_matrix.shape[0]):
	# 	# for i, var in enumerate(fast_matrix):
	# 		if not all(fast_matrix[i,:].applyfunc(self.ZeroFilter)):
	# 		# if var == SympyInteger(0):
	# 		# 	print i
	# 			fast_vars.append(self.parentModel.variablesOdes[kept_variables[i]].symbol.getSymbol())
	# 
	# 
	# 	# print fast_vars
	# 	formulas = {}
	# 	for law in self.fastLaws:
	# 		law = law.subs(subs)
	# 		intersect = set(fast_vars).intersection(set(law.atoms(SympySymbol)))
	# 		if len(intersect) > 0:
	# 			# print intersect
	# 			# print law
	# 			# print law.subs
	# 			var = list(intersect)[0]
	# 			res = solve(law, var)
	# 			formulas.update({var: res[0]})
	# 
	# 		# pprint(SympyEqual(law, SympyInteger(0)))
	# 		pprint(SympyEqual(var, formulas[var]))
	# 
	# 
	# 
