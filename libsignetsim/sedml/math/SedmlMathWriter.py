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
from __future__ import absolute_import

# from builtins import str


from libsignetsim.settings.Settings import Settings
from libsignetsim.sedml.SedmlException import SedmlMathException
import libsbml
# token: cn , ci , csymbol , sep
from libsedml import AST_NAME, AST_NAME_TIME, AST_INTEGER, AST_REAL
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
	AST_PLUS, AST_MINUS, AST_TIMES, AST_DIVIDE, AST_FUNCTION_POWER, AST_FUNCTION_ROOT, AST_FUNCTION_ABS, AST_FUNCTION_EXP,
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
from libsedml import (AST_FUNCTION_SINH, AST_FUNCTION_COSH, AST_FUNCTION_TANH, AST_FUNCTION_COTH)
from .sympy_shortcuts import (SympySinh, SympyCosh, SympyTanh, SympyCoth)

# trigonometric operators: arcsin , arccos , arctan , arcsec , arccsc , arccot
from libsedml import (
	AST_FUNCTION_ARCSIN, AST_FUNCTION_ARCCOS, AST_FUNCTION_ARCTAN,
	AST_FUNCTION_ARCSEC, AST_FUNCTION_ARCCSC, AST_FUNCTION_ARCCOT
)
from .sympy_shortcuts import (SympyAsin, SympyAcos, SympyAtan, SympyAsec, SympyAcsc, SympyAcot)

# trigonometric operators: arcsinh , arccosh , arctanh , arcsech , arccsch , arccoth
from libsedml import (
	AST_FUNCTION_ARCSINH, AST_FUNCTION_ARCCOSH, AST_FUNCTION_ARCTANH,
	AST_FUNCTION_ARCSECH, AST_FUNCTION_ARCCSCH, AST_FUNCTION_ARCCOTH
)
from .sympy_shortcuts import (SympyAsinh, SympyAcosh, SympyAtanh, SympyAcoth)

from .sympy_shortcuts import (SympyUndefinedFunction)
# constants: true , false , notanumber , pi , infinity , exponentiale
# TODO : Infinity, NaN
from libsedml import (AST_CONSTANT_TRUE, AST_CONSTANT_FALSE, AST_CONSTANT_PI, AST_CONSTANT_E)
from .sympy_shortcuts import (
	SympyTrue, SympyFalse, SympyPi, SympyE, SympyExp1, SympyInf, SympyNan, SympyOne, SympyNegOne, SympyHalf, SympyZero
)
# import libsbml
from libsedml import ASTNode, parseFormula, formulaToString
from six.moves import reload_module
reload_module(libsbml)


