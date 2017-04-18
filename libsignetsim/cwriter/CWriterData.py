#!/usr/bin/env python
""" CWriterData.py


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
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
class CWriterData(object):

	def __init__ (self, listOfExperiments=None, mapping=None, workingModel=None, interpolate=False, subdir=None):

		self.mapping = mapping
		self.listOfExperiments = listOfExperiments
		self.workingModel = workingModel
		self.subdir = subdir


	def writeDataFiles(self):

		f_c = open(self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "data.c", 'w')
		f_h = open(self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "data.h", 'w')


		self.writeDataHeaders(f_c, f_h)
		self.writeDataInitialization(f_c, f_h)
		self.writeDataFinalization(f_c, f_h)

		f_c.close()
		f_h.close()


	def writeDataHeaders(self, f_c, f_h):

		#Writing headers for the c file
		f_c.write("/*****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *   data.c                                                      *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *   written by Vincent Noel                                     *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *   Data definition for optimization                            *\n")
		f_c.write(" *   Generated by libSigNetSim                                      *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" *****************************************************************\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" * Copyright (C) 2012-2015 Vincent Noel                          *\n")
		f_c.write(" * the full GPL copyright notice can be found in lsa.c           *\n")
		f_c.write(" *                                                               *\n")
		f_c.write(" ****************************************************************/\n\n")
		f_c.write("#include \"data.h\"\n")
		f_c.write("#include <stdlib.h>\n\n")
		f_c.write("Experiment * experiments;\n")
		f_c.write("int nb_experiments;\n\n")
		f_c.write("Experiment * getListOfExperiments()\n")
		f_c.write("{\n")
		f_c.write("  return experiments;\n")
		f_c.write("}\n\n")
		f_c.write("int getNbExperiments()\n")
		f_c.write("{\n")
		f_c.write("  return nb_experiments;\n")
		f_c.write("}\n")

		# Writing headers for the h file
		f_h.write("/*****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *   data.h                                                      *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *   written by Vincent Noel                                     *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *   Data definition for optimization                            *\n")
		f_h.write(" *   Generated by libSigNetSim                                      *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *****************************************************************\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" * Copyright (C) 2012-2015 Vincent Noel                          *\n")
		f_h.write(" * the full GPL copyright notice can be found in lsa.c           *\n")
		f_h.write(" *                                                               *\n")
		f_h.write(" *****************************************************************/\n\n")

		f_h.write("#include \"integrate/datas.h\"\n\n")


		f_h.write("Experiment * getListOfExperiments();\n")
		f_h.write("int getNbExperiments();\n")


	def writeDataInitialization(self, f_c, f_h):

		f_h.write("void init_data();\n")
		f_c.write("void init_data()\n")
		f_c.write("{\n")


		if self.listOfExperiments is not None and len(self.listOfExperiments) > 0:
			f_c.write("    nb_experiments = %d;\n" % len(self.listOfExperiments))
			f_c.write("    experiments = malloc(sizeof(Experiment)*nb_experiments);\n")
			f_c.write("\n")


			for i, experiment in enumerate(self.listOfExperiments):

				f_c.write("    experiments[%d].name = \"%s\";\n" % (i, experiment.name))
				f_c.write("    experiments[%d].nb_conditions = %d;\n" % (i, len(experiment.listOfConditions.keys())))
				f_c.write("    experiments[%d].conditions = malloc(sizeof(ExperimentalCondition)*experiments[%d].nb_conditions);\n" % (i,i))
				f_c.write("\n")

				for j, condition in enumerate(experiment.listOfConditions.values()):

					# Here we need to find all the timings of the treatments. That will be the set of initial values.
					# Then, each set of initial values can have multiple assignments
					t_times = []
					for initial_value in condition.listOfInitialConditions.values():
						t_times.append(initial_value.t)

					# Removing doublons
					t_times = list(set(t_times))

					# Initial values
					f_c.write("    experiments[%d].conditions[%d].name = \"%s\";\n" % (i, j, condition.name))
					f_c.write("    experiments[%d].conditions[%d].nb_timed_treatments = %d;\n" % (i, j, len(t_times)))
					f_c.write("    experiments[%d].conditions[%d].timed_treatments = malloc(sizeof(TimedTreatments)*experiments[%d].conditions[%d].nb_timed_treatments);\n" % (i,j,i,j))
					f_c.write("\n")

					for k, t_time in enumerate(t_times):

						treatments = []
						for initial_value in condition.listOfInitialConditions.values():
							if initial_value.t == t_time:
								treatments.append(initial_value)

						f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].t = %g;\n" % (i, j, k, t_time))
						f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].nb_treatments = %d;\n" % (i, j, k, len(treatments)))
						f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].treatments = malloc(sizeof(Treatment)*experiments[%d].conditions[%d].timed_treatments[%d].nb_treatments);\n" % (i,j,k,i,j,k))
						for l, treatment in enumerate(treatments):

							t_variable = None

							# if self.workingModel.listOfSpecies.containsName(treatment.name):
							# 	t_variable = self.workingModel.listOfSpecies.getByName(treatment.name)
							# elif self.workingModel.listOfParameters.containsName(treatment.name):
							# 	t_variable = self.workingModel.listOfParameters.getByName(treatment.name)
							# elif self.workingModel.listOfCompartments.containsName(treatment.name):
							# 	t_variable = self.workingModel.listOfCompartments.getByName(treatment.name)



							if self.workingModel.getMathModel().listOfVariables.containsSymbol(SympySymbol(treatment.name)):
								t_variable = self.workingModel.getMathModel().listOfVariables.getBySymbol(SympySymbol(treatment.name))


							if t_variable is not None:

								f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].treatments[%d] = (Treatment) {%g, %d, %d};\n" % (
												i, j, k, l, treatment.value, t_variable.type, t_variable.ind))


					 # Observed_values
					f_c.write("    experiments[%d].conditions[%d].nb_observed_values = %d;\n" % (i, j, len(condition.listOfExperimentalData.keys())))
					f_c.write("    experiments[%d].conditions[%d].observed_values = malloc(sizeof(ExperimentalObservation)*experiments[%d].conditions[%d].nb_observed_values);\n" % (i,j,i,j))
					f_c.write("\n")
					vars_observed = {}

					for k, observed_value in enumerate(condition.listOfExperimentalData.values()):

						# print "Observed values %d" % k

						t_variable = None
						if self.workingModel.getMathModel().listOfVariables.containsSymbol(SympySymbol(observed_value.name)):
							t_variable = self.workingModel.getMathModel().listOfVariables.getBySymbol(SympySymbol(observed_value.name))

						if t_variable not in vars_observed.keys():
							vars_observed.update({t_variable: len(vars_observed.keys()) })

						if t_variable is not None:
							t_variable_id = t_variable.getPos()

							f_c.write("    experiments[%d].conditions[%d].observed_values[%d] = (ExperimentalObservation) {%g, %g, %g, %d, %g, %g, %d, %d, %d, %d};\n" % (
											i,j,k,
											observed_value.t, observed_value.value, observed_value.value_dev,
											int(observed_value.steady_state), float(observed_value.min_steady_state), float(observed_value.max_steady_state),
											t_variable.type, t_variable.ind, t_variable_id, vars_observed[t_variable]))
						else:
							print "> ERROR: Couldn't find variable %s" % observed_value.name
		else:
			f_c.write("    nb_experiments = 0;\n")
			f_c.write("\n")

		f_c.write("\n}\n\n")



	def writeDataFinalization(self, f_c, f_h):

		f_h.write("void finalize_data();\n")
		f_c.write("void finalize_data()\n")
		f_c.write("{\n")
		if self.listOfExperiments is not None and len(self.listOfExperiments) > 0:
			# print self.listOfExperiments
			for i, experiment in enumerate(self.listOfExperiments):
				for j, condition in enumerate(experiment.listOfConditions.values()):

					if len(condition.listOfInitialConditions.keys()) > 0:
						f_c.write("    free(experiments[%d].conditions[%d].timed_treatments);\n" % (i,j))

						t_times = []
						for initial_value in condition.listOfInitialConditions.values():
							t_times.append(initial_value.t)

						# Removing doublons
						t_times = list(set(t_times))

						for k, t_time in enumerate(t_times):
							f_c.write("    free(experiments[%d].conditions[%d].timed_treatments[%d].treatments);\n" % (i,j,k))


					if len(condition.listOfExperimentalData.keys()) > 0:
						f_c.write("    free(experiments[%d].conditions[%d].observed_values);\n" % (i,j))

				f_c.write("    free(experiments[%d].conditions);\n" % i)
			f_c.write("    free(experiments);\n")
		f_c.write("\n}\n\n")
