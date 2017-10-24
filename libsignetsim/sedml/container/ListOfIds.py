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

from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.settings.Settings import Settings


class ListOfIds(list):

	def __init__(self, document):

		list.__init__(self)
		self.__document = document

	def ids(self):
		""" Return a set of ids of the sedml objects """
		return [obj.getId() for obj in self]

	def getById(self, sedml_id, pos=0):
		""" Find sedml objects by their Id """

		res = []
		for obj in self:
			if obj.getId() == sedml_id:
				res.append(obj)

		if len(res) > 0:
			return res[pos]

	def containsId(self, sedml_id):
		""" Test if an sbml id is in the list """

		res = False
		for obj in self:
			if sedml_id == obj.getId():
				res = True

		return res
