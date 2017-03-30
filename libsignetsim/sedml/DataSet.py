#!/usr/bin/env python
""" DataSet.py


	This file ...


	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.

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

	def setLabel(self, label):
		self.__label = label

	def build(self):

		data_generator = self.__document.listOfDataGenerators.getDataGenerator(self.__dataReference)
		math = data_generator.getMath()
		data_variables = data_generator.listOfVariables.getData()

		self.__data = []

		for i in range(len(data_variables[data_variables.keys()[0]])):

			subs = {}
			for var in data_generator.listOfVariables:
				subs.update({var.getSympySymbol():float(data_variables[var][i])})

			subs.update(data_generator.listOfParameters.getSubs())

			self.__data.append(float(math.getInternalMathFormula().subs(subs)))

	def getData(self):

		return {self.__label: self.__data}

