#!/usr/bin/env python
""" MathEquation.py


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
from libsignetsim.model.ModelException import ModelException

class MathEquation(MathFormula):

    MATH_EQ             =  10
    MATH_NEQ            =  11
    MATH_LT             =  12
    MATH_GT             =  13
    MATH_LEQ            =  14
    MATH_GEQ            =  15

    def __init__(self, model):
        MathFormula.__init__(self, model, MathFormula.MATH_EQUATION)


    def getCLHS(self):
        return self.writeCCode(self.getDeveloppedInternalMathFormula().args[0])


    def getCRHS(self):
        return self.writeCCode(self.getDeveloppedInternalMathFormula().args[1])


    def getOperator(self):
        return self.getInternalMathFormula().func


    def isOperatorEq(self):
        return self.getOperator() == SympyEqual


    def isOperatorNeq(self):
        return self.getOperator() == SympyUnequal


    def isOperatorGeq(self):
        return self.getOperator() == SympyGreaterThan


    def isOperatorLeq(self):
        return self.getOperator() == SympyLessThan


    def isOperatorGt(self):
        return self.getOperator() == SympyStrictGreaterThan


    def isOperatorLt(self):
        return self.getOperator() == SympyStrictLessThan