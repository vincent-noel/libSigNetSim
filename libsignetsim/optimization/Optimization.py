#!/usr/bin/env python
""" Optimization.py


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



from libsignetsim.cwriter.CWriterOptimization import CWriterOptimization
from libsignetsim.optimization.OptimizationParameters import OptimizationParameters
from libsignetsim.optimization.OptimizationExecution import OptimizationExecution

from os.path import join, isfile
from os import mkdir


class Optimization(OptimizationExecution, OptimizationParameters):

	MODEL_VS_MODEL = 0
	MODEL_VS_DATA = 1
	MODEL_VS_STEADYSTATES = 2

	def __init__ (self, SigNetSim=None, workingModel=None, parameters_to_fit=None, optimization_type=MODEL_VS_DATA):

		self.workingModel = workingModel
		self.optimizationType = optimization_type

		OptimizationExecution.__init__(self)
		OptimizationParameters.__init__(self, workingModel, parameters_to_fit)


	def writeOptimizationFilesMain(self, nb_procs=1):

		mkdir(self.getTempDirectory())

		if self.workingModel.parentDoc is not None:
			self.workingModel.parentDoc.writeSbmlToFile(join(self.getTempDirectory(), "model.sbml"))
		self.workingModel.build(dont_reduce=True)


	def initializeOptimizationParameters(self):

		for constant_type, constant in self.constantsToFit:
			if constant_type == 1:
				self.workingModel.listOfSpecies[constant].init_value = 1e-8
			elif constant_type == 2:
				self.workingModel.listOfParameters[constant].value = 1e-8
			elif constant_type == 3:
				(r_id, lp_id) = constant
				self.workingModel.listOfReactions[r_id].listOfLocalParameters[lp_id].value = 1e-8


	def getBestResult(self, nb_procs):

		if isfile(join(self.getTempDirectory(), "logs/score/score")):
			f_best_score = open(join(self.getTempDirectory(), "logs/score/score"), 'r')
			t_score = f_best_score.readline()
			if t_score is not None and t_score != "":
				res = float(t_score)
			else:
				return (-1, 1e+100)
			f_best_score.close()

			return (0, res)

		return (-1,1e+100)
