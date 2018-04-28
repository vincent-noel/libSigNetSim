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
from libsignetsim.LibSigNetSimException import UnknownObservationException, UnknownTreatmentException, NoTreatmentException, NoObservationException


class CWriterData(object):

	def __init__(self, listOfExperiments=None, mapping=None, workingModel=None, interpolate=False, subdir=None, hasTreatments=False, hasObservations=False):

		self.mapping = mapping
		self.listOfExperiments = listOfExperiments
		self.workingModel = workingModel
		self.subdir = subdir
		self.hasTreatments = hasTreatments
		self.hasObservations = hasObservations

		self.checkListOfExperiments()

	def checkListOfExperiments(self):

		if self.listOfExperiments is not None and len(self.listOfExperiments) > 0:
			for i, experiment in enumerate(self.listOfExperiments):
				for j, condition in enumerate(experiment.listOfConditions.values()):

					# Here we need to find all the timings of the treatments. That will be the set of initial values.
					# Then, each set of initial values can have multiple assignments
					t_times = []
					for initial_value in list(condition.listOfInitialConditions.values()):
						t_times.append(initial_value.t)

					# Removing doublons
					t_times = list(set(t_times))


					nb_treatments = 0
					nb_observable = 0

					for k, t_time in enumerate(t_times):

						treatments = []
						for initial_value in list(condition.listOfInitialConditions.values()):
							if initial_value.t == t_time:
								treatments.append(initial_value)

						for l, treatment in enumerate(treatments):

							t_variable = None

							if self.mapping is not None and len(self.mapping) > 0:
								if i < len(self.mapping) and treatment.name in list(self.mapping[i].keys()):
									t_variable = self.workingModel.parentDoc.getByXPath(
										self.mapping[i][treatment.name],
										instance=self.workingModel.parentDoc.useCompPackage
									)
								# else:
								# 	raise UnknownTreatmentException(
								# 		"Variable %s not found in mapping" % treatment.name)

							elif treatment.name_attribute == "name":
								if self.workingModel.listOfVariables.containsName(treatment.name):
									t_variable = self.workingModel.listOfVariables.getByName(treatment.name)
								else:
									raise UnknownTreatmentException("Cannot find a variable called %s" % treatment.name)

							elif treatment.name_attribute == "id":
								if self.workingModel.listOfVariables.containsSbmlId(treatment.name):
									t_variable = self.workingModel.listOfVariables.getBySbmlId(treatment.name)
								else:
									raise UnknownTreatmentException("Cannot find a variable called %s" % treatment.name)

							else:
								raise UnknownTreatmentException(
									"Unknown attribute for variable : %s" % treatment.name_attribute)

							if t_variable is not None:
								nb_treatments += 1

						# Observed_values
					vars_observed = {}

					for k, observed_value in enumerate(condition.listOfExperimentalData.values()):

						t_variable = None
						if self.mapping is not None and len(self.mapping) > 0:
							if i < len(self.mapping) and observed_value.name in list(self.mapping[i].keys()):
								t_variable = self.workingModel.parentDoc.getByXPath(
									self.mapping[i][observed_value.name],
									instance=self.workingModel.parentDoc.useCompPackage
								)
							# else:
							# 	raise UnknownObservationException("Variable %s not found in mapping" % observed_value.name)

						elif observed_value.name_attribute == "name":
							if self.workingModel.listOfVariables.containsName(observed_value.name):
								t_variable = self.workingModel.listOfVariables.getByName(observed_value.name)
							else:
								raise UnknownTreatmentException(
									"Cannot find a variable called %s" % observed_value.name)

						elif observed_value.name_attribute == "id":
							if self.workingModel.listOfVariables.containsSbmlId(observed_value.name):
								t_variable = self.workingModel.listOfVariables.getBySbmlId(observed_value.name)
							else:
								raise UnknownTreatmentException(
									"Cannot find a variable called %s" % observed_value.name)

						else:
							raise UnknownTreatmentException(
								"Unknown attribute for variable : %s" % observed_value.name_attribute)

						if t_variable is not None and t_variable not in list(vars_observed.keys()):
							vars_observed.update({t_variable: len(list(vars_observed.keys()))})

							nb_observable += 1

					if nb_observable == 0 and self.hasObservations:
						raise NoObservationException("No observation !")

					if nb_treatments == 0 and self.hasTreatments:
						raise NoTreatmentException("No treatments !")

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
				f_c.write("    experiments[%d].nb_conditions = %d;\n" % (i, len(list(experiment.listOfConditions.keys()))))
				f_c.write("    experiments[%d].conditions = malloc(sizeof(ExperimentalCondition)*experiments[%d].nb_conditions);\n" % (i,i))
				f_c.write("\n")

				for j, condition in enumerate(experiment.listOfConditions.values()):

					# Here we need to find all the timings of the treatments. That will be the set of initial values.
					# Then, each set of initial values can have multiple assignments
					t_times = []
					for initial_value in list(condition.listOfInitialConditions.values()):
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
						for initial_value in list(condition.listOfInitialConditions.values()):
							if initial_value.t == t_time:
								treatments.append(initial_value)

						f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].t = %g;\n" % (i, j, k, t_time))
						f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].nb_treatments = %d;\n" % (i, j, k, len(treatments)))
						f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].treatments = malloc(sizeof(Treatment)*experiments[%d].conditions[%d].timed_treatments[%d].nb_treatments);\n" % (i,j,k,i,j,k))
						for l, treatment in enumerate(treatments):

							t_variable = None
							if self.mapping is not None and len(self.mapping) > 0:
								if i < len(self.mapping) and treatment.name in list(self.mapping[i].keys()):
									# print "> MApping: %s : %s" % (treatment.name, self.mapping[i][treatment.name])
									t_variable = self.workingModel.parentDoc.getByXPath(
										self.mapping[i][treatment.name],
										instance=self.workingModel.parentDoc.useCompPackage
									)
								# else:
								# 	raise UnknownTreatmentException(
								# 		"Variable %s not found in mapping" % treatment.name)

							elif treatment.name_attribute == "name":
								if self.workingModel.listOfVariables.containsName(treatment.name):
									t_variable = self.workingModel.listOfVariables.getByName(treatment.name)
								else:
									raise UnknownTreatmentException("Cannot find a variable called %s" % treatment.name)

							elif treatment.name_attribute == "id":
								if self.workingModel.listOfVariables.containsSbmlId(treatment.name):
									t_variable = self.workingModel.listOfVariables.getBySbmlId(treatment.name)
								else:
									raise UnknownTreatmentException("Cannot find a variable called %s" % treatment.name)

							else:
								raise UnknownTreatmentException("Unknown attribute for variable : %s" % treatment.name_attribute)


							if t_variable is not None:
								f_c.write("  experiments[%d].conditions[%d].timed_treatments[%d].treatments[%d] = (Treatment) {%g, %d, %d};\n" % (
											i, j, k, l, treatment.value, t_variable.type, t_variable.ind))
							# else:
							# 	print "> ERROR: Couldn't find variable %s" % observed_value.name

					 # Observed_values
					f_c.write("    experiments[%d].conditions[%d].nb_observed_values = %d;\n" % (i, j, len(list(condition.listOfExperimentalData.keys()))))
					f_c.write("    experiments[%d].conditions[%d].observed_values = malloc(sizeof(ExperimentalObservation)*experiments[%d].conditions[%d].nb_observed_values);\n" % (i,j,i,j))
					f_c.write("\n")
					vars_observed = {}

					for k, observed_value in enumerate(condition.listOfExperimentalData.values()):

						t_variable = None
						if self.mapping is not None and len(self.mapping) > 0:
							if i < len(self.mapping) and observed_value.name in list(self.mapping[i].keys()):
								# print "> MApping: %s : %s" % (observed_value.name, self.mapping[i][observed_value.name])
								t_variable = self.workingModel.parentDoc.getByXPath(self.mapping[i][observed_value.name], instance=self.workingModel.parentDoc.useCompPackage)
							# else:
							# 	raise UnknownObservationException("Variable %s not found in mapping" % observed_value.name)

						elif observed_value.name_attribute == "name":
							if self.workingModel.listOfVariables.containsName(observed_value.name):
								t_variable = self.workingModel.listOfVariables.getByName(observed_value.name)
							else:
								raise UnknownObservationException("Cannot find a variable called %s" % observed_value.name)

						elif observed_value.name_attribute == "id":
							if self.workingModel.listOfVariables.containsSbmlId(observed_value.name):
								t_variable = self.workingModel.listOfVariables.getBySbmlId(observed_value.name)
							else:
								raise UnknownObservationException("Cannot find a variable called %s" % observed_value.name)

						else:
							raise UnknownObservationException(
								"Unknown attribute for variable : %s" % observed_value.name_attribute)


						if t_variable is not None:
							if t_variable not in list(vars_observed.keys()):
								vars_observed.update({t_variable: len(list(vars_observed.keys())) })

							# if t_variable is not None:
							t_variable_id = t_variable.getPos()

							f_c.write("    experiments[%d].conditions[%d].observed_values[%d] = (ExperimentalObservation) {%g, %g, %g, %d, %g, %g, %d, %d, %d, %d, \"%s\"};\n" % (
											i,j,k,
											observed_value.t, observed_value.value, observed_value.value_dev,
											int(observed_value.steady_state), float(observed_value.min_steady_state), float(observed_value.max_steady_state),
											t_variable.type, t_variable.ind, t_variable_id, vars_observed[t_variable], t_variable.getXPath()))
							# else:
							# 	print "> ERROR: Couldn't find variable %s" % observed_value.name
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

					if len(list(condition.listOfInitialConditions.keys())) > 0:
						f_c.write("    free(experiments[%d].conditions[%d].timed_treatments);\n" % (i,j))

						t_times = []
						for initial_value in list(condition.listOfInitialConditions.values()):
							t_times.append(initial_value.t)

						# Removing doublons
						t_times = list(set(t_times))

						for k, t_time in enumerate(t_times):
							f_c.write("    free(experiments[%d].conditions[%d].timed_treatments[%d].treatments);\n" % (i,j,k))


					if len(list(condition.listOfExperimentalData.keys())) > 0:
						f_c.write("    free(experiments[%d].conditions[%d].observed_values);\n" % (i,j))

				f_c.write("    free(experiments[%d].conditions);\n" % i)
			f_c.write("    free(experiments);\n")
		f_c.write("\n}\n\n")
