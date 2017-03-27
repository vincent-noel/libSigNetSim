#!/usr/bin/env python
""" Model.py


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
from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.HasId import HasId
from libsignetsim.sedml.SedmlException import SedmlModelLanguageNotSupported, SedmlModelNotFound
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.settings.Settings import Settings
from os.path import exists, join

class Model(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__language = None
		self.__source = None
		self.__sbmlModel = None

	def readSedml(self, model, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, model, level, version)
		HasId.readSedml(self, model, level, version)

		if model.isSetLanguage():
			self.__language = model.getLanguage()

			if self.__language != "urn:sedml:language:sbml":

				if len(self.__language.split(":")) == 4:
					raise SedmlModelLanguageNotSupported("Language %s not supported" % self.__language.split(":")[3])
				else:
					raise SedmlModelLanguageNotSupported("Language %s not supported" % self.__language)

		if model.isSetSource():
			self.__source = model.getSource()

			if not exists(join(self.__document.path, self.__source)):
				raise SedmlModelNotFound("File %s not found" % self.__source)

			else:
				if Settings.verbose >= 1:
					print "> Loading SBML Document %s" % self.__source

	def writeSedml(self, model, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, model, level, version)
		HasId.writeSedml(self, model, level, version)

		if self.__language is not None:
			model.setLanguage(self.__language)

		if self.__source is not None:
			model.setSource(self.__source)

	def getSbmlModel(self):

		if self.__sbmlModel is None:
			self.__loadModel()

		return self.__sbmlModel

	def __loadModel(self):

		sbml_doc = SbmlDocument()
		sbml_doc.readSBMLFromFile(join(self.__document.path, self.__source))

		self.__sbmlModel = sbml_doc.getModelInstance()


