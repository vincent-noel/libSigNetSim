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



from sympy import simplify, srepr
from libsignetsim.model.math.sympy_shortcuts import *

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathException import MathException, DelayNotImplemented

class CMathWriter(object):
	""" Class for handling math formulaes """

	MATH_ERR            =  -1

	MATH_SBML           =   0
	MATH_INTERNAL       =   1
	MATH_DEVINTERNAL    =   2
	MATH_C              =   3
	MATH_PRETTYPRINT    =   4

	MATH_FORMULA        =  20
	MATH_EQUATION       =  21
	MATH_VARIABLE       =  22
	MATH_KINETICLAW     =  23
	MATH_FUNCTION       =  24
	MATH_RATERULE       =  25
	MATH_EVENTASSIGNMENT=  26
	MATH_ASSIGNMENTRULE =  27
	MATH_ALGEBRAICRULE  =  28


	ZERO = SympyInteger(0)

	def __init__(self, model):
		""" Constructor """

		self.model = model

	def writeCCode(self, tree):

		math = self.translateForC(tree)
		if Settings.verbose >= 2:
			print("\n> writeCCode")
			print(">> input : %s" % srepr(tree))
			print(">> input simplified : %s" % str(tree))
			print(">> output : %s" % math)

		return math




	def translateVariableForC(self, variable, derivative=False):
		""" Translates a Sympy symbol in C """

		if str(variable) == "_time_":
			return "t"

		elif str(variable) == "_avogadro_":
			return "RT_NA"

		t_var = None

		if self.model.listOfVariables.containsSymbol(variable):
			t_var = self.model.listOfVariables.getBySymbol(variable)
		else:
			print("> Err : %s" % str(variable))

		t_pos = None
		if t_var.isDerivative():
			if derivative:
				c_var = "ydot"
			else:
				c_var = "y"

			t_pos = t_var.ind+1

		elif t_var.isAssignment():
			c_var = "ass"
			t_pos = t_var.ind+1

		elif t_var.isConstant():
			c_var = "cst"
			t_pos = t_var.ind+1

		elif t_var.isAlgebraic():
			if derivative:
				c_var = "ydot"
			else:
				c_var = "y"

			t_pos = self.model.nbOdes + t_var.ind+1

		else:
			raise MathException("Cannot determine the mathematical type of variable %s" % str(variable))

		return "Ith(%s,%s)" % (c_var, t_pos)


	def translateForC(self, tree):
		""" Translate a sympy tree into a C string """

		if isinstance(tree, int):
			return "RCONST(%d.0)" % tree

		elif isinstance(tree, float):
			t_string = "%.16g" % tree
			if "." not in t_string and "e" not in t_string:
				t_string += ".0"

			return "RCONST(%s)" % t_string

		elif tree.func == SympySymbol:
			return self.translateVariableForC(tree)

		elif tree.func == SympyDerivative:
			return self.translateVariableForC(tree.args[0], derivative=True)

		elif tree.func == SympyInteger:
			return "RCONST(%d.0)" % int(tree)

		elif tree.func == SympyFloat:
			t_string = "%.16g" % float(tree)
			if "." not in t_string and "e" not in t_string:
				t_string += ".0"

			return "RCONST(%s)" % t_string

		elif tree.func == SympyRational:
			return "(%s/%s)" % (self.translateForC(tree.p), self.translateForC(tree.q))

		elif tree.func == SympyNegOne:
			return "RCONST(-1.0)"

		elif tree.func == SympyOne:
			return "RCONST(1.0)"

		elif tree.func == SympyHalf:
			return "RCONST(0.5)"

		elif tree.func == SympyZero:
			return "RCONST(0.0)"

		elif tree == SympyPi:
			return "RT_PI"

		elif tree.func == SympyE or tree.func == SympyExp1:
			return "RT_E"

		elif tree == SympyInf:
			return "RT_INF"

		elif tree == -SympyInf:
			return "-RT_INF"

		elif tree == SympyNan:
			return "RT_NAN"

		elif tree == SympyTrue or tree == True:
			return "1"

		elif tree == SympyFalse or tree == False:
			return "0"

		elif tree.func == SympyMax:
			return "max(%s, %s)" % (
				self.translateForC(tree.args[0]),
				self.translateForC(tree.args[1])
			)


		elif tree.func == SympyAdd:

			t_add = "("
			for i_arg, arg in enumerate(tree.args):
				if i_arg > 0:
					t_add = t_add + " + "
				t_add = t_add + self.translateForC(arg)

			return t_add + ")"


		elif tree.func == SympyMul:

			if len(tree.args) == 2:
				if tree.args[0].func == SympyNegOne:
					return "-" + self.translateForC(tree.args[1])
				if tree.args[1].func == SympyNegOne:
					return "-" + self.translateForC(tree.args[0])


			started = False
			t_minus = ""
			t_mul = ""
			t_divider = ""
			for i_arg, arg in enumerate(tree.args):

				if arg.func == SympyNegOne:
					t_mul = "-" + t_mul

				elif arg.func == SympyPow and arg.args[1].func == SympyNegOne:
					if t_divider == "":
						t_divider = "%s" % self.translateForC(arg.args[0])
					else:
						t_divider += "*%s" % self.translateForC(arg.args[0])
				else:
					if started:
						t_mul += "*"

					started = True
					t_mul += self.translateForC(arg)

			if t_divider == "":
				return t_mul
			else:
				return t_minus + "(" + t_mul + "/(%s))" % t_divider

		# AST_FUNCTION_ABS
		elif tree.func == SympyAbs:
			return "rt_abs(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_QUOTIENT
		elif tree.func == SympyQuotient:
			return "((int) rt_floor(%s/%s))" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		# AST_FUNCTION_REM
		elif tree.func == SympyRem:
			return "((int) fmod(%s, %s))" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))


		# AST_FUNCTION_ARCCOS
		elif tree.func == SympyAcos:
			return "rt_acos(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCCOSH
		elif tree.func == SympyAcosh:
			return "rt_acosh(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCCOT
		elif tree.func == SympyAcot:
			return "rt_acot(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCCSC
		elif tree.func == SympyAcsc:
			return "rt_acsc(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCCOTH
		elif tree.func == SympyAcoth:
			return "rt_acoth(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCSIN
		elif tree.func == SympyAsec:
			return "rt_asec(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCSIN
		elif tree.func == SympyAsin:
			return "rt_asin(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCSINH
		elif tree.func == SympyAsinh:
			return "rt_asinh(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCTAN
		elif tree.func == SympyAtan:
			return "rt_atan(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_ARCTANH
		elif tree.func == SympyAtanh:
			return "rt_atanh(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_CEILING
		elif tree.func == SympyCeiling:
			return "rt_ceil(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_COS
		elif tree.func == SympyCos:
			return "rt_cos(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_COSH
		elif tree.func == SympyCosh:
			return "rt_cosh(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_COT
		elif tree.func == SympyCot:
			return "rt_cot(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_COTH
		elif tree.func == SympyCoth:
			return "rt_coth(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_CSC
		elif tree.func == SympyCsc:
			return "rt_csc(%s)" % self.translateForC(tree.args[0])
		# AST_FUNCTION_DELAY
		#TODO
		#SEE BELOW !
		# AST_FUNCTION_EXP
		elif tree.func == SympyExp:
			return "rt_exp(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_FACTORIAL
		elif tree.func == SympyFactorial:
			return "rt_factorial(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_FLOOR
		elif tree.func == SympyFloor:
			return "rt_floor(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_LOG
		elif tree.func == SympyLog:
			if len(tree.args) == 2:
				return "(rt_log(%s)/rt_log(%s))" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))
			else:
				return "rt_log(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_PIECEWISE
		elif tree.func == SympyPiecewise:
			(t_val, t_cond) = tree.args[0]
			line = "(%s?%s" % (self.translateForC(t_cond), self.translateForC(t_val))
			line_end = ")"

			for piece in range(1, len(tree.args)):
				(t_val, t_cond) = tree.args[piece]
				line = line + ":(%s?%s" % (self.translateForC(t_cond), self.translateForC(t_val))
				line_end = line_end + ")"

			line = line + ":(RCONST(0.0))" + line_end
			return line

		# AST_FUNCTION_PIECEWISE
		elif tree.func == SympyITE:
			t_cond = tree.args[0]
			t_val = tree.args[1]
			t_other_val = tree.args[2]
			line = "(%s?%s:%s)" % (self.translateForC(t_cond), self.translateForC(t_val), self.translateForC(t_other_val))

			return line

		# AST_FUNCTION_POWER
		elif tree.func == SympyPow:

			if len(tree.args) == 2 and tree.args[1].func == SympyNegOne:
				return "RCONST(1.0)/(%s)" % self.translateForC(tree.args[0])

			return "rt_pow(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		# AST_FUNCTION_ROOT
		elif tree.func == SympyRoot:
			return "rt_pow(%s,(RCONST(1.0)/%s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		# AST_FUNCTION_SEC
		elif tree.func == SympySec:
			return "rt_sec(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_SIN
		elif tree.func == SympySin:
			return "rt_sin(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_SINH
		elif tree.func == SympySinh:
			return "rt_sinh(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_TAN
		elif tree.func == SympyTan:
			return "rt_tan(%s)" % self.translateForC(tree.args[0])

		# AST_FUNCTION_TANH
		elif tree.func == SympyTanh:
			return "rt_tanh(%s)" % self.translateForC(tree.args[0])

		elif tree.func == SympyEqual:
			return "rt_eq(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		elif tree.func == SympyUnequal:
			return "rt_neq(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		elif tree.func == SympyGreaterThan:
			return "rt_geq(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		elif tree.func == SympyLessThan:
			return "rt_leq(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		elif tree.func == SympyStrictGreaterThan:
			return "rt_gt(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		elif tree.func == SympyStrictLessThan:
			return "rt_lt(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		elif tree.func == SympyAnd:
			t_args = "("
			for i_arg in range(0, len(tree.args)):
				if i_arg > 0:
					t_args = t_args + " && "
				t_args = t_args + self.translateForC(tree.args[i_arg])
			return t_args + ")"

		elif tree.func == SympyOr:
			t_args = "("
			for i_arg in range(0, len(tree.args)):
				if i_arg > 0:
					t_args = t_args + " || "
				t_args = t_args + self.translateForC(tree.args[i_arg])
			return t_args + ")"

		elif tree.func == SympyXor:
			return self.translateForC(simplify(tree))

		elif tree.func == SympyNot:
			return "(!%s)" % self.translateForC(tree.args[0])

		elif tree.func == SympyImplies:
			# p -> q == !p || q
			# print srepr(tree)
			# print tree.evalf()
			return "(!" + self.translateForC(tree.args[0]) + " || " + self.translateForC(tree.args[1]) + ")"

		elif tree.func == SympyUnevaluatedMin:
			if len(tree.args) == 1:
				return self.translateForC(tree.args[0])

			elif len(tree.args) > 1:
				str = "min(" + self.translateForC(tree.args[0]) + ", " + self.translateForC(tree.args[1]) + ")"

				for i, arg in enumerate(tree.args):
					if i > 1:
						str = "min(" + str + ", " + self.translateForC(tree.args[i]) + ")"
			return str

		elif tree.func == SympyUnevaluatedMax:
			if len(tree.args) == 1:
				return self.translateForC(tree.args[0])

			elif len(tree.args) > 1:
				str = "max(" + self.translateForC(tree.args[0]) + ", " + self.translateForC(tree.args[1]) + ")"

				for i, arg in enumerate(tree.args):
					if i > 1:
						str = "max(" + str + ", " + self.translateForC(tree.args[i]) + ")"
			return str


		elif tree.func == SympyFunction:
			raise DelayNotImplemented()

		else:
			raise MathException("C Math Writer : Unknown Sympy Symbol %s" % str(tree))
			return str(tree)
