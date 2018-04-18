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

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.ConservationLaw import ConservationLaw
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger, SympyEqual
from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.model.sbml.ConservedMoiety import ConservedMoiety
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

from sympy import eye, Matrix, ones, pretty


class ListOfConservationLaws(list):
	""" Sbml model class """

	def __init__(self, model):
		""" Constructor of model class """

		list.__init__(self)
		self.__model = model

		self.extraVariables = ListOfVariables(self.__model)
		self.conservationMatrix = None

	def hasConservationLaws(self):
		return len(self) > 0

	def clear(self):
		del self[:]
		to_remove = []

		for variable in self.__model.listOfVariables:
			if variable.isConservedMoiety():
				to_remove.append(variable)
				self.__model.variablesConstant.remove(variable)

		for variable in to_remove:
			self.__model.listOfVariables.remove(variable)


	def __getVariableFormula(self, variable):

		formula = variable.symbol.getSymbol()

		if variable.isSpecies():
			if not variable.hasOnlySubstanceUnits:
				formula /= variable.getCompartment().symbol.getSymbol()

			if variable.isSetConversionFactor():
				formula /= variable.getSymbolConversionFactor()

			elif self.__model.isSetConversionFactor():
				formula /= self.__model.getSymbolConversionFactor()

		elif self.__model.isSetConversionFactor():
			formula /= self.__model.getSymbolConversionFactor()

		return formula

	def __getVariableValue(self, variable):

		symbol = variable.symbol.getSymbol()

		if symbol in self.__model.solvedInitialConditions.keys():

			value = self.__model.solvedInitialConditions[symbol].getDeveloppedInternalMathFormula()
			if variable.isSpecies():
				if not variable.hasOnlySubstanceUnits:
					value /= variable.getCompartment().symbol.getSymbol()

				if variable.isSetConversionFactor():
					conv_factor = variable.getSymbolConversionFactor()
					value /= self.__model.solvedInitialConditions[conv_factor].getDeveloppedInternalMathFormula()

				elif self.__model.isSetConversionFactor():
					conv_factor = self.__model.getSymbolConversionFactor()
					value /= self.__model.solvedInitialConditions[conv_factor].getDeveloppedInternalMathFormula()
			elif self.__model.isSetConversionFactor():
				conv_factor = self.__model.getSymbolConversionFactor()
				value /= self.__model.solvedInitialConditions[conv_factor].getDeveloppedInternalMathFormula()

		else:
			value = SympySymbol("_%s_0_" % str(symbol))

		return value

	def __buildConservationLaw(self, t_law, t_value):

		t_vars = []
		for t_atom in t_law.atoms(SympySymbol):

			if not self.__model.listOfVariables.getBySymbol(t_atom).isCompartment():
				t_vars.append(t_atom)

		t_lhs = MathFormula(self.__model)
		t_lhs.setInternalMathFormula(t_law)

		new_var = ConservedMoiety(self.__model)
		new_var.setSbmlId("total_%d" % len(self))
		new_var.value.setInternalMathFormula(t_value)

		self.__model.listOfVariables.addVariable(new_var)
		self.__model.listOfVariables.changeVariableType(new_var, ConservedMoiety.VAR_CST)

		solved_value = MathFormula(self.__model)
		t_solved_value = new_var.value.getInternalMathFormula()

		for var in t_solved_value.atoms(SympySymbol):
			if var not in [SympySymbol("_avogadro_")]:
				t_solved_value = unevaluatedSubs(
					t_solved_value,
					{var: self.__model.solvedInitialConditions[var].getInternalMathFormula()})

		solved_value.setInternalMathFormula(t_solved_value)
		self.__model.solvedInitialConditions.update({new_var.symbol.getSymbol(): solved_value})

		t_rhs = MathFormula(self.__model)
		t_rhs.setInternalMathFormula(t_value)

		t_conservation_law = ConservationLaw(self.__model)
		t_conservation_law.new(t_lhs, t_rhs, t_vars)
		list.append(self, t_conservation_law)

	def __build(self, stoichiometry_matrix=None):

		laws = []
		if not self.__model.listOfReactions.hasVariableStoichiometry():

			conservation_matrix = self.__model.conservationMatrix.getConservationMatrix(stoichiometry_matrix)
			if conservation_matrix is not None:
				for i in range(conservation_matrix.shape[0]):

					t_res = conservation_matrix[i, :]

					t_law = MathFormula.ZERO
					t_value = MathFormula.ZERO

					nb_vars_found = t_res * ones(conservation_matrix.shape[1], 1)

					if int(nb_vars_found[0, 0]) > 1:

						for ii, tt_res in enumerate(t_res):

							variable = self.__model.variablesOdes[ii]
							tt_symbol_formula = self.__getVariableFormula(variable)
							tt_value = self.__getVariableValue(variable)

							if tt_res == SympyInteger(1):
								t_law += tt_symbol_formula
								t_value += tt_value

							elif tt_res == SympyInteger(-1):
								t_law -= tt_symbol_formula
								t_value -= tt_value

							else:
								t_law += tt_res * tt_symbol_formula
								t_value += tt_res * tt_value

						laws.append((t_law, t_value))


		return laws

	def getRawFormulas(self, stoichiometry_matrix):
		return [SympyEqual(law, value) for law, value in self.__build(stoichiometry_matrix)]

	def build(self):

		self.clear()
		laws = self.__build()
		for law, value in laws:
			self.__buildConservationLaw(law, value)
	#
	# def __buildS(self, T, n):
	# 	S = []
	# 	for i in range(T.shape[0]):
	# 		S.append(set([ii for ii, ii_val in enumerate(T[i, n:T.shape[1] + 1]) if ii_val == 0]))
	# 	return S
	#
	# def __getCondition1(self, T, i, j, k):
	# 	return T[i, j] * T[k, j] < 0
	#
	# def __getCondition2(self, T, S, i, k):
	#
	# 	intersection = S[i].intersection(S[k])
	# 	result = True
	# 	for l in range(T.shape[0]):
	# 		if l != k and l != i:
	# 			if intersection.issubset(S[l]):
	# 				result = False
	#
	# 	return result
	#
	# def __buildIndices(self, T, S, j):
	#
	# 	indices = []
	# 	for i in range(T.shape[0]):
	# 		for k in range(T.shape[0]):
	# 			if i != k and i < k:
	# 				if self.__getCondition1(T, i, j, k) and self.__getCondition2(T, S, i, k):
	# 					indices.append((i, k))
	#
	# 	return indices
	#
	# def __buildVectors(self, T, j, indices):
	#
	# 	result = []
	# 	for i, k in indices:
	# 		vector = abs(T[i, j]) * T[k, :] + abs(T[k, j]) * T[i, :]
	# 		result.append(vector)
	#
	# 	return result
	#
	# def __buildTp1(self, T, j, vectors):
	#
	# 	T_p1 = Matrix([[]])
	# 	if len(vectors) > 0:
	# 		for i in range(len(vectors)):
	# 			T_p1 = T_p1.col_join(vectors[i])
	#
	# 	for i in range(T.shape[0]):
	# 		if T[i, j] == 0:
	# 			T_p1 = T_p1.col_join(T[i, :])
	#
	# 	return T_p1
	#
	# def __next_tableau(self, T_i, j, n):
	#
	# 	S = self.__buildS(T_i, n)
	# 	indices = self.__buildIndices(T_i, S, j)
	# 	vectors = self.__buildVectors(T_i, j, indices)
	# 	T_ip1 = self.__buildTp1(T_i, j, vectors)
	#
	# 	return T_ip1
	#
	# def getConservationMatrix(self, stoichiometry_matrix=None):
	#
	# 	if self.conservationMatrix is None:
	# 		self.buildConservationMatrix(stoichiometry_matrix)
	#
	# 	return self.conservationMatrix
	#
	# def buildConservationMatrix(self, stoichiometry_matrix=None):
	#
	# 	if stoichiometry_matrix is None:
	# 		sm = self.__model.stoichiometryMatrix.getStoichiometryMatrix()
	# 	else:
	# 		sm = stoichiometry_matrix.getStoichiometryMatrix()
	#
	# 	if sm is not None:
	# 		sm = sm.evalf()
	# 		T0 = sm.row_join(eye(sm.shape[0]))
	# 		n = sm.shape[1]
	#
	# 		Ts = [T0]
	# 		j = 0
	#
	# 		all_zero = False
	# 		while not all_zero:
	# 			Ts.append(self.__next_tableau(Ts[j], j, n))
	# 			j += 1
	# 			all_zero = True
	# 			for i in range(Ts[j].shape[0]):
	# 				all_zero &= all([j_i == 0 for j_i in Ts[j][i, 0:n]])
	#
	# 		last_T = Ts[len(Ts) - 1]
	# 		self.conservationMatrix = last_T[:, n:n + sm.shape[0]]

	def __str__(self):
		res = ""
		for law in self:
			res += "%s\n" % law
		return res

	def pprint(self):

		for cons in self:
			cons.pprint()
			print("\n")
