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
from libsignetsim.model.math.SbmlMathReader import SbmlMathReader
from libsignetsim.cwriter.CMathWriter import CMathWriter
from libsignetsim.model.math.SbmlMathWriter import SbmlMathWriter
from libsignetsim.model.math.MathDevelopper import MathDevelopper
from libsignetsim.model.ModelException import SbmlException

from libsbml import parseL3Formula
from sympy import simplify

from MathDevelopper import unevaluatedSubs

class MathFormula(SbmlMathReader, CMathWriter, SbmlMathWriter, MathDevelopper):
	""" Class for handling math formulaes """

	MATH_ERR            =  -1

	MATH_SBML           =   0
	MATH_INTERNAL       =   1
	MATH_DEVINTERNAL    =   2
	MATH_C              =   3
	MATH_PRETTYPRINT    =   4
	MATH_FINALINTERNAL  =   5

	MATH_FORMULA        =  20
	MATH_EQUATION       =  21
	MATH_VARIABLE       =  22
	MATH_KINETICLAW     =  23
	MATH_FUNCTION       =  24
	MATH_RATERULE       =  25
	MATH_EVENTASSIGNMENT=  26
	MATH_ASSIGNMENTRULE =  27
	MATH_ALGEBRAICRULE  =  28
	MATH_VALUE          =  29
	MATH_RATIONAL       =  30
	MATH_ZERO           =  31

	ZERO                = SympyInteger(0)
	ONE                 = SympyInteger(1)

	t                   = SympySymbol("t")

	def __init__(self, model, typeOfFormula=MATH_FORMULA, isFromReaction=None):
		""" Constructor """

		self.__model = model
		SbmlMathReader.__init__(self, model)
		CMathWriter.__init__(self, model)
		SbmlMathWriter.__init__(self, model)
		MathDevelopper.__init__(self, model)

		self.typeOfFormula = typeOfFormula

		self.sbmlLevel = model.sbmlLevel
		self.sbmlVersion = model.sbmlVersion

		self.internalTree = None
		self.simplifiedInternalTree = None
		self.simplifiedInternalTree_v2 = None

		self.isFormula = (typeOfFormula == self.MATH_FORMULA)
		self.isEquation = (typeOfFormula == self.MATH_EQUATION)
		self.isVariable = (typeOfFormula == self.MATH_VARIABLE)
		self.isKineticLaw = (typeOfFormula == self.MATH_KINETICLAW)
		self.isFunctionDefinition = (typeOfFormula == self.MATH_FUNCTION)
		self.isRateRule = (typeOfFormula == self.MATH_RATERULE)
		self.isEventAssignment = (typeOfFormula == self.MATH_EVENTASSIGNMENT)
		self.isAssignmentRule = (typeOfFormula == self.MATH_ASSIGNMENTRULE)
		self.isAlgebraicRule = (typeOfFormula == self.MATH_ALGEBRAICRULE)

		if isFromReaction is not None:
			self.isFromReaction = isFromReaction.objId
		else:
			self.isFromReaction = None

		if self.isKineticLaw:
			self.internalTree = self.ONE

		if typeOfFormula == self.MATH_ZERO:
			self.internalTree = self.ZERO

	def getSbmlMathFormula(self, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		return MathFormula.getMathFormula(self, MathFormula.MATH_SBML, sbml_level, sbml_version)


	def getPrettyPrintMathFormula(self):

		t_math_formula = str(MathFormula.getInternalMathFormula(self))
		for species in self.__model.listOfSpecies.values():
			if species.isConcentration():
				t_math_formula = t_math_formula.replace(("_speciesForcedConcentration_%s_" % str(species.symbol.getInternalMathFormula())), species.getSbmlId())

		return t_math_formula


	def getInternalMathFormula(self):
		return MathFormula.getMathFormula(self, MathFormula.MATH_INTERNAL)


	def getDeveloppedInternalMathFormula(self):
		return MathFormula.getMathFormula(self, MathFormula.MATH_DEVINTERNAL)

	# def getFinalMathFormula(self, forcedConcentration=False):
	# 	return MathFormula.getMathFormula(self, MathFormula.MATH_FINALINTERNAL, forcedConcentration=forcedConcentration)

	def getCMathFormula(self):
		return MathFormula.getMathFormula(self, MathFormula.MATH_C)


	def getValueMathFormula(self):
		return float(MathFormula.getMathFormula(self, MathFormula.MATH_INTERNAL))


	def getMathFormula(self,
						math_type=MATH_DEVINTERNAL,
						sbml_level=Settings.defaultSbmlLevel,
						sbml_version=Settings.defaultSbmlVersion
	):

		if math_type == self.MATH_SBML:
			return self.writeSbml(sbml_level, sbml_version)

		elif math_type == self.MATH_INTERNAL:
			return self.internalTree

		elif math_type == self.MATH_PRETTYPRINT:
			pass

		elif math_type == self.MATH_DEVINTERNAL:
			return self.translateForDeveloppedInternal(MathFormula.getMathFormula(self, self.MATH_INTERNAL))

		# elif math_type == self.MATH_FINALINTERNAL:
		# 	# print self.getInternalMathFormula()
		# 	return self.translateForFinalInternal(MathFormula.getMathFormula(self, self.MATH_DEVINTERNAL), forcedConcentration)

		elif math_type == self.MATH_C:
			if MathFormula.getInternalMathFormula(self) is None:
				return "RCONST(0.0)"
			else:
				t_formula = MathFormula.getMathFormula(self, self.MATH_DEVINTERNAL)
				return self.writeCCode(t_formula)

		else:
			return "Unknown math type !"

	def setSbmlMathFormula(self, tree, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		self.setMathFormula(tree, self.MATH_SBML, sbml_level, sbml_version)

	def setInternalMathFormula(self, tree):
		self.setMathFormula(tree, self.MATH_INTERNAL)

	def setValueMathFormula(self, value):
		if isinstance(value, int):
			self.internalTree = SympyInteger(value)
		elif isinstance(value, float):
			self.internalTree = SympyFloat(value)
		else:
			self.internalTree = SympySymbol(value)

	# def setFinalMathFormula(self, tree):
	# 	self.setMathFormula(tree, math_type=self.MATH_FINALINTERNAL)

	def setPrettyPrintMathFormula(self, string, rawFormula=False):
		""" Sets the formula for substance. If forcedConcentration, the species are replaced by their concentration"""

		sbml_formula = parseL3Formula(str(string))
		if sbml_formula is None:
			raise SbmlException("MathFormula : Unable to parse math formula")

		self.readSbml(sbml_formula, self.sbmlLevel, self.sbmlVersion)
		if not rawFormula:
			t_subs_mask = {}
			for t_var in self.__model.listOfSpecies.values():
				if t_var.isConcentration():
					t_subs_mask.update({t_var.symbol.getInternalMathFormula():SympySymbol("_speciesForcedConcentration_%s_" % str(t_var.symbol.getInternalMathFormula()))})

			self.setInternalMathFormula(self.getInternalMathFormula().subs(t_subs_mask))


	def setMathFormula(self, tree, math_type=MATH_INTERNAL, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if math_type == self.MATH_INTERNAL:
			self.internalTree = tree
		elif math_type == self.MATH_FINALINTERNAL:
			self.internalTree = self.translateFinalForInternal(tree)


		elif math_type == self.MATH_SBML:
			self.internalTree = None
			self.readSbml(tree, sbml_level, sbml_version)


	def getMathFormulaDerivative(self, variable, mathType):
		if (mathType == self.MATH_DEVINTERNAL or mathType == self.MATH_INTERNAL):
			return self.generateDeveloppedInternalDerivative(self.getDeveloppedInternalMathFormula(), variable)

		elif mathType == self.MATH_C:
			t_derivative = self.generateDeveloppedInternalDerivative(self.getDeveloppedInternalMathFormula(), variable)
			return self.writeCCode(t_derivative)

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)
		old_symbol_concentration = SympySymbol("_speciesForcedConcentration_%s_" % old_sbml_id)


		if old_symbol in self.getInternalMathFormula().atoms():
			self.setInternalMathFormula(unevaluatedSubs(
				self.internalTree,
				{old_symbol: SympySymbol(new_sbml_id)}
			))

		if old_symbol_concentration in self.getInternalMathFormula().atoms():
			self.setInternalMathFormula(unevaluatedSubs(
				self.internalTree,
				{old_symbol_concentration: SympySymbol("_speciesForcedConcentration_%s_" % new_sbml_id)}
			))


	def subs(self, substitutions):
		self.internalTree = self.internalTree.subs(substitutions)

	def simpleSubsDevelopped(self, substitutions):
		# print ">> simple subs : " + str(self.getDeveloppedInternalMathFormula())
		return unevaluatedSubs(self.getDeveloppedInternalMathFormula(), substitutions)


	def isOne(self):

		return (self.getMathFormula(self.MATH_DEVINTERNAL) == SympyOne
				or self.getMathFormula(self.MATH_DEVINTERNAL) == SympyInteger(1)
				or self.getMathFormula(self.MATH_DEVINTERNAL) == SympyFloat(1.0))

	def isEqual(self, string):

		return self.getInternalMathFormula() == SbmlMathReader.readSbml(self, parseL3Formula(str(string)), self.sbmlLevel, self.sbmlVersion)
