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

from libsignetsim import SbmlDocument, TimeseriesSimulation

from unittest import TestCase
from os.path import join, dirname
from os import getcwd


class TestReduceModel(TestCase):
	""" Tests high level functions """


	def testReduceModel(self):

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(testfiles_path, "modelqlzB7i.xml"))

		sbml_model = sbml_doc.getModelInstance()
		sbml_model.build(reduce=False)

		sim = TimeseriesSimulation([sbml_model], time_min=0, time_max=10000, time_ech=100)
		sim.run()
		t, ys = sim.getRawData()[0]

		sbml_model.asymetricModel.build()

		sim_reduced = TimeseriesSimulation([sbml_model], time_min=0, time_max=10000, time_ech=100)
		sim_reduced.run()
		t_reduced, ys_reduced = sim_reduced.getRawData()[0]

		for i, y in enumerate(ys['mapk_pp']):
			self.assertAlmostEqual(y, ys_reduced['mapk_pp'][i], delta=y*1e-4)
