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


from libsignetsim.settings.Settings import Settings


class CWriterModels(object):

	def __init__ (self, list_of_models,
				  	time_min,
					list_samples,
					abs_tol,
					rel_tol):

		self.listOfModels = list_of_models

		# Simulation variables
		self.timeMin = time_min
		self.listSamples = list_samples
		self.absTol = abs_tol
		self.relTol = rel_tol

	def writeModelsHeaders(self, f_h, f_c):

		# Writing headers for the c file
		f_c.write("/*****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *   model.c                                                     *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *   written by Vincent Noel                                     *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *   Model definition for simulation and optimization            *\n")
		f_c.write(" *   Generated by libSigNetSim                                      *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" * Copyright (C) 2012-2014 Vincent Noel                          *\n")
		f_c.write(" * the full GPL copyright notice can be found in lsa.c           *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" ****************************************************************/\n\n")
		f_c.write("#include <stdlib.h>\n")
		f_c.write("#include <stdio.h>\n")
		f_c.write("#include \"model.h\"\n\n")
		f_c.write("#include \"integrate/realtype_math.h\"\n\n")

		f_c.write("#define min(x, y) (((x) < (y)) ? (x) : (y))\n")
		f_c.write("#define max(x, y) (((x) > (y)) ? (x) : (y))\n")
		f_c.write("#define Ith(v,i)    NV_Ith_S(v,i-1)       /* Ith numbers components 1..NEQ */\n")
		f_c.write("#define IJth(A,i,j) DENSE_ELEM(A,i-1,j-1) /* IJth numbers rows,cols 1..NEQ */\n\n")

		# Writing headers for the h file
		f_h.write("/*****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *   model.h                                                     *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *   written by Vincent Noel                                     *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *   Model definition for simulation and optimization            *\n")
		f_h.write(" *   Generated by libSigNetSim                                      *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" * Copyright (C) 2012-2014 Vincent Noel                          *\n")
		f_h.write(" * the full GPL copyright notice can be found in lsa.c           *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" ****************************************************************/\n\n")

		f_h.write("#include \"integrate/models.h\"\n")
		f_h.write("#include \"integrate/integrate.h\"\n")

	def writeModelsInitialization(self, f_h, f_c):

		f_c.write("list_of_models models;\n\n")

		for modelInd, model in enumerate(self.listOfModels):
			f_c.write("ModelDefinition     model_%d;\n\n" % modelInd)

		f_c.write("list_of_models * getListOfModels()\n")
		f_c.write("{\n")
		f_c.write("  return &models;\n")
		f_c.write("}\n")

		f_h.write("list_of_models * getListOfModels();\n")
		f_h.write("double * getInitValues(int i);\n")
		f_c.write("\ndouble * getInitValues(int i)\n")
		f_c.write("{\n")
		f_c.write("  return NULL;\n")
		f_c.write("}\n")


		f_h.write("void init_models();\n")
		f_c.write("void init_models()\n{\n")

		f_c.write("  models.nb_models = " + str(len(self.listOfModels)) + ";\n")
		f_c.write("  models.models = malloc(sizeof(ModelDefinition)*models.nb_models);\n")

		for modelInd, _ in enumerate(self.listOfModels):
			f_c.write("  init_model_%d();\n" % modelInd)
			f_c.write("  models.models[%d] = &model_%d;\n" % (modelInd, modelInd))

		f_c.write("}\n\n")


	def writeModelsFinalization(self, f_h, f_c):

		f_h.write("void finalize_models();\n")
		f_c.write("void finalize_models()\n{\n")

		for modelInd, _ in enumerate(self.listOfModels):
			f_c.write("  finalize_model_%d();\n" % modelInd)

		f_c.write("  free(models.models);\n")

		f_c.write("}\n\n")


	def writeModelFiles(self):

		f_c = open(self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "model.c", 'w')
		f_h = open(self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "model.h", 'w')

		self.writeModelsHeaders(f_h, f_c)
		self.writeModelsInitialization(f_h, f_c)
		self.writeModelsFinalization(f_h, f_c)

		for i_model, model in enumerate(self.listOfModels):
			model.writeCCode(f_h, f_c, i_model, self.timeMin[i_model], self.listSamples[i_model], self.absTol[i_model], self.relTol[i_model])

		f_c.close()
		f_h.close()
