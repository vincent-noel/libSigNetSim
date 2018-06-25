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


from libsignetsim.settings.Settings import Settings
from libsignetsim.sedml.SedmlException import SedmlUnknownURI
from libsignetsim.sedml.math.sympy_shortcuts import SympySymbol

class URI(object):

	SEDML = "sedml"
	MIRIAM = "miriam"

	BIOMODELS = "biomodels.db"
	SYMBOL = "symbol"

	def __init__(self, document):
		self.__document = document

		self.__type = None
		self.__tokens = None

		self.__symbol = None

		self.__url = None
		self.__filename = None

	def readSedml(self, uri, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		self.parseURI(uri)


	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		if self.__tokens is not None:
			return ":".join(self.__tokens)


	def parseURI(self, uri):
		if uri.startswith("urn:"):

			self.__tokens = uri.split(":")

			if len(self.__tokens) == 4 and self.__tokens[1] == self.MIRIAM and self.__tokens[2] == self.BIOMODELS:
				self.__url = "http://www.ebi.ac.uk/biomodels-main/download?mid=%s" % self.__tokens[3]
				self.__filename = "%s.xml" % self.__tokens[3]
				self.__type = self.BIOMODELS

			elif len(self.__tokens) == 4 and self.__tokens[1] == self.SEDML and self.__tokens[2] == self.SYMBOL:
				if self.__tokens[3] == 'time':
					self.__type = self.SYMBOL
					self.__symbol = SympySymbol("time")

				else:
					raise SedmlUnknownURI("Unknown symbol %s" % self.__tokens[3])

			else:
				raise SedmlUnknownURI("Unknown URI %s" % uri)


		else:
			raise SedmlUnknownURI(uri)

	def getURL(self):
		return self.__url

	def getFilename(self):
		return self.__filename

	def setURI(self, uri):
		self.parseURI(uri)

	def getSymbol(self):
		if self.__type == self.SYMBOL and self.__symbol is not None:
			return self.__symbol

	def isTime(self):
		return self.__type == self.SYMBOL and self.__symbol is not None and self.__symbol == SympySymbol("time")

	def setTime(self):
		self.parseURI("urn:sedml:symbol:time")