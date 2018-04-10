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
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from sympy import solve, simplify, ones, Lambda, Min, Symbol, pretty
from random import choice
from itertools import groupby


class MathAsymmetricModel(MathSubmodel):
	""" Sbml model class """

	def __init__(self, parent_model=None):
		""" Constructor of model class """

		MathSubmodel.__init__(self, parent_model=parent_model)

	def copyEquations(self):
		for cfe in self.parentModel.listOfCFEs:
			t_var = self.listOfVariables.getBySymbol(cfe.getVariable().symbol.getSymbol())
			t_cfe_formula = MathFormula(self)
			t_cfe_formula.setInternalMathFormula(cfe.getDefinition().getDeveloppedInternalMathFormula())
			t_cfe = CFE(self)
			t_cfe.new(t_var, t_cfe_formula)
			self.listOfCFEs.append(t_cfe)

		for dae in self.parentModel.listOfDAEs:
			t_dae_formula = MathFormula(self)
			t_dae_formula.setInternalMathFormula(dae.getDefinition().getDeveloppedInternalMathFormula())
			t_dae = DAE(self)
			t_dae.new(t_dae_formula)
			self.listOfDAEs.append(t_dae)

		self.copyEvents()
		self.copyInitialAssignments()

	def build(self, treated_variables=[]):

		DEBUG = False

		if len(self.parentModel.listOfConservationLaws) > 0:
			all_variables = range(len(self.parentModel.variablesOdes))

			forbidden_variables = []
			for i_species, species in enumerate(self.parentModel.variablesOdes):
				if (species.getSymbolStr() in treated_variables or species.hasEventAssignment() or species.hasInitialAssignment()):
					forbidden_variables.append(i_species)

			allowed_variables = list(set(all_variables).difference(set(forbidden_variables)))

			forbidden_laws = []
			for i, law in enumerate(self.parentModel.listOfConservationLaws):
				for var in law.vars:
					variable = self.parentModel.listOfVariables.getBySymbol(var)
					if variable.hasEventAssignment() or variable.hasInitialAssignment():
						forbidden_laws.append(i)

			if DEBUG:
				print("%d laws forbidden (%s)" % (len(forbidden_laws), str(forbidden_laws)))
			allowed_laws = list(set(range(len(self.parentModel.listOfConservationLaws))).difference(set(forbidden_laws)))

			cons_matrix = self.parentModel.listOfConservationLaws.getConservationMatrix()
			cons_matrix = cons_matrix[allowed_laws, :]
			cons_matrix_allowed = cons_matrix[:, allowed_variables]

			# Here we are trying to find groups of symmetrical variables.
			# The idea is that we first look at the number of time a species is in a conservation law.
			# Then, we group withing each law by the number of time it is in a conservation law modelwide
			# Each group is added to a list of global groups
			times_in_cons = ones(1, cons_matrix_allowed.shape[0]) * cons_matrix_allowed

			groups = []
			for i_cons in range(cons_matrix.shape[0]):

				i_matrix = cons_matrix[i_cons, allowed_variables]
				i_time_in_cons = i_matrix.multiply_elementwise(times_in_cons)

				t_dict = {int(val): [] for val in set(list(i_time_in_cons)) if val > 0}
				for i, val in enumerate(i_time_in_cons):
					if val > 0:
						t_dict[int(val)].append(i)

				for nb, species in t_dict.items():
					if species not in groups:
						groups.append(species)

			# Once we have these groups, we take one if each of them
			dependent_vars = []
			for group in groups:
				dependent_vars.append(allowed_variables[choice(group)])

			independent_species = list(set(all_variables).difference(set(dependent_vars)))
			if DEBUG:
				print("> Dependent : %s" % dependent_vars)
				print("> Independent : %s" % independent_species)

			## Here we want to solve them all at once, with all the conservation laws.
			## Otherwise we might not know which one toc hoose for which variable
			system = []
			vars = []

			i_var = 0

			for i_law, cons_law in enumerate(self.parentModel.listOfConservationLaws):
				if i_law not in forbidden_laws and i_var < len(dependent_vars):

					# cons_law = self.parentModel.listOfConservationLaws[i]
					system.append(cons_law.getFormula())

					dependent_species = self.parentModel.variablesOdes[dependent_vars[i_var]]
					vars.append(dependent_species.symbol.getSymbol())
					i_var += 1


			# for i, dependent_var in enumerate(dependent_vars):
			# 	if i < len(self.parentModel.listOfConservationLaws):
			# 		cons_law = self.parentModel.listOfConservationLaws[i]
			# 		system.append(cons_law.getFormula())
			#
			# 		dependent_species = self.parentModel.variablesOdes[dependent_var]
			# 		vars.append(dependent_species.symbol.getSymbol())

			if DEBUG:
				print(system)
				print(vars)

			# this might not work for some selection of vars... to investigate
			result_system = solve(system, vars)

			if DEBUG:
				print result_system

			independent_species = []
			independent_species_formula = []

			if len(result_system) > 0:
				if isinstance(result_system, dict):
					for var, value in result_system.items():
						independent_species.append(var)
						independent_species_formula.append(value)
				else:
					print result_system

			if len(independent_species) > 0:

				self.copyVariables()
				self.copyEquations()

				for var in self.parentModel.variablesOdes:
					new_var = self.listOfVariables.getBySymbol(var.symbol.getSymbol())
					if var.symbol.getSymbol() in independent_species:

						t_formula = MathFormula(self)

						t_formula.setInternalMathFormula(
							independent_species_formula[independent_species.index(var.symbol.getSymbol())]
						)

						t_cfe = CFE(self)
						t_cfe.new(new_var, t_formula)
						self.listOfCFEs.append(t_cfe)
						self.listOfVariables.changeVariableType(new_var, MathVariable.VAR_ASS)

					else:

						t_formula = MathFormula(self)
						t_formula.setInternalMathFormula(
							self.parentModel.listOfODEs.getByVariable(var).getDefinition().getDeveloppedInternalMathFormula()
						)

						t_ode = ODE(self)
						t_ode.new(new_var, t_formula)
						self.listOfODEs.append(t_ode)

				self.setUpToDate(True)
				self.listOfCFEs.developCFEs()
				# print("> %d variables reduced from the model" % len(dependent_vars))

				# if DEBUG:
				# 	self.listOfODEs.pprint()