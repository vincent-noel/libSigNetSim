#!/usr/bin/env python
""" Output.py


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
from libsignetsim.sedml.container.ListOfCurves import ListOfCurves
from libsignetsim.settings.Settings import Settings


class Plot2D(Output):

	def __init__(self, document):

		Output.__init__(self, document)

		self.__document = document
		self.listOfCurves = ListOfCurves(self.__document)

	def readSedml(self, plot, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Output.readSedml(self, plot, level, version)
		self.listOfCurves.readSedml(plot.getListOfCurves(), level, version)

	def writeSedml(self, plot, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Output.writeSedml(self, plot, level, version)
		self.listOfCurves.writeSedml(plot.getListOfCurves(), level, version)