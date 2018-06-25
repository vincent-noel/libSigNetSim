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

class ListOf(list):
	""" Parent class for all the ListOf.* containers in a sbml model """

	def __init__(self, model=None):

		list.__init__(self)
		self.__model = model
		self.isListOfSbmlObjects = False
		self.currentObjId = -1

	def nextId(self):
		self.currentObjId += 1
		return self.currentObjId

	def add(self, sbml_object):
		list.append(self, sbml_object)

	def index(self, object):
		return list.index(self, object)

	def ids(self):
		""" Return a set of ids of the sbml objects """
		return [obj.objId for obj in self]

	def getById(self, obj_id, pos=0):
		""" Find sbml objects by their import Id """

		res = []
		for obj in self:
			if obj.objId == obj_id:
				res.append(obj)

		if len(res) > 0:
			return res[pos]
		else:
			return None

	def getByPos(self, pos):
		""" Find sbml objects by their position """
		return list.__getitem__(self, pos)

	def getPosById(self, id):
		return self.index(self.getById(id))

	def remove(self, sbml_obj, full_remove=True):
		""" Remove an object from the list """

		if not self.isListOfSbmlObjects and full_remove:
			self.__model.listOfSbmlObjects.remove(sbml_obj)
		list.remove(self, sbml_obj)

	def removeById(self, obj_id):
		""" Remove an object from the list """
		self.remove(self.getById(obj_id))

	def clear(self):
		self.currentObjId = -1
		list.__init__(self)
