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

from libsignetsim.model.ListOfMathVariables import ListOfMathVariables
from libsignetsim.model.ListOfSbmlVariables import ListOfSbmlVariables
from libsignetsim.model.math.sympy_shortcuts import SympySymbol

class ListOfVariables(ListOfMathVariables, ListOfSbmlVariables, list):
	""" Parent class for all the ListOf containers in a sbml model """

	def __init__(self, model):

		self.__model = model
		ListOfMathVariables.__init__(self, model)
		ListOfSbmlVariables.__init__(self, model)
		list.__init__(self)

	def addVariable(self, variable, string=None):

		t_sbmlId = ListOfSbmlVariables.newSbmlId(self, variable, string)
		list.append(self, variable)
		return t_sbmlId

	def removeVariable(self, variable):
		list.remove(self, variable)

	# Symbols
	def symbols(self):
		""" Return a set of symbols of the sbml variables """
		return [obj.symbol.getInternalMathFormula() for obj in self]

	def containsSymbol(self, symbol):
		""" Returns if a symbol is in the list of sbml variables"""
		for var in self:
			if var.symbol.getSymbol() == symbol:
				return True
		return False

	def getBySymbol(self, symbol):
		""" Get a sbml variable by his symbol"""
		for var in self:
			if var.symbol.getSymbol() == symbol:
				return var

	def getBySymbolStr(self, symbol_str):
		""" Get a sbml variable by his symbol string"""
		for var in self:
			if var.getSymbolStr() == symbol_str:
				return var

	# Renaming variable
	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)
		if old_symbol in self.symbols():
			t_var = self.getBySymbol(old_symbol)
			t_var.renameSymbol(old_sbml_id, new_sbml_id)

		for var in self:
			var.renameSbmlIdInValue(old_sbml_id, new_sbml_id)


	def clear(self):
		list.__init__(self)

	def getFastVariables(self):
		return [species for species in self.__model.listOfSpecies if species.isOnlyInFastReactions()]

	def getMixedVariables(self):
		return [species for species in self.__model.listOfSpecies if species.isInFastReactions()]

	def getSlowVariables(self):
		return [species for species in self.__model.listOfSpecies if not species.isInFastReactions()]
