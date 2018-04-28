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

	This file is made for 'high level' tests, using various components

"""

from libsignetsim import SbmlDocument, Experiment, ModelVsTimeseriesOptimization

from unittest import TestCase
from os.path import join, dirname


class TestOptimizationComp(TestCase):
	""" Tests high level functions """

	def testOptimizeCompModel(self):

		doc = SbmlDocument()
		doc.readSbmlFromFile(join(dirname(__file__), "files", "comp_model", "modelz9xdww.xml"))

		experiment = Experiment()
		experiment.readNuMLFromFile(join(join(dirname(__file__), "files"), "ras_data.xml"))

		# Fitting the hierarchical model
		sos_submodel = doc.model.listOfSubmodels.getBySbmlId("sos_mod").getModelObject()
		param_def = sos_submodel.listOfParameters.getByName("SOS inactivation by Mapk catalytic constant")

		selected_parameters = [(param_def, 1, 1e-6, 1e+6, 8)]

		fit = ModelVsTimeseriesOptimization(
			workingModel=doc.model,
			list_of_experiments=[experiment],
			parameters_to_fit=selected_parameters,
			p_lambda=1, p_freeze_count=1
		)

		score_def = fit.runOptimization(2)
		res_def = fit.readOptimizationOutput()

		self.assertEqual(list(res_def.keys())[0], param_def)
		self.assertAlmostEqual(score_def, 1.006, delta=1e-3)
		self.assertAlmostEqual(res_def[param_def], 18.87788, delta=res_def[param_def]*1e-4)
