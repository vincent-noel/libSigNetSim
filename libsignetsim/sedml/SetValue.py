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

from libsignetsim.sedml.ComputeChange import ComputeChange
from libsignetsim.sedml.SedmlException import SedmlUnknownXPATH
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.settings.Settings import Settings


class SetValue(ComputeChange):

	TARGET = 0
	SYMBOL = 1

	def __init__(self, document, repeated_task):

		ComputeChange.__init__(self, document)
		self.__document = document
		self.__repeatedTask = repeated_task
		self.__modelReference = None
		self.__range = None
		self.__variableType = None
		self.__symbol = None

	def readSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		ComputeChange.readSedml(self, change, level, version)

		if change.isSetModelReference():
			self.__modelReference = change.getModelReference()

		if change.isSetRange():
			self.__range = change.getRange()

		if change.isSetSymbol():
			self.__symbol = change.getSymbol()

	def writeSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		ComputeChange.writeSedml(self, change, level, version)

		if self.__modelReference is not None:
			change.setModelReference(self.__modelReference)

		if self.__range is not None:
			change.setRange(self.__range)

		if self.__symbol is not None:
			change.setSymbol(self.__symbol)

	def isTargetChange(self):
		return self.getTarget().getXPath() is not None

	def isSymbolChange(self):
		return self.__symbol is not None

	def setModelReference(self, model_reference):
		self.__modelReference = model_reference

	def setModel(self, model):
		self.__modelReference = model.getId()

	def setRangeReference(self, range_reference):
		self.__range = range_reference

	def setRange(self, range_obj):
		self.__range = range_obj.getId()


	def getValueChange(self):

		if self.isTargetChange():
			try:
				model = self.__document.listOfModels.getSbmlModelByReference(self.__modelReference)
				target = self.getTarget().getModelObject(model)

				range = self.__repeatedTask.listOfRanges.getByRangeId(self.__range)
				array_values = range.getValuesArray()

				return {target: array_values}
			except InvalidXPath as e:
				raise SedmlUnknownXPATH("Unknown XPath : %s" % e.message)

