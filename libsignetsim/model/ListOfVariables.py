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


# from libsignetsim.model.sbml.container.ListOfSbmlObjects import ListOfSbmlObjects
from libsignetsim.model.ListOfMathVariables import ListOfMathVariables
from libsignetsim.model.ListOfSbmlVariables import ListOfSbmlVariables


class ListOfVariables(ListOfMathVariables, ListOfSbmlVariables, dict):
	""" Parent class for all the ListOf_ containers in a sbml model """

	def __init__ (self, model):

		self.__model = model
		ListOfMathVariables.__init__(self, model)
		ListOfSbmlVariables.__init__(self, model)
		dict.__init__(self)
		# self.listOfVariables = ListOfSbmlObjects(model)


	# Overloading standard methods to get ordering
	def keys(self):
		""" Override keys() to sort by id """
		return sorted(dict.keys(self),
					  key=lambda sbmlObj: str(dict.__getitem__(self, sbmlObj).symbol.getInternalMathFormula()))

	def items(self):
		""" Override items() to sort by id """
		return [(obj, dict.__getitem__(self, obj)) for obj in self.keys()]

	def values(self):
		""" Override values() to sort by id """
		return [dict.__getitem__(self, obj) for obj in self.keys()]



	def sbmlIds(self):
		""" Return a set of ids of the sbml objects """
		return [obj.getSbmlId() for obj in self.values()]

	def symbols(self):
		""" Return a set of ids of the sbml objects """
		return [obj.symbol.getInternalMathFormula() for obj in self.values()]




	def addVariable(self, variable, string=None):

		t_sbmlId = ListOfSbmlVariables.newSbmlId(self, variable, string)
		dict.update(self, {t_sbmlId: variable})
		return t_sbmlId

	def removeVariable(self, variable):

		del self[variable.getSbmlId()]

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
			# print dict.keys(self)
		if old_sbml_id in dict.keys(self):
			t_var = dict.__getitem__(self, old_sbml_id)
			dict.__delitem__(self, old_sbml_id)
			dict.update(self, {new_sbml_id: t_var})

	def containsSymbol(self, symbol):

		for var in dict.values(self):
			if var.symbol.getSymbol() == symbol:
				return True
		return False

	def getBySymbol(self, symbol):

		for var in dict.values(self):
			if var.symbol.getSymbol() == symbol:
				return var
	#
	# def subsToFlatten(self):
	#
	# 	res = {}
	# 	for var in dict.values(self):
	# 		res.update({var.getSbmlId():var.getTopLevelSbmlId()})
	#
	# 	return res
