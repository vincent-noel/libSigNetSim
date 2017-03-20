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

	def __init__ (self, list_of_models=[],
						list_of_initial_values=None,
						experiment=None,
						timeMin=Settings.simulationTimeMin,
						timeMax=Settings.simulationTimeMax,
						ech=Settings.simulationTimeEch,
						abs_tol=1e-8,
						rel_tol=1e-6):

		CWriterModels.__init__(self, list_of_models, timeMin, timeMax, ech, abs_tol, rel_tol)

		if experiment is not None:
			CWriterData.__init__(self, {0:experiment}, workingModel=list_of_models[0])
		else:
			CWriterData.__init__(self, experiment, workingModel=list_of_models[0])

		self.experiment = experiment
		self.listOfModels = list_of_models
		self.timeMin = timeMin


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

		# if not exists(join(self.getTempDirectory(), Settings.C_simulationDirectory)):
		#     copytree(Settings.C_simulationSrcDirectory,
		#                 join(self.getTempDirectory(), Settings.C_simulationDirectory))
		#
		# if not exists(join(self.getTempDirectory(), Settings.C_sharedDirectory)):
		#     copytree(Settings.C_sharedSrcDirectory,
		#                 join(self.getTempDirectory(), Settings.C_sharedDirectory))
		#
		# if not exists(self.getTempDirectory() + Settings.C_generatedDirectory):
		#     mkdir(self.getTempDirectory() + Settings.C_generatedDirectory)

		t_vars_to_keep = []
		if self.experiment is not None:
			t_vars_to_keep = self.experiment.getTreatedVariables()


		for modelInd, model in enumerate(self.listOfModels):
			model.build(dont_reduce=True, tmin=self.timeMin)

		start = time()
		self.writeModelFiles()
		self.writeDataFiles()

		if Settings.verbose >= 1:
				print ">> Files written in %.2fs" % (time()-start)
