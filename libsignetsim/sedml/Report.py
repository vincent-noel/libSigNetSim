#!/usr/bin/env python
""" Report.py


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
from libsignetsim.sedml.Output import Output
from libsignetsim.sedml.container.ListOfDataSets import ListOfDataSets
from libsignetsim.settings.Settings import Settings


class Report(Output):

	def __init__(self, document):

		Output.__init__(self, document)

		self.__document = document
		self.listOfDataSets = ListOfDataSets(self.__document, self)

	def readSedml(self, report, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Output.readSedml(self, report, level, version)
		self.listOfDataSets.readSedml(report.getListOfDataSets(), level, version)

	def writeSedml(self, report, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Output.writeSedml(self, report, level, version)
		self.listOfDataSets.writeSedml(report.getListOfDataSets(), level, version)

	def build(self):
		self.listOfDataSets.build()

	def getData(self):

		return self.listOfDataSets.getData()

	def getDataToGenerate(self):

		return self.listOfDataSets.getDataToGenerate()
