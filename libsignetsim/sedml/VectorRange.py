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

from libsignetsim.sedml.Range import Range
from libsignetsim.settings.Settings import Settings


class VectorRange(Range):

	def __init__(self, document):
		Range.__init__(self, document)
		self.__document = document
		self.__values = None

	def readSedml(self, vector_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Range.readSedml(self, vector_range, level, version)
		self.__values = vector_range.getValues()

	def writeSedml(self, vector_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Range.writeSedml(self, vector_range, level, version)
		if self.__values is not None:
			vector_range.setValues(self.__values)

	def getValues(self):
		return self.__values

	def setValues(self, values):
		self.__values = values

	def getValuesArray(self):
		return self.__values
