#!/usr/bin/env python
""" testSigNetSim.py


	This file is made for 'high level' tests, using various components


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


import unittest

from libsignetsim.model.Model import Model
from libsignetsim.optimization.ModelVsTimeseriesOptimization import ModelVsTimeseriesOptimization

from libsignetsim.data.Experiment import Experiment as Experiment
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.ExperimentalData import ExperimentalData

class TestOptimization(unittest.TestCase):
	""" Tests high level functions """


	def testOptimizeMichaelisMenten(self):

		reference_times = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
		reference_data = [0.0, 1.897738450655051, 3.756955074247717,
						5.56216742392093, 7.287473256778753, 8.886428870529057,
						10.27109002756082, 11.2877220979055, 11.80436967759331,
						11.95991169490768, 11.99256430291778, 11.99865017124369,
						11.99975594720175, 11.99995589772631, 11.99999202708974,
						11.99999855444305, 11.99999973767934, 11.99999993029574,
						11.99999999125534, 11.99999999568526, 12.00000000008859]

		m = Model()
		m.setName("Enzymatic Reaction")

		e = m.listOfSpecies.new("E")
		s = m.listOfSpecies.new("S")
		p = m.listOfSpecies.new("P")

		vmax = m.listOfParameters.new("vmax")
		km = m.listOfParameters.new("km")

		r = m.listOfReactions.new("Enzymatic reaction")
		r.listOfReactants.add(s)
		r.listOfModifiers.add(e)
		r.listOfProducts.add(p)
		r.kineticLaw.setPrettyPrintMathFormula("vmax*E*S/(km+S)")

		e.setValue(10)
		s.setValue(12)
		p.setValue(0)

		#Initial guess
		vmax.setValue(1)
		km.setValue(1)


		# Building the experiment
		list_of_treatments = ListOfExperimentalData()
		list_of_observations = ListOfExperimentalData()
		for i, data in enumerate(reference_data):
			t_observation = ExperimentalData()
			t_observation.readDB('P', reference_times[i], data, 0, False, 0, 0)
			list_of_observations.add(t_observation)

		condition = ExperimentalCondition()
		condition.read(list_of_treatments, list_of_observations)

		experiment = Experiment()
		experiment.addCondition(condition)

		selected_parameters = []
		for parameter in m.listOfParameters.values():
			selected_parameters.append((None, parameter.objId, True,
									parameter.getNameOrSbmlId(),
									parameter.getValue(),
									1e-6, 1e+6))


		fit = ModelVsTimeseriesOptimization(workingModel=m,
										list_of_experiments={0:experiment},
										mapping=None,
										parameters_to_fit=selected_parameters)
		fit.runOptimization(2, None, None)
		# _,y = sim.getRawData()[0]
		# model_data = y['P']
		#
		# for i, t_data in enumerate(reference_data):
		# 	self.assertAlmostEqual(t_data, model_data[i], delta=1e-6)
