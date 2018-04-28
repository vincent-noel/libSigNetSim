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
from __future__ import print_function
from __future__ import absolute_import



from libsignetsim.sedml.SedmlException import SedmlMathException

import libsbml
# token: cn , ci , csymbol , sep
from libsedml import AST_NAME, AST_NAME_TIME
from .sympy_shortcuts import SympyInteger, SympyFloat, SympySymbol
# qualifiers: degree , bvar , logbase

# general : apply , piecewise , piece , otherwise , lambda
from libsedml import AST_FUNCTION_PIECEWISE, AST_LAMBDA
from .sympy_shortcuts import SympyPiecewise, SympyITE, SympyLambda

# relational operators: eq , neq , gt , lt , geq , leq
from libsedml import (
	AST_RELATIONAL_EQ, AST_RELATIONAL_NEQ, AST_RELATIONAL_GT, AST_RELATIONAL_LT, AST_RELATIONAL_GEQ, AST_RELATIONAL_LEQ
)
from .sympy_shortcuts import (
	SympyEqual, SympyUnequal, SympyStrictGreaterThan, SympyStrictLessThan, SympyGreaterThan, SympyLessThan
)

# arithmetic operators: plus , minus , times , divide , power , root , abs , exp , ln , log , floor , ceiling ,
from libsedml import (
	AST_PLUS, AST_MINUS, AST_TIMES, AST_DIVIDE, AST_POWER, AST_FUNCTION_POWER, AST_FUNCTION_ROOT, AST_FUNCTION_ABS, AST_FUNCTION_EXP,
	AST_FUNCTION_LN, AST_FUNCTION_LOG, AST_FUNCTION_FLOOR, AST_FUNCTION_CEILING
)
from .sympy_shortcuts import (SympyAdd, SympyMul, SympyPow, SympyAbs, SympyExp, SympyLog, SympyFloor, SympyCeiling)


# factorial
from libsedml import AST_FUNCTION_FACTORIAL
from .sympy_shortcuts import SympyFactorial

# logical operators: and , or , xor , not
from libsedml import AST_LOGICAL_AND, AST_LOGICAL_OR, AST_LOGICAL_XOR, AST_LOGICAL_NOT
from .sympy_shortcuts import SympyAnd, SympyOr, SympyXor, SympyNot

# trigonometric operators: sin , cos , tan , sec , csc , cot
from libsedml import (
	AST_FUNCTION_SIN, AST_FUNCTION_COS, AST_FUNCTION_TAN, AST_FUNCTION_SEC, AST_FUNCTION_CSC, AST_FUNCTION_COT
)
from .sympy_shortcuts import (SympySin, SympyCos, SympyTan, SympySec, SympyCsc, SympyCot)


# trigonometric operators: sinh , cosh , tanh , sech , csch , coth ,
from libsedml import (
	AST_FUNCTION_SINH, AST_FUNCTION_COSH, AST_FUNCTION_TANH, AST_FUNCTION_SECH, AST_FUNCTION_CSCH, AST_FUNCTION_COTH
)
from .sympy_shortcuts import (SympySinh, SympyCosh, SympyTanh, SympyCoth)

# trigonometric operators: arcsin , arccos , arctan , arcsec , arccsc , arccot
from libsedml import (
	AST_FUNCTION_ARCSIN, AST_FUNCTION_ARCCOS, AST_FUNCTION_ARCTAN, AST_FUNCTION_ARCSEC, AST_FUNCTION_ARCCSC,
	AST_FUNCTION_ARCCOT
)
from .sympy_shortcuts import (SympyAsin, SympyAcos, SympyAtan, SympyAsec, SympyAcsc, SympyAcot)

# trigonometric operators: arcsinh , arccosh , arctanh , arcsech , arccsch , arccoth
from libsedml import (
	AST_FUNCTION_ARCSINH, AST_FUNCTION_ARCCOSH, AST_FUNCTION_ARCTANH, AST_FUNCTION_ARCSECH,
	AST_FUNCTION_ARCCSCH, AST_FUNCTION_ARCCOTH
)
from .sympy_shortcuts import (SympyAsinh, SympyAcosh, SympyAtanh, SympyAcoth)

# aggregate functions : min, max, sum, product
from .sympy_shortcuts import SympyFunction

