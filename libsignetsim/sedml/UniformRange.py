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

from numpy import linspace, logspace, log10
class UniformRange(Range):

	LINEAR = "linear"
	LOG = "log"

	def __init__(self, document):

		Range.__init__(self, document)
		self.__document = document

		self.__start = None
		self.__end = None
		self.__numberOfPoints = None
		self.__type = None

	def readSedml(self, uniform_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		Range.readSedml(self, uniform_range, level, version)

		if uniform_range.isSetStart():
			self.__start = uniform_range.getStart()

		if uniform_range.isSetEnd():
			self.__end = uniform_range.getEnd()

		if uniform_range.isSetNumberOfPoints():
			self.__numberOfPoints = uniform_range.getNumberOfPoints()

		if uniform_range.isSetType():
			self.__type = uniform_range.getType()

	def writeSedml(self, uniform_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		Range.writeSedml(self, uniform_range, level, version)

		if self.__start is not None:
			uniform_range.setStart(self.__start)

		if self.__end is not None:
			uniform_range.setEnd(self.__end)

		if self.__numberOfPoints is not None:
			uniform_range.setNumberOfPoints(self.__numberOfPoints)

		if self.__type is not None:
			uniform_range.setType(self.__type)

	def getStart(self):
		return self.__start

	def getEnd(self):
		return self.__end

	def getNumberOfPoints(self):
		return self.__numberOfPoints

	def getType(self):
		return self.__type

	def setStart(self, start):
		self.__start = start

	def setEnd(self, end):
		self.__end = end

	def setNumberOfPoints(self, number_of_points):
		self.__numberOfPoints = number_of_points

	def setStype(self, type):
		self.__type = type

	def setLinear(self):
		self.__type = self.LINEAR

	def setLog(self):
		self.__type = self.LOG

	def getValuesArray(self):
		if self.__type == self.LOG:
			return [0]+list(logspace(log10(self.__start), log10(self.__end), self.__numberOfPoints+1))
		else:
			return linspace(self.__start, self.__end, self.__numberOfPoints+1)
