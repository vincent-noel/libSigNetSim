#!/usr/bin/env python
""" Manifest.py


	Initialization of the combine archive module


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

from lxml import etree

class Manifest(object):

	OMEX_MANIFEST = "{http://identifiers.org/combine.specifications/omex-manifest}"
	CONTENT = OMEX_MANIFEST + "content"
	LOCATION = "location"
	FORMAT = "format"
	MASTER = "master"

	def __init__(self, archive):

		self.__archive = archive
		self.__locations = []
		self.__formats = []
		self.__masters = []

	def readManifest(self, manifest):

		root = etree.fromstring(manifest)
		for child in root:
			if child.tag == self.CONTENT:
				if self.LOCATION in child.keys() and self.FORMAT in child.keys():

					self.__locations.append(child.get(self.LOCATION)[2:])

					t_format = child.get(self.FORMAT).split("/")
					self.__formats.append(t_format[len(t_format)-1])

					if child.get(self.MASTER) is not None:
						self.__masters.append(child.get(self.MASTER) == "true")
					else:
						self.__masters.append(False)

	def getMaster(self):

		ind_master = self.__masters.index(True)
		return (self.__locations[ind_master], self.__formats[ind_master])

	def getAllSedmls(self):
		return [self.__locations[i] for i, format in enumerate(self.__formats) if format.startswith("sed-ml")]

	def getAllSbmls(self):
		return [self.__locations[i] for i, format in enumerate(self.__formats) if format.startwith("sbml")]

	def getTestSuiteExpectedResults(self):

		for location in self.__locations:
			if location.endswith("results.csv"):
				return location

	def getTempDirectory(self):
		return self.path
