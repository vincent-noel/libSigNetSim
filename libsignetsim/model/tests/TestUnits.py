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

from libsignetsim import Model
from libsignetsim.model.sbml.UnitDefinition import UnitDefinition, Unit

from unittest import TestCase
from libsbml import UNIT_KIND_GRAM, UNIT_KIND_LITRE, UNIT_KIND_MOLE, UNIT_KIND_SECOND


class TestUnits(TestCase):
	""" Tests high level functions """


	def testModelUnits(self):
		""" First three test to check the definition of mass action, michaelis and hill kinetics, the last one
			just to check mass action for species defined as substance. All check the option rawFormula, which 
		"""

		model = Model()
		model.setDefaultUnits()

		c = model.listOfCompartments.new("c", value=2)

		s1 = model.listOfSpecies.new("s1")
		s2 = model.listOfSpecies.new("s2", hasOnlySubstanceUnits=True)

		nm = Unit(model)
		nm.new(UNIT_KIND_MOLE, 1, -9)
		l = Unit(model)
		l.new(UNIT_KIND_LITRE, 1, 1)
		lm1 = Unit(model)
		lm1.new(UNIT_KIND_LITRE, -1, 1)
		s = Unit(model)
		s.new(UNIT_KIND_SECOND, 1, 1)

		ud1 = UnitDefinition(model)
		ud1.listOfUnits.append(nm)

		ud2 = UnitDefinition(model)
		ud2.listOfUnits.append(l)

		ud3 = UnitDefinition(model)
		ud3.listOfUnits.append(s)

		ud4 = UnitDefinition(model)
		ud4.listOfUnits.append(nm)
		ud4.listOfUnits.append(lm1)

		self.assertTrue(model.getSubstanceUnits().isEqual(ud1))
		self.assertTrue(model.getExtentUnits().isEqual(ud1))
		self.assertTrue(model.getTimeUnits().isEqual(ud3))
		self.assertTrue(model.getCompartmentUnits().isEqual(ud2))
		self.assertTrue(c.getUnits().isEqual(ud2))
		self.assertTrue(s1.getUnits().isEqual(ud4))
		self.assertTrue(s2.getUnits().isEqual(ud1))
