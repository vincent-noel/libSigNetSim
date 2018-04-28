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
from libsignetsim.numl.AtomicDescription import AtomicDescription
from libsignetsim.settings.Settings import Settings

class TupleDescription (DimensionDescription):

	def __init__(self, document, name=None):
		DimensionDescription.__init__(self, document, name)
		self.__document = document
		self.__atomicDescriptions = []

	def createAtomicDescription(self, name=None, value_type="double"):
		atomic_description = AtomicDescription(self.__document, name, value_type)
		atomic_description.setId("%s_0" % self.getId())
		self.__atomicDescriptions.append(atomic_description)
		return atomic_description

	def readNuML(self, tuple_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		DimensionDescription.readNuML(self, tuple_description, level, version)

		for i in range(tuple_description.size()):
			t_atomic_description = AtomicDescription(self.__document)
			t_atomic_description.readNuML(tuple_description.getAtomicDescription(i), level, version)
			self.__atomicDescriptions.append(t_atomic_description)

	def writeNuML(self, tuple_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		DimensionDescription.writeNuML(self, tuple_description, level, version)
		for atomic_description in self.__atomicDescriptions:
			t_atomic_description = tuple_description.createAtomicDescription()
			atomic_description.writeNuML(t_atomic_description, level, version)

	def getAtomicDescriptions(self):
		return self.__atomicDescriptions