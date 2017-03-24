#!/usr/bin/env python
""" MathFormula.py


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

from libsignetsim.sedml.math.SedmlMathReader import SedmlMathReader
# from libsignetsim.sedml.math.SedmlMathWriter import SedmlMathWriter
from libsignetsim.settings.Settings import Settings

from libsignetsim.model.math.sympy_shortcuts import (SympySymbol, SympyInteger)

# from MathDevelopper import unevaluatedSubs
from libsedml import parseFormula
# from libsbml import parseL3Formula
from sympy import simplify


class MathFormula(SedmlMathReader):#, SedmlMathWriter):
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
		# SedmlMathWriter.__init__(self, document)

		self.level = None
		self.version = None
		self.internalTree = None

	def readSedml(self, formula, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		""" Import a math formula from sedml """

		self.level = level
		self.version = version
		self.internalTree = SedmlMathReader.translateForInternal(self, formula)

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		""" Export math formula to sbml """

		# formula = SedmlMathWriter.translateForSbml(self, self.internalTree, level, version)
		formula = parseFormula(str(self.internalTree))
		# if Settings.verbose >= 2:
		# 	print "\n> writeSbml"
		# 	print ">> input : %s" % srepr(self.getInternalMathFormula())
		# 	print ">> output : %s" % self.printSbml(formula, level, version)

		return formula
	#
	# def getSbmlMathFormula(self, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
	# 	return MathFormula.getMathFormula(self, MathFormula.MATH_SBML, sbml_level, sbml_version)
	#
	#
	# def getPrettyPrintMathFormula(self):
	#
	# 	t_math_formula = str(MathFormula.getInternalMathFormula(self))
	# 	for species in self.__model.listOfSpecies.values():
	# 		if species.isConcentration():
	# 			t_math_formula = t_math_formula.replace(
	# 				("_speciesForcedConcentration_%s_" % str(species.symbol.getInternalMathFormula())),
	# 				species.getSbmlId()
	# 			)
	#
	# 	return t_math_formula
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
	#
	# def setSbmlMathFormula(self, tree, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
	# 	self.setMathFormula(tree, self.MATH_SBML, sbml_level, sbml_version)
	#
	# def setInternalMathFormula(self, tree):
	# 	self.setMathFormula(tree, self.MATH_INTERNAL)
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
	# def setPrettyPrintMathFormula(self, string):
	#
	# 	sbml_formula = parseL3Formula(str(string))
	# 	if sbml_formula is None:
	# 		raise SbmlException("MathFormula : Unable to parse math formula")
	#
	# 	self.readSbml(sbml_formula, self.sbmlLevel, self.sbmlVersion)
	# 	t_subs_mask = {}
	# 	for t_var in self.__model.listOfSpecies.values():
	# 		if t_var.isConcentration():
	# 			t_subs_mask.update({t_var.symbol.getInternalMathFormula():SympySymbol("_speciesForcedConcentration_%s_" % str(t_var.symbol.getInternalMathFormula()))})
	#
	# 	self.setInternalMathFormula(self.getInternalMathFormula().subs(t_subs_mask))
	#
	#
	# def setMathFormula(self, tree, math_type=MATH_INTERNAL, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
	#
	# 	if math_type == self.MATH_INTERNAL:
	# 		self.internalTree = tree
	# 	elif math_type == self.MATH_FINALINTERNAL:
	# 		self.internalTree = self.translateFinalForInternal(tree)
	#
	#
	# 	elif math_type == self.MATH_SBML:
	# 		self.internalTree = None
	# 		self.readSbml(tree, sbml_level, sbml_version)
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
