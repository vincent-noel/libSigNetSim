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

from libsignetsim.numl.DimensionDescription import DimensionDescription
from libsignetsim.settings.Settings import Settings

class AtomicDescription (DimensionDescription):

	def __init__(self, document, name=None, value_type="double"):
		DimensionDescription.__init__(self, document, name)
		self.__document = document
		self.__valueType = value_type
		self.__ontologyTerm = None

	def readNuML(self, atomic_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		DimensionDescription.readNuML(self, atomic_description, level, version)
		self.__valueType = atomic_description.getValueType()
		self.__ontologyTerm = self.__document.listOfOntologyTerms.getByOntologyTerm(atomic_description.getOntologyTerm())

	def writeNuML(self, atomic_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		DimensionDescription.writeNuML(self, atomic_description, level, version)
		if self.__valueType is not None:
			atomic_description.setValueType(self.__valueType)

		if self.__ontologyTerm is not None:
			atomic_description.setOntologyTerm(self.__ontologyTerm.getId())
