#!/usr/bin/env python
""" MathCFEs.py


	This file ...


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

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import  (
	SympySymbol, SympyInteger, SympyFloat, SympyRational, SympyAtom,
	SympyOne, SympyNegOne, SympyZero, SympyPi, SympyE, SympyExp1, SympyHalf,
	SympyInf, SympyNan, SympyAdd, SympyMul, SympyPow,
	SympyFunction, SympyUndefinedFunction, SympyLambda, SympyDerivative,
	SympyCeiling, SympyFloor, SympyAbs, SympyLog, SympyExp, SympyPiecewise,
	SympyFactorial, SympyRoot, SympyAcos, SympyAsin, SympyAtan, SympyAcosh,
	SympyAsinh, SympyAtanh, SympyCos, SympySin, SympyTan, SympyAcot,
	SympyAcoth, SympyCosh, SympySinh, SympyTanh, SympySec, SympyCsc,
	SympyCot, SympyCoth, SympyAcsc, SympyAsec,
	SympyEqual, SympyUnequal, SympyGreaterThan, SympyLessThan,
	SympyStrictGreaterThan, SympyStrictLessThan,
	SympyAnd, SympyOr, SympyXor, SympyNot, SympyTrue, SympyFalse,
	SympyMax, SympyMin)
from sympy import simplify, diff, solve


class MathCFEs(object):
	""" Sbml model class """


	ASSIGNMENT          = 0
	REACTION            = 1
	SOLVED              = 2


	def __init__ (self):
		""" Constructor of model class """

		# Closed forms equations
		self.CFEs = []
		self.CFE_vars = []
		self.CFE_types = []


	def hasCFEs(self):
		return len(self.CFEs) > 0

	def getCCFE(self, ind):
		return self.CFEs[ind].getCMathFormula()

	def getCFEs(self, forcedConcentration=False):

		res = []

		for i, t_type in enumerate(self.CFE_types):
			if t_type != self.REACTION:

				if forcedConcentration:
					t_var = self.CFE_vars[i].getFinalMathFormula(forcedConcentration)
					if len(self.listOfCompartments.keys()) == 1:
						t_comp = self.listOfCompartments.values()[0]
						t_cfe = self.CFEs[i].getDeveloppedInternalMathFormula().subs({t_comp.symbol.getInternalMathFormula():t_comp.value.getInternalMathFormula()})
					else:
						t_cfe = self.CFEs[i].getDeveloppedInternalMathFormula()#.subs(self.listOfVariables.getAmountsToConcentrations())

					t_variable = self.listOfVariables[str(self.CFE_vars[i].getInternalMathFormula())]
					# if t_variable.isConcentration():
					#     t_cfe /= t_variable.getCompartment().symbol.getInternalMathFormula()

					t_formula = MathFormula(self)
					t_formula.setInternalMathFormula(t_cfe)
					t_value = t_formula.getFinalMathFormula(forcedConcentration)

				else:
					t_var = self.CFE_vars[i].getFinalMathFormula(forcedConcentration)
					t_value = self.CFEs[i].getFinalMathFormula(forcedConcentration)

				res.append(SympyEqual(t_var, t_value))

		return res

	def buildCFE(self):

		self.CFEs = []
		self.CFE_vars = []
		self.CFE_types = []

		if self.listOfRules.hasAssignmentRule():
			for rule in self.listOfRules.values():
				if rule.isAssignment():
					self.CFE_types.append(self.ASSIGNMENT)

					t_var = MathFormula(self, MathFormula.MATH_VARIABLE)
					t_var.setInternalMathFormula(rule.getVariable().symbol.getInternalMathFormula())
					self.CFE_vars.append(t_var)
					print t_var.getPrettyPrintMathFormula()

					t_cfe = MathFormula(self)
					t_cfe.setInternalMathFormula(rule.getDefinition().getInternalMathFormula())
					self.CFEs.append(t_cfe)
					print t_cfe.getPrettyPrintMathFormula()


		for reaction in self.listOfReactions.values():
			self.CFE_types.append(self.REACTION)

			t_var = MathFormula(self, MathFormula.MATH_VARIABLE)
			t_var.setInternalMathFormula(reaction.symbol.getInternalMathFormula())
			self.CFE_vars.append(t_var)

			t_cfe = MathFormula(self)
			t_cfe.setInternalMathFormula(reaction.value.getInternalMathFormula())
			self.CFEs.append(t_cfe)


		self.developCFEs()


	def developCFEs(self):

		# print "developping CFEs"
		# Here we just develop the expression,
		# so that no closed-form depends on another.
		# Just to be sure not to get any ordering constraints
		# In two passes, not sure it's the right thing to do, but it works

		if len(self.CFEs) > 0:
			for i_cfe, t_cfe in enumerate(self.CFEs):
				tt_cfe = t_cfe.getDeveloppedInternalMathFormula()
				for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
					if t_cfe_var.getInternalMathFormula() in tt_cfe.atoms(SympySymbol) and i_cfe_var < i_cfe:
						tt_cfe = tt_cfe.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
				self.CFEs[i_cfe].setInternalMathFormula(tt_cfe)


			for i_cfe, t_cfe in enumerate(self.CFEs):
				tt_cfe = t_cfe.getDeveloppedInternalMathFormula()
				for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
					if t_cfe_var.getInternalMathFormula() in tt_cfe.atoms(SympySymbol):
						tt_cfe = tt_cfe.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
				self.CFEs[i_cfe].setInternalMathFormula(simplify(tt_cfe))


	def printCFEs(self):

		print "-----------------------------"
		for i_equ, equ in enumerate(self.CFEs):
			print ">> %s = %s" % (str(self.CFE_vars[i_equ].getDeveloppedInternalMathFormula()),
								str(equ.getDeveloppedInternalMathFormula()))
