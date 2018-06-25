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
from six import string_types



from libsignetsim.model.math.sympy_shortcuts import *
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathException import MathException

import libsbml
from sympy import srepr
from re import match


class SbmlMathWriter(object):
	""" Class for handling math formulaes """

	def __init__(self, model):
		""" Constructor """

		self.model = model


	def writeSbml(self, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Export math formula to sbml """

		formula = self.translateForSbml(self.getInternalMathFormula(), sbml_level, sbml_version)
		if Settings.verbose >= 2:
			print("\n> writeSbml")
			print(">> input : %s" % srepr(self.getInternalMathFormula()))
			print(">> output : %s" % self.printSbml(formula, sbml_level, sbml_version))

		return formula

	def printSbml(self, formula, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if isinstance(formula, string_types):
			return formula
		elif isinstance(formula, libsbml.ASTNode):
			if sbml_level <= 2:
				return libsbml.formulaToString(formula)
			else:
				return libsbml.formulaToL3String(formula)
		else:
			return str(formula)

	def translateVariableForSbml(self, variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Translates a Sympy symbol in C """

		#Input is a Sympy symbol, we need to convert to string
		variable = str(variable)

		if variable == "_time_":
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_NAME_TIME)
			t_ast.setName("time")
			return t_ast

		elif variable == "_avogadro_":
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_NAME_AVOGADRO)
			return t_ast


		if variable.startswith("_speciesForcedConcentration_"):
			res_match = match(r"_speciesForcedConcentration_(.*)_", variable)
			t_sbml_id = str(res_match.groups()[0])
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_NAME)
			t_ast.setName(self.model.listOfSpecies.getBySbmlId(t_sbml_id).getSbmlId())
			return t_ast

		elif "_speciesForcedAmount_" in variable:
			res_match = match(r"_speciesForcedAmount_(\d+)_", variable)
			t_id = int(res_match.groups()[0])
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_NAME)
			t_ast.setName(self.model.listOfSpecies[t_id].getSbmlId())
			return t_ast

		elif "_local_" in variable:
			res_match = match(r"_local_(\d+)_(.*)", variable)
			t_rid = int(res_match.groups()[0])
			t_sbmlid = str(res_match.groups()[1])
			t_localparam = self.model.listOfReactions[t_rid].listOfLocalParameters.getBySbmlId(t_sbmlid)
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_NAME)
			t_ast.setName(t_localparam.getSbmlId())
			return t_ast

		elif "_functionDefinition_" in str(variable):
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION)

			res_match = match(r"_functionDefinition_(\d+)_", str(variable))
			t_id = int(res_match.groups()[0])

			t_ast.setName(self.model.listOfFunctionDefinitions[t_id].getSbmlId())
			return t_ast

		else:
			# print "translateVariableToSbml unknown variable type ! (%s)" % variable
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_NAME)
			t_ast.setName(variable)
			return t_ast


	def translateForSbml(self, tree, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Translate a sympy tree into a C string """

		# if isinstance(tree, int):
		# 	t_ast = libsbml.ASTNode()
		# 	t_ast.setType(libsbml.AST_INTEGER)
		# 	t_ast.setValue(tree)
		# 	return t_ast
		#
		# elif isinstance(tree, float):
		# 	t_ast = libsbml.ASTNode()
		# 	t_ast.setType(libsbml.AST_REAL)
		# 	t_ast.setValue(tree)
		# 	return t_ast

		# elif isinstance(tree, str):
		# 	return self.translateVariableForSbml(tree, sbml_level, sbml_version)

		if tree is None:
			return None

		elif tree.func == SympyTrue:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_CONSTANT_TRUE)
			return t_ast

		elif tree.func == SympyFalse:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_CONSTANT_FALSE)
			return t_ast

		elif tree.func == SympySymbol or tree.func == SympyDummy:
			return self.translateVariableForSbml(str(tree), sbml_level, sbml_version)

		# elif isinstance(tree.func, SympyUndefinedFunction) and tree.args == (SympySymbol("t"),) and str(tree.func) in self.model.listOfVariables.keys():
		# 	return self.translateVariableForSbml(str(tree.func), sbml_level, sbml_version)

		elif tree.func == SympyInteger:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_INTEGER)
			t_ast.setValue(int(tree))
			return t_ast

		elif tree.func == SympyFloat:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_REAL)
			t_ast.setValue(float(tree))
			return t_ast


		elif tree.func == SympyRational:
			# One of the values is a float...
			# The python libsbml doesn't seems to be implemented in that case.
			# Not sure if it's standard or not, but the test case exists... so
			if float(int(tree.p)) != float(tree.p) or float(int(tree.p)) != float(tree.p):
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_DIVIDE)
				t_ast.addChild(self.translateForSbml(tree.p, sbml_level, sbml_version))
				t_ast.addChild(self.translateForSbml(tree.q, sbml_level, sbml_version))
				return t_ast


			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_RATIONAL)
			t_ast.setValue(int(tree.p), int(tree.q))
			return t_ast

		elif tree.func == SympyNegOne:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_INTEGER)
			t_ast.setValue(-1)
			return t_ast

		elif tree.func == SympyOne:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_INTEGER)
			t_ast.setValue(1)
			return t_ast

		elif tree.func == SympyHalf:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_REAL)
			t_ast.setValue(0.5)
			return t_ast

		elif tree.func == SympyZero:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_INTEGER)
			t_ast.setValue(0)
			return t_ast

		elif tree == SympyPi:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_CONSTANT_PI)
			return t_ast

		elif tree.func == SympyE or tree.func == SympyExp1:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_CONSTANT_E)
			return t_ast

		elif tree == SympyInf:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_REAL)
			t_ast.setValue(float("inf"))
			return t_ast

		elif tree == -SympyInf:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_REAL)
			t_ast.setValue(float("-inf"))
			return t_ast

		elif tree == SympyNan:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_REAL)
			t_ast.setValue(float("nan"))
			return t_ast

		elif tree == SympyTrue or tree == True:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_CONSTANT_TRUE)
			return t_ast

		elif tree == SympyFalse or tree == False:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_CONSTANT_FALSE)
			return t_ast

		elif tree.func == SympyAdd:

			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_PLUS)
			for i_arg, arg in enumerate(tree.args):
				t_ast.addChild(self.translateForSbml(arg, sbml_level, sbml_version))

			return t_ast

		elif tree.func == SympyMul:

			if len(tree.args) == 2:
				if tree.args[0].func == SympyNegOne:
					t_ast = libsbml.ASTNode()
					t_ast.setType(libsbml.AST_MINUS)
					t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
					return t_ast

				if tree.args[1].func == SympyNegOne:
					t_ast = libsbml.ASTNode()
					t_ast.setType(libsbml.AST_MINUS)
					t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
					return t_ast

			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_TIMES)
			# t_ast_2 = None
			t_tree_denominator = None
			t_tree_numerator = None

			for i_arg, arg in enumerate(tree.args):
				if arg.func == SympyPow and arg.args[1].func == SympyNegOne:

					if t_tree_denominator is None:
						t_tree_denominator = self.translateForSbml(arg.args[0], sbml_level, sbml_version)
					elif t_tree_denominator.getType() != libsbml.AST_TIMES:
						t_tree_denominator_new = libsbml.ASTNode()
						t_tree_denominator_new.setType(libsbml.AST_TIMES)
						t_tree_denominator_new.addChild(t_tree_denominator)
						t_tree_denominator_new.addChild(self.translateForSbml(arg.args[0], sbml_level, sbml_version))
						t_tree_denominator = t_tree_denominator_new
					else:
						t_tree_denominator.addChild(self.translateForSbml(arg.args[0], sbml_level, sbml_version))
				else:
					t_tree_numerator = self.translateForSbml(arg, sbml_level, sbml_version)
					# t_ast.addChild(t_tree_numerator)
					t_ast.addChild(self.translateForSbml(arg, sbml_level, sbml_version))

			if t_tree_denominator is not None:
				t_ast_2 = libsbml.ASTNode()
				t_ast_2.setType(libsbml.AST_DIVIDE)
				if t_ast.getNumChildren() == 1:
					t_ast_2.addChild(t_tree_numerator)
				else:
					t_ast_2.addChild(t_ast)
				t_ast_2.addChild(t_tree_denominator)
				return t_ast_2

			return t_ast

		# rateOf
		elif tree.func == SympyRateOf:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_RATE_OF)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# quotient
		elif tree.func == SympyQuotient:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_QUOTIENT)
			# t_ast.setName("quotient")
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		# quotient
		elif tree.func == SympyRem:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_REM)
			# t_ast.setName("rem")
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		# implies
		elif tree.func == SympyImplies:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_LOGICAL_IMPLIES)
			# t_ast.setName("implies")
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		# min
		elif tree.func == SympyUnevaluatedMin:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_MIN)
			for i_arg, arg in enumerate(tree.args):
				t_ast.addChild(self.translateForSbml(arg, sbml_level, sbml_version))

			return t_ast

		# max
		elif tree.func == SympyUnevaluatedMax:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_MAX)
			for i_arg, arg in enumerate(tree.args):
				t_ast.addChild(self.translateForSbml(arg, sbml_level, sbml_version))

			return t_ast

		# AST_FUNCTION_ABS
		elif tree.func == SympyAbs:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ABS)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCCOS
		elif tree.func == SympyAcos:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCCOS)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCCOSH
		elif tree.func == SympyAcosh:
			if tree.args[0].func == SympyPow and tree.args[0].args[1] == SympyInteger(-1):
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_FUNCTION_ARCSECH)
				t_ast.addChild(self.translateForSbml(tree.args[0].args[0], sbml_level, sbml_version))
				return t_ast

			else:
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_FUNCTION_ARCCOSH)
				t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
				return t_ast

		# AST_FUNCTION_ARCCOT
		elif tree.func == SympyAcot:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCCOT)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCCOTH
		elif tree.func == SympyAcoth:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCCOTH)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCSIN
		elif tree.func == SympyAsin:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCSIN)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCSINH
		elif tree.func == SympyAsinh:
			if tree.args[0].func == SympyPow and tree.args[0].args[1] == SympyInteger(-1):
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_FUNCTION_ARCCSCH)
				t_ast.addChild(self.translateForSbml(tree.args[0].args[0], sbml_level, sbml_version))
				return t_ast
			else:
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_FUNCTION_ARCSINH)
				t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
				return t_ast

		# AST_FUNCTION_ARCTAN
		elif tree.func == SympyAtan:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCTAN)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCTANH
		elif tree.func == SympyAtanh:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCTANH)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCSEC
		elif tree.func == SympyAsec:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCSEC)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_ARCCSC
		elif tree.func == SympyAcsc:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_ARCCSC)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_CEILING
		elif tree.func == SympyCeiling:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_CEILING)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_COS
		elif tree.func == SympyCos:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_COS)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_COSH
		elif tree.func == SympyCosh:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_COSH)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_COT
		elif tree.func == SympyCot:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_COT)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_COTH
		elif tree.func == SympyCoth:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_COTH)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_CSC
		elif tree.func == SympyCsc:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_CSC)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_DELAY
		# TODO
		#
		# AST_FUNCTION_EXP
		elif tree.func == SympyExp:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_EXP)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_FACTORIAL
		elif tree.func == SympyFactorial:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_FACTORIAL)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_FLOOR
		elif tree.func == SympyFloor:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_FLOOR)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_LOG
		#TODO
		elif tree.func == SympyLog:
			if len(tree.args) < 2:
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_FUNCTION_LN)
				t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
				return t_ast

			else:
				if tree.args[1] == SympyInteger(10):
					t_ast = libsbml.ASTNode()
					t_ast.setType(libsbml.AST_FUNCTION_LOG)

					t_ast_2 = libsbml.ASTNode()
					t_ast_2.setType(libsbml.AST_INTEGER)
					t_ast_2.setValue(10)

					t_ast.addChild(t_ast_2)
					t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
					return t_ast
				else:
					t_ast = libsbml.ASTNode()
					t_ast.setType(libsbml.AST_FUNCTION_LOG)
					t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
					t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
					return t_ast

		# AST_FUNCTION_PIECEWISE
		elif tree.func == SympyPiecewise:

			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_PIECEWISE)

			(t_val, t_cond) = tree.args[0]

			t_ast.addChild(self.translateForSbml(t_val, sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(t_cond, sbml_level, sbml_version))
			last_child = []
			for piece in range(1, len(tree.args)):
				(t_val, t_cond) = tree.args[piece]

				if piece == (len(tree.args)-1):
					t_ast.addChild(self.translateForSbml(t_val, sbml_level, sbml_version))
				else:
					t_ast.addChild(self.translateForSbml(t_val, sbml_level, sbml_version))
					t_ast.addChild(self.translateForSbml(t_cond, sbml_level, sbml_version))

			return t_ast

		elif tree.func == SympyITE:

			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_PIECEWISE)

			t_cond = tree.args[0]
			t_val = tree.args[1]
			t_val_else = tree.args[2]
			t_ast.addChild(self.translateForSbml(t_val, sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(t_cond, sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(t_val_else, sbml_level, sbml_version))
			return t_ast

		#TODO
		# AST_FUNCTION_POWER
		elif tree.func == SympyPow:

			# A standard 1/b division will be written mul(1, pow(b,-1))
			# We recognize it and write it as a division
			# Important to note that a/b is written mul(a, mul(1, pow(b,-1)))
			# so we don't need to look for a
			if tree.args[1].func == SympyNegOne:
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_DIVIDE)

				t_ast_2 = libsbml.ASTNode()
				t_ast_2.setType(libsbml.AST_INTEGER)
				t_ast_2.setValue(1)

				t_ast.addChild(t_ast_2)
				t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
				return t_ast

			# Similar for SQRT(x), it's written pow(x, pow(2, -1))
			elif tree.args[1].func == SympyPow and tree.args[1].args[0] == SympyInteger(2) and tree.args[1].args[1].func == SympyNegOne:
				t_ast = libsbml.ASTNode()
				t_ast.setType(libsbml.AST_FUNCTION_ROOT)

				t_ast_2 = libsbml.ASTNode()
				t_ast_2.setType(libsbml.AST_INTEGER)
				t_ast_2.setValue(2)

				t_ast.addChild(t_ast_2)
				t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
				return t_ast

			# print "\n"
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_POWER)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		# #TODO
		# # AST_FUNCTION_ROOT
		# elif tree.func == SympyRoot:
		#     print "> Root case... Not done yet. Truth is I don't think it's used..."
		#     # t_ast = libsbml.ASTNode()
		#     # t_ast.setType(libsbml.AST_POWER)
		#     return "rt_pow(" + self.translateForSbml(tree.args[0], sbml_level, sbml_version) + ",((realtype)1)/" + self.translateForSbml(tree.args[1], sbml_level, sbml_version) + ")"

		# AST_FUNCTION_SEC
		elif tree.func == SympySec:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_SEC)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_SIN
		elif tree.func == SympySin:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_SIN)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_SINH
		elif tree.func == SympySinh:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_SINH)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_TAN
		elif tree.func == SympyTan:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_TAN)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		# AST_FUNCTION_TANH
		elif tree.func == SympyTanh:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION_TANH)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyEqual:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_RELATIONAL_EQ)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyUnequal:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_RELATIONAL_NEQ)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyGreaterThan:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_RELATIONAL_GEQ)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyLessThan:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_RELATIONAL_LEQ)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyStrictGreaterThan:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_RELATIONAL_GT)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyStrictLessThan:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_RELATIONAL_LT)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyAnd:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_LOGICAL_AND)
			for i_arg in range(0, len(tree.args)):
				t_ast.addChild(self.translateForSbml(tree.args[i_arg], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyOr:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_LOGICAL_OR)
			for i_arg in range(0, len(tree.args)):
				t_ast.addChild(self.translateForSbml(tree.args[i_arg], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyXor:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_LOGICAL_XOR)
			for i_arg in range(0, len(tree.args)):
				t_ast.addChild(self.translateForSbml(tree.args[i_arg], sbml_level, sbml_version))
			return t_ast

		elif tree.func == SympyNot:
			# print tree
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_LOGICAL_NOT)
			t_ast.addChild(self.translateForSbml(tree.args[0], sbml_level, sbml_version))
			return t_ast
		elif tree.func == SympyLambda or tree.func == SympyIdentityFunction:
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_LAMBDA)
			t_args = list(tree.args[0])
			for arg in t_args:
				t_ast.addChild(self.translateForSbml(arg, sbml_level, sbml_version))
			t_ast.addChild(self.translateForSbml(tree.args[1], sbml_level, sbml_version))
			return t_ast

		elif "_functionDefinition_" in str(tree.func):
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION)

			res_match = match(r"_functionDefinition_(\d+)_", str(tree.func))
			t_id = int(res_match.groups()[0])

			t_ast.setName(self.model.listOfFunctionDefinitions[t_id].getSbmlId())
			for i_arg in range(0, len(tree.args)):
				# print tree.args[i_arg]
				t_ast.addChild(self.translateForSbml(tree.args[i_arg], sbml_level, sbml_version))

			return t_ast

		elif "_functionDefinition_" in str(tree):
			t_ast = libsbml.ASTNode()
			t_ast.setType(libsbml.AST_FUNCTION)

			res_match = match(r"_functionDefinition_(\d+)_", str(tree))
			t_id = int(res_match.groups()[0])

			t_ast.setName(self.model.listOfFunctionDefinitions[t_id].getSbmlId())
			# for i_arg in range(0, len(tree.args)):
			# 	# print tree.args[i_arg]
			# 	t_ast.addChild(self.translateForSbml(tree.args[i_arg], sbml_level, sbml_version))

			return t_ast
		else:
			# print str(tree)
			raise MathException("Sbml Math Writer : Unknown Sympy Symbol %s" % str(tree))
			return str(tree)
