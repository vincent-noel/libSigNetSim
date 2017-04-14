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

from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyInf, SympyNan, SympyAdd, SympyEqual, SympyStrictLessThan
)
from sympy import simplify, diff, solve, zeros, Lambda, flatten


class MathStoichiometryMatrix(object):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		self.stoichiometryMatrix = None
		self.listOfSpecies = []

	def build(self, including_fast_reactions=True, including_slow_reactions=True):

		matrix = []
		for i, reaction in enumerate(self.__model.listOfReactions.values()):
			if (
				(reaction.fast and including_fast_reactions)
				or
				(not reaction.fast and including_slow_reactions)
			):
					matrix += reaction.getStoichiometryMatrix()

		self.stoichiometryMatrix = matrix
		for species in self.__model.listOfSpecies.values():
			self.listOfSpecies.append(species.symbol.getSymbol())


	def getSimpleStoichiometryMatrix(self):

		if self.stoichiometryMatrix is None:
			self.buildStoichiometryMatrix()

		matrix = None
		if self.stoichiometryMatrix != None:
			for i, reaction in enumerate(self.stoichiometryMatrix):

				t_reaction = zeros(1,len(self.__model.listOfSpecies))

				for j, t_formula in enumerate(reaction):
					t_reaction[j] = t_formula.getDeveloppedInternalMathFormula()

				if matrix is None:
					matrix = t_reaction
				else:
					matrix = matrix.col_join(t_reaction)

			return matrix

	def hasNullSpace(self):
		res = self.stoichiometryMatrix is not None and len(self.stoichiometryMatrix) > 0
		for var in flatten(self.getSimpleStoichiometryMatrix()):
			if var in [SympyInf, -SympyInf, SympyNan]:
				res = False
		return res

	def getSimpleNullspace(self):

		return self.fixnullspace(self.getSimpleStoichiometryMatrix().nullspace())


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