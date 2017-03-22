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
from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation

class TestTimeseries(unittest.TestCase):
	""" Tests high level functions """


	def testSimulateMichaelisMenten(self):

		reference_data = [0.0, 1.897738187453314, 3.756955433409792, 5.562177924708521, 7.287504219961273,
						  8.886453435701496, 10.27109268766486, 11.28772309320835, 11.80437071324164,
						  11.95991226988507, 11.99256438900284, 11.99865019516933, 11.9997559549625,
						  11.99995590896604, 11.99999203526398, 11.99999856126113, 11.99999974010935,
						  11.99999995305381, 11.99999999151893, 11.99999999846709, 11.99999999972277]
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
		vmax.setValue(0.211)
		km.setValue(1.233)

		sim = TimeseriesSimulation([m], time_min=0, time_ech=1, time_max=20)
		sim.run()
		_,y = sim.getRawData()[0]
		model_data = y['P']

		for i, t_data in enumerate(reference_data):
			self.assertAlmostEqual(t_data, model_data[i], delta=1e-6)
