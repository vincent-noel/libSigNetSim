#!/usr/bin/env python
""" DataGenerator.py


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
from libsignetsim.sedml.container.ListOfParameters import ListOfParameters
from libsignetsim.sedml.container.ListOfVariables import ListOfVariables
from libsignetsim.sedml.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
import libsedml
import libsbml


class DataGenerator(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.listOfVariables = ListOfVariables(self.__document, self)
		self.listOfParameters = ListOfParameters(self.__document, self)
		self.__math = MathFormula(self.__document)

		self.__data = None

	def readSedml(self, data_generator, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, data_generator, level, version)
		HasId.readSedml(self, data_generator, level, version)

		self.listOfVariables.readSedml(data_generator.getListOfVariables(), level, version)
		self.listOfParameters.readSedml(data_generator.getListOfParameters(), level, version)
		reload(libsedml)
		self.__math.readSedml(data_generator.getMath(), level, version)
		reload(libsbml)

	def writeSedml(self, data_generator, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, data_generator, level, version)
		HasId.writeSedml(self, data_generator, level, version)

		self.listOfVariables.writeSedml(data_generator.getListOfVariables(), level, version)
		self.listOfParameters.writeSedml(data_generator.getListOfParameters(), level, version)
		data_generator.setMath(self.__math.writeSedml(level, version))

	def getMath(self):
		return self.__math

	def setMath(self, math):
		self.__math = math

	def getTasksToRun(self):
		return self.listOfVariables.getTasksToRun()

	def build(self):
		# print self.listOfVariables.getData()
		self.__data = self.getMath().evaluateMathFormula(self.listOfVariables.getData(), self.listOfParameters.getSubs())

	def getData(self):
		return self.__data
