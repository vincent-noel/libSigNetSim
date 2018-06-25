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
from six import string_types
# from builtins import str

from libsignetsim.sedml.math.SedmlMathReader import SedmlMathReader
from libsignetsim.sedml.math.SedmlMathWriter import SedmlMathWriter
from libsignetsim.settings.Settings import Settings
from .sympy_shortcuts import (SympySymbol, SympyInteger, SympyFloat, SympyTrue, SympyFalse, SympyLambda)

import libsbml
from libsedml import formulaToString, ASTNode, parseFormula, parseL3Formula
from six.moves import reload_module
reload_module(libsbml)

from sympy import srepr
from numpy import sum, product

class MathFormula(SedmlMathReader, SedmlMathWriter):
	""" Class for handling math formulaes """

	MATH_SBML = 0
	MATH_INTERNAL = 1
	MATH_PRETTYPRINT = 2
	MATH_VALUE = 3

	ZERO                = SympyInteger(0)
	ONE                 = SympyInteger(1)
	t                   = SympySymbol("t")

	def __init__(self, document):
		""" Constructor """

		self.__document = document
		SedmlMathReader.__init__(self, document)
		SedmlMathWriter.__init__(self, document)

		self.level = None
		self.version = None
		self.internalTree = None

	def readSedml(self, formula, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		""" Import a math formula from sedml """
		# print ">> input : %s" % formulaToString(formula)

		self.level = level
		self.version = version
		if formula is not None:
			self.internalTree = SedmlMathReader.translateForInternal(self, formula)

			if Settings.verbose >= 2:
				print("\n> readSedml : ")
				print(">> input : %s" % self.printSbml(formula))
				print(">> output simplified : %s" % str(self.internalTree))
				print(">> output : %s" % srepr(self.internalTree))

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		""" Export math formula to sbml """

		if self.internalTree is not None:
			formula = SedmlMathWriter.translateForSedml(self, self.internalTree, level, version)

			if Settings.verbose >= 2:
				print("\n> writeSedml")
				print(">> input : %s" % srepr(self.internalTree))
				print(">> input simplified : %s" % str(self.internalTree))
				print(">> output : %s" % self.printSbml(formula, level, version))

			return formula



	def printSbml(self, formula, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if isinstance(formula, string_types):
			return formula
		elif isinstance(formula, ASTNode):# or isinstance(formula, ASTNodeSBML):
			return formulaToString(formula)
		else:
			return str(formula)

	def evaluateMathFormula(self, data, parameters):

		nb_timepoints = len(list(data.values())[0])
		return self.evaluate(self.internalTree, data, parameters, nb_timepoints)

	def evaluate(self, expr, data, parameters, nb_timepoints):
		# print "evaluating %s" % str(expr)

		if expr.func == SympyFloat:
			return [float(expr)]*nb_timepoints

		elif expr.func == SympyInteger:
			return [int(expr)]*nb_timepoints

		elif expr == SympyTrue:
			return [True]*nb_timepoints

		elif expr == SympyFalse:
			return [False]*nb_timepoints

		elif expr in list(data.keys()):
			return data[expr]

		elif expr in list(parameters.keys()):
			return [parameters[expr]]*nb_timepoints

		elif str(expr.func) in ["min", "max", "sum", "product"]:
			evaluated_arg = self.evaluate(expr.args[0], data, parameters, nb_timepoints)

			if str(expr.func) == "min":
				return [min(evaluated_arg)]*nb_timepoints
			elif str(expr.func) == "max":
				return [max(evaluated_arg)]*nb_timepoints
			elif str(expr.func) == "sum":
				return [sum(evaluated_arg)]*nb_timepoints
			elif str(expr.func) == "product":
				return [product(evaluated_arg)]*nb_timepoints

		else:

			evaluated_args = [self.evaluate(arg, data, parameters, nb_timepoints) for arg in expr.args]
			# print evaluated_args
			values = []
			for timepoint in range(nb_timepoints):
				evaluated_timepoint = (arg[timepoint] for arg in evaluated_args)
				# print list(evaluated_timepoint)
				values.append(expr.func(*evaluated_timepoint))

			return values


	#
	# def getSbmlMathFormula(self, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
	# 	return MathFormula.getMathFormula(self, MathFormula.MATH_SBML, sbml_level, sbml_version)
	#
	#
	def getPrettyPrint(self):
		return str(self.internalTree)
	#
	#
	def getInternalMathFormula(self):
		return MathFormula.getMathFormula(self, MathFormula.MATH_INTERNAL)
	#
	#
	# def getDeveloppedInternalMathFormula(self):
	# 	return MathFormula.getMathFormula(self, MathFormula.MATH_DEVINTERNAL)
	#
	#
	# def getValueMathFormula(self):
	# 	return float(MathFormula.getMathFormula(self, MathFormula.MATH_INTERNAL))
	#
	#
	def getMathFormula(self, math_type=MATH_INTERNAL):

		if math_type == self.MATH_SBML:
			pass
			# return self.writeSbml(sbml_level, sbml_version)

		elif math_type == self.MATH_INTERNAL:
			return self.internalTree

		elif math_type == self.MATH_PRETTYPRINT:
			pass

		else:
			return "Unknown math type !"

	def setSbmlMathFormula(self, tree, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		self.setMathFormula(tree, self.MATH_SBML, sbml_level, sbml_version)

	def setInternalMathFormula(self, tree):
		self.setMathFormula(tree, self.MATH_INTERNAL)
	#
	# def setValueMathFormula(self, value):
	# 	if isinstance(value, int):
	# 		self.internalTree = SympyInteger(value)
	# 	elif isinstance(value, float):
	# 		self.internalTree = SympyFloat(value)
	# 	else:
	# 		self.internalTree = SympySymbol(value)
	#
	# def setFinalMathFormula(self, tree):
	# 	self.setMathFormula(tree, math_type=self.MATH_FINALINTERNAL)
	#
	def setPrettyPrintMathFormula(self, string):

		try:
			sbml_formula = parseFormula(string)
			if sbml_formula is not None:
				self.readSedml(sbml_formula, self.level, self.version)
			else:
				sbml_formula = parseL3Formula(string)
				self.readSedml(sbml_formula, self.level, self.version)

		except:
			try:
				sbml_formula = parseL3Formula(string)
				self.readSedml(sbml_formula, self.level, self.version)

			except:
				raise Exception("MathFormula : Unable to parse math formula")



	def setMathFormula(self, tree, math_type=MATH_INTERNAL, sbml_level=Settings.defaultSedmlLevel, sbml_version=Settings.defaultSedmlVersion):

		if math_type == self.MATH_INTERNAL:
			self.internalTree = tree

		elif math_type == self.MATH_SBML:
			self.internalTree = None
			self.readSbml(tree, sbml_level, sbml_version)

		elif math_type == self.MATH_PRETTYPRINT:
			pass
	#
	#
	# def renameSbmlId(self, old_sbml_id, new_sbml_id):
	#
	# 	old_symbol = SympySymbol(old_sbml_id)
	# 	if old_symbol in self.getInternalMathFormula().atoms():
	# 		self.setInternalMathFormula(self.getInternalMathFormula().subs(old_symbol, SympySymbol(new_sbml_id)))
	#
	# def subs(self, substitutions):
	# 	self.internalTree = self.internalTree.subs(substitutions)
	#
	# def simpleSubs(self, substitutions):
	# 	return unevaluatedSubs(self.internalTree, substitutions)
	#
	#
	# def isOne(self):
	#
	# 	return (self.getMathFormula(self.MATH_DEVINTERNAL) == SympyOne
	# 			or self.getMathFormula(self.MATH_DEVINTERNAL) == SympyInteger(1)
	# 			or self.getMathFormula(self.MATH_DEVINTERNAL) == SympyFloat(1.0))
	#
	# def isEqual(self, string):
	#
	# 	return self.getInternalMathFormula() == SbmlMathReader.readSbml(self, parseL3Formula(str(string)), self.sbmlLevel, self.sbmlVersion)
