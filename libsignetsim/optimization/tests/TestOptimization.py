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

from libsignetsim import Model, Experiment, ModelVsTimeseriesOptimization

from unittest import TestCase


class TestOptimization(TestCase):
	""" Tests high level functions """

	def testOptimizeMichaelisMenten(self):

		reference_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
		reference_data = [
			0.0, 1.897738450655051, 3.756955074247717, 5.56216742392093, 7.287473256778753, 8.886428870529057,
			10.27109002756082, 11.2877220979055, 11.80436967759331, 11.95991169490768, 11.99256430291778,
			11.99865017124369, 11.99975594720175, 11.99995589772631, 11.99999202708974, 11.99999855444305,
			11.99999973767934, 11.99999993029574, 11.99999999125534, 11.99999999568526, 12.00000000008859
		]

		m = Model()
		m.setName("Enzymatic Reaction")

		e = m.listOfSpecies.new("E")
		s = m.listOfSpecies.new("S")
		p = m.listOfSpecies.new("P")

		m.listOfParameters.new("vmax")
		m.listOfParameters.new("km")

		r = m.listOfReactions.new("Enzymatic reaction")
		r.listOfReactants.add(s)
		r.listOfModifiers.add(e)
		r.listOfProducts.add(p)
		r.kineticLaw.setPrettyPrintMathFormula("vmax*E*S/(km+S)")

		e.setValue(10)
		s.setValue(12)
		p.setValue(0)

		# Building the experiment
		experiment = Experiment()
		condition = experiment.createCondition()
		for i, data in enumerate(reference_data):
			condition.addObservation(reference_times[i], 'P', data)

		selected_parameters = []
		for parameter in m.listOfParameters:
			selected_parameters.append((parameter, 1, 1e-6, 1e+6, 4))

		fit = ModelVsTimeseriesOptimization(
			workingModel=m,
			list_of_experiments=[experiment],
			parameters_to_fit=selected_parameters,
			nb_procs=2
		)

		score = fit.runOptimization(2)
		parameters = fit.readOptimizationOutput()

		self.assertEqual(score, 0.001)
		self.assertAlmostEqual(parameters[m.listOfParameters.getBySbmlId('vmax')], 0.211, delta=1e-3)
		self.assertAlmostEqual(parameters[m.listOfParameters.getBySbmlId('km')], 1.233, delta=1e-3)

	def testOptimizeMichaelisMentenLocalParameters(self):

		# Reference data to fit against
		reference_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
		reference_data = [
			0.0, 1.897738450655051, 3.756955074247717, 5.56216742392093, 7.287473256778753, 8.886428870529057,
			10.27109002756082, 11.2877220979055, 11.80436967759331, 11.95991169490768, 11.99256430291778,
			11.99865017124369, 11.99975594720175, 11.99995589772631, 11.99999202708974, 11.99999855444305,
			11.99999973767934, 11.99999993029574, 11.99999999125534, 11.99999999568526, 12.00000000008859
		]

		# Building the model
		m = Model()
		m.setName("Enzymatic Reaction")

		e = m.listOfSpecies.new("E")
		s = m.listOfSpecies.new("S")
		p = m.listOfSpecies.new("P")

		r = m.listOfReactions.new("Enzymatic reaction")
		r.listOfReactants.add(s)
		r.listOfModifiers.add(e)
		r.listOfProducts.add(p)

		r.listOfLocalParameters.new("vmax")
		r.listOfLocalParameters.new("km")

		r.kineticLaw.setPrettyPrintMathFormula("vmax*E*S/(km+S)")

		e.setValue(10)
		s.setValue(12)
		p.setValue(0)

		# Building the experiment
		experiment = Experiment()
		condition = experiment.createCondition()
		for i, data in enumerate(reference_data):
			condition.addObservation(reference_times[i], 'P', data)

		selected_parameters = []
		for parameter in r.listOfLocalParameters:
			selected_parameters.append((parameter, 1, 1e-6, 1e+6, 4))

		fit = ModelVsTimeseriesOptimization(
			workingModel=m,
			list_of_experiments=[experiment],
			parameters_to_fit=selected_parameters,
			nb_procs=2
		)

		score = fit.runOptimization(2)
		parameters = fit.readOptimizationOutput()

		self.assertEqual(score, 0.001)
		self.assertAlmostEqual(parameters[r.listOfLocalParameters.getBySbmlId('vmax')], 0.211, delta=1e-3)
		self.assertAlmostEqual(parameters[r.listOfLocalParameters.getBySbmlId('km')], 1.233, delta=1e-3)
