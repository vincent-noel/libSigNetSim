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

	Initialization of the combine archive module

"""

from libsignetsim.settings.Settings import Settings
from os.path import dirname, basename, join
from mimetypes import guess_type
from lxml import etree
from libsbml import SBMLReader
import libsbml
from libnuml import readNUMLFromString
from libsedml import readSedMLFromString
reload(libsbml)
from shutil import copy


class File(object):

	__XML = "http://purl.org/NET/mediatypes/application/xml"
	__SBML = "http://identifiers.org/combine.specifications/sbml"
	__SEDML = "http://identifiers.org/combine.specifications/sed-ml"
	__NUML = "http://identifiers.org/combine.specifications/numl"
	__CELLML = "http://identifiers.org/combine.specifications/cellml"
	__MANIFEST = "http://identifiers.org/combine.specifications/omex-manifest"
	__PDF = "http://purl.org/NET/mediatypes/application/pdf"
	__MARKDOWN = "http://purl.org/NET/mediatypes/text/markdown"
	__UNKNOWN = "http://purl.org/NET/mediatypes/application/octet-stream"

	__KNOWN_FORMATS = {
		"xml" : __XML,
		"sbml" : __SBML,
		"sedml" : __SEDML,
		"numl" : __NUML,
		"cellml" : __CELLML,
		"pdf" : __PDF,
		"md" : __MARKDOWN,
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
		self.__extension = self.__filename.split(".")[-1]

		if self.__manifest.isInManifest(self.getFilename()) and self.__manifest.getFormat(self.getFilename()) is not None:
			self.__format = self.__manifest.getFormat(self.getFilename())

		elif self.__extension in self.__KNOWN_FORMATS:

			self.__format = self.__KNOWN_FORMATS[self.__extension]

			if self.__format == self.__XML:
				self.__format = self.__guessXML(archive_file.read(filename))

		else:
			self.__format = "http://purl.org/NET/mediatypes/%s" % guess_type(filename)[0]

		if self.__format is None:
			self.__format = self.__UNKNOWN


		if not self.__manifest.isInManifest(self.getFilename()):
			self.__manifest.addInManifest(self.getFilename(), self.__format)

		elif self.__manifest.getFormat(self.getFilename()) is None:
			self.__manifest.setFormat(self.getFilename(), self.__format)

	def newFile(self, filename):

		self.__filename = basename(filename)
		self.__extension = self.__filename.split('.')[-1]

		if self.__extension in self.__KNOWN_FORMATS:
			self.__format = self.__KNOWN_FORMATS[self.__extension]
			if self.__format == self.__XML:
				self.__format = self.__guessXML(open(filename, 'r').read())

		else:
			self.__format = "http://purl.org/NET/mediatypes/%s" % guess_type(filename)[0]

		if self.__format is None:
			self.__format = self.__UNKNOWN

		self.__manifest.addInManifest(self.__filename, self.__format)


	def isMaster(self):
		""" Tests if the file is set as a master file of the archive """
		return self.__manifest.isInManifest(self.getFilename()) and self.__manifest.isMaster(self.getFilename())

	def setMaster(self):
		""" Sets the file as a master file of the archive """
		if self.__manifest.isInManifest(self.getFilename()):
			self.__manifest.setMaster(self.getFilename())

	def isSedml(self):
		""" Tests if the file is a SEDML"""
		return (self.__manifest.isInManifest(self.getFilename())
				and self.__manifest.getFormat(self.getFilename()).startswith(self.__SEDML)
		)

	def isSbml(self):
		""" Tests if the file is a SBML"""
		return (self.__manifest.isInManifest(self.getFilename())
				and self.__manifest.getFormat(self.getFilename()).startswith(self.__SBML)
		)

	def isNuml(self):
		""" Tests if the file is a NUML"""
		return (
			self.__manifest.isInManifest(self.getFilename())
			and self.__manifest.getFormat(self.getFilename()).startswith(self.__NUML)
		)

	def getFilename(self):
		""" Returns the filename """
		if self.__path is not None:
			return join(self.__path, self.__filename)
		else:
			return self.__filename

	def getFormat(self):
		""" Returns the file's format """
		return self.__format

	def __guessXML(self, xml_content):
		root = etree.fromstring(xml_content)
		tag = root.tag.split("}")[1]

		if tag == "sbml":
			sbmlReader = SBMLReader()
			if sbmlReader is not None:
				sbmlDoc = sbmlReader.readSBMLFromString(xml_content)
				return self.__SBML + ".level-%d.version-%d" % (sbmlDoc.getLevel(), sbmlDoc.getVersion())
			else:
				return self.__SBML

		elif tag == "sedML":
			sedmlDoc = readSedMLFromString(xml_content)
			return self.__SEDML + ".level-%d.version-%d" % (sedmlDoc.getLevel(), sedmlDoc.getVersion())

		elif tag == "numl":
			numlDoc = readNUMLFromString(xml_content)
			return self.__NUML + ".level-%d.version-%d" % (numlDoc.getLevel(), numlDoc.getVersion())

		elif tag == "omexManifest":
			return self.__MANIFEST

		else:
			return self.__XML