# constants: true , false , notanumber , pi , infinity , exponentiale
# TODO : Infinity, NaN
from libsedml import (AST_CONSTANT_TRUE, AST_CONSTANT_FALSE, AST_CONSTANT_PI, AST_CONSTANT_E)
from .sympy_shortcuts import (SympyTrue, SympyFalse, SympyPi, SympyE, SympyInf, SympyNan)

from libsedml import parseFormula, formulaToString
from six.moves import reload_module
reload_module(libsbml)


class SedmlMathReader(object):
	""" Class for handling math formulaes """

	def __init__(self, document):
		""" Constructor """

		self.__document = document

	def translateForInternal(self, tree):

		""" Translate an SBML Tree in a Sympy Tree """

		if tree.isInfinity():
			return SympyInf

		elif tree.isNegInfinity():
			return SympyMul(SympyInteger(-1), SympyInf)

		elif tree.isNaN():
			return SympyNan

		elif tree.getType() == AST_NAME:
			return SympySymbol(tree.getName())

		elif tree.getType() == AST_NAME_TIME:
			return SympySymbol("time")

		elif tree.isNumber():

			if tree.isInteger():
				return SympyInteger(tree.getInteger())

			elif tree.isReal():
				return SympyFloat(tree.getReal())

			else:
				raise SedmlMathException("SedMathReader : Unknown type of number")

		elif tree.isConstant():
			if tree.getType() == AST_CONSTANT_E:
				return SympyE

			elif tree.getType() == AST_CONSTANT_FALSE:
				return SympyFalse

			elif tree.getType() == AST_CONSTANT_TRUE:
				return SympyTrue

			elif tree.getType() == AST_CONSTANT_PI:
				return SympyPi

			else:
				raise SedmlMathException("SedmlMathReader : Unknown constant")

		elif tree.isOperator():

			if tree.getType() == AST_PLUS:

				if tree.getNumChildren() == 0:
					return SympyInteger(0)

				else:
					t_children = []
					for i_arg in range(tree.getNumChildren()):
						t_children.append(self.translateForInternal(tree.getChild(i_arg)))
					return SympyAdd(*t_children, evaluate=False)

			elif tree.getType() == AST_MINUS:

				if tree.getNumChildren() == 2:
					return SympyAdd(
								self.translateForInternal(tree.getChild(0)),
								SympyMul(
									SympyInteger(-1),
									self.translateForInternal(tree.getChild(1)),
									evaluate=False),
								evaluate=False)

				elif tree.getNumChildren() == 1:
					return SympyMul(
								SympyInteger(-1),
								self.translateForInternal(tree.getChild(0)),
								evaluate=False)

				elif tree.getNumChildren() == 0:
					return SympyInteger(0)

				else:
					t_tree = SympyAdd(
								self.translateForInternal(tree.getChild(0)),
								SympyMul(
									SympyInteger(-1),
									self.translateForInternal(tree.getChild(1)), evaluate=False),
								evaluate=False)

					for i_arg in range(2, tree.getNumChildren()):
						t_tree = SympyAdd(
									t_tree,
									SympyMul(
										SympyInteger(-1),
										self.translateForInternal(tree.getChild(i_arg)), evaluate=False),
									evaluate=False)

					return t_tree

			elif tree.getType() == AST_TIMES:

				if tree.getNumChildren() == 0:
					return SympyInteger(1)
				else:
					t_children = []

					for i_arg in range(tree.getNumChildren()):
						t_children.append(self.translateForInternal(tree.getChild(i_arg)))

					return SympyMul(*t_children, evaluate=False)

			elif tree.getType() == AST_DIVIDE:
				return SympyMul(
								self.translateForInternal(tree.getChild(0)),
								SympyPow(self.translateForInternal(tree.getChild(1)), SympyInteger(-1)))

			elif tree.getType() == AST_POWER or tree.getType() == AST_FUNCTION_POWER:
				t_x = self.translateForInternal(tree.getChild(0))
				t_n = self.translateForInternal(tree.getChild(1))
				return SympyPow(t_x, t_n, evaluate=False)

			else:
				raise SedmlMathException("SedmlMathReader : Unknown operator")

		elif tree.isFunction():

				# AST_FUNCTION_ABS
			if tree.getType() == AST_FUNCTION_ABS:
				return SympyAbs(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCCOS
			elif tree.getType() == AST_FUNCTION_ARCCOS:
				return SympyAcos(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCCOSH
			elif tree.getType() == AST_FUNCTION_ARCCOSH:
				return SympyAcosh(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCCOT
			elif tree.getType() == AST_FUNCTION_ARCCOT:
				return SympyAcot(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCCOTH
			elif tree.getType() == AST_FUNCTION_ARCCOTH:
				return SympyAcoth(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCCSC
			elif tree.getType() == AST_FUNCTION_ARCCSC:
				return SympyAcsc(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCCSCH
			elif tree.getType() == AST_FUNCTION_ARCCSCH:
				return SympyAsinh(
						SympyPow(self.translateForInternal(tree.getChild(0)), SympyInteger(-1), evaluate=False),
						evaluate=False)

				# AST_FUNCTION_ARCSEC
			elif tree.getType() == AST_FUNCTION_ARCSEC:
				return SympyAsec(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCSECH
			elif tree.getType() == AST_FUNCTION_ARCSECH:
				return SympyAcosh(
						SympyPow(self.translateForInternal(tree.getChild(0)), SympyInteger(-1), evaluate=False),
						evaluate=False)

				# AST_FUNCTION_ARCSIN
			elif tree.getType() == AST_FUNCTION_ARCSIN:
				return SympyAsin(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCSINH
			elif tree.getType() == AST_FUNCTION_ARCSINH:
				return SympyAsinh(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCTAN
			elif tree.getType() == AST_FUNCTION_ARCTAN:
				return SympyAtan(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_ARCTANH
			elif tree.getType() == AST_FUNCTION_ARCTANH:
				return SympyAtanh(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_CEILING
			elif tree.getType() == AST_FUNCTION_CEILING:
				return SympyCeiling(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_COS
			elif tree.getType() == AST_FUNCTION_COS:
				return SympyCos(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_COSH
			elif tree.getType() == AST_FUNCTION_COSH:
				return SympyCosh(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_COT
			elif tree.getType() == AST_FUNCTION_COT:
				return SympyCot(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_COTH
			elif tree.getType() == AST_FUNCTION_COTH:
				return SympyCoth(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_CSC
			elif tree.getType() == AST_FUNCTION_CSC:
				return SympyCsc(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_CSCH
			elif tree.getType() == AST_FUNCTION_CSCH:
				# return SympyCsch(self.translateForInternal(tree.getChild(0)), evaluate=False)
				return SympyPow(
						SympySinh(self.translateForInternal(tree.getChild(0)), evaluate=False),
						SympyInteger(-1), evaluate=False)

				# AST_FUNCTION_EXP
			elif tree.getType() == AST_FUNCTION_EXP:
				return SympyExp(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_FACTORIAL
			elif tree.getType() == AST_FUNCTION_FACTORIAL:
				return SympyFactorial(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_FLOOR
			elif tree.getType() == AST_FUNCTION_FLOOR:
				return SympyFloor(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_LN
			elif tree.getType() == AST_FUNCTION_LN:
				return SympyLog(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_LOG
			elif tree.getType() == AST_FUNCTION_LOG:
				t_n = self.translateForInternal(tree.getChild(0))
				t_x = self.translateForInternal(tree.getChild(1))

				return SympyLog(t_x, t_n, evaluate=False)

				# AST_FUNCTION_PIECEWISE
			elif tree.getType() == AST_FUNCTION_PIECEWISE:

				i_arg = 0
				t_pieces = []
				value_piecewise = False
				while i_arg < tree.getNumChildren():

					if (i_arg+1) < tree.getNumChildren():
						t_value = self.translateForInternal(tree.getChild(i_arg))
						t_condition = self.translateForInternal(tree.getChild(i_arg+1))

						if isinstance(t_value, bool):
							value_piecewise = True

						t_pieces.append((t_value, t_condition))
						i_arg += 2
					else:
						t_value = self.translateForInternal(tree.getChild(i_arg))
						if isinstance(t_value, bool):
							value_piecewise = True
						t_pieces.append((t_value, True))
						i_arg += 1

				if not value_piecewise:
					return SympyPiecewise(*t_pieces, evaluate=False)
				else:
					return SympyITE(t_pieces[0][1], t_pieces[0][0], t_pieces[1][0])

				# AST_FUNCTION_POWER
			elif tree.getType() == AST_POWER or tree.getType() == AST_FUNCTION_POWER:
				t_x = self.translateForInternal(tree.getChild(0))
				t_n = self.translateForInternal(tree.getChild(1))
				return SympyPow(t_x, t_n, evaluate=False)

				# AST_FUNCTION_ROOT
			elif tree.getType() == AST_FUNCTION_ROOT:
				return SympyPow(
						self.translateForInternal(tree.getChild(1)),
						SympyPow(
							self.translateForInternal(tree.getChild(0)),
							SympyInteger(-1), evaluate=False),
						evaluate=False)

				# AST_FUNCTION_SEC
			elif tree.getType() == AST_FUNCTION_SEC:
				return SympySec(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_SECH
			elif tree.getType() == AST_FUNCTION_SECH:
				return SympyPow(
							SympyCosh(self.translateForInternal(tree.getChild(0)), evaluate=False),
							SympyInteger(-1), evaluate=False)

				# AST_FUNCTION_SIN
			elif tree.getType() == AST_FUNCTION_SIN:
				return SympySin(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_SINH
			elif tree.getType() == AST_FUNCTION_SINH:
				return SympySinh(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_TAN
			elif tree.getType() == AST_FUNCTION_TAN:
				return SympyTan(self.translateForInternal(tree.getChild(0)), evaluate=False)

				# AST_FUNCTION_TANH
			elif tree.getType() == AST_FUNCTION_TANH:
				return SympyTanh(self.translateForInternal(tree.getChild(0)), evaluate=False)

			else:
				str_tree = formulaToString(tree)
				if str_tree.startswith("min("):
					return SympyFunction("min")(*([self.translateForInternal(tree.getChild(0))]))

				elif str_tree.startswith("max("):
					return SympyFunction("max")(*([self.translateForInternal(tree.getChild(0))]))

				elif str_tree.startswith("sum("):
					return SympyFunction("sum")(*([self.translateForInternal(tree.getChild(0))]))

				elif str_tree.startswith("product("):
					return SympyFunction("product")(*([self.translateForInternal(tree.getChild(0))]))

				print(tree.getType() == AST_POWER)
				print(tree.getType() == AST_FUNCTION_POWER)
				raise SedmlMathException("SedmlMathReader : Unknown function %s" % formulaToString(tree))

		elif tree.getType() == AST_LAMBDA:

			t_args = []
			for param in range(0, tree.getNumChildren()-1):
				t_args.append(self.translateForInternal(tree.getChild(param)))

			t_def = self.translateForInternal(tree.getChild(tree.getNumChildren()-1))

			return SympyLambda(tuple(t_args), t_def)

		elif tree.isRelational():

			if tree.getType() == AST_RELATIONAL_EQ:
				t_res = SympyEqual(
						self.translateForInternal(tree.getChild(0)),
						self.translateForInternal(tree.getChild(1)), evaluate=False)

				if tree.getNumChildren() > 2:
					# Here the idea is to make a chain, like a==b && b==c && c==d, which should be equal to a==b==c==d
					t_final_res = [t_res]
					for child in range(2, tree.getNumChildren()):
						t_final_res.append(SympyEqual(
								self.translateForInternal(tree.getChild(child-1)),
								self.translateForInternal(tree.getChild(child)), evaluate=False))
					return SympyAnd(*t_final_res, evaluate=False)
				else:
					return t_res

			elif tree.getType() == AST_RELATIONAL_NEQ:
				t_res = SympyUnequal(
						self.translateForInternal(tree.getChild(0)),
						self.translateForInternal(tree.getChild(1)), evaluate=False)

				if tree.getNumChildren() > 2:
					# Here the idea is to make a chain, like a!=b && b!=c && c!=d, which should be equal to a!=b!=c!=d
					t_final_res = [t_res]
					for child in range(2, tree.getNumChildren()):
						t_final_res.append(SympyUnequal(
								self.translateForInternal(tree.getChild(child-1)),
								self.translateForInternal(tree.getChild(child)), evaluate=False))
					return SympyAnd(*t_final_res, evaluate=False)
				else:
					return t_res

			elif tree.getType() == AST_RELATIONAL_GT:
				t_res = SympyStrictGreaterThan(
						self.translateForInternal(tree.getChild(0)),
						self.translateForInternal(tree.getChild(1)), evaluate=False)

				if tree.getNumChildren() > 2:
					# Here the idea is to make a chain, like a>b && b>c, which should be equal to a>b>c
					t_final_res = [t_res]
					for child in range(2, tree.getNumChildren()):
						t_final_res.append(SympyStrictGreaterThan(
								self.translateForInternal(tree.getChild(child-1)),
								self.translateForInternal(tree.getChild(child)), evaluate=False))
					return SympyAnd(*t_final_res, evaluate=False)
				else:
					return t_res

			elif tree.getType() == AST_RELATIONAL_LT:
				t_res = SympyStrictLessThan(
						self.translateForInternal(tree.getChild(0)),
						self.translateForInternal(tree.getChild(1)), evaluate=False)

				if tree.getNumChildren() > 2:
					# Here the idea is to make a chain, like a<b && b<c, which should be equal to a<b<c
					t_final_res = [t_res]
					for child in range(2, tree.getNumChildren()):
						t_final_res.append(SympyStrictLessThan(
								self.translateForInternal(tree.getChild(child-1)),
								self.translateForInternal(tree.getChild(child)), evaluate=False))
					return SympyAnd(*t_final_res, evaluate=False)
				else:
					return t_res

			elif tree.getType() == AST_RELATIONAL_GEQ:
				t_res = SympyGreaterThan(
						self.translateForInternal(tree.getChild(0)),
						self.translateForInternal(tree.getChild(1)), evaluate=False)

				if tree.getNumChildren() > 2:
					# Here the idea is to make a chain, like a>=b && b>=c, which should be equal to a>=b>=c
					t_final_res = [t_res]
					for child in range(2, tree.getNumChildren()):
						t_final_res.append(SympyGreaterThan(
								self.translateForInternal(tree.getChild(child-1)),
								self.translateForInternal(tree.getChild(child)), evaluate=False))
					return SympyAnd(*t_final_res, evaluate=False)
				else:
					return t_res

			elif tree.getType() == AST_RELATIONAL_LEQ:
				t_res = SympyLessThan(
						self.translateForInternal(tree.getChild(0)),
						self.translateForInternal(tree.getChild(1)), evaluate=False)

				if tree.getNumChildren() > 2:
					# Here the idea is to make a chain, like a<=b && b<=c, which should be equal to a<=b<=c
					t_final_res = [t_res]
					for child in range(2, tree.getNumChildren()):
						t_final_res.append(SympyLessThan(
								self.translateForInternal(tree.getChild(child-1)),
								self.translateForInternal(tree.getChild(child)), evaluate=False))
					return SympyAnd(*t_final_res, evaluate=False)
				else:
					return t_res

			else:
				raise SedmlMathException("SedmlMathReader : Unknown relational operator")

		elif tree.isLogical():

			if tree.getType() == AST_LOGICAL_AND:
				t_children = []
				for child in range(0, tree.getNumChildren()):
					t_children.append(self.translateForInternal(tree.getChild(child)))

				return SympyAnd(*t_children, evaluate=False)

			elif tree.getType() == AST_LOGICAL_OR:
				t_children = []
				for child in range(0, tree.getNumChildren()):
					t_children.append(self.translateForInternal(tree.getChild(child)))

				return SympyOr(*t_children, evaluate=False)

			elif tree.getType() == AST_LOGICAL_XOR:
				t_children = []
				for child in range(0, tree.getNumChildren()):
					t_children.append(self.translateForInternal(tree.getChild(child)))

				return SympyXor(*t_children, evaluate=False)

			elif tree.getType() == AST_LOGICAL_NOT:
				return SympyNot(self.translateForInternal(tree.getChild(0)), evaluate=False)

			else:
				raise SedmlMathException("SedmlMathReader : Unknown logical operator")

		else:
			raise SedmlMathException("SedmlMathReader : Unknown mathematical term : %s" % parseFormula(tree))
