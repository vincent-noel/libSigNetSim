#!/usr/bin/env python
""" URI.py


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
from libsignetsim.settings.Settings import Settings
from libsignetsim.sedml.SedmlException import SedmlUnknownURI
from re import match
from urllib import URLopener
from os.path import join, exists
import json
import requests

class URI(object):

	SEDML = "sedml"
	MIRIAM = "miriam"

	def __init__(self, document):
		self.__document = document
		self.__type = None
		self.__tokens = None
		self.__url = None
		self.__filename = None

	def readSedml(self, source, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		self.parseURI(source)
		# if source.startswith("urn:"):
		#
		# 	tokens = source.split(":")
		# 	if len(tokens) == 4 and tokens[1] == "miriam" and tokens[2] == "biomodels.db":
		# 		self.__url = "http://www.ebi.ac.uk/biomodels-main/download?mid=%s" % tokens[3]
		# 		self.__filename = "%s.xml" % tokens[3]
		#
		# else:
		# 	raise SedmlUnknownURI(source)
	#
	# def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
	# 	if self.__source is not None:
	# 		return self.__source
	def parseURI(self, uri):
		if uri.startswith("urn:"):

			tokens = uri.split(":")
			if len(tokens) == 4 and tokens[1] == "miriam" and tokens[2] == "biomodels.db":
				self.__url = "http://www.ebi.ac.uk/biomodels-main/download?mid=%s" % tokens[3]
				self.__filename = "%s.xml" % tokens[3]

		else:
			raise SedmlUnknownURI(uri)

	def getURL(self):
		return self.__url

	def getFilename(self):
		return self.__filename

	def setURI(self, uri):
		self.parseURI(uri)