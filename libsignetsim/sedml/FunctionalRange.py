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
from libsignetsim.sedml.container.ListOfParameters import ListOfParameters
from libsignetsim.sedml.container.ListOfVariables import ListOfVariables
from libsignetsim.sedml.math.MathFormula import MathFormula
from libsignetsim.sedml.SedmlException import SedmlNotImplemented
from libsignetsim.settings.Settings import Settings


class FunctionalRange(Range):

	def __init__(self, document):

		Range.__init__(self, document)

		self.__document = document
		self.listOfVariables = ListOfVariables(self.__document, self)
		self.listOfParameters = ListOfParameters(self.__document, self)
		self.__math = MathFormula(self.__document)

	def readSedml(self, functional_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Range.readSedml(self, functional_range, level, version)

		self.listOfVariables.readSedml(functional_range.getListOfVariables(), level, version)
		self.listOfParameters.readSedml(functional_range.getListOfParameters(), level, version)
		self.__math.readSedml(functional_range.getMath(), level, version)

	def writeSedml(self, functional_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Range.writeSedml(self, functional_range, level, version)

		self.listOfVariables.writeSedml(functional_range.getListOfVariables(), level, version)
		self.listOfParameters.writeSedml(functional_range.getListOfParameters(), level, version)
		functional_range.setMath(self.__math.writeSedml(level, version))

	def getMath(self):
		return self.__math

	def setMath(self, math):
		self.__math = math

	def getValuesArray(self):
		raise SedmlNotImplemented("Functional range is not implemented yet")