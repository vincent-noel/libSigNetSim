#!/usr/bin/env python
""" SetValue.py


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
from libsignetsim.sedml.ComputeChange import ComputeChange
from libsignetsim.settings.Settings import Settings


class SetValue(ComputeChange):

	def __init__(self, document):

		ComputeChange.__init__(self, document)
		self.__document = document
		self.__modelReference = None
		self.__range = None
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

