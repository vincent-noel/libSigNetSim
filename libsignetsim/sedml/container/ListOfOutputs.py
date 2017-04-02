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

from libsignetsim.sedml.container.ListOf import ListOf
from libsignetsim.sedml.Plot2D import Plot2D
from libsignetsim.sedml.Report import Report
from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_OUTPUT_PLOT2D, SEDML_OUTPUT_REPORT
reload(libsbml)

class ListOfOutputs(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)
		self.__document = document
		self.__outputCounter = 0

	def new(self, output_type, output_id=None):

		t_output_id = output_id
		if t_output_id is None:
			t_output_id = "output_%d" % self.__outputCounter

		if output_type == SEDML_OUTPUT_PLOT2D:
			output = Plot2D(self.__document)
			output.setId(t_output_id)
			ListOf.append(self, output)
			self.__outputCounter += 1
			return output

		elif output_type == SEDML_OUTPUT_REPORT:
			output = Report(self.__document)
			output.setId(t_output_id)
			ListOf.append(self, output)
			self.__outputCounter += 1
			return output

	def createPlot2D(self, output_id=None):
		return self.new(SEDML_OUTPUT_PLOT2D, output_id)

	def createReport(self, output_id=None):
		return self.new(SEDML_OUTPUT_REPORT, output_id)

	def readSedml(self, list_of_outputs, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_outputs, level, version)

		for t_output in list_of_outputs:

			if t_output.getTypeCode() == SEDML_OUTPUT_PLOT2D:
				output = Plot2D(self.__document)
				output.readSedml(t_output, level, version)
				ListOf.append(self, output)
				self.__outputCounter += 1

			elif t_output.getTypeCode() == SEDML_OUTPUT_REPORT:
				output = Report(self.__document)
				output.readSedml(t_output, level, version)
				ListOf.append(self, output)
				self.__outputCounter += 1

	def writeSedml(self, list_of_outputs, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_outputs, level, version)

		for t_output in self:

			if isinstance(t_output, Plot2D):
				output = list_of_outputs.createPlot2D()
				t_output.writeSedml(output, level, version)

			elif isinstance(t_output, Report):
				output = list_of_outputs.createReport()
				t_output.writeSedml(output, level, version)

	def build(self):

		for output in self:
			output.build()

	def getReports(self):

		reports = []
		for output in self:
			if isinstance(output, Report):
				reports.append(output)

		return reports

	def getDataToGenerate(self):

		data = []
		for output in self:
			data += output.getDataToGenerate()

		return list(set(data))