#!/usr/bin/env python
""" ListOfSbmlObjects.py


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

from libsignetsim.model.sbml.container.ListOf_v2 import ListOf_v2
from libsignetsim.model.sbml.container.HasMetaIds import HasMetaIds


class ListOfSbmlObjects(ListOf_v2, HasMetaIds):
	""" Class for the listOfModelDefinition in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		ListOf_v2.__init__(self, model)
		HasMetaIds.__init__(self, model)
		self.isListOfSbmlObjects = True
		self.currentObjId = -1

	def nextMetaId(self):
		self.currentObjId += 1
		return "_meta_id_%d_" % self.currentObjId

	def addSbmlObject(self, sbml_object, prefix=""):

		if sbml_object.getMetaId() is None:
			sbml_object.setMetaId(self.nextMetaId())

		if self.containsMetaId(sbml_object.getMetaId()):

			t_meta_id = sbml_object.getMetaId()
			while self.containsMetaId(t_meta_id):
				t_meta_id = self.nextMetaId()

			sbml_object.rawSetMetaId(t_meta_id)

		self.append(sbml_object)

		return sbml_object

	def getListOfSubstitutions(self):

		res = []
		for obj in ListOf_v2.values(self):
			if obj.hasReplacedElements():
				res += obj.getReplacedElements()

			if obj.isReplaced():
				res.append(obj.getReplacedBy())

		return res
