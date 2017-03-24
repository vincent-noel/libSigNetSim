#!/usr/bin/env python
""" Parameter.py


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

class Parameter(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__value = None


	def readSedml(self, parameter, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, parameter, level, version)
		HasId.readSedml(self, parameter, level, version)

		if parameter.isSetValue():
			self.__value = parameter.getValue()

	def writeSedml(self, parameter, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, parameter, level, version)
		HasId.writeSedml(self, parameter, level, version)

		if self.__value is not None:
			parameter.setValue(self.__value)

	def getValue(self):
		return self.__value

	def setValue(self, value):
		self.__value = value