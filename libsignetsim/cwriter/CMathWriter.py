#!/usr/bin/env python
""" CMathWriter.py


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

from sympy import simplify, srepr
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

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.ModelException import ModelException

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
			print "\n> writeCCode"
			print ">> input : %s" % srepr(tree)
			print ">> input simplified : %s" % str(tree)
			print ">> output : %s" % math

		return math




	def translateVariableForC(self, variable, derivative=False):
		""" Translates a Sympy symbol in C """

		#Input is a Sympy symbol, we need to convert to string
		variable = str(variable)

		# print variable
		if variable == "_time_":
			return "t"

		elif variable == "_avogadro_":
			return "rt_na"

		t_var = None

		if variable in self.model.listOfVariables.keys():
			t_var = self.model.listOfVariables[variable]
		else:
			print "> Err : %s" % str(variable)

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
			# print "No clue what this variable is : %s" % t_var.getSbmlId()
			c_var = "err"


		# print "Variable %s : %s,%s" % (t_var.getSbmlId(), c_var, t_pos)
		return "Ith(%s,%s)" % (c_var, t_pos)


	def translateForC(self, tree):
		""" Translate a sympy tree into a C string """

		if isinstance(tree, int):
			return "RCONST(%d.0)" % tree

		elif isinstance(tree, float):
			t_string = "%.15g" % tree
			if "." not in t_string and "e" not in t_string:
				t_string += ".0"
			return "RCONST(%s)" % t_string
		elif tree.func == SympySymbol:
			return self.translateVariableForC(str(tree))

		elif isinstance(tree.func, SympyUndefinedFunction) and tree.args == (SympySymbol("t"),) and str(tree.func) in self.model.listOfVariables.keys():
			return self.translateVariableForC(str(tree.func))

		elif tree.func == SympyDerivative:
			# print tree.args[0]
			# print str(tree.args[0])
			return self.translateVariableForC(str(tree.args[0]),derivative=True)

		elif tree.func == SympyInteger:
			return "RCONST(%d.0)" % int(tree)

		elif tree.func == SympyFloat:
			t_string = "%.15g" % float(tree)
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
			return "rt_pi"

		elif tree.func == SympyE or tree.func == SympyExp1:
			return "rt_e"

		elif tree == SympyInf:
			return "rt_inf"

		elif tree == -SympyInf:
			return "-rt_inf"

		elif tree == SympyNan:
			return "rt_nan"

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
			t_mul = ""
			t_divider = ""
			for i_arg, arg in enumerate(tree.args):

				if arg.func == SympyNegOne:
					t_mul = "-" + t_mul

				elif arg.func == SympyPow and arg.args[1].func == SympyNegOne:
					if t_divider == "":
						t_divider = "(%s)" % self.translateForC(arg.args[0])
					else:
						t_divider += "*(%s)" % self.translateForC(arg.args[0])
				else:
					if started:
						t_mul += "*"

					started = True
					t_mul += self.translateForC(arg)

			if t_divider == "":
				return t_mul
			else:
				return t_mul + "/(%s)" % t_divider

		# AST_FUNCTION_ABS
		elif tree.func == SympyAbs:
			return "rt_abs(%s)" % self.translateForC(tree.args[0])

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
			return "((realtype) rt_factorial(%s))" % self.translateForC(tree.args[0])

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
			# print line
			return line

		# AST_FUNCTION_POWER
		elif tree.func == SympyPow:

			if len(tree.args) == 2 and tree.args[1].func == SympyNegOne:
				return "RCONST(1.0)/(%s)" % self.translateForC(tree.args[0])

			return "rt_pow(%s, %s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

		# AST_FUNCTION_ROOT
		elif tree.func == SympyRoot:
			return "rt_pow(%s,((realtype)1)/%s)" % (self.translateForC(tree.args[0]), self.translateForC(tree.args[1]))

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
			# t_args = "("
			#
			# for i_arg in range(0, min(2, len(tree.args))):
			#     if i_arg > 0:
			#         t_args = t_args + " && "
			#     t_args = t_args + "(!" + self.translateForC(tree.args[i_arg]) + ")"
			#
			# print t_args + ")"
			# if len(tree.args) > 2:
			#     for i_arg in range(2, len(tree.args)):
			#
			#         t_args = "(" + t_args + ") && (!" + self.translateForC(tree.args[i_arg]) + ")"
			# print t_args + ")"
			#
			# return t_args + ")"


		elif tree.func == SympyNot:
			return "(!%s)" % self.translateForC(tree.args[0])

		elif tree.func == SympyFunction:
			#TODO
			#This case *should* only be used by the delay function. And right now, we just return the variable
			#ie : It's not working !!!
			return self.translateForC(tree.args[0])
		else:
			print str(tree)
			raise ModelException(ModelException.MATH_ERROR, "")
			return str(tree)
