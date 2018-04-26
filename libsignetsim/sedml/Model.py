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

from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.HasId import HasId
from libsignetsim.sedml.container.ListOfChanges import ListOfChanges
from libsignetsim.sedml.Source import Source
from libsignetsim.sedml.SedmlException import SedmlModelLanguageNotSupported
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.settings.Settings import Settings
from os.path import exists, join, basename
from lxml import etree


class Model(SedBase, HasId):

	LANGUAGE_SBML = "urn:sedml:language:sbml"

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__language = None
		self.__source = Source(self.__document)
		self.__sbmlModel = None

		self.listOfChanges = ListOfChanges(self.__document, self)
		self.__nbChanges = 0
		self.__changesApplied = False

	def readSedml(self, model, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, model, level, version)
		HasId.readSedml(self, model, level, version)

		if model.isSetLanguage():
			self.__language = model.getLanguage()

			if not self.__language.startswith(self.LANGUAGE_SBML):

				if len(self.__language.split(":")) == 4:
					raise SedmlModelLanguageNotSupported("Language %s not supported" % self.__language.split(":")[3])
				else:
					raise SedmlModelLanguageNotSupported("Language %s not supported" % self.__language)

		if model.isSetSource():
			self.__source.readSedml(model.getSource(), level, version)

		self.listOfChanges.readSedml(model.getListOfChanges(), level, version)

	def writeSedml(self, model, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, model, level, version)
		HasId.writeSedml(self, model, level, version)

		if self.__language is not None:
			model.setLanguage(self.__language)

		if self.__source.writeSedml(level, version) is not None:
			model.setSource(str(self.__source.writeSedml(level, version)))

		self.listOfChanges.writeSedml(model.getListOfChanges(), level, version)

	def getSbmlModel(self):

		if self.__sbmlModel is None or self.__nbChanges != len(self.listOfChanges):

			self.__loadModel()
			self.__nbChanges = len(self.listOfChanges)

			if len(self.listOfChanges) > 0:
				self.listOfChanges.applyChanges(self.__sbmlModel)
				self.__changesApplied = True
		return self.__sbmlModel

	def __loadModel(self):
		sbml_doc = SbmlDocument()

		if self.listOfChanges.nbXMLChanges() > 0:
			with open(self.__source.getFilename(), 'rb') as sbml_file:
				sbmlTree = etree.XML(sbml_file.read())
				self.listOfChanges.applyXMLChanges(sbmlTree)
				sbml_doc.readSbmlFromString(etree.tostring(sbmlTree).decode('utf-8'))
		else:
			sbml_doc.readSbmlFromFile(self.__source.getFilename())

		self.__sbmlModel = sbml_doc.getModelInstance()

	def makeRelativePath(self, path):
		self.__source.makeRelativePath(path)

	def writeSbmlModelToPath(self, path):

		if self.__sbmlModel is None or self.__changesApplied:
			self.__loadModel()

		self.__sbmlModel.parentDoc.writeSbmlToFile(self.__source.getSource(), path)
		self.__source.setSource(basename(self.__source.getFilename()))

	def setLanguageSbml(self):
		self.__language = self.LANGUAGE_SBML

	def setSource(self, source):
		self.__source.setSource(source)

	def getSource(self):
		return self.__source

	def removePaths(self):
		self.__source.removePaths()

	def makeLocalSource(self):
		return self.__source.makeLocalSource()

