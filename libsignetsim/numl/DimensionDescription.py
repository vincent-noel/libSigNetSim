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

from libsignetsim.numl.NMBase import NMBase
from libsignetsim.settings.Settings import Settings

class DimensionDescription (NMBase):

	def __init__(self, document, name=None):

		NMBase.__init__(self, document)
		self.__document = document
		self.__id = None
		self.__name = name
		# self.__ontologyTerm = None

	def readNuML(self, dimension_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		NMBase.readNuML(self, dimension_description, level, version)

		self.__id = dimension_description.getId()
		if dimension_description.isSetName():
			self.__name = dimension_description.getName()

		# self.__ontologyTerm = self.__document.listOfOntologyTerms.getByOntologyTerm(dimension_description.getOntologyTerm())


	def writeNuML(self, dimension_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		NMBase.writeNuML(self, dimension_description, level, version)

		if self.__id is not None:
			dimension_description.setId(self.__id)

		if self.__name is not None:
			dimension_description.setName(self.__name)

		# if self.__ontologyTerm is not None:
		# 	dimension_description.setOntologyTerm(self.__ontologyTerm.getId())

	def getName(self):
		return self.__name

	def getId(self):
		return self.__id

	def setId(self, description_id):
		self.__id = description_id