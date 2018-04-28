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

from future import standard_library
standard_library.install_aliases()

from libsignetsim.sedml.URI import URI
from libsignetsim.sedml.SedmlException import SedmlFileNotFound
from libsignetsim.settings.Settings import Settings
from six.moves.urllib.request import urlretrieve
from os.path import join, exists, isabs, relpath, commonprefix, basename
from os import getcwd

class Source(object):

	LOCAL = 0
	DISTANT = 1
	URN = 2
	REF = 3

	def __init__(self, document):
		self.__document = document
		self.__source = None
		self.__sourceType = None
		self.__sourceAvailable = False
		self.__filename = None
		self.__url = None
		self.__uri = URI(self.__document)

	def readSedml(self, source, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		self.__source = source
		self.parseSource(source)

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		if self.__source is not None:
			return self.__source

	def parseSource(self, source):

		if source.startswith("http:"):
			self.__sourceType = self.DISTANT
			self.__url = source
			self.__filename = join(Settings.tempDirectory, source.split('/')[-1])

		elif source.startswith("urn:"):

			self.__sourceType = self.URN
			self.__uri.setURI(source)
			if self.__uri.getURL():
				self.__url = self.__uri.getURL()
				self.__filename = join(Settings.tempDirectory, self.__uri.getFilename())

		elif self.__document.listOfModels.getModelByReference(source) is not None:
			self.__sourceType = self.REF
			self.__ref = source
			# self.__filename = self.__document.listOfModels.getModelByReference(source).getSource().getFilename()
			# self.__sourceAvailable = True
		else:
			self.__sourceType = self.LOCAL
			self.__sourceAvailable = True
			if isabs(source) or exists(join(getcwd(), source)):
				self.__filename = source

			elif self.__document.path is not None:
				self.__filename = join(self.__document.path, source)
			else:
				raise SedmlFileNotFound("File not found : %s" % source)

	def buildSource(self):

		if self.__sourceType == self.LOCAL:
			return self.__source

		elif self.__sourceType == self.DISTANT:
			return self.__url

		elif self.__sourceType == self.URN:
			return self.__uri.writeSedml()

		elif self.__sourceType == self.REF:
			return self.__ref


	def downloadSource(self):

		urlretrieve(self.__url, self.__filename)
		self.__sourceAvailable = True

	def getSource(self):
		return self.__source

	def getFilename(self):
		# print "Getting filename for %s" % self.__source

		if self.__sourceType == self.REF:
			return self.__document.listOfModels.getModelByReference(self.__source).getSource().getFilename()
		elif not self.__sourceAvailable:
			self.downloadSource()
		return self.__filename

	def setSource(self, source):
		self.__source = source
		self.parseSource(source)

	def isLocal(self):
		return self.__sourceType == self.LOCAL

	def makeRelativePath(self, path):

		if self.__sourceType == self.LOCAL and (isabs(self.__source) or commonprefix([self.__source, path]) != ""):
			self.__source = relpath(self.__source, path)

	def getSourceType(self):
		return self.__sourceType

	def removePaths(self):

		if self.__sourceType == self.LOCAL:
			self.__filename = basename(self.__filename)
			self.__source = basename(self.__source)

	def makeLocalSource(self):

		if self.__sourceType in [self.URN, self.DISTANT]:

			t_filename = self.getFilename()
			self.__sourceType = self.LOCAL
			self.__filename = t_filename.split('/')[-1]
			self.__sourceAvailable = True
			return t_filename
