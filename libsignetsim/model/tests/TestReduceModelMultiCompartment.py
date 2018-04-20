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

	Testing the research for conservation laws, and the subsequent reduction

"""
from libsignetsim import Model, KineticLaw, TimeseriesSimulation

from unittest import TestCase


class TestReduceModelMultiCompartment(TestCase):
	""" Tests high level functions """


	def testReduceModel(self):

		model = Model()
		cytosol = model.listOfCompartments.new("Cytosol", value=100)
		membrane = model.listOfCompartments.new("Membrane", value=10)

		ras_cytosol = model.listOfSpecies.new("Ras (cytosol)", cytosol, 27.5)
		ras_membrane = model.listOfSpecies.new("Ras (membrane)", membrane, 0)

		kf = model.listOfParameters.new("To cytosol", 1)
		kr = model.listOfParameters.new("To membrane", 1)

		r = model.listOfReactions.new("Ras transport")
		r.listOfReactants.add(ras_membrane)
		r.listOfProducts.add(ras_cytosol)

		r.setKineticLaw(KineticLaw.MASS_ACTION, reversible=True, parameters=[kf, kr])

		model.build(reduce=False)

		sim = TimeseriesSimulation([model], time_min=0, time_max=100, time_ech=10)
		sim.run()
		t, ys = sim.getRawData()[0]

		model.build(reduce=True, vars_to_keep=[ras_cytosol.getSymbolStr()])

		sim_reduced = TimeseriesSimulation([model], time_min=0, time_max=100, time_ech=10)
		sim_reduced.run()
		t_reduced, ys_reduced = sim_reduced.getRawData()[0]

		for i, y in enumerate(ys['Ras_cytosol']):
			self.assertAlmostEqual(y, ys_reduced['Ras_cytosol'][i], delta=y*1e-4)