class SedmlMathWriter(object):
	""" Class for handling math formulaes """

	def __init__(self, document):
		""" Constructor """

		self.__document = document

	def translateForSedml(self, tree, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		""" Translate a sympy tree into a C string """

		if tree.func == SympySymbol:
			# if str(tree) == '_time_':
			# 	t_ast = ASTNode()
			# 	t_ast.setType(AST_NAME_TIME)
			# 	t_ast.setName("time")
			# 	return t_ast
			#
			# else:
			t_ast = ASTNode()
			t_ast.setType(AST_NAME)
			t_ast.setName(tree.name)
			return t_ast

		elif tree.func == SympyInteger:
			t_ast = ASTNode()
			t_ast.setType(AST_INTEGER)
			t_ast.setValue(int(tree))
			return t_ast

		elif tree.func == SympyFloat:
			t_ast = ASTNode()
			t_ast.setType(AST_REAL)
			t_ast.setValue(float(tree))
			return t_ast

		elif tree.func == SympyNegOne:
			t_ast = ASTNode()
			t_ast.setType(AST_INTEGER)
			t_ast.setValue(-1)
			return t_ast

		elif tree.func == SympyOne:
			t_ast = ASTNode()
			t_ast.setType(AST_INTEGER)
			t_ast.setValue(1)
			return t_ast

		elif tree.func == SympyHalf:
			t_ast = ASTNode()
			t_ast.setType(AST_REAL)
			t_ast.setValue(0.5)
			return t_ast

		elif tree.func == SympyZero:
			t_ast = ASTNode()
			t_ast.setType(AST_INTEGER)
			t_ast.setValue(0)
			return t_ast

		elif tree == SympyPi:
			t_ast = ASTNode()
			t_ast.setType(AST_CONSTANT_PI)
			return t_ast

		elif tree.func == SympyE or tree.func == SympyExp1:
			t_ast = ASTNode()
			t_ast.setType(AST_CONSTANT_E)
			return t_ast

		elif tree == SympyInf:
			t_ast = ASTNode()
			t_ast.setType(AST_REAL)
			t_ast.setValue(float("inf"))
			return t_ast

		elif tree == -SympyInf:
			t_ast = ASTNode()
			t_ast.setType(AST_REAL)
			t_ast.setValue(float("-inf"))
			return t_ast

		elif tree == SympyNan:
			t_ast = ASTNode()
			t_ast.setType(AST_REAL)
			t_ast.setValue(float("nan"))
			return t_ast

		elif tree == SympyTrue or tree == True:
			t_ast = ASTNode()
			t_ast.setType(AST_CONSTANT_TRUE)
			return t_ast

		elif tree == SympyFalse or tree == False:
			t_ast = ASTNode()
			t_ast.setType(AST_CONSTANT_FALSE)
			return t_ast

		elif tree.func == SympyAdd:

			t_ast = ASTNode()
			t_ast.setType(AST_PLUS)
			for i_arg, arg in enumerate(tree.args):
				t_ast.addChild(self.translateForSedml(arg, level, version))

			return t_ast

		elif tree.func == SympyMul:

			if len(tree.args) == 2:
				if tree.args[0].func == SympyNegOne:
					t_ast = ASTNode()
					t_ast.setType(AST_MINUS)
					t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
					return t_ast

				if tree.args[1].func == SympyNegOne:
					t_ast = ASTNode()
					t_ast.setType(AST_MINUS)
					t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
					return t_ast

			t_ast = ASTNode()
			t_ast.setType(AST_TIMES)
			t_tree_denominator = None
			# t_tree_numerator = None
			# for i_arg, arg in enumerate(tree.args):
			# 	if arg.func == SympyPow and arg.args[1].func == SympyNegOne:
			#
			# 		if t_tree_denominator is None:
			# 			t_tree_denominator = self.translateForSedml(arg.args[0], level, version)
			# 		elif t_tree_denominator.getType() != AST_TIMES:
			# 			t_tree_denominator_new = ASTNode()
			# 			t_tree_denominator_new.setType(AST_TIMES)
			# 			t_tree_denominator_new.addChild(t_tree_denominator)
			# 			t_tree_denominator_new.addChild(self.translateForSedml(arg.args[0], level, version))
			# 			t_tree_denominator = t_tree_denominator_new
			# 		else:
			# 			t_tree_denominator.addChild(self.translateForSedml(arg.args[0], level, version))
			# 	else:
			# 		t_tree_numerator = self.translateForSedml(arg, level, version)
			# 		t_ast.addChild(t_tree_numerator)
			#
			# if t_tree_denominator is not None:
			# 	t_ast_2 = ASTNode()
			# 	t_ast_2.setType(AST_DIVIDE)
			# 	if t_ast.getNumChildren() == 1:
			# 		t_ast_2.addChild(t_tree_numerator)
			# 	else:
			# 		t_ast_2.addChild(t_ast)
			# 	t_ast_2.addChild(t_tree_denominator)
			# 	# print formulaToString(t_ast_2)
			# 	return t_ast_2
			# # print formulaToString(t_ast)
			# return t_ast
			t_tree_numerator = None
			for i_arg, arg in enumerate(tree.args):
				if arg.func == SympyPow and arg.args[1].func == SympyNegOne:

					if t_tree_denominator is None:
						t_tree_denominator = self.translateForSedml(arg.args[0], level, version)
					elif t_tree_denominator.getType() != AST_TIMES:
						t_tree_denominator_new = ASTNode()
						t_tree_denominator_new.setType(AST_TIMES)
						t_tree_denominator_new.addChild(t_tree_denominator)
						t_tree_denominator_new.addChild(self.translateForSedml(arg.args[0], level, version))
						t_tree_denominator = t_tree_denominator_new
					else:
						t_tree_denominator.addChild(self.translateForSedml(arg.args[0], level, version))
				else:
					t_tree_numerator = self.translateForSedml(arg, level, version)
					t_ast.addChild(self.translateForSedml(arg, level, version))
					# t_ast.addChild(self.translateForSedml(arg, level, version))

			if t_tree_denominator is not None:
				t_ast_2 = ASTNode()
				t_ast_2.setType(AST_DIVIDE)
				if t_ast.getNumChildren() == 1:
					t_ast_2.addChild(t_tree_numerator)
				else:
					t_ast_2.addChild(t_ast)
				t_ast_2.addChild(t_tree_denominator)
				# print formulaToString(t_ast_2)
				return t_ast_2
			# print formulaToString(t_ast)
			return t_ast


		# AST_FUNCTION_ABS
		elif tree.func == SympyAbs:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ABS)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCCOS
		elif tree.func == SympyAcos:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCCOS)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCCOSH
		elif tree.func == SympyAcosh:
			if tree.args[0].func == SympyPow and tree.args[0].args[1] == SympyInteger(-1):
				t_ast = ASTNode()
				t_ast.setType(AST_FUNCTION_ARCSECH)
				t_ast.addChild(self.translateForSedml(tree.args[0].args[0], level, version))
				return t_ast

			else:
				t_ast = ASTNode()
				t_ast.setType(AST_FUNCTION_ARCCOSH)
				t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
				return t_ast

		# AST_FUNCTION_ARCCOT
		elif tree.func == SympyAcot:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCCOT)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCCOTH
		elif tree.func == SympyAcoth:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCCOTH)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCSIN
		elif tree.func == SympyAsin:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCSIN)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCSINH
		elif tree.func == SympyAsinh:
			if tree.args[0].func == SympyPow and tree.args[0].args[1] == SympyInteger(-1):
				t_ast = ASTNode()
				t_ast.setType(AST_FUNCTION_ARCCSCH)
				t_ast.addChild(self.translateForSedml(tree.args[0].args[0], level, version))
				return t_ast
			else:
				t_ast = ASTNode()
				t_ast.setType(AST_FUNCTION_ARCSINH)
				t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
				return t_ast

		# AST_FUNCTION_ARCTAN
		elif tree.func == SympyAtan:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCTAN)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCTANH
		elif tree.func == SympyAtanh:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCTANH)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCSEC
		elif tree.func == SympyAsec:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCSEC)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_ARCCSC
		elif tree.func == SympyAcsc:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_ARCCSC)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_CEILING
		elif tree.func == SympyCeiling:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_CEILING)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_COS
		elif tree.func == SympyCos:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_COS)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_COSH
		elif tree.func == SympyCosh:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_COSH)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_COT
		elif tree.func == SympyCot:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_COT)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_COTH
		elif tree.func == SympyCoth:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_COTH)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_CSC
		elif tree.func == SympyCsc:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_CSC)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_DELAY
		# TODO
		#
		# AST_FUNCTION_EXP
		elif tree.func == SympyExp:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_EXP)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_FACTORIAL
		elif tree.func == SympyFactorial:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_FACTORIAL)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_FLOOR
		elif tree.func == SympyFloor:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_FLOOR)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_LOG
		#TODO
		elif tree.func == SympyLog:
			if len(tree.args) < 2:
				t_ast = ASTNode()
				t_ast.setType(AST_FUNCTION_LN)
				t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
				return t_ast

			else:
				if tree.args[1] == SympyInteger(10):
					t_ast = ASTNode()
					t_ast.setType(AST_FUNCTION_LOG)

					t_ast_2 = ASTNode()
					t_ast_2.setType(AST_INTEGER)
					t_ast_2.setValue(10)

					t_ast.addChild(t_ast_2)
					t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
					return t_ast
				else:
					t_ast = ASTNode()
					t_ast.setType(AST_FUNCTION_LOG)
					t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
					t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
					return t_ast

		# AST_FUNCTION_PIECEWISE
		elif tree.func == SympyPiecewise:

			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_PIECEWISE)

			(t_val, t_cond) = tree.args[0]

			t_ast.addChild(self.translateForSedml(t_val, level, version))
			t_ast.addChild(self.translateForSedml(t_cond, level, version))
			last_child = []
			for piece in range(1, len(tree.args)):
				(t_val, t_cond) = tree.args[piece]

				if piece == (len(tree.args)-1):
					t_ast.addChild(self.translateForSedml(t_val, level, version))
				else:
					t_ast.addChild(self.translateForSedml(t_val, level, version))
					t_ast.addChild(self.translateForSedml(t_cond, level, version))

			return t_ast

		elif tree.func == SympyITE:

			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_PIECEWISE)

			t_cond = tree.args[0]
			t_val = tree.args[1]
			t_val_else = tree.args[2]
			t_ast.addChild(self.translateForSedml(t_val, level, version))
			t_ast.addChild(self.translateForSedml(t_cond, level, version))
			t_ast.addChild(self.translateForSedml(t_val_else, level, version))
			return t_ast

		#TODO
		# AST_FUNCTION_POWER
		elif tree.func == SympyPow:

			# A standard 1/b division will be written mul(1, pow(b,-1))
			# We recognize it and write it as a division
			# Important to note that a/b is written mul(a, mul(1, pow(b,-1)))
			# so we don't need to look for a
			if tree.args[1].func == SympyNegOne:
				t_ast = ASTNode()
				t_ast.setType(AST_DIVIDE)

				t_ast_2 = ASTNode()
				t_ast_2.setType(AST_INTEGER)
				t_ast_2.setValue(1)

				t_ast.addChild(t_ast_2)
				t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
				return t_ast

			# Similar for SQRT(x), it's written pow(x, pow(2, -1))
			elif (
					tree.args[1].func == SympyPow
					and tree.args[1].args[0] == SympyInteger(2)
					and tree.args[1].args[1].func == SympyNegOne
			):
				t_ast = ASTNode()
				t_ast.setType(AST_FUNCTION_ROOT)

				t_ast_2 = ASTNode()
				t_ast_2.setType(AST_INTEGER)
				t_ast_2.setValue(2)

				t_ast.addChild(t_ast_2)
				t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
				return t_ast

			# print "\n"
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_POWER)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		# AST_FUNCTION_SEC
		elif tree.func == SympySec:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_SEC)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_SIN
		elif tree.func == SympySin:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_SIN)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_SINH
		elif tree.func == SympySinh:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_SINH)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_TAN
		elif tree.func == SympyTan:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_TAN)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast

		# AST_FUNCTION_TANH
		elif tree.func == SympyTanh:
			t_ast = ASTNode()
			t_ast.setType(AST_FUNCTION_TANH)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast






		elif tree.func == SympyEqual:
			t_ast = ASTNode()
			t_ast.setType(AST_RELATIONAL_EQ)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		elif tree.func == SympyUnequal:
			t_ast = ASTNode()
			t_ast.setType(AST_RELATIONAL_NEQ)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		elif tree.func == SympyGreaterThan:
			t_ast = ASTNode()
			t_ast.setType(AST_RELATIONAL_GEQ)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		elif tree.func == SympyLessThan:
			t_ast = ASTNode()
			t_ast.setType(AST_RELATIONAL_LEQ)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		elif tree.func == SympyStrictGreaterThan:
			t_ast = ASTNode()
			t_ast.setType(AST_RELATIONAL_GT)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		elif tree.func == SympyStrictLessThan:
			t_ast = ASTNode()
			t_ast.setType(AST_RELATIONAL_LT)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		elif tree.func == SympyAnd:
			t_ast = ASTNode()
			t_ast.setType(AST_LOGICAL_AND)
			for i_arg in range(0, len(tree.args)):
				t_ast.addChild(self.translateForSedml(tree.args[i_arg], level, version))
			return t_ast

		elif tree.func == SympyOr:
			t_ast = ASTNode()
			t_ast.setType(AST_LOGICAL_OR)
			for i_arg in range(0, len(tree.args)):
				t_ast.addChild(self.translateForSedml(tree.args[i_arg], level, version))
			return t_ast

		elif tree.func == SympyXor:
			t_ast = ASTNode()
			t_ast.setType(AST_LOGICAL_XOR)
			for i_arg in range(0, len(tree.args)):
				t_ast.addChild(self.translateForSedml(tree.args[i_arg], level, version))
			return t_ast

		elif tree.func == SympyNot:
			# print tree
			t_ast = ASTNode()
			t_ast.setType(AST_LOGICAL_NOT)
			t_ast.addChild(self.translateForSedml(tree.args[0], level, version))
			return t_ast
		elif tree.func == SympyLambda:
			t_ast = ASTNode()
			t_ast.setType(AST_LAMBDA)
			t_args = list(tree.args[0])
			for arg in t_args:
				t_ast.addChild(self.translateForSedml(arg, level, version))
			t_ast.addChild(self.translateForSedml(tree.args[1], level, version))
			return t_ast

		elif isinstance(tree.func, SympyUndefinedFunction):
			if str(tree.func) == "min":
				return parseFormula("min(" + formulaToString(self.translateForSedml(tree.args[0], level, version)) + ")")
			elif str(tree.func) == "max":
				return parseFormula("max(" + formulaToString(self.translateForSedml(tree.args[0], level, version)) + ")")
			elif str(tree.func) == "sum":
				return parseFormula("sum(" + formulaToString(self.translateForSedml(tree.args[0], level, version)) + ")")
			elif str(tree.func) == "product":
				return parseFormula("product(" + formulaToString(self.translateForSedml(tree.args[0], level, version)) + ")")
			else:
				raise SedmlMathException("SedmlMathWriter : Unknown Sympy Function %s" % str(tree.func))
		else:
			raise SedmlMathException("SedmlMathWriter : Unknown Sympy Symbol %s" % str(tree))
