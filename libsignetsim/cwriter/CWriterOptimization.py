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

	This file the CWriterOptimization class definition, which writes
	the common code for the different optimizations.

"""


from libsignetsim.settings.Settings import Settings
from libsignetsim.optimization.OptimizationException import OptimizationCompilationException
from shutil import copytree, copyfile
from os.path import join, isfile
from os import mkdir
from glob import glob
from random import randrange


class CWriterOptimization(object):

	def __init__(self, workingModel, parameters,
				p_lambda=Settings.defaultPlsaLambda,
				p_criterion=Settings.defaultPlsaCriterion,
				p_precision=Settings.defaultPlsaPrecision,
				p_initial_temperature=Settings.defaultPlsaInitialTemperature,
				p_gain=Settings.defaultPlsaGainForJumpSizeControl,
				p_interval=Settings.defaultPlsaInterval,
				p_mix=Settings.defaultPlsaMixInterval,
				p_initial_moves=Settings.defaultPlsaInitialMoves,
				p_tau=Settings.defaultPlsaTau,
				p_freeze_count=Settings.defaultPlsaFreezeCount,
	):

		self.workingModel = workingModel
		self.parameters = parameters
		self.pLambda = p_lambda
		self.pCriterion = p_criterion
		self.pPrecision = p_precision
		self.pInitialTemp = p_initial_temperature
		self.pGain = p_gain
		self.pInterval = p_interval
		self.pMix = p_mix
		self.pInitialMoves = p_initial_moves
		self.pTau = p_tau
		self.pFreezeCount = p_freeze_count

	def writeOptimizationFiles(self, nb_procs):

		mkdir(join(self.getTempDirectory(), "src"))
		mkdir(join(self.getTempDirectory(), "lib"))

		# First the code
		mkdir(join(self.getTempDirectory(), "src/integrate"))
		copyfile(join(Settings.basePath, "lib/integrate/src/integrate.h"), join(self.getTempDirectory(), "src/integrate/integrate.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/models.h"), join(self.getTempDirectory(), "src/integrate/models.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/datas.h"), join(self.getTempDirectory(), "src/integrate/datas.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/realtype_math.h"), join(self.getTempDirectory(), "src/integrate/realtype_math.h"))
		copyfile(join(Settings.basePath, "lib/integrate/src/types.h"), join(self.getTempDirectory(), "src/integrate/types.h"))

		mkdir(join(self.getTempDirectory(), "src/plsa"))
		copyfile(join(Settings.basePath, "lib/plsa/src/sa.h"), join(self.getTempDirectory(), "src/plsa/sa.h"))
		copyfile(join(Settings.basePath, "lib/plsa/src/config.h"), join(self.getTempDirectory(), "src/plsa/config.h"))
		copyfile(join(Settings.basePath, "lib/plsa/src/types.h"), join(self.getTempDirectory(), "src/plsa/types.h"))

		copyfile(join(Settings.basePath, "lib/scoreFunctions.h"), join(self.getTempDirectory(), "src/scoreFunctions.h"))
		copyfile(join(Settings.basePath, "lib/scoreFunctions.c"), join(self.getTempDirectory(), "src/scoreFunctions.c"))

		# Then the shared
		if not isfile(join(Settings.basePath, "lib/integrate/integrate.so")):
			integrate_filename = glob(join(Settings.basePath, "lib", "integrate", "integrate*.so"))
			if len(integrate_filename) > 0:
				copyfile(integrate_filename[0],
						 join(self.getTempDirectory(), "lib/integrate.so"))
			else:
				raise OptimizationCompilationException("Could not find the numerical integration library. Please reinstall libSigNetSim")
		else:
			copyfile(join(Settings.basePath, "lib/integrate/integrate.so"), join(self.getTempDirectory(), "lib/integrate.so"))

		if not isfile(join(Settings.basePath, "lib/plsa/libplsa-serial.so")):
			plsa_serial_filename = glob(join(Settings.basePath, "lib", "plsa", "libplsa-serial*.so"))
			if len(plsa_serial_filename) > 0:
				copyfile(plsa_serial_filename[0],
						 join(self.getTempDirectory(), "lib/libplsa-serial.so"))
			else:
				raise OptimizationCompilationException(
					"Could not find the numerical integration library. Please reinstall libSigNetSim")
		else:
			copyfile(join(Settings.basePath, "lib/plsa/libplsa-serial.so"), join(self.getTempDirectory(), "lib/libplsa-serial.so"))

		if not isfile(join(Settings.basePath, "lib/plsa/libplsa-parallel.so")):
			plsa_parallel_filename = glob(join(Settings.basePath, "lib", "plsa", "libplsa-parallel*.so"))
			if len(plsa_parallel_filename) > 0:
				copyfile(plsa_parallel_filename[0],
						 join(self.getTempDirectory(), "lib/libplsa-parallel.so"))
			else:
				raise OptimizationCompilationException(
					"Could not find the numerical integration library. Please reinstall libSigNetSim")
		else:
			copyfile(join(Settings.basePath, "lib/plsa/libplsa-parallel.so"), join(self.getTempDirectory(), "lib/libplsa-parallel.so"))

		copyfile(join(Settings.basePath, "lib/templates/data_optimization/Makefile"), join(self.getTempDirectory(), "Makefile") )
		copyfile(join(Settings.basePath, "lib/templates/data_optimization/main.c"), join(self.getTempDirectory(), "src/main.c") )

	def writeOptimizationFilesHeaders(self, f_c, f_h):

		f_c.write("#include <stdlib.h>\n")
		f_c.write("#include <stdio.h>\n")
		f_c.write("#include \"optim.h\"\n")

		f_h.write("#include \"plsa/sa.h\"\n")
		f_h.write("#include \"plsa/config.h\"\n")
		f_h.write("#include \"integrate/models.h\"\n")
		f_h.write("#include \"scoreFunctions.h\"\n")

	def writeOptimizationGlobals(self, f_c, f_h):

		f_c.write("PArrPtr * my_plist;\n")

	def writeOptimizationGlobalMethods(self, f_c, f_h):

		f_h.write("PArrPtr * getOptimParameters(void);\n")
		f_c.write("PArrPtr * getOptimParameters(void)\n")
		f_c.write("{\n\treturn my_plist;\n}\n\n")

	def writeOptimizationParameters(self, f_c, f_h):

		f_h.write("void init_params(ModelDefinition * model);\n")
		f_c.write("void init_params(ModelDefinition * model)\n{\n")

		f_c.write("\tmy_plist = InitPLSAParameters(%d);\n" % len(self.parameters))

		for (i_param, (param, value, lb, ub, precision)) in enumerate(self.parameters):
			f_c.write("\tmy_plist->array[%d] = (ParamList) {&(model->constant_variables[%d].value), %g, (Range) {%g, %g}, %g, \"%s\"};\n" % (i_param, param.ind, value, lb, ub, precision, param.getXPath()))

		f_c.write("}")

	def writeOptimizationSettings(self, f_c, f_h):

		f_h.write("void init_settings(SAType * settings);\n")
		f_c.write("void init_settings(SAType * settings)\n{\n")

		f_c.write("\tsettings->seed = %g;\n" % self.randomPlsaSeed())
		f_c.write("\tsettings->initial_temp = %g;\n" % self.pInitialTemp)
		f_c.write("\tsettings->gain_for_jump_size_control = %g;\n" % self.pGain)
		f_c.write("\tsettings->interval = %g;\n" % self.pInterval)
		f_c.write("\tsettings->initial_moves = %g;\n" % self.pInitialMoves)
		f_c.write("\tsettings->tau = %g;\n" % self.pTau)
		f_c.write("#ifdef MPI\n")
		f_c.write("\tsettings->mix_interval = %g;\n" % self.pMix)
		f_c.write("#endif\n")
		f_c.write("\tsettings->lambda = %g;\n" % self.pLambda)
		f_c.write("\tsettings->criterion = %g;\n" % self.pCriterion)
		f_c.write("\tsettings->param_precision = %g;\n" % self.pPrecision)
		f_c.write("\tsettings->freeze_count = %d;\n" % self.pFreezeCount)
		f_c.write("}")


	def randomPlsaSeed(self):
		return randrange(-2147483647, +2147483647)
