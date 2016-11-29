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
	    (time_max, time_ech) = self.findSimulationSettings()

	    CWriterModels.__init__(self, [workingModel], 0, time_max, time_ech, subdir="src")
	    CWriterData.__init__(self, listOfExperiments, mapping, workingModel=workingModel, subdir="src")
	    CWriterOptimization.__init__(self, workingModel, parameters_to_fit)



	def findSimulationSettings(self):

		#Find out max time
		time_max = 0
		for experiment in self.listOfExperiments.values():
		    if time_max < experiment.getMaxTime():
		        time_max = experiment.getMaxTime()

		#Find out necessary sampling
		time_ech = 10000.0
		cant_do_better = False

		while not cant_do_better:
			#We decrease the sampling
			time_ech = time_ech/10

			#While all values are not true
			cant_do_better = True
			for experiment in self.listOfExperiments.values():
				for t_point in experiment.getTimes():
					if float(t_point) > 0:
						#If the ratio between the sample time and the sampling time is superior to 1
						cant_do_better &= int(float(t_point)/time_ech) >= 1

					# time_ech = 30

		return (time_max, time_ech)


	def writeOptimizationFiles(self, nb_procs):

		CWriterOptimization.writeOptimizationFiles(self, nb_procs)
		print "finished copying libs"
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

	    self.writeOptimizationSettings(f_c, f_h, nb_procs)
	    self.writeOptimizationParameters(f_c, f_h)

	    # self.writeOptimizationFinalizeSettings(f_c, f_h)
	    # self.writeOptimizationFinalizeSettings(f_c, f_h)

	    f_c.close()
	    f_h.close()
