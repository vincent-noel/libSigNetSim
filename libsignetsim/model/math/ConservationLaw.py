#!/usr/bin/env python
""" ConservationLaw.py


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


# from libsignetsim.model.math.MathFormula import MathFormula
# from libsignetsim.model.math.sympy_shortcuts import  (
# 	SympySymbol, SympyInteger, SympyFloat, SympyRational, SympyAtom,
# 	SympyOne, SympyNegOne, SympyZero, SympyPi, SympyE, SympyExp1, SympyHalf,
# 	SympyInf, SympyNan, SympyAdd, SympyMul, SympyPow,
# 	SympyFunction, SympyUndefinedFunction, SympyLambda, SympyDerivative,
# 	SympyCeiling, SympyFloor, SympyAbs, SympyLog, SympyExp, SympyPiecewise,
# 	SympyFactorial, SympyRoot, SympyAcos, SympyAsin, SympyAtan, SympyAcosh,
# 	SympyAsinh, SympyAtanh, SympyCos, SympySin, SympyTan, SympyAcot,
# 	SympyAcoth, SympyCosh, SympySinh, SympyTanh, SympySec, SympyCsc,
# 	SympyCot, SympyCoth, SympyAcsc, SympyAsec,
# 	SympyEqual, SympyUnequal, SympyGreaterThan, SympyLessThan,
# 	SympyStrictGreaterThan, SympyStrictLessThan,
# 	SympyAnd, SympyOr, SympyXor, SympyNot, SympyTrue, SympyFalse,
# 	SympyMax, SympyMin)
# from libsignetsim.settings.Settings import Settings
# from sympy import simplify, diff, solve, srepr, linsolve
# from time import time
# from sympy.solvers.solveset import nonlinsolve
class ConservationLaw(object):
	""" Sbml model class """

	def __init__ (self):
		""" Constructor of model class """

		self.LHSs = []
		self.RHSs = []
		self.vars = []
