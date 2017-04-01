#!/usr/bin/env python
""" AlgorithmParameter.py


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
from libsignetsim.settings.Settings import Settings

class AlgorithmParameter(SedBase):

	REL_TOL = 'KISAO:0000209'
	ABS_TOL = 'KISAO:0000211'

	def __init__(self, document):

		SedBase.__init__(self, document)

		self.__document = document
		self.__kisaoID = None
		self.__value = None

	def readSedml(self, algo_param, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, algo_param, level, version)

		if algo_param.isSetKisaoID():
			self.__kisaoID = algo_param.getKisaoID()

		if algo_param.isSetValue():
			self.__value = algo_param.getValue()

	def writeSedml(self, algo_param, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, algo_param, level, version)

		if self.__kisaoID is not None:
			algo_param.setKisaoID(self.__kisaoID)

		if self.__value is not None:
			algo_param.setValue(self.__value)

	def isRelTol(self):
		return self.__kisaoID == self.REL_TOL

	def isAbsTol(self):
		return self.__kisaoID == self.ABS_TOL

	def getValue(self):
		return self.__value