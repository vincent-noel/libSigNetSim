#!/usr/bin/env python
""" CWriterSimulation.py


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

from os.path import join, exists
from os import mkdir
from shutil import copytree, copyfile
from time import time

class CWriterSimulation(CWriterModels, CWriterData):

	def __init__ (self, list_of_models,
						list_samples,
						experiment=None,
						abs_tol=Settings.defaultAbsTol,
						rel_tol=Settings.defaultRelTol):

		if abs_tol is not None:
			self.absTol = abs_tol
		else:
			self.absTol = Settings.defaultAbsTol

		if rel_tol is not None:
			self.relTol = rel_tol
		else:
			self.relTol = Settings.defaultRelTol

		CWriterModels.__init__(self, list_of_models, list_samples, self.absTol, self.relTol)

		if experiment is not None:
			CWriterData.__init__(self, [experiment], workingModel=list_of_models[0])
		else:
			CWriterData.__init__(self, experiment, workingModel=list_of_models[0])

		self.listSamples = list_samples
		self.experiment = experiment
		self.listOfModels = list_of_models


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
		copyfile(join(Settings.basePath, "lib/integrate/integrate.so"), join(self.getTempDirectory(), "lib/integrate.so"))

		copyfile(join(Settings.basePath, "lib/templates/simulation/Makefile"), join(self.getTempDirectory(), "Makefile") )
		copyfile(join(Settings.basePath, "lib/templates/simulation/main.c"), join(self.getTempDirectory(), "src/main.c") )

		# t_vars_to_keep = []
		# if self.experiment is not None:
		# 	t_vars_to_keep = self.experiment.getTreatedVariables()


		for modelInd, model in enumerate(self.listOfModels):
			model.build(dont_reduce=True, tmin=min(self.listSamples))

		start = time()
		self.writeModelFiles()
		self.writeDataFiles()

		if Settings.verboseTiming >= 1:
				print ">> Files written in %.2fs" % (time()-start)
