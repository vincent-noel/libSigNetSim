#!/usr/bin/env python
""" Curve.py


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


class Curve(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__xDataReference = None
		self.__yDataReference = None
		self.__logX = False
		self.__logY = False

	def readSedml(self, curve, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, curve, level, version)
		HasId.readSedml(self, curve, level, version)

		if curve.isSetXDataReference():
			self.__xDataReference = curve.getXDataReference()

		if curve.isSetYDataReference():
			self.__yDataReference = curve.getYDataReference()

		if curve.isSetLogX():
			self.__logX = curve.getLogX()

		if curve.isSetLogY():
			self.__logY = curve.getLogY()

	def getXDataReference(self):
		return self.__xDataReference

	def getYDataReference(self):
		return self.__yDataReference

	def getLogX(self):
		return self.__logX

	def getLogY(self):
		return self.__logY
