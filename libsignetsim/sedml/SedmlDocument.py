#!/usr/bin/env python
""" SedmlDocument.py


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

from libsignetsim.sedml.container.ListOfModels import ListOfModels
from libsignetsim.sedml.container.ListOfSimulations import ListOfSimulations
from libsignetsim.sedml.container.ListOfTasks import ListOfTasks
from libsignetsim.sedml.container.ListOfDataGenerators import ListOfDataGenerators
from libsignetsim.sedml.container.ListOfOutputs import ListOfOutputs

from libsignetsim.sedml.SedmlException import SedmlFileNotFound

from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import readSedMLFromFile, writeSedMLToFile, SedDocument
reload(libsbml)

from os.path import dirname, basename, exists

class SedmlDocument(SedBase):
	""" Sedml document class """

	def __init__ (self):
		""" Constructor of model class """

		SedBase.__init__(self, self)

		self.path = None
		self.filename = None
		self.level = Settings.defaultSedmlLevel
		self.version = Settings.defaultSedmlVersion

		self.listOfModels = ListOfModels(self)
		self.listOfSimulations = ListOfSimulations(self)
		self.listOfTasks = ListOfTasks(self)
		self.listOfDataGenerators = ListOfDataGenerators(self)
		self.listOfOutputs = ListOfOutputs(self)


	def readSedmlFromFile(self, filename):

		if not exists(filename):
			raise SedmlFileNotFound("SED-ML file %s not found" % filename)

		document = readSedMLFromFile(filename)

		self.path = dirname(filename)
		self.filename = basename(filename)
		self.readSedml(document)

	def readSedml(self, document):

		self.level = document.getLevel()
		self.version = document.getVersion()

		SedBase.readSedml(self, document, self.level, self.version)

		self.listOfModels.readSedml(document.getListOfModels(), self.level, self.version)
		self.listOfSimulations.readSedml(document.getListOfSimulations(), self.level, self.version)
		self.listOfTasks.readSedml(document.getListOfTasks(), self.level, self.version)
		self.listOfDataGenerators.readSedml(document.getListOfDataGenerators(), self.level, self.version)
		self.listOfOutputs.readSedml(document.getListOfOutputs(), self.level, self.version)

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		document = SedDocument()

		document.setLevel(self.level)
		document.setVersion(self.version)

		SedBase.writeSedml(self, document, self.level, self.version)

		self.listOfModels.writeSedml(document.getListOfModels(), self.level, self.version)
		self.listOfSimulations.writeSedml(document.getListOfSimulations(), self.level, self.version)
		self.listOfTasks.writeSedml(document.getListOfTasks(), self.level, self.version)
		self.listOfDataGenerators.writeSedml(document.getListOfDataGenerators(), self.level, self.version)
		self.listOfOutputs.writeSedml(document.getListOfOutputs(), self.level, self.version)
		return document

	def writeSedmlToFile(self, filename, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		document = self.writeSedml(level, version)
		writeSedMLToFile(document, filename)

	def run(self):
		self.listOfTasks.buildTasks()
		self.listOfTasks.runTasks()
		self.listOfOutputs.build()
		# print self.listOfOutputs.getReports()[0].getData()




