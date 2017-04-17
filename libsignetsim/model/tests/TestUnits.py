#!/usr/bin/env python
""" TestModelDefinition.py


	Testing the research for conservation laws, and the subsequent reduction


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

from libsignetsim.model.Model import Model
from libsignetsim.model.sbml.KineticLaw import KineticLaw
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympyEqual, SympyZero
from unittest import TestCase
from sympy import simplify
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

		p1 = model.listOfParameters.new("p1")


		print model.getSubstanceUnits()
		print model.getExtentUnits()
		print model.getTimeUnits()
		print c.getUnits()
		print s1.getUnits()
		print s2.getUnits()


	def sympyEqual(self, a, b):

		# print "test %s == %s : %s" % (simplify(a), simplify(b), (simplify(a-b) == 0))
		# print "test %s == %s : %s" % (a, b, (simplify(a-b) == 0))
		return simplify(a-b) == 0