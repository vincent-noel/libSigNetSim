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


from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.ConservationLaw import ConservationLaw
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger, SympyEqual, SympyAdd, SympyMul, SympyPow
from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.model.sbml.ConservedMoiety import ConservedMoiety
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

from sympy import ones, pretty, srepr


class ListOfConservationLaws(list):
	""" Sbml model class """

	def __init__(self, model):
		""" Constructor of model class """

		list.__init__(self)
		self.__model = model

		self.extraVariables = ListOfVariables(self.__model)
		self.conservationMatrix = None
		self.__upToDate = False
	def getRawFormulas(self, stoichiometry_matrix):
		return [SympyEqual(law, value) for law, value in self.__build(stoichiometry_matrix)]

	def isUpToDate(self):
		return self.__upToDate

	def build(self):

		self.clear()
		laws = self.__build()
		for law, value in laws:
			self.__buildConservationLaw(law, value)

		self.__upToDate = True

	def __str__(self):
		res = ""
		for law in self:
			res += "%s\n" % law
		return res

	def pprint(self):

		for cons in self:
			cons.pprint()
			print("\n")

	def hasConservationLaws(self):
		return len(self) > 0

	def clear(self):
		del self[:]
		to_remove = []

		for variable in self.__model.listOfVariables:
			if variable.isConservedMoiety():
				to_remove.append(variable)
				if variable.isConstant():
					self.__model.variablesConstant.remove(variable)
					self.__model.nbConstants -= 1

		for variable in to_remove:
			self.__model.listOfVariables.remove(variable)

	def __getVariableFormula(self, variable):

		formula = variable.symbol.getSymbol()

		if variable.isSpecies():
			if variable.isSetConversionFactor():
				formula /= variable.getSymbolConversionFactor()

			elif self.__model.isSetConversionFactor():
				formula /= self.__model.getSymbolConversionFactor()

		elif self.__model.isSetConversionFactor():
			formula /= self.__model.getSymbolConversionFactor()

		return formula

	def __getVariableValue(self, variable):

		symbol = variable.symbol.getSymbol()

		if symbol in list(self.__model.listOfInitialConditions.keys()):

			value = self.__model.listOfInitialConditions[symbol].getDeveloppedInternalMathFormula()
			if variable.isSpecies():
				if variable.isSetConversionFactor():
					conv_factor = variable.getSymbolConversionFactor()
					value /= self.__model.listOfInitialConditions[conv_factor].getDeveloppedInternalMathFormula()

				elif self.__model.isSetConversionFactor():
					conv_factor = self.__model.getSymbolConversionFactor()
					value /= self.__model.listOfInitialConditions[conv_factor].getDeveloppedInternalMathFormula()
			elif self.__model.isSetConversionFactor():
				conv_factor = self.__model.getSymbolConversionFactor()
				value /= self.__model.listOfInitialConditions[conv_factor].getDeveloppedInternalMathFormula()

		else:
			value = SympySymbol("_%s_0_" % str(symbol))

		return value

	def __addConservedMoiety(self, value):

		new_var = ConservedMoiety(self.__model)
		name = "total_%d" % len(self)
		new_var.new(name, value)
		self.__solveInitialConditions(new_var)

		return new_var.symbol.getInternalMathFormula(rawFormula=True)

	def __solveInitialConditions(self, moiety):

		solved_value = MathFormula(self.__model)
		t_solved_value = moiety.value.getInternalMathFormula()

		for var in t_solved_value.atoms(SympySymbol):
			if var not in [SympySymbol("_avogadro_")]:
				t_solved_value = unevaluatedSubs(
					t_solved_value,
					{var: self.__model.listOfInitialConditions[var].getInternalMathFormula()})

		solved_value.setInternalMathFormula(t_solved_value)
		self.__model.listOfInitialConditions.update({moiety.symbol.getSymbol(): solved_value})

	def __buildConservationLaw(self, t_law, t_value):

		t_vars = []
		for t_atom in t_law.atoms(SympySymbol):

			if not self.__model.listOfVariables.getBySymbol(t_atom).isCompartment():
				t_vars.append(t_atom)

		t_lhs = MathFormula(self.__model)
		t_lhs.setInternalMathFormula(t_law)

		final_value = SympyInteger(0)

		if t_value.func == SympyAdd:
			# Should be only positive terms, divided by the compartment
			for arg in t_value.args:
				moeity_value = self.__addConservedMoiety(arg)
				final_value += moeity_value
		else:
			final_value = self.__addConservedMoiety(t_value)

		t_rhs = MathFormula(self.__model)
		t_rhs.setInternalMathFormula(final_value)

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
