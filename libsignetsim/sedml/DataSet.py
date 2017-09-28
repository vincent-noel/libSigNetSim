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
from libsignetsim.sedml.HasId import HasId
from libsignetsim.settings.Settings import Settings


class DataSet(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__dataReference = None
		self.__label = None

		self.__data = None

	def readSedml(self, data_set, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, data_set, level, version)
		HasId.readSedml(self, data_set, level, version)

		if data_set.isSetDataReference():
			self.__dataReference = data_set.getDataReference()

		if data_set.isSetLabel():
			self.__label = data_set.getLabel()

	def writeSedml(self, data_set, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, data_set, level, version)
		HasId.writeSedml(self, data_set, level, version)

		if self.__dataReference is not None:
			data_set.setDataReference(self.__dataReference)

		if self.__label is not None:
			data_set.setLabel(self.__label)

	def getDataReference(self):
		return self.__dataReference

	def getLabel(self):
		return self.__label

	def setDataReference(self, data_reference):
		self.__dataReference = data_reference

	def setData(self, data):
		self.__dataReference = data.getId()

	def setLabel(self, label):
		self.__label = label

	def getData(self):

		data_generator = self.__document.listOfDataGenerators.getDataGenerator(self.__dataReference)
		return {self.__label: data_generator.getData()}

	def getDataToGenerate(self):

		return self.__document.listOfDataGenerators.getDataGenerator(self.__dataReference)