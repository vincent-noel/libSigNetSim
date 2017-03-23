#!/usr/bin/env python
""" Variable.py


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

class Variable(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__taskReference = None
		self.__modelReference = None
		self.__symbol = None
		self.__target = None


	def readSedml(self, variable, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, variable, level, version)
		HasId.readSedml(self, variable, level, version)

		if variable.isSetTaskReference():
			self.__taskReference = variable.getTaskReference()

		if variable.isSetModelReference():
			self.__modelReference = variable.getModelReference()

		if variable.isSetSymbol():
			self.__symbol = variable.getSymbol()

		if variable.isSetTarget():
			self.__target = variable.getTarget()

	def getTaskReference(self):
		return self.__taskReference

	def getModelReference(self):
		return self.__modelReference

	def getSymbol(self):
		return self.__symbol

	def getTarget(self):
		return self.__target
