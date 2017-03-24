#!/usr/bin/env python
""" ListOfOutputs.py


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
from libsignetsim.sedml.Plot2D import Plot2D
from libsignetsim.sedml.Report import Report
from libsignetsim.settings.Settings import Settings
# import libsbml

from libsedml import SEDML_OUTPUT_PLOT2D, SEDML_OUTPUT_REPORT
# reload(libsbml)

class ListOfOutputs(SedBase):

	def __init__(self, document):

		SedBase.__init__(self, document)
		self.__document = document
		self.listOfOutputs = []

	def readSedml(self, list_of_outputs, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, list_of_outputs, level, version)

		for t_output in list_of_outputs:

			if t_output.getTypeCode() == SEDML_OUTPUT_PLOT2D:
				output = Plot2D(self.__document)
				output.readSedml(t_output, level, version)
				self.listOfOutputs.append(output)

			elif t_output.getTypeCode() == SEDML_OUTPUT_REPORT:
				output = Report(self.__document)
				output.readSedml(t_output, level, version)
				self.listOfOutputs.append(output)

	def writeSedml(self, list_of_outputs, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, list_of_outputs, level, version)

		for t_output in self.listOfOutputs:

			if isinstance(t_output, Plot2D):
				output = list_of_outputs.createPlot2D()
				t_output.writeSedml(output, level, version)

			elif isinstance(t_output, Report):
				output = list_of_outputs.createReport()
				t_output.writeSedml(output, level, version)