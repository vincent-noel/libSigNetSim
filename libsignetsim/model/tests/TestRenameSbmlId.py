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

from libsignetsim import Model, KineticLaw, MathFormula

from unittest import TestCase
from sympy import simplify


class TestRenameSbmlId(TestCase):
	""" Tests high level functions """


	def testRenameSbmlId(self):

		model = Model()

		c = model.listOfCompartments.new("c")

		s1 = model.listOfSpecies.new("s1")
		s2 = model.listOfSpecies.new("s2")
		s3 = model.listOfSpecies.new("s3")
		s4 = model.listOfSpecies.new("s4")
		s5 = model.listOfSpecies.new("s5")

		p1 = model.listOfParameters.new("p1")
		p2 = model.listOfParameters.new("p2")
		p3 = model.listOfParameters.new("p3")
		p4 = model.listOfParameters.new("p4")

		r1 = model.listOfReactions.new("reaction 1")
		r1.listOfReactants.add(s1)
		r1.listOfReactants.add(s2)
		r1.listOfProducts.add(s3)
		r1.setKineticLaw(KineticLaw.MASS_ACTION, reversible=True, parameters=[p1, p2])

		a1 = model.listOfRules.newAssignmentRule(s4, "p1*s3")
		rate1 = model.listOfRules.newRateRule(s5, "p4*s3")
		alg1 = model.listOfRules.newAlgebraicRule("p4*s3-p3")

		e1 = model.listOfEvents.new()
		e1.setTrigger("p2/s1 > p4/s3")
		e_ass = e1.addEventAssignment(s3, "p3*s3")


		model.renameSbmlId("s3", "s3_bis")

		fr1 = MathFormula(model)
		fr1.setPrettyPrintMathFormula("c * (p1 * (s1 / c) * (s2 / c) - p2 * s3_bis / c)", rawFormula=True)
		self.assertTrue(self.sympyEqual(
			r1.kineticLaw.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula(),
			fr1.getDeveloppedInternalMathFormula()
		))

		fa1 = MathFormula(model)
		fa1.setPrettyPrintMathFormula("c * p1 * (s3_bis / c)", rawFormula=True)
		self.assertTrue(self.sympyEqual(
			a1.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula(),
			fa1.getDeveloppedInternalMathFormula()
		))

		frate1 = MathFormula(model)
		frate1.setPrettyPrintMathFormula("c * p4 * (s3_bis / c)", rawFormula=True)
		self.assertTrue(self.sympyEqual(
			rate1.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula(),
			frate1.getDeveloppedInternalMathFormula()
		))

		falg1 = MathFormula(model)
		falg1.setPrettyPrintMathFormula("-p3 + p4 * (s3_bis / c)", rawFormula=True)
		self.assertTrue(self.sympyEqual(
			alg1.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula(),
			falg1.getDeveloppedInternalMathFormula()
		))

		fe_trigger = MathFormula(model)
		fe_trigger.setPrettyPrintMathFormula("p2/(s1/c) > p4/(s3_bis/c)", rawFormula=True)
		self.assertTrue(self.sympyEqual(
			e1.trigger.getDeveloppedInternalMathFormula(),
			fe_trigger.getDeveloppedInternalMathFormula()
		))

		fe_ass = MathFormula(model)
		fe_ass.setPrettyPrintMathFormula("p3*(s3_bis/c)", rawFormula=True)
		self.assertTrue(self.sympyEqual(
			e_ass.getDefinition().getDeveloppedInternalMathFormula(),
			fe_ass.getDeveloppedInternalMathFormula()
		))

	def sympyEqual(self, a, b):

		return simplify(a-b) == 0