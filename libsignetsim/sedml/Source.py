#!/usr/bin/env python
""" Source.py


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
from libsignetsim.sedml.URI import URI
from libsignetsim.settings.Settings import Settings
from libsignetsim.sedml.SedmlException import SedmlModelNotFound
from re import match
from urllib import URLopener
from os.path import join, exists
import json
import requests

class Source(object):

	LOCAL = 0
	DISTANT = 1
	URN = 2

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
		# if source.startswith("http:"):
		# 	self.__sourceType = self.DISTANT
		# 	self.__url = source
		# 	self.__filename = join(Settings.tempDirectory, source.split('/')[-1])
		#
		# 	# download_file = URLopener()
		# 	# download_file.retrieve(self.__url, self.__filename)
		#
		# elif source.startswith("urn:"):
		# 	# print "URN detected"
		# 	self.__sourceType = self.URN
		# 	self.__uri.readSedml(source, level, version)
		# 	if self.__uri.getURL():
		# 		self.__url = self.__uri.getURL()
		#
		# 		# print "Download URN done"
		# else:
		# 	self.__sourceType = self.LOCAL
		# 	self.__sourceAvailable = True
		# 	self.__filename = join(self.__document.path, source)
		#
		# if not exists(self.__filename):
		# 	raise SedmlModelNotFound("File %s not found" % self.__source)
		#
		# else:
		# 	if Settings.verbose >= 1:
		# 		print "> Loading SBML Document %s" % self.__source

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

		else:
			self.__sourceType = self.LOCAL
			self.__sourceAvailable = True
			self.__filename = join(self.__document.path, source)

	def downloadSource(self):

		download_file = URLopener()
		download_file.retrieve(self.__url, self.__filename)
		self.__sourceAvailable = True

	def getSource(self):
		return self.__source

	def getFilename(self):
		if not self.__sourceAvailable:
			self.downloadSource()
		return self.__filename

	def setSource(self, source):
		self.__source = source
		self.parseSource(source)
