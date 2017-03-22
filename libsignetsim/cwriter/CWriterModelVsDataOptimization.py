#!/usr/bin/env python
""" CWriterModelVsDataOptimization.py


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

from libsignetsim.cwriter.CWriterModels import CWriterModels
from libsignetsim.cwriter.CWriterData import CWriterData
from libsignetsim.cwriter.CWriterOptimization import CWriterOptimization

class CWriterModelVsDataOptimization(CWriterOptimization, CWriterModels, CWriterData):

	def __init__ (self, workingModel, listOfExperiments=None, mapping=None, parameters_to_fit=None):

		self.listOfExperiments = listOfExperiments

		self.timeMin = None
		self.timeMax = None
		self.listOfSamples = None

		self.findSimulationSettings()

		CWriterModels.__init__(self, [workingModel], self.listOfSamples, Settings.defaultAbsTol, Settings.defaultRelTol, subdir="src")
		CWriterData.__init__(self, listOfExperiments, mapping, workingModel=workingModel, subdir="src")
		CWriterOptimization.__init__(self, workingModel, parameters_to_fit)



	def findSimulationSettings(self):

		# We need to start it at zero, even if the first observation is laters
		times = [0.0]
		for experiment in self.listOfExperiments:
			times += experiment.getTimes()

		self.listOfSamples = list(set(times))
		self.timeMin = min(self.listOfSamples)
		self.timeMax = max(self.listOfSamples)

	def writeOptimizationFiles(self, nb_procs):

		CWriterOptimization.writeOptimizationFiles(self, nb_procs)
		self.writeModelFiles()
		self.writeDataFiles()
		self.writeOptimFiles(nb_procs)


	def writeOptimFiles(self, nb_procs):

		c_filename = self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "optim.c"
		h_filename = self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "optim.h"

		f_c = open(c_filename, 'w')
		f_h = open(h_filename, 'w')

		self.writeOptimizationFilesHeaders(f_c, f_h)
		self.writeOptimizationGlobals(f_c, f_h)
		self.writeOptimizationGlobalMethods(f_c, f_h)
		self.writeOptimizationParameters(f_c, f_h)

		f_c.close()
		f_h.close()
