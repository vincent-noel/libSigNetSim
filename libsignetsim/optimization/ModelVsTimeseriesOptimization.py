#!/usr/bin/env python
""" ModelVsTimeseriesOptimization.py


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


from libsignetsim.data.ExperimentalData import ExperimentalData
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.Experiment import Experiment
from libsignetsim.settings.Settings import Settings
from libsignetsim.optimization.Optimization import Optimization
from libsignetsim.optimization.NoiseGenerator import NoiseGenerator
from libsignetsim.cwriter.CWriterModelVsDataOptimization import CWriterModelVsDataOptimization

from re import match
from os.path import isfile

class ModelVsTimeseriesOptimization(Optimization, CWriterModelVsDataOptimization, NoiseGenerator):

	def __init__(self, workingModel, parameters_to_fit=None,
				list_of_experiments=None, reference_data=None,
				mapping=None, noise=0, sampling=None, nb_procs=1,
				p_lambda=Settings.defaultPlsaLambda,
				p_criterion=Settings.defaultPlsaCriterion
	):

		self.workingModel = workingModel

		if list_of_experiments is not None:
			self.listOfExperiments = list_of_experiments
		# else:
		# 	self.listOfExperiments = {}
		#
		# 	if reference_data is not None:
		# 		# self.workingModel.build
		# 		self.setReferenceData(reference_data)


		Optimization.__init__(self,
			workingModel=workingModel,
			parameters_to_fit=parameters_to_fit,
			optimization_type=Optimization.MODEL_VS_DATA)

		CWriterModelVsDataOptimization.__init__(self, workingModel, self.listOfExperiments, mapping, parameters_to_fit, p_lambda=p_lambda, p_criterion=p_criterion)
		NoiseGenerator.__init__(self, self.listOfExperiments, noise, sampling)

		self.mapping = mapping
		self.noise = noise
		self.sampling = sampling
		# self.writeOptimizationFiles(nb_procs)



	def writeOptimizationFiles(self, nb_procs=1):

		Optimization.writeOptimizationFilesMain(self, nb_procs)
		vars_to_keep = self.findTreatedVariables()
		CWriterModelVsDataOptimization.writeOptimizationFiles(self, nb_procs)


	def findTreatedVariables(self):
		if self.listOfExperiments is not None and len(self.listOfExperiments) > 0:

			variables = []
			for experiment in self.listOfExperiments:
				variables += experiment.getTreatedVariables()

			if len(variables) > 1:
				variables = list(set(variables))

			var_objects = []
			for variable in variables:
				if variable in self.workingModel.listOfSpecies.names():
					var_objects.append(self.workingModel.listOfVariables.getByName(variable).getSbmlId())

			return var_objects

	#
	# def setReferenceData(self, referenceData):
	#
	# 	if not isfile(referenceData):
	# 		print " > Error : no observed concentrations file"
	#
	# 	else:
	# 		f_observed_concentrations = open(referenceData, 'r')
	# 		# self.listOfExperimentalData = ListOfExperimentalData()
	# 		still_reading = False
	# 		variables_names = []
	# 		variables_values = []
	# 		variables_id = []
	#
	# 		for line in f_observed_concentrations:
	#
	# 			# Comments
	# 			if line.startswith("#"):
	# 				pass
	#
	# 			# Empty line
	# 			elif not line.strip():
	# 				pass
	#
	# 			# Reaction
	# 			else:
	#
	# 				if line.startswith("time"):
	#
	# 					res_match = match(r"time (.*)", line.strip())
	# 					time_values = res_match.groups()[0].strip().split()
	# 					still_reading = True
	#
	# 				elif line.startswith("[") and still_reading:
	#
	# 					res_match = match(r"\[(\S*)\](.*)", line.strip())
	# 					variable = self.workingModel.listOfVariables.getByName(res_match.groups()[0].strip())
	#
	# 					if variable:
	# 						if Settings.verbose:
	# 							print "> Found that variable %s had Id %d" % (res_match.groups()[0].strip(), variable.objId)
	#
	# 						variables_names.append(res_match.groups()[0].strip())
	# 						variables_values.append(res_match.groups()[1].strip().split())
	# 						variables_id.append(variable.objId)
	#
	# 					else:
	# 						print"> Species %s not found !" % res_match.groups()[0].strip()
	#
	# 				elif line.startswith("ratio") and still_reading:
	#
	# 					res_match = match(r"ratio (.*)", line.strip())
	# 					quantification_ratio = res_match.groups()[0].strip()
	#
	# 					still_reading = False
	#
	# 					t_condition = ExperimentalCondition()
	#
	# 					for i_variable, variable_name in enumerate(variables_names):
	#
	# 						for i_value, time_value in enumerate(time_values):
	# 							t_experimental_data = ExperimentalData()
	# 							t_experimental_data.readDB(variable_name,
	# 														float(time_value),
	# 														float(variables_values[i_variable][i_value]),
	# 														quantification_ratio=float(quantification_ratio))
	#
	# 							t_condition.listOfExperimentalData.add(t_experimental_data)
	#
	# 					t_experiment = Experiment()
	# 					t_experiment.addCondition(t_condition)
	# 					self.listOfExperiments.update({0: t_experiment})
	#
	# 				else:
	# 					print "> Unexpected behaviour in the observed concentration files"
	#
	# 		f_observed_concentrations.close()
	#

	def runOptimization(self, nb_procs, timeout=None, maxiter=None):

		self.writeOptimizationFiles(nb_procs)
		return Optimization.runOptimization(self, nb_procs, timeout, maxiter)
