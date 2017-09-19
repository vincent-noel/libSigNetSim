#!/usr/bin/env python
""" ChangeAttribute.py


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
from libsignetsim.sedml.Change import Change
from libsignetsim.sedml.XPath import XPath
from libsignetsim.settings.Settings import Settings
from libsignetsim.sedml.SedmlException import SedmlModelObjectNotFound

class ChangeAttribute(Change):

	def __init__(self, document):

		Change.__init__(self, document)
		self.__document = document
		self.__newValue = None

	def readSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Change.readSedml(self, change, level, version)
		if change.isSetNewValue():
			self.__newValue = change.getNewValue()

	def writeSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Change.writeSedml(self, change, level, version)

		if self.__newValue is not None:
			change.setNewValue(str(self.__newValue))

	def setNewValue(self, value):
		self.__newValue = value

	def getNewValue(self):
		return self.__newValue

	def applyChange(self, sbml_model):
		self.getTarget().changeModelObject(sbml_model, self.__newValue)

