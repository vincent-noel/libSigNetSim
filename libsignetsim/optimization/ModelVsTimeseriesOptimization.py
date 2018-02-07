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

from libsignetsim.model.ModelInstance import ModelInstance
from libsignetsim.settings.Settings import Settings
from libsignetsim.optimization.Optimization import Optimization
from libsignetsim.optimization.NoiseGenerator import NoiseGenerator
from libsignetsim.cwriter.CWriterModelVsDataOptimization import CWriterModelVsDataOptimization


class ModelVsTimeseriesOptimization(Optimization, CWriterModelVsDataOptimization, NoiseGenerator):

	def __init__(
			self, workingModel, parameters_to_fit=None,
			list_of_experiments=None, reference_data=None,
			mapping=None, noise=0, sampling=None, nb_procs=1,
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
			s_neg_penalty=Settings.defaultScoreNegativePenalty,
	):

		self.compModelDefinition = None

		if workingModel.parentDoc.isCompEnabled() and not isinstance(workingModel, ModelInstance):
			self.compModelDefinition = workingModel
			self.workingModel = workingModel.parentDoc.getModelInstance()
			self.parameters = []
			for parameter, init_val, lower_bound, upper_bound, precision in parameters_to_fit:
				self.parameters.append((
					self.workingModel.getInstanceVariableByXPath(parameter.getXPath()), init_val, lower_bound, upper_bound, precision
				))

		else:

			self.workingModel = workingModel
			self.parameters = []
			for parameter, init_val, lower_bound, upper_bound, precision in parameters_to_fit:
				self.parameters.append((
					workingModel.parentDoc.getByXPath(parameter.getXPath()), init_val, lower_bound, upper_bound, precision
				))

			self.workingModel = workingModel

		if list_of_experiments is not None:
			self.listOfExperiments = list_of_experiments

		Optimization.__init__(
			self,
			workingModel=self.workingModel,
			parameters_to_fit=self.parameters,
			optimization_type=Optimization.MODEL_VS_DATA,
			model_instance=(self.compModelDefinition is not None)
		)

		CWriterModelVsDataOptimization.__init__(
			self, self.workingModel, self.listOfExperiments, mapping, self.parameters,
			p_lambda=p_lambda, p_criterion=p_criterion, p_precision=p_precision,
			p_initial_temperature=p_initial_temperature, p_gain=p_gain, p_interval=p_interval, p_mix=p_mix,
			p_initial_moves=p_initial_moves, p_tau=p_tau, p_freeze_count=p_freeze_count, s_neg_penalty=s_neg_penalty
		)
		NoiseGenerator.__init__(self, self.listOfExperiments, noise, sampling)

		self.mapping = mapping
		self.noise = noise
		self.sampling = sampling


	def writeOptimizationFiles(self, nb_procs=1):

		Optimization.writeOptimizationFilesMain(self, nb_procs)
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
