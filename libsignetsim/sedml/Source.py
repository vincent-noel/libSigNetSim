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
from libsignetsim.settings.Settings import Settings
from libsignetsim.sedml.SedmlException import SedmlModelNotFound
from re import match
from urllib import URLopener
from os.path import join, exists
import json
import requests

class Source(object):

	def __init__(self, document):
		self.__document = document
		self.__source = None
		self.__filename = None

	def readSedml(self, source, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		self.__source = source

		if source.startswith("http:"):
			self.__filename = join(Settings.tempDirectory, source.split('/')[-1])

			download_file = URLopener()
			download_file.retrieve(source, self.__filename)

		elif source.startswith("urn:"):

			tokens = source.split(":")
			if len(tokens) == 4 and tokens[1] == "miriam" and tokens[2] == "biomodels.db":
				self.__filename = join(Settings.tempDirectory, tokens[3] + ".xml")
				link = "http://www.ebi.ac.uk/biomodels-main/download?mid=%s" % tokens[3]

				download_file = URLopener()
				download_file.retrieve(link, self.__filename)

			# server = "http://www.ebi.ac.uk"
			# ext = "/miriamws/main/rest/resolve/"
			# r = requests.get(server + ext + source, headers={"Accept": "application/json"})
			#
			# if not r.ok:
			# 	r.raise_for_status()
			# else:
			# 	jobject = json.loads(r.content)
			# 	urls = [uri['$'] for uri in jobject["uri"]]
			# 	for uri in jobject["uri"]:
			# 		print uri['$']
			#

		else:
			self.__filename = join(self.__document.path, source)

		if not exists(self.__filename):
			raise SedmlModelNotFound("File %s not found" % self.__source)

		else:
			if Settings.verbose >= 1:
				print "> Loading SBML Document %s" % self.__source

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		if self.__source is not None:
			return self.__source

	def getSource(self):
		return self.__source

	def getFilename(self):
		return self.__filename

	def setSource(self, source):
		self.__source = source
		# self.__filename = join(self.__document.path, source)
