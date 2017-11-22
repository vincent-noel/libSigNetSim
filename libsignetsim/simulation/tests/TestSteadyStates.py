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

from libsignetsim import Model, SteadyStatesSimulation

from unittest import TestCase


class TestSteadyStates(TestCase):
	""" Tests high level functions """

	def testNoInitialValues(self):

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

		reference_data = 12.0

		sim = SteadyStatesSimulation(
			list_of_models=[m],
		)
		sim.run()

		results = sim.getRawData()

		self.assertAlmostEqual(reference_data, results[p.getSbmlId()][0], delta=reference_data*0.001)

	def testSeveralInitialValues(self):

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

		input_data = [1.2, 12.0, 120.0, 1200.0]
		input_species = s

		reference_data = [1.2, 12.0, 120.0, 1200.0]

		sim = SteadyStatesSimulation(
			list_of_models=[m],
			species_input=input_species,
			list_of_initial_values=input_data,
		)
		sim.run()

		results = sim.getRawData()

		for i, t_data in enumerate(reference_data):
			self.assertAlmostEqual(t_data, results[p.getSbmlId()][i], delta=t_data*0.001)
