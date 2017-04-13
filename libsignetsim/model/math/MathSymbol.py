#!/usr/bin/env python
""" MathSymbol.py


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
from libsignetsim.settings.Settings import Settings
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


class MathSymbol(MathFormula):

	def __init__(self, model, variable, is_from_reaction=None):

		self.__model = model
		self.__variable = variable
		MathFormula.__init__(self, model, MathFormula.MATH_VARIABLE, isFromReaction=is_from_reaction)


	def setInternalVariable(self, internal_variable):
		MathFormula.setInternalMathFormula(self, internal_variable)

	def getInternalMathFormula(self, forcedConcentration=True):

		from libsignetsim.model.math.MathVariable import MathVariable

		# The if type(var) test is to check is the variable is a copied, simple math variable,
		# or if it's a more complex type, like species or parameter, which inherit from MathVariable
		# If it's just a math variable, if has no method isConcentration()
		if type(self.__variable) == MathVariable or not self.__variable.isConcentration() or (self.__variable.isConcentration() and forcedConcentration):
			return MathFormula.getInternalMathFormula(self)
		else:
			return SympySymbol("_speciesForcedConcentration_%s_" % str(MathFormula.getInternalMathFormula(self)))


	def getMathFormulaDerivative(self, math_type):

		if math_type in [MathFormula.MATH_INTERNAL, MathFormula.MATH_DEVINTERNAL, MathFormula.MATH_FINALINTERNAL]:
			f = MathFormula.getMathFormula(self, math_type)
			return SympyDerivative(f, MathFormula.t)


	def getDerivative(self):

		f = MathFormula.getInternalMathFormula(self)
		t_formula = MathFormula(self.__model, MathFormula.MATH_VARIABLE)
		t_formula.setInternalMathFormula(SympyDerivative(f, MathFormula.t))
		return t_formula

	def getInternalMathFormulaDerivative(self):
		return self.getMathFormulaDerivative(MathFormula.MATH_INTERNAL)

	def getSbmlMathFormula(self, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		return MathFormula.getMathFormula(self, self.MATH_SBML)

	def getFinalMathFormula(self, forcedConcentration=False):
		if self.isFromReaction is not None:
			t_formula = MathFormula.getInternalMathFormula(self)
			t_math = MathFormula(self.__model)
			t_symbol = MathFormula.getInternalMathFormula(self)
			t_new_symbol = SympySymbol(MathFormula.getSbmlMathFormula(self).getName())
			t_math.setInternalMathFormula(t_formula.subs({t_symbol: t_new_symbol}))
			return t_math.getFinalMathFormula(forcedConcentration=True)
		else:
			return MathFormula.getFinalMathFormula(self,forcedConcentration=True)


	def readUI(self, sbml_id):
		MathFormula.setValueMathFormula(self, sbml_id)

	def getCMathFormula(self):
		return self.writeCCode(MathFormula.getInternalMathFormula(self))

	def getPrettyPrintMathFormula(self):
		return str(MathFormula.getInternalMathFormula(self))
