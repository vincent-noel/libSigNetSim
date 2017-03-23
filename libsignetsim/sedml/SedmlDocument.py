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

from libsignetsim.sedml.container.ListOfModels import ListOfModels
from libsignetsim.sedml.container.ListOfSimulations import ListOfSimulations
from libsignetsim.sedml.container.ListOfTasks import ListOfTasks
from libsignetsim.sedml.container.ListOfDataGenerators import ListOfDataGenerators
from libsignetsim.sedml.container.ListOfOutputs import ListOfOutputs
from libsignetsim.settings.Settings import Settings

from libsedml import readSedMLFromFile


class SedmlDocument(object):
	""" Sedml document class """

	def __init__ (self):
		""" Constructor of model class """

		self.listOfModels = ListOfModels(self)
		self.listOfSimulations = ListOfSimulations(self)
		self.listOfTasks = ListOfTasks(self)
		self.listOfDataGenerators = ListOfDataGenerators(self)
		self.listOfOutputs = ListOfOutputs(self)

		self.level = Settings.defaultSedmlLevel
		self.version = Settings.defaultSedmlVersion


	def readSedml(self, filename):

		document = readSedMLFromFile(filename)

		self.level = document.getLevel()
		self.version = document.getVersion()
		self.listOfModels.readSedml(document.getListOfModels(), self.level, self.version)
		self.listOfTasks.readSedml(document.getListOfTasks(), self.level, self.version)
		self.listOfSimulations.readSedml(document.getListOfSimulations(), self.level, self.version)
		self.listOfDataGenerators.readSedml(document.getListOfDataGenerators(), self.level, self.version)
		self.listOfOutputs.readSedml(document.getListOfOutputs(), self.level, self.version)