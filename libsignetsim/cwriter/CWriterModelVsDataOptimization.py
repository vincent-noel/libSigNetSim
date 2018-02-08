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

from libsignetsim.cwriter.CWriterModels import CWriterModels
from libsignetsim.cwriter.CWriterData import CWriterData
from libsignetsim.cwriter.CWriterOptimization import CWriterOptimization

class CWriterModelVsDataOptimization(CWriterOptimization, CWriterModels, CWriterData):

	def __init__(self, workingModel, listOfExperiments=None, mapping=None, parameters_to_fit=None,
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


		self.listOfExperiments = listOfExperiments

		self.timeMin = None
		self.timeMax = None
		self.listOfSamples = None
		self.scoreNegativePenalty = s_neg_penalty
		self.findSimulationSettings()

		CWriterModels.__init__(self, [workingModel], [Settings.simulationTimeMin], [self.listOfSamples], [Settings.defaultAbsTol], [Settings.defaultRelTol])
		CWriterData.__init__(self, listOfExperiments, mapping, workingModel, subdir="src", hasObservations=True)
		CWriterOptimization.__init__(
			self, workingModel, parameters_to_fit,
			p_lambda=p_lambda, p_criterion=p_criterion, p_precision=p_precision,
			p_initial_temperature=p_initial_temperature,
			p_gain=p_gain, p_interval=p_interval, p_tau=p_tau,
			p_mix=p_mix, p_initial_moves=p_initial_moves,
			p_freeze_count=p_freeze_count
		)

	def findSimulationSettings(self):

		# We need to start it at zero, even if the first observation is laters
		times = [0.0]
		for experiment in self.listOfExperiments:
			times += experiment.getTimes()

		self.listOfSamples = sorted(list(set(times)))
		self.timeMin = min(self.listOfSamples)
		self.timeMax = max(self.listOfSamples)

	def writeOptimizationFiles(self, nb_procs):

		CWriterOptimization.writeOptimizationFiles(self, nb_procs)
		self.writeModelFiles()
		self.writeDataFiles()
		self.writeOptimFiles(nb_procs)

	def writeOptimFiles(self, nb_procs):

		c_filename = self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "optim.c"
		h_filename = self.getTempDirectory() + Settings.C_generatedDirectory_v2 + "optim.h"

		f_c = open(c_filename, 'w')
		f_h = open(h_filename, 'w')

		self.writeOptimizationFilesHeaders(f_c, f_h)
		self.writeOptimizationGlobals(f_c, f_h)
		self.writeOptimizationGlobalMethods(f_c, f_h)
		self.writeOptimizationParameters(f_c, f_h)
		self.writeOptimizationSettings(f_c, f_h)
		self.writeOptimizationScoreSettings(f_c, f_h)

		f_c.close()
		f_h.close()



	def writeOptimizationScoreSettings(self, f_c, f_h):

		f_h.write("ScoreSettings * init_score_settings();\n")
		f_c.write("ScoreSettings * init_score_settings()\n{\n")

		f_c.write("  ScoreSettings * settings = malloc(sizeof(ScoreSettings));\n")
		f_c.write("  settings->negative_penalty = %.2g;\n" % self.scoreNegativePenalty)
		f_c.write("  return settings;\n")
		f_c.write("}")
