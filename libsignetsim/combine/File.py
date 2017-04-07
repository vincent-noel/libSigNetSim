#!/usr/bin/env python
""" File.py


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
from os.path import dirname, basename, join
from mimetypes import guess_type
from lxml import etree
from libsbml import SBMLReader

import libsbml
from libsedml import readSedMLFromString
reload(libsbml)

class File(object):

	XML = "application/xml"
	SBML = "http://identifiers.org/combine.specifications/sbml"
	SEDML = "http://identifiers.org/combine.specifications/sed-ml"
	CELLML = "http://identifiers.org/combine.specifications/cellml"
	MANIFEST = "http://identifiers.org/combine.specifications/omex-manifest"
	PDF = "application/pdf"
	MARKDOWN = "text/markdown"
	UNKNOWN = "application/octet-stream"


	KNOWN_FORMATS = {
		"xml" : XML,
		"sbml" : SBML,
		"sedml" : SEDML,
		"cellml" : CELLML,
		"pdf" : PDF,
		"md" : MARKDOWN,
	}

	def __init__(self, archive, manifest):

		self.__archive = archive
		self.__manifest = manifest
		self.__fullFilename = None
		self.__content = None

		self.__path = None
		self.__filename = None
		self.__extension = None
		self.__format = None

	def readFile(self, filename, archive_file):

		self.__path = dirname(filename)
		self.__filename = basename(filename)
		self.__extension = self.__filename.split(".")[1]
		if self.__extension in self.KNOWN_FORMATS:
			self.__format = self.KNOWN_FORMATS[self.__extension]
			if self.__format == self.XML:
				self.__format = self.guessXML(archive_file.read(filename))
		else:
			self.__format = guess_type(filename)[0]

		if self.__format is None:
			self.__format = self.UNKNOWN

		# print "Guessing mime type of %s : %s" % (filename, self.__format)

	def isMaster(self):
		return self.__manifest.isInManifest(self.getFilename()) and self.__manifest.isMaster(self.getFilename())

	def isSedml(self):
		return (self.__manifest.isInManifest(self.getFilename())
				and self.__manifest.getFormat(self.getFilename()).startswith("sed-ml")
		)

	def getFilename(self):
		return join(self.__path, self.__filename)

	def getFormat(self):
		return self.__format

	def guessXML(self, xml_content):
		root = etree.fromstring(xml_content)
		tag = root.tag.split("}")[1]

		if tag == "sbml":
			sbmlReader = SBMLReader()
			if sbmlReader is not None:
				sbmlDoc = sbmlReader.readSBMLFromString(xml_content)
				return self.SBML + ".level-%d.version-%d" % (sbmlDoc.getLevel(), sbmlDoc.getVersion())
			else:
				return self.SBML

		elif tag == "sedML":
			sedmlDoc = readSedMLFromString(xml_content)
			return self.SEDML + ".level-%d.version-%d" % (sedmlDoc.getLevel(), sedmlDoc.getVersion())

		elif tag == "omexManifest":
			return self.MANIFEST

		else:
			return self.XML


