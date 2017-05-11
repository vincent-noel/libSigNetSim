#!/usr/bin/env python
""" ListOfVariables.py


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

from libsignetsim.model.ListOfMathVariables import ListOfMathVariables
from libsignetsim.model.ListOfSbmlVariables import ListOfSbmlVariables
from libsignetsim.model.math.sympy_shortcuts import SympySymbol

class ListOfVariables(ListOfMathVariables, ListOfSbmlVariables, dict):
	""" Parent class for all the ListOf_ containers in a sbml model """

	def __init__ (self, model):

		self.__model = model
		ListOfMathVariables.__init__(self, model)
		ListOfSbmlVariables.__init__(self, model)
		dict.__init__(self)

	# Add/Remove variables
	def addVariable(self, variable, string=None):

		t_sbmlId = ListOfSbmlVariables.newSbmlId(self, variable, string)
		dict.update(self, {t_sbmlId: variable})

		return t_sbmlId

	def removeVariable(self, variable):
		del variable

	# Symbols
	def symbols(self):
		""" Return a set of symbols of the sbml variables """
		return [obj.symbol.getInternalMathFormula() for obj in self.values()]

	def containsSymbol(self, symbol):
		""" Returns if a symbol is in the list of sbml variables"""
		for var in dict.values(self):
			if var.symbol.getSymbol() == symbol:
				return True
		return False

	def getBySymbol(self, symbol):
		""" Get a sbml variable by his symbol"""
		for var in dict.values(self):
			if var.symbol.getSymbol() == symbol:
				return var

	# Renaming variable
	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)
		if old_symbol in self.symbols():
			t_var = self.getBySymbol(old_symbol)
			t_var.renameSymbol(old_sbml_id, new_sbml_id)
			dict.__delitem__(self, old_sbml_id)
			dict.update(self, {new_sbml_id: t_var})

		for var in dict.values(self):
			var.renameSbmlIdInValue(old_sbml_id, new_sbml_id)
