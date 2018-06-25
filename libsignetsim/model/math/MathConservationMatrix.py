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



from sympy import eye, Matrix, pretty, srepr


class MathConservationMatrix(object):
	""" Sbml model class """

	def __init__(self, model):
		""" Constructor of model class """

		self.__model = model
		self.conservationMatrix = None

	def getConservationMatrix(self, stoichiometry_matrix=None):

		if stoichiometry_matrix is not None:
			return self.buildConservationMatrix(stoichiometry_matrix)

		elif self.conservationMatrix is None:
			self.conservationMatrix = self.buildConservationMatrix(stoichiometry_matrix)

		return self.conservationMatrix

	def buildConservationMatrix(self, stoichiometry_matrix=None):

		conservationMatrix = None
		if stoichiometry_matrix is None:
			sm = self.__model.stoichiometryMatrix.getStoichiometryMatrix()
		else:
			sm = stoichiometry_matrix.getStoichiometryMatrix()

		if sm is not None:
			sm = sm.evalf()
			T0 = sm.row_join(eye(sm.shape[0]))
			n = sm.shape[1]

			Ts = [T0]
			j = 0

			all_zero = False
			while not all_zero:
				Ts.append(self.__next_tableau(Ts[j], j, n))
				j += 1
				all_zero = True
				for i in range(Ts[j].shape[0]):
					all_zero &= all([j_i == 0 for j_i in Ts[j][i, 0:n]])

			last_T = Ts[len(Ts) - 1]
			conservationMatrix = last_T[:, n:n + sm.shape[0]]

		return conservationMatrix
	def __str__(self):
		if self.conservationMatrix is not None:
			return srepr(self.conservationMatrix)

	def pprint(self):
		if self.conservationMatrix is not None:
			print("> Conservation matrix: ")
			print(pretty(self.conservationMatrix))
			print("\n")


	def __buildS(self, T, n):
		S = []
		for i in range(T.shape[0]):
			S.append(set([ii for ii, ii_val in enumerate(T[i, n:T.shape[1] + 1]) if ii_val == 0]))
		return S

	def __getCondition1(self, T, i, j, k):
		return T[i, j] * T[k, j] < 0

	def __getCondition2(self, T, S, i, k):

		intersection = S[i].intersection(S[k])
		result = True
		for l in range(T.shape[0]):
			if l != k and l != i:
				if intersection.issubset(S[l]):
					result = False

		return result

	def __buildIndices(self, T, S, j):

		indices = []
		for i in range(T.shape[0]):
			for k in range(T.shape[0]):
				if i != k and i < k:
					if self.__getCondition1(T, i, j, k) and self.__getCondition2(T, S, i, k):
						indices.append((i, k))

		return indices

	def __buildVectors(self, T, j, indices):

		result = []
		for i, k in indices:
			vector = abs(T[i, j]) * T[k, :] + abs(T[k, j]) * T[i, :]
			result.append(vector)

		return result

	def __buildTp1(self, T, j, vectors):

		T_p1 = Matrix([[]])
		if len(vectors) > 0:
			for i in range(len(vectors)):
				T_p1 = T_p1.col_join(vectors[i])

		for i in range(T.shape[0]):
			if T[i, j] == 0:
				T_p1 = T_p1.col_join(T[i, :])

		return T_p1

	def __next_tableau(self, T_i, j, n):

		S = self.__buildS(T_i, n)
		indices = self.__buildIndices(T_i, S, j)
		vectors = self.__buildVectors(T_i, j, indices)
		T_ip1 = self.__buildTp1(T_i, j, vectors)

		return T_ip1
