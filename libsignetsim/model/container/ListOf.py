#!/usr/bin/env python
""" ListOf.py


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


# from libsignetsim.model.container.ListOfSbmlObjects import ListOfSbmlObjects

class ListOf(dict):
	""" Parent class for all the ListOf.* containers in a sbml model """

	def __init__ (self, model=None):

		dict.__init__(self)
		self.__model = model
		self.isListOfSbmlObjects = False
		self.currentObjId = -1


	def nextId(self):
		self.currentObjId += 1
		return self.currentObjId


	def add(self, sbml_object):
		dict.update(self, {sbml_object.objId: sbml_object})


	# Overloading standard methods to get ordering
	def keys(self):
		""" Override keys() to sort by id """
		return sorted(dict.keys(self),
					  key=lambda sbmlObj: dict.__getitem__(self, sbmlObj).objId)

	def items(self):
		""" Override items() to sort by id """
		return [(obj, dict.__getitem__(self, obj)) for obj in self.keys()]

	def values(self):
		""" Override values() to sort by id """
		return [dict.__getitem__(self, obj) for obj in self.keys()]



	def ids(self):
		""" Return a set of ids of the sbml objects """
		return [obj.objId for obj in self.values()]



	def getById(self, obj_id, pos=0):
		""" Find sbml objects by their import Id """

		res = []
		for obj in self.values():
			if obj.objId == obj_id:
				res.append(obj)

		if len(res) > 0:
			return res[pos]
		else:
			return None



	def getByPos(self, pos):
		""" Find sbml objects by their position """
		return self.__getitem__(self.keys()[pos])


	def getPosById(self, id):
		return self.keys().index(id)


	def remove(self, sbml_obj):
		""" Remove an object from the list """

		if not self.isListOfSbmlObjects:
			self.__model.listOfSbmlObjects.remove(sbml_obj)
		dict.__delitem__(self, sbml_obj.objId)


	def clear(self):
		dict.clear(self)
		self.currentObjId = -1
