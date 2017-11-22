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

	Testing the creation and destruction of local parameters

"""

from libsignetsim import SbmlDocument, Model, KineticLaw, Settings

from unittest import TestCase
from os.path import join

class TestLocalParameters(TestCase):
	""" Tests local parameters """


	def testLocalParameter(self):
		""" Just create and local parameter, and then destroy it
		"""

		model = Model()

		c = model.listOfCompartments.new("c", value=2)

		s1 = model.listOfSpecies.new("s1")

		p1 = model.listOfParameters.new("p1")

		r1 = model.listOfReactions.new("reaction 1")
		r1.listOfReactants.add(s1)
		r1.setKineticLaw(KineticLaw.MASS_ACTION, reversible=False, parameters=[p1])

		self.assertEqual(len(r1.listOfLocalParameters), 0)

		lp1 = r1.listOfLocalParameters.new("lp1")

		self.assertEqual(len(r1.listOfLocalParameters), 1)
		self.assertEqual(r1.listOfLocalParameters[0].getName(), "lp1")

		model.parentDoc.writeSbmlToFile(join(Settings.tempDirectory, "model.sbml"))
		new_doc = SbmlDocument()
		new_doc.readSbmlFromFile(join(Settings.tempDirectory, "model.sbml"))
		model_2 = new_doc.getModelInstance()

		self.assertEqual(len(model_2.listOfReactions[0].listOfLocalParameters), 1)


		r1.listOfLocalParameters.remove(lp1)
		self.assertEqual(len(r1.listOfLocalParameters), 0)

		model.parentDoc.writeSbmlToFile(join(Settings.tempDirectory, "model.sbml"))
		new_doc = SbmlDocument()
		new_doc.readSbmlFromFile(join(Settings.tempDirectory, "model.sbml"))
		model_2 = new_doc.getModelInstance()

		self.assertEqual(len(model_2.listOfReactions[0].listOfLocalParameters), 0)
		self.assertEqual(len(model.listOfParameters), 1)

		p1.toLocal(r1)
		self.assertEqual(len(model.listOfReactions[0].listOfLocalParameters), 1)
		self.assertEqual(len(model.listOfParameters), 0)

		p1.toGlobal()
		self.assertEqual(len(model.listOfReactions[0].listOfLocalParameters), 0)
		self.assertEqual(len(model.listOfParameters), 1)
