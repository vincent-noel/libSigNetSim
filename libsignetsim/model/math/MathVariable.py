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


from six import string_types
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs


class MathVariable(object):

	# C code variable type
	VAR_ODE = 0
	VAR_ASS = 1
	VAR_CST = 2
	VAR_DAE = 3

	def __init__(self, model, is_from_reaction=None):

		self.__model = model

		self.type = None
		self.ind = None

		self.symbol = MathSymbol(self.__model, self, is_from_reaction)

		self.value = MathFormula(self.__model)
		self.derivative_value = MathFormula(self.__model)

		self.isInitialized = False
		self.isDerivativeInitialized = False
		self.constant = None
		self.boundaryCondition = False
		self.is_in_dae = None
		self.isFromReaction = is_from_reaction

		self.mathVariable = False
		# self.mathIsConcentration = None
		# self.mathCompartment = None

	def new(self, string=None):

		if self.isFromReaction is not None:
			self.symbol.setInternalMathFormula(SympySymbol("_local_%d_%s" % (self.isFromReaction.objId, self.getSbmlId())))
		else:
			self.symbol.setInternalMathFormula(SympySymbol(self.getSbmlId()))

		self.setValue(0)
		self.setDerivativeValue(0)

	def copy(self, obj, symbols_subs={}, conversion_factor=None, pure_math_variable=False):

		if obj.symbol.getSymbol() in list(symbols_subs.keys()):
			self.symbol.setInternalMathFormula(symbols_subs[obj.symbol.getSymbol()])
		else:
			self.symbol.setInternalMathFormula(obj.symbol.getSymbol())

		# self.symbol.setInternalMathFormula(SympySymbol(prefix + str(obj.symbol.getSymbol())))

		if obj.value is not None and obj.value.getInternalMathFormula() is not None:
			t_formula = unevaluatedSubs(obj.value.getInternalMathFormula(), symbols_subs)
			# t_formula = unevaluatedSubs(t_formula, replacements)

			if conversion_factor is not None:
				t_formula *= conversion_factor
			self.value.setInternalMathFormula(t_formula)

		if obj.derivative_value is not None and obj.derivative_value.getInternalMathFormula() is not None:
			t_formula = unevaluatedSubs(obj.derivative_value.getInternalMathFormula(), symbols_subs)
			# t_formula = unevaluatedSubs(t_formula, replacements)

			if conversion_factor is not None:
				t_formula *= conversion_factor

			self.derivative_value.setInternalMathFormula(t_formula)

		self.isInitialized = obj.isInitialized
		self.isDerivativeInitialized = obj.isDerivativeInitialized
		self.constant = obj.constant
		self.is_in_dae = obj.is_in_dae
		self.boundaryCondition = obj.boundaryCondition
		self.ind = obj.ind
		self.type = obj.type

		if pure_math_variable:
			self.mathVariable = True
		# 	if not obj.mathVariable:
		# 		if obj.isSpecies() and obj.isConcentration():
		# 			self.mathIsConcentration = True
		# 			self.mathCompartment = obj.getCompartment().symbol.getInternalMathFormula()
		# 	else:
		# 		self.mathIsConcentration = obj.mathIsConcentration
		# 		self.mathCompartment = obj.mathCompartment

	def readSbml(self, sbml_variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		self.readSbmlVariable(sbml_variable, sbml_level, sbml_version)


	def writeSbml(self, sbml_variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		self.writeSbmlVariable(sbml_variable, sbml_level, sbml_version)

	def getValue(self):
		if self.isInitialized:
			return self.value.getValueMathFormula()

	def setValue(self, value):
		if value is None:
			self.isInitialized = False
			self.value.setInternalMathFormula(None)

		elif isinstance(value, int) or isinstance(value, float):
			self.isInitialized = True
			self.value.setValueMathFormula(value)

		elif isinstance(value, string_types):
			self.isInitialized = True
			self.value.setPrettyPrintMathFormula(value)

	def setDerivativeValue(self, value):
		if isinstance(value, int) or isinstance(value, float):
			self.derivative_value.setValueMathFormula(value)

	def getSbmlValue(self, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		return self.value.getSbmlMathFormula(sbml_level, sbml_version)

	def setSbmlValue(self, sbml_value, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		return self.value.setSbmlMathFormula(sbml_value, sbml_level, sbml_version)


	def getSbmlSymbol(self, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		return self.symbol.getSbmlMathFormula(sbml_level, sbml_version)

	def getCValue(self):

		if (self.isSpecies() and (self.isConcentration() or self.isDeclaredConcentration)) or self.isReaction():
			return "RCONST(0.0)"

		elif self.value.getInternalMathFormula() is None:
			if self.isCompartment() or self.isParameter():
				return "RCONST(1.0)"
			else:
				return "RCONST(0.0)"

		return self.value.getCMathFormula()


	def getDerivativeCValue(self):

		if (self.isSpecies() and self.isDeclaredConcentration) or self.isReaction() or self.derivative_value.getInternalMathFormula() is None:
			return "RCONST(0.0)"

		return self.derivative_value.getCMathFormula()


	def isDerivative(self):
		return self.type == self.VAR_ODE


	def isAssignment(self):
		return self.type == self.VAR_ASS


	def isConstant(self):
		return self.type == self.VAR_CST

	def isAlgebraic(self):
		return self.type == self.VAR_DAE


	def getPos(self):

		if self.type == self.VAR_ODE:
			return self.ind

		elif self.type == self.VAR_DAE:
			return self.__model.nbOdes + self.ind
		elif self.type == self.VAR_ASS:
			return self.__model.nbOdes + self.__model.nbAlgebraics + self.ind

		elif self.type == self.VAR_CST:
			return self.__model.nbOdes + self.__model.nbAlgebraics + self.__model.nbAssignments + self.ind


	# def getODE(self, including_fast_reactions=None, math_type=MathFormula.MATH_INTERNAL, forcedConcentration=False, symbols=False, rawFormula=True):
	#
	# 	if self.isRateRuled():
	# 		return self.isRuledBy().getDefinition(forcedConcentration).getMathFormula(math_type)
	#
	# 	else:
	# 		return MathFormula.ZERO
	#
	# def getODE(self, including_fast_reactions=True, forcedConcentration=False):
	#
	# 	if self.isRateRuled():
	# 		return self.isRuledBy().getDefinition(forcedConcentration)
	#
	# 	else:
	# 		t_formula = MathFormula(self.__model)
	# 		t_formula.setInternalMathFormula(MathFormula.ZERO)
	# 		return t_formula


	def getODE(self, including_fast_reactions=True, rawFormula=False):

		if self.isRateRuled() and self.isRuledBy().isValid():
			return self.isRuledBy().getDefinition(rawFormula=rawFormula)

		else:
			t_formula = MathFormula(self.__model)
			t_formula.setInternalMathFormula(MathFormula.ZERO)
			return t_formula

	def setSbmlId(self, sbml_id, prefix=""):
		self.symbol.setValueMathFormula(prefix+sbml_id)

	def renameSymbol(self, old_sbml_id, new_sbml_id):
		self.symbol.renameSbmlId(old_sbml_id, new_sbml_id)

	def renameSbmlIdInValue(self, old_sbml_id, new_sbml_id):
		self.value.renameSbmlId(old_sbml_id, new_sbml_id)

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		self.value.renameSbmlId(old_sbml_id, new_sbml_id)
		self.symbol.renameSbmlId(old_sbml_id, new_sbml_id)

	def isInRules(self):
		return self.__model.listOfRules.containsVariable(self)

	def isInReactionsRates(self):
		return self.__model.listOfReactions.containsVariable(self)

	def isConcentration(self):
		""" There *IS* a case where a species doesn't have compartment I guess,
			so we actually need to check before looking at the spatialDimensions
		"""

		return (not self.mathVariable and self.isSpecies()
				and (self.getCompartment() is not None and not self.getCompartment().spatialDimensions == 0)
				and not self.hasOnlySubstanceUnits)

	def getSymbol(self):

		return self.symbol

	def getSymbolStr(self):

		return self.symbol.getSymbol().name