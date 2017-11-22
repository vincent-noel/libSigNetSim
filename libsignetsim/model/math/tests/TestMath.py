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

from libsignetsim import Model, MathFormula, KineticLaw

from libsignetsim.model.math.sympy_shortcuts import SympyEqual, SympyZero
from unittest import TestCase
from sympy import simplify


class TestMath(TestCase):
	""" Tests high level functions """


	def testPrettyPrint(self):

		model = Model()

		c = model.listOfCompartments.new("c")

		s1 = model.listOfSpecies.new("s1")
		s2 = model.listOfSpecies.new("s2")
		s3 = model.listOfSpecies.new("s3")

		s4 = model.listOfSpecies.new("s4", hasOnlySubstanceUnits=True)
		s5 = model.listOfSpecies.new("s5", hasOnlySubstanceUnits=True)
		s6 = model.listOfSpecies.new("s6", hasOnlySubstanceUnits=True)


		f1 = MathFormula(model)
		f1.setPrettyPrintMathFormula("s1+s2*s3")

		f2 = MathFormula(model)
		f2.setPrettyPrintMathFormula("s1/c + (s2/c)*(s3/c)", rawFormula=True)

		f3 = MathFormula(model)
		f3.setPrettyPrintMathFormula("s4+s5*s6")

		f4 = MathFormula(model)
		f4.setPrettyPrintMathFormula("s4+s5*s6", rawFormula=True)

		self.assertTrue(self.sympyEqual(
			f1.getDeveloppedInternalMathFormula(),
			f2.getDeveloppedInternalMathFormula()
		))

		self.assertTrue(self.sympyEqual(
			f3.getDeveloppedInternalMathFormula(),
			f4.getDeveloppedInternalMathFormula()
		))

	def sympyEqual(self, a, b):

		# print "test %s == %s : %s" % (simplify(a), simplify(b), (simplify(a-b) == 0))
		# print "test %s == %s : %s" % (a, b, (simplify(a-b) == 0))
		return simplify(a-b) == 0