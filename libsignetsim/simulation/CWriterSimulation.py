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
from __future__ import print_function

from libsignetsim.settings.Settings import Settings
from libsignetsim.cwriter.CWriterModels import CWriterModels
from libsignetsim.cwriter.CWriterData import CWriterData
from libsignetsim.simulation.SimulationException import SimulationException
from os.path import join, isfile
from os import mkdir
from shutil import copyfile
from time import time
from glob import glob


class CWriterSimulation(CWriterModels, CWriterData):

	def __init__ (self, list_of_models,
						time_min,
						list_samples,
						experiment,
						abs_tol,
						rel_tol):

		self.listOfModels = list_of_models
		self.timeMin = time_min
		self.listOfSamples = list_samples
		self.absTol = abs_tol
		self.relTol = rel_tol
		CWriterModels.__init__(self, self.listOfModels, self.timeMin, self.listSamples, self.absTol, self.relTol)

		if experiment is not None:
			CWriterData.__init__(self, [experiment], workingModel=list_of_models[0])
		else:
			CWriterData.__init__(self, experiment, workingModel=list_of_models[0])

		self.experiment = experiment

	def writeSimulationFiles(self):

		mkdir(join(self.getTempDirectory(), "src"))
		mkdir(join(self.getTempDirectory(), "lib"))

		# First the code
		mkdir(join(self.getTempDirectory(), "src/integrate"))
		copyfile(join(Settings.basePath, "lib/integrate/src/integrate.h"), join(self.getTempDirectory(), "src/integrate/integrate.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/models.h"), join(self.getTempDirectory(), "src/integrate/models.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/datas.h"), join(self.getTempDirectory(), "src/integrate/datas.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/realtype_math.h"), join(self.getTempDirectory(), "src/integrate/realtype_math.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/types.h"), join(self.getTempDirectory(), "src/integrate/types.h"))

		# Then the shared libraries
		if not isfile(join(Settings.basePath, "lib/integrate/integrate.so")):
			integrate_filename = glob(join(Settings.basePath, "lib", "integrate", "integrate*.so"))
			if len(integrate_filename) > 0:
				copyfile(integrate_filename[0], join(self.getTempDirectory(), "lib/integrate.so"))
			else:
				raise SimulationException("Could not find the numerical integration library. Please reinstall libSigNetSim")
		else:
			copyfile(join(Settings.basePath, "lib/integrate/integrate.so"), join(self.getTempDirectory(), "lib/integrate.so"))

		copyfile(join(Settings.basePath, "lib/templates/simulation/Makefile"), join(self.getTempDirectory(), "Makefile") )
		copyfile(join(Settings.basePath, "lib/templates/simulation/main.c"), join(self.getTempDirectory(), "src/main.c") )

		treated_variables_names = []
		if self.experiment is not None:
			treated_variables_names = self.experiment.getTreatedVariables()

		for modelInd, model in enumerate(self.listOfModels):
			treated_variables = []
			for name in treated_variables_names:
				if model.listOfVariables.containsName(name):
					treated_variables.append(model.listOfVariables.getByName(name).getSbmlId())
				elif model.listOfVariables.containsSbmlId(name):
					treated_variables.append(model.listOfVariables.getBySbmlId(name).getSbmlId())

			reduce = Settings.reduceByDefault

			if len(treated_variables) > 0:
				reduce = False

			model.build(vars_to_keep=treated_variables, reduce=reduce, tmin=self.timeMin[modelInd])

		start = time()
		self.writeModelFiles()
		self.writeDataFiles()

		if Settings.verboseTiming >= 1:
				print(">> Files written in %.2fs" % (time()-start))
