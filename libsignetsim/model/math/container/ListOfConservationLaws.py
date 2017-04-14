#!/usr/bin/env python
""" MathConservationLaws.py


	This file ...


	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.ConservationLaw import ConservationLaw
from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyInf, SympyNan, SympyAdd, SympyEqual, SympyStrictLessThan
)
from sympy import solve, Lambda, flatten


class ListOfConservationLaws(list):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """


		list.__init__(self)
		self.__model = model


	def hasConservationLaws(self):
		return len(self) > 0

	def clear(self):
		del self[:]

	def fixnullspace(self, nullspace):
		"""
			Here we look for the rows containing negatives values, find a row
			where there is the complementary of this negative value, and if
			adding the two rows gives us a row without a negative value then
			we consider it fixed
			Naive approach, but it seems to work, and hopefully it's not that
			inefficient.
		"""

		# Function returning a boolean if the value is negative
		neg_filter = Lambda(SympySymbol('x'),
							SympyStrictLessThan(
								SympySymbol('x'),
								SympyInteger(0)
							)
					)

		to_fix = []
		fixed = []
		for i, sol in enumerate(nullspace):

			#If all positive, it's already fixed
			if not any(sol.applyfunc(neg_filter)):
				fixed.append(sol)
				# This break should work. TODO test
				#break

			#We look for negative value, and write down the row and column
			for j, element in enumerate(sol):
				if element < 0:
					to_fix.append((i,j))

		# We look at the row, columns pairs which need fixing
		for i,j in to_fix:

			# We look for a row
			for i_sol, sol in enumerate(nullspace):

				#Which is not the one to be fixed, and which countains the
				#complementary of the negative value to fix
				if i_sol != i and sol[j] == -nullspace[i][j]:

					#If the sum of the two rows doesn't countains negative
					#values, then it's fixed
					if (not any((sol+nullspace[i]).applyfunc(neg_filter)) and sol+nullspace[i] not in fixed):
						fixed.append(sol+nullspace[i])
						break

		return fixed


	def build(self, stoichiometry_matrix=None):

		DEBUG = False

		del self[:]

		if stoichiometry_matrix is None:
			stoichiometry_matrix = self.__model.stoichiometryMatrix
		if stoichiometry_matrix.hasNullSpace():

			for i, t_res in enumerate(stoichiometry_matrix.getSimpleNullspace()):
				t_law = MathFormula.ZERO
				t_value = MathFormula.ZERO

				unknowns = []
				t_vars = []

				for ii, tt_res in enumerate(t_res):

					# t_species = stoichiometry_matrix.listOfSpecies[ii]
					# tt_symbol = t_species.symbol.getInternalMathFormula()

					tt_symbol = stoichiometry_matrix.listOfSpecies[ii]
					# tt_symbol = t_species.symbol.getInternalMathFormula()

					# print self.__model.solvedInitialConditions.keys()
					# print t_species

					if tt_symbol in self.__model.solvedInitialConditions.keys():
						tt_value = self.__model.solvedInitialConditions[tt_symbol].getDeveloppedInternalMathFormula()

					else:
						t_unknown = SympySymbol("_%s_0_" % str(tt_symbol))
						tt_value = t_unknown

						tt_unknown = MathFormula(self.__model, MathFormula.MATH_VARIABLE)
						tt_unknown.setInternalMathFormula(t_unknown)
						unknowns.append(tt_unknown)

					if tt_res == SympyInteger(1):
						t_law += tt_symbol
						t_value += tt_value

					elif tt_res == SympyInteger(-1):
						t_law -= tt_symbol
						t_value -= tt_value

					else:
						t_law += tt_res * tt_symbol
						t_value += tt_res * tt_value

					t_vars.append(tt_symbol)

				if t_law.func == SympyAdd:
					t_vars = []
					for t_atom in t_law.atoms(SympySymbol):
						if self.__model.listOfVariables.getBySymbol(t_atom).isDerivative():
							t_var = MathFormula(self.__model, MathFormula.MATH_VARIABLE)
							t_var.setInternalMathFormula(t_atom)
							t_vars.append(t_var)

					t_lhs = MathFormula(self.__model)
					t_lhs.setInternalMathFormula(t_law)

					t_rhs = MathFormula(self.__model)
					t_rhs.setInternalMathFormula(t_value)

					if DEBUG:
						print "New conservation law : "
						print "%s = %s" % (str(t_law), str(t_value))
					t_conservation_law = ConservationLaw(self.__model)
					t_conservation_law.new(t_lhs, t_rhs, vars)
					list.append(self, t_conservation_law)

	# 
	# def findReducibleVariables(self, vars_to_keep=[]):
	# 
	# 	odes_vars_in_laws = []
	# 	for law in self.LHSs_v2:
	# 		t_vars = []
	# 		for var in law.getDeveloppedInternalMathFormula().atoms(SympySymbol):
	# 			t_variable = self.listOfVariables[str(var)]
	# 			if t_variable.isDerivative() and not t_variable.isCompartment():
	# 				t_vars.append(var)
	# 		odes_vars_in_laws.append(t_vars)
	# 
	# 
	# 	system = []
	# 	for i, law in enumerate(self.LHSs_v2):
	# 		t_law = law.getDeveloppedInternalMathFormula()
	# 		t_value = self.RHSs_v2[i].getDeveloppedInternalMathFormula()
	# 		system.append(SympyEqual(t_law, t_value))
	# 
	# 
	# 	vars_to_extract = []
	# 	for i, ode_var in enumerate(odes_vars_in_laws):
	# 
	# 		j=0
	# 		while j < len(ode_var) and (
	# 			(len(vars_to_extract) > 0 and ode_var[j] in vars_to_extract)
	# 			or (len(vars_to_keep) > 0 and str(ode_var[j]) in vars_to_keep)):
	# 			j += 1
	# 
	# 		if j < len(ode_var):
	# 			vars_to_extract.append(ode_var[j])
	# 
	# 	# print [equ for equ in system]
	# 	# print vars_to_extract[1]
	# 
	# 	# print solve(system, vars_to_extract[1])
	# 	solutions = solve(system, vars_to_extract)
	# 	# print solutions
	# 	if len(solutions) > 0:
	# 		self.reducibleVariables = solutions
	# 	else:
	# 		self.reducibleVariables = {}

	def __str__(self):
		res = ""
		for law in self:
			res += "%s\n" % law
		return res