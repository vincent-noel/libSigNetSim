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

	def writeManifest(self):

		root = etree.Element("omexManifest")
		root.set("xmlns","http://identifiers.org/combine.specifications/omex-manifest")

		archive = etree.SubElement(root, "content")
		archive.set("location", ".")
		archive.set("format", "http://identifiers.org/combine.specifications/omex")

		manifest = etree.SubElement(root, "content")
		manifest.set("location", "./manifest.xml")
		manifest.set("format", "http://identifiers.org/combine.specifications/omex-manifest")

		for file in self.__archive.getListOfFiles():
			t_content = etree.SubElement(root, "content")
			t_content.set("location", "./" + file.getFilename())
			t_content.set("format", file.getFormat())
			if file.isMaster():
				t_content.set("master", "true")

		str = etree.tostring(root, encoding='utf-8', pretty_print=True, xml_declaration=True)
		# print str
		return str

	def getMaster(self):
		return self.__locations[self.__masters.index(True)]

	def isInManifest(self, filename):
		return filename in self.__locations

	def addInManifest(self, filename, format, master=False):
		self.__locations.append(filename)
		self.__format.append(format)
		self.__masters.append(master)

	def getFormat(self, filename):
		return self.__formats[self.__locations.index(filename)]

	def setFormat(self, filename, format):
		self.__formats[self.__locations.index(filename)] = format


	def isMaster(self, filename):
		return self.__masters[self.__locations.index(filename)]

	def setMaster(self, filename):
		if True in self.__formats:
			self.__formats = [False]*len(self.__locations)

		self.__formats[self.__locations.index(filename)] = True

