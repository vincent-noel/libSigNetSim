#!/usr/bin/env python
""" CWriterOptimization.py


	This file the CWriterOptimization class definition, which writes
	the common code for the different optimizations.


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

from shutil import copytree, copyfile
from os.path import join
from os import mkdir
from random import randrange

class CWriterOptimization(object):

	def __init__ (self, workingModel, parameters):

		self.workingModel = workingModel
		self.parameters = parameters


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


		# Then the shared libraries
		copyfile(join(Settings.basePath, "lib/plsa/libplsa-serial.so"), join(self.getTempDirectory(), "lib/libplsa-serial.so"))
		copyfile(join(Settings.basePath, "lib/plsa/libplsa-parallel.so"), join(self.getTempDirectory(), "lib/libplsa-parallel.so"))
		copyfile(join(Settings.basePath, "lib/integrate/integrate.so"), join(self.getTempDirectory(), "lib/integrate.so"))

		copyfile(join(Settings.basePath, "lib/templates/data_optimization/Makefile"), join(self.getTempDirectory(), "Makefile") )
		copyfile(join(Settings.basePath, "lib/templates/data_optimization/main.c"), join(self.getTempDirectory(), "src/main.c") )




	def writeOptimizationFilesHeaders(self, f_c, f_h):

		f_c.write("#include <stdlib.h>\n")
		f_c.write("#include \"optim.h\"\n")

		f_h.write("#include \"plsa/sa.h\"\n")
		f_h.write("#include \"plsa/config.h\"\n")
		f_h.write("#include \"integrate/models.h\"\n")



	def writeOptimizationGlobals(self, f_c, f_h):

		f_c.write("PArrPtr * my_plist;\n")
		f_c.write("SAType * settings;\n")


	def writeOptimizationGlobalMethods(self, f_c, f_h):

		f_h.write("SAType * getOptimSettings();\n")
		f_c.write("SAType * getOptimSettings(void)\n")
		f_c.write("{\n")
		f_c.write("    return settings;\n")
		f_c.write("}\n\n")

		f_h.write("PArrPtr * getOptimParameters(void);\n")
		f_c.write("PArrPtr * getOptimParameters(void)\n")
		f_c.write("{\n\treturn my_plist;\n}\n\n")


	def writeOptimizationParameters(self, f_c, f_h):

		f_h.write("void init_params(ModelDefinition * model);\n")
		f_c.write("void init_params(ModelDefinition * model)\n{\n")


		f_c.write("\tmy_plist = InitPLSAParameters(%d);\n" % len(self.parameters))

		for (i_param, (param, value, lb, ub)) in enumerate(self.parameters):
			f_c.write("\tmy_plist->array[%d] = (ParamList) {&(model->constant_variables[%d].value), %g, (Range) {%g, %g}, \"%s\"};\n" % (i_param, param.ind, value, lb, ub, param.symbol.getPrettyPrintMathFormula()))

		f_c.write("}")



	def randomPlsaSeed(self):
		return randrange(-2147483647,+2147483647)
