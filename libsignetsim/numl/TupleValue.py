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


from libsignetsim.numl.Dimension import Dimension
from libsignetsim.numl.AtomicValue import AtomicValue
from libsignetsim.settings.Settings import Settings

class TupleValue (Dimension):

	def __init__(self, document, result_component, description):
		Dimension.__init__(self, document, result_component, description)
		self.__document = document
		self.__atomicValues = []

	def createAtomicValue(self, description=None, value=None):

		atomic_value = AtomicValue(self.__document, self.getResultComponent(), description, value)
		self.__atomicValues.append(atomic_value)
		return atomic_value

	def readNuML(self, tuple_value, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		Dimension.readNuML(self, tuple_value, level, version)

		for i in range(tuple_value.size()):
			t_atomic_value = AtomicValue(self.__document, self.getResultComponent(), self.getDescription().getAtomicDescriptions()[i])
			t_atomic_value.readNuML(tuple_value.getAtomicValue(i), level, version)
			self.__atomicValues.append(t_atomic_value)

	def writeNuML(self, tuple_value, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		Dimension.writeNuML(self, tuple_value, level, version)

		for atomic_value in self.__atomicValues:
			t_atomic_value = tuple_value.createAtomicValue()
			atomic_value.writeNuML(t_atomic_value, level, version)

	def getAtomicValues(self):
		return self.__atomicValues