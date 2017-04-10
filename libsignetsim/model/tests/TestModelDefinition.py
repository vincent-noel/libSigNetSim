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
class TestModelDefinition(TestCase):
	""" Tests high level functions """


	def testKineticLaws(self):

		model = Model()

		s1 = model.listOfSpecies.new("s1")
		s2 = model.listOfSpecies.new("s2")
		s3 = model.listOfSpecies.new("s3")

		p1 = model.listOfParameters.new("p1")
		p2 = model.listOfParameters.new("p2")
		p3 = model.listOfParameters.new("p3")

		r1 = model.listOfReactions.new("reaction 1")
		r1.listOfReactants.add(s1)
		r1.listOfReactants.add(s2)
		r1.listOfProducts.add(s3)
		r1.setKineticLaw(KineticLaw.MASS_ACTION, reversible=True, parameters=[p1,p2])

		formula_r1 = MathFormula(model)
		formula_r1.setPrettyPrintMathFormula("p1*s1*s2 - p2*s3")
		self.assertTrue(self.sympyEqual(
			r1.kineticLaw.getDefinition(forcedConcentration=True).getDeveloppedInternalMathFormula(),
			formula_r1.getDeveloppedInternalMathFormula()
		))

		formula_r1_amount = MathFormula(model)
		formula_r1_amount.setPrettyPrintMathFormula("compartment_0*(p1*s1*s2 - p2*s3)")
		self.assertTrue(self.sympyEqual(
			r1.kineticLaw.getDefinition().getDeveloppedInternalMathFormula(),
			formula_r1_amount.getDeveloppedInternalMathFormula()
		))

		r2 = model.listOfReactions.new("reaction 2")
		r2.listOfReactants.add(s1)
		r2.listOfModifiers.add(s2)
		r2.listOfProducts.add(s3)
		r2.setKineticLaw(KineticLaw.MICHAELIS, reversible=False, parameters=[p1, p2])

		formula_r2 = MathFormula(model)
		formula_r2.setPrettyPrintMathFormula("p1*s1*s2/(p2+s1)")
		self.assertTrue(self.sympyEqual(
			r2.kineticLaw.getDefinition(forcedConcentration=True).getDeveloppedInternalMathFormula(),
			formula_r2.getDeveloppedInternalMathFormula()
		))

		formula_r2_amount = MathFormula(model)
		formula_r2_amount.setPrettyPrintMathFormula("compartment_0*p1*s1*s2/(p2+s1)")
		self.assertTrue(self.sympyEqual(
			r2.kineticLaw.getDefinition().getDeveloppedInternalMathFormula(),
			formula_r2_amount.getDeveloppedInternalMathFormula()
		))

		r3 = model.listOfReactions.new("reaction 3")
		r3.listOfReactants.add(s1)
		r3.listOfModifiers.add(s2)
		r3.listOfProducts.add(s3)
		r3.setKineticLaw(KineticLaw.HILL, reversible=False, parameters=[p1, p2, p3])

		formula_r3 = MathFormula(model)
		formula_r3.setPrettyPrintMathFormula("p1*s1^p3*s2/(p2+s1^p3)")
		self.assertTrue(self.sympyEqual(
			r3.kineticLaw.getDefinition(forcedConcentration=True).getDeveloppedInternalMathFormula(),
			formula_r3.getDeveloppedInternalMathFormula()
		))

		formula_r3_amount = MathFormula(model)
		formula_r3_amount.setPrettyPrintMathFormula("compartment_0*p1*s1^p3*s2/(p2+s1^p3)")
		self.assertTrue(self.sympyEqual(
			r3.kineticLaw.getDefinition().getDeveloppedInternalMathFormula(),
			formula_r3_amount.getDeveloppedInternalMathFormula()
		))

	def sympyEqual(self, a, b):

		# print "test %s == %s : %s" % (a, b, (simplify(a-b) == 0))
		return simplify(a-b) == 0