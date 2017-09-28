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

from libsignetsim.sedml.Change import Change
from libsignetsim.sedml.container.ListOfParameters import ListOfParameters
from libsignetsim.sedml.container.ListOfVariables import ListOfVariables
from libsignetsim.sedml.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings


class ComputeChange(Change):

	def __init__(self, document):

		Change.__init__(self, document)
		self.__document = document
		self.listOfVariables = ListOfVariables(self.__document, self)
		self.listOfParameters = ListOfParameters(self.__document, self)
		self.__math = MathFormula(self.__document)

	def readSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Change.readSedml(self, change, level, version)
		self.listOfVariables.readSedml(change.getListOfVariables(), level, version)
		self.listOfParameters.readSedml(change.getListOfParameters(), level, version)
		self.__math.readSedml(change.getMath(), level, version)

	def writeSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Change.writeSedml(self, change, level, version)
		self.listOfVariables.writeSedml(change.getListOfVariables(), level, version)
		self.listOfParameters.writeSedml(change.getListOfParameters(), level, version)
		change.setMath(self.__math.writeSedml(level, version))

	def getMath(self):
		return self.__math

	def setMath(self, math):
		self.__math = math