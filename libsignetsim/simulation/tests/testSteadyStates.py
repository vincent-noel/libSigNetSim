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


class TestSteadyStates(unittest.TestCase):
	""" Tests high level functions """

	#
	# def testSimulateMichaelisMenten(self):
	#
	# 	reference_data = 12.0
	# 	m = Model()
	# 	m.setName("Enzymatic Reaction")
	#
	# 	e = m.listOfSpecies.new("E")
	# 	s = m.listOfSpecies.new("S")
	# 	p = m.listOfSpecies.new("P")
	#
	# 	vmax = m.listOfParameters.new("vmax")
	# 	km = m.listOfParameters.new("km")
	#
	# 	r = m.listOfReactions.new("Enzymatic reaction")
	# 	r.listOfReactants.add(s)
	# 	r.listOfModifiers.add(e)
	# 	r.listOfProducts.add(p)
	# 	r.kineticLaw.setPrettyPrintMathFormula("vmax*E*S/(km+S)")
	#
	# 	e.setValue(10)
	# 	s.setValue(12)
	# 	p.setValue(0)
	# 	vmax.setValue(0.211)
	# 	km.setValue(1.233)
	#
	# 	sim = TimeseriesSimulation([m], time_min=0, time_ech=1, time_max=20)
	# 	sim.run()
	# 	_,y = sim.getRawData()[0]
	# 	model_data = y['P']
	#
	# 	for i, t_data in enumerate(reference_data):
	# 		self.assertAlmostEqual(t_data, model_data[i], delta=1e-6)
