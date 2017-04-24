#!/usr/bin/env python
""" MathStoichiometryMatrix.py


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
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyInf, SympyNan, SympyAdd, SympyEqual, SympyUnequal, SympyStrictLessThan
)
from sympy import simplify, diff, solve, zeros, Lambda, flatten, pprint


class MathStoichiometryMatrix(object):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		self.stoichiometryMatrix = []

		self.rawStoichiometryMatrix = None
		self.listOfSpecies = []
		#
		# self.rawFastStoichiometryMatrix = None
		# self.listOfFastSpecies = []
		#
		# self.rawSlowStoichiometryMatrix = None
		# self.listOfSlowSpecies = []

		self.rawNullspace = None

		# Function returning a boolean if the value is not zero
		self.notZeroFilter = Lambda(
			SympySymbol('x'),
			SympyUnequal(
				SympySymbol('x'),
				SympyInteger(0)
			)
		)

	def build(self, including_fast_reactions=True, including_slow_reactions=True, include_variable_stoichiometry=False):


		subs = {}
		for var, value in self.__model.solvedInitialConditions.items():
			subs.update({var: value.getInternalMathFormula()})

		matrix = None
		for i, reaction in enumerate(self.__model.listOfReactions.values()):
			# if (
			# 			not reaction.hasVariableStoichiometry() or include_variable_stoichiometry
			# ) and (
			# 		(reaction.fast and including_fast_reactions)
			# 	or
			# 		((not reaction.fast) and including_slow_reactions)
			# ):

			reaction_matrix = reaction.getRawStoichiometryMatrix(subs,
					including_fast_reactions=including_fast_reactions,
					including_slow_reactions=including_slow_reactions,
					include_variable_stoichiometry=include_variable_stoichiometry
			)

			if matrix is None:
				matrix = reaction_matrix
			else:
				matrix = matrix.col_join(reaction_matrix)

		self.rawStoichiometryMatrix = matrix

		for i, species in enumerate(self.__model.variablesOdes):
			# if all(self.rawStoichiometryMatrix[:,i].applyfunc(self.notZeroFilter)):
				self.listOfSpecies.append(species.symbol.getSymbol())



		if self.rawStoichiometryMatrix is not None:
			self.getSimpleNullspace()

	def hasNullSpace(self):

		if self.rawStoichiometryMatrix is None:
			return False

		for var in flatten(self.rawStoichiometryMatrix):
			if var in [SympyInf, -SympyInf, SympyNan]:
				return False

		return True

	def getRawNullspace(self):

		if self.rawNullspace is None:
			self.rawNullspace = self.rawStoichiometryMatrix.nullspace()
		return self.rawNullspace
	def getSimpleNullspace(self):

		# simple_stoichiometry = self.rawStoichiometryMatrix
		#
		# # t0 = time()
		# raw_nullspace = simple_stoichiometry.nullspace()
		# print "> generated raw nullspace in %.2gs" % (time()-t0)

		# t0 = time()
		# print self.getRawNullspace()
		return self.getRawNullspace()
		# res = self.fixnullspace(self.getRawNullspace())
		# res = self.fixnullspace_v2(self.getRawNullspace())
		# print "> generated fixed nullspace in %.2gs" % (time()-t0)

		return res


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


	def fixnullspace_v2(self, nullspace):
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
		neg_lines = []
		to_fix = []
		fixed = []
		for i, sol in enumerate(nullspace):

			#If all positive, it's already fixed
			if not any(sol.applyfunc(neg_filter)):
				fixed.append(sol)
				# This break should work. TODO test
				#break
			else:
				neg_lines.append(sol)
			#We look for negative value, and write down the row and column
			for j, element in enumerate(sol):
				if element < 0:
					to_fix.append((i,j))

		full_neg_lines = []
		for i, line in enumerate(neg_lines):
			print [int(var) for var in line]
			full_neg_lines.append(line)
			for j, line2 in enumerate(neg_lines):
				if i != j:
					t_line = line+line2
					if t_line not in full_neg_lines:
						full_neg_lines.append(line+line2)
		print ""
		for i, line in enumerate(full_neg_lines):
			print [int(var) for var in line]		# for i in to_fix:
		# 	sol = nullspace[i]



		# # We look at the row, columns pairs which need fixing
		# for i,j in to_fix:
		#
		# 	# We look for a row
		# 	for i_sol, sol in enumerate(nullspace):
		#
		# 		#Which is not the one to be fixed, and which countains the
		# 		#complementary of the negative value to fix
		# 		if i_sol != i and sol[j] == -nullspace[i][j]:
		#
		# 			#If the sum of the two rows doesn't countains negative
		# 			#values, then it's fixed
		# 			if (not any((sol+nullspace[i]).applyfunc(neg_filter)) and sol+nullspace[i] not in fixed):
		# 				fixed.append(sol+nullspace[i])
		# 				# break

		return fixed