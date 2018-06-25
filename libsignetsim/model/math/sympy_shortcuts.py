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

	This file ...

"""

from sympy.core.symbol import Symbol as SympySymbol
from sympy.core.numbers import Integer as SympyInteger
from sympy.core.numbers import Float as SympyFloat
from sympy.core.basic import Atom as SympyAtom
from sympy.core.containers import Tuple as SympyTuple
from sympy.core.symbol import Dummy as SympyDummy
#numbers
from sympy.core.numbers import One as SympyOne
from sympy.core.numbers import NegativeOne as SympyNegOne
from sympy.core.numbers import Zero as SympyZero
from sympy.core.numbers import pi as SympyPi
from sympy.core.numbers import E as SympyE
from sympy.core.numbers import Exp1 as SympyExp1
from sympy.core.numbers import Half as SympyHalf
from sympy.core.numbers import Rational as SympyRational
from sympy.core.numbers import oo as SympyInf
from sympy.core.numbers import nan as SympyNan
from sympy.physics.units import avogadro_number as SympyAvogadro
#basic operators
from sympy.core.add import Add as SympyAdd
from sympy.core.mul import Mul as SympyMul
from sympy.core.power import Pow as SympyPow

#advanced operators
from sympy.core.function import Function as SympyFunction
from sympy.core.function import UndefinedFunction as SympyUndefinedFunction
from sympy.core.function import Lambda as SympyLambda
from sympy.functions.elementary.miscellaneous import IdentityFunction as SympyIdentityFunction

from sympy.core.function import Derivative as SympyDerivative
from sympy.functions.elementary.integers import ceiling as SympyCeiling
from sympy.functions.elementary.integers import floor as SympyFloor
from sympy.functions.elementary.complexes import Abs as SympyAbs
from sympy.functions.elementary.exponential import log as SympyLog
from sympy.functions.elementary.exponential import exp as SympyExp
from sympy.functions.elementary.piecewise import Piecewise as SympyPiecewise
from sympy.functions.elementary.piecewise import ExprCondPair as SympyExprCondPair

from sympy.functions.combinatorial.factorials import factorial as SympyFactorial
from sympy.functions import root as SympyRoot

#trigo
from sympy.functions import acos as SympyAcos
from sympy.functions import asin as SympyAsin
from sympy.functions import atan as SympyAtan
from sympy.functions import acosh as SympyAcosh
from sympy.functions import asinh as SympyAsinh
from sympy.functions import atanh as SympyAtanh
from sympy.functions import cos as SympyCos
from sympy.functions import sin as SympySin
from sympy.functions import tan as SympyTan
from sympy.functions import acot as SympyAcot
from sympy.functions import acoth as SympyAcoth
from sympy.functions import cosh as SympyCosh
from sympy.functions import sinh as SympySinh
from sympy.functions import tanh as SympyTanh
from sympy.functions import sec as SympySec
from sympy.functions import csc as SympyCsc
from sympy.functions import cot as SympyCot
from sympy.functions import coth as SympyCoth
from sympy.functions import acsc as SympyAcsc
from sympy.functions import asec as SympyAsec
# from sympy.mpmath import acsch as SympyAcsch
# from sympy.mpmath import asech as SympyAsech

#comparaison
from sympy.core import Equality as SympyEqual
from sympy.core import Unequality as SympyUnequal
from sympy.core import GreaterThan as SympyGreaterThan
from sympy.core import LessThan as SympyLessThan
from sympy.core import StrictGreaterThan as SympyStrictGreaterThan
from sympy.core import StrictLessThan as SympyStrictLessThan

#logic
from sympy.logic.boolalg import And as SympyAnd
from sympy.logic.boolalg import Or as SympyOr
from sympy.logic.boolalg import Xor as SympyXor
from sympy.logic.boolalg import Not as SympyNot
from sympy.logic.boolalg import Implies as SympyImplies
from sympy.logic.boolalg import true as SympyTrue
from sympy.logic.boolalg import false as SympyFalse
from sympy.logic.boolalg import ITE as SympyITE

from sympy.functions.elementary.miscellaneous import Max as SympyMax
from sympy.functions.elementary.miscellaneous import Min as SympyMin

SympyRateOf = SympyFunction("rateOf")
SympyQuotient = SympyFunction("quotient")
SympyRem = SympyFunction("rem")
SympyUnevaluatedMin = SympyFunction("min")
SympyUnevaluatedMax = SympyFunction("max")
