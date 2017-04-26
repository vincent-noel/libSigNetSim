#!/usr/bin/env python
""" MathVariable.py


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


from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import SympySymbol


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

	def new(self, string=None):

		if self.isFromReaction is not None:
			self.symbol.setInternalMathFormula(SympySymbol("_local_%d_%s" % (self.isFromReaction.objId, self.getSbmlId())))
		else:
			self.symbol.setInternalMathFormula(SympySymbol(self.getSbmlId()))

		self.setValue(0)
		self.setDerivativeValue(0)

	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversion_factor=None):

		# self.symbol.setInternalMathFormula(SympySymbol(prefix + obj.getSbmlId()))
		self.symbol.setInternalMathFormula(SympySymbol(prefix + str(obj.symbol.getSymbol())))

		if obj.value is not None and obj.value.getInternalMathFormula() is not None:
			if conversion_factor is None:
				self.value.setInternalMathFormula(obj.value.getInternalMathFormula().subs(subs).subs(replacements))
			else:
				self.value.setInternalMathFormula(obj.value.getInternalMathFormula().subs(subs).subs(replacements)*conversion_factor)

		if obj.derivative_value is not None and obj.derivative_value.getInternalMathFormula() is not None:
			if conversion_factor is None:
				self.derivative_value.setInternalMathFormula(obj.derivative_value.getInternalMathFormula().subs(subs).subs(replacements))
			else:
				self.derivative_value.setInternalMathFormula(obj.derivative_value.getInternalMathFormula().subs(subs).subs(replacements)*conversion_factor)


		self.isInitialized = obj.isInitialized
		self.isDerivativeInitialized = obj.isDerivativeInitialized
		self.constant = obj.constant
		self.is_in_dae = obj.is_in_dae
		self.boundaryCondition = obj.boundaryCondition
		self.ind = obj.ind
		self.type = obj.type

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

		else:
			if isinstance(value, int) or isinstance(value, float):
				self.isInitialized = True
				self.value.setValueMathFormula(value)
			elif isinstance(value, str):
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

		if self.isRateRuled():
			return self.isRuledBy().getDefinition(rawFormula=rawFormula)

		else:
			t_formula = MathFormula(self.__model)
			t_formula.setInternalMathFormula(MathFormula.ZERO)
			return t_formula

	def setSbmlId(self, sbml_id, prefix=""):
		self.symbol.setValueMathFormula(prefix+sbml_id)

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		self.value.renameSbmlId(old_sbml_id, new_sbml_id)

	def isInRules(self):
		return self.__model.listOfRules.containsVariable(self)

	def isInReactionsRates(self):
		return self.__model.listOfReactions.containsVariable(self)

	def isConcentration(self):
		""" There *IS* a case where a species doesn't have compartment I guess,
			so we actually need to check before looking at the spatialDimensions
		"""

		return (self.isSpecies()
				and (self.getCompartment() is not None and not self.getCompartment().spatialDimensions == 0)
				and not self.hasOnlySubstanceUnits)

	def getInitialValue(self, math_type=MathFormula.MATH_INTERNAL):
		# Getting value
		if self.hasInitialAssignment():
			tt_value = self.hasInitialAssignmentBy().getExpressionMath().getMathFormula(math_type)

			for tt_species in self.listOfSpecies.values():
				ttt_symbol = tt_species.symbol.getMathFormula(math_type)
				ttt_value = tt_species.value.getMathFormula(math_type)
				if ttt_symbol in tt_value.atoms(SympySymbol) and ttt_value is not None:
					tt_value = tt_value.subs(ttt_symbol, ttt_value)

			if self.isConcentration():
				tt_value /= self.getCompartment().symbol.getMathFormula(math_type)

			if SympySymbol("_time_") in tt_value.atoms():
				tt_value = tt_value.subs(SympySymbol("_time_"), 0)

		elif self.value.getFinalMathFormula() is not None:
			tt_value =  self.getMathValue().getMathFormula(math_type)
			if self.isConcentration():
				tt_value /= self.getCompartment().symbol.getMathFormula(math_type)
