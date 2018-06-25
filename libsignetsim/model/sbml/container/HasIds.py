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

from libsignetsim.model.sbml.container.HasMetaIds import HasMetaIds

class HasIds(HasMetaIds):
	""" Parent class for all the ListOf containers in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		HasMetaIds.__init__(self, model)



	def sbmlIds(self):
		""" Return a set of import ids of the sbml objects """
		return [obj.getSbmlId() for obj in self]

	def getBySbmlId(self, sbml_id, pos=0):
		""" Find sbml objects by their import Id """

		res = []
		for obj in self:
			if obj.getSbmlId() == sbml_id:
				res.append(obj)

		if len(res) > 0:
			return res[pos]


	def containsSbmlId(self, sbml_id):
		""" Test if an sbml id is in the list """

		res = False
		for obj in self:
			if sbml_id == obj.getSbmlId():
				res = True

		return res



	def names(self):
		""" Return set of names of the sbml objects """
		return [obj.getName() for obj in self]

	def getByName(self, name, pos=0):
		""" Find sbml objects by their name """

		res = []
		for obj in self:
			if obj.getName() == name:
				res.append(obj)

		if len(res) > 0:
			return res[pos]



	def containsName(self, name):
		""" Test if a name is in the list """

		res = False
		for obj in self:
			if name == obj.getName():
				res = True

		return res
