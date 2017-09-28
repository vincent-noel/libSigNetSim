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

from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.container.ListOfAlgorithmParameters import ListOfAlgorithmParameters
from libsignetsim.settings.Settings import Settings

class Algorithm(SedBase):

	KINSOL = "KISAO:0000282"
	CVODE = "KISAO:0000019"

	def __init__(self, document):

		SedBase.__init__(self, document)

		self.__document = document
		self.__kisaoID = None
		self.listOfAlgorithmParameters = ListOfAlgorithmParameters(document)

	def readSedml(self, algo, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, algo, level, version)

		if algo.isSetKisaoID():
			self.__kisaoID = algo.getKisaoID()

		self.listOfAlgorithmParameters.readSedml(algo.getListOfAlgorithmParameters(), level, version)

	def writeSedml(self, algo, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, algo, level, version)

		if self.__kisaoID is not None:
			algo.setKisaoID(self.__kisaoID)

		self.listOfAlgorithmParameters.writeSedml(algo.getListOfAlgorithmParameters(), level, version)

	def hasRelTol(self):
		return self.listOfAlgorithmParameters.hasRelTol()

	def hasAbsTol(self):
		return self.listOfAlgorithmParameters.hasAbsTol()

	def getRelTol(self):
		return self.listOfAlgorithmParameters.getRelTol()

	def getAbsTol(self):
		return self.listOfAlgorithmParameters.getAbsTol()

	def setKinSol(self):
		self.__kisaoID = self.KINSOL

	def setCVODE(self):
		self.__kisaoID = self.CVODE