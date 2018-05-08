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
from __future__ import division

from libsignetsim.model.sbml.Rule import Rule
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsbml import SBML_SPECIES_CONCENTRATION_RULE,\
					SBML_PARAMETER_RULE,\
					SBML_COMPARTMENT_VOLUME_RULE

from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger, SympyMul, SympyPow
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs


class RateRule(Rule):
	""" Class for rate rules """

	def __init__ (self, model, obj_id):

		self.__model = model
		Rule.__init__(self, model, obj_id, Rule.RULE_RATE)

		self.__definition = MathFormula(model, MathFormula.MATH_RATERULE)
		self.__var = None

	def readSbml(self, rate_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		Rule.readSbml(self, rate_rule, sbml_level, sbml_version)

		if self.__model.listOfVariables.containsSbmlId(rate_rule.getVariable()):
			self.__var = self.__model.listOfVariables.getBySbmlId(rate_rule.getVariable())
			self.getVariable().setRuledBy(self)

		self.__definition.readSbml(rate_rule.getMath())

		if self.__definition.getInternalMathFormula() is not None:
			if self.getVariable().isConcentration():
				self.__definition.setInternalMathFormula(
						SympyMul(self.__definition.getInternalMathFormula(),
						self.getVariable().getCompartment().symbol.getInternalMathFormula()))

	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		rate_rule = sbml_model.createRateRule()
		if sbml_level < 2:

			if self.getVariable().isSpecies():
				rate_rule.setL1TypeCode(SBML_SPECIES_CONCENTRATION_RULE)
			elif self.getVariable().isParameter():
				rate_rule.setL1TypeCode(SBML_PARAMETER_RULE)
			elif self.getVariable().isCompartment():
				rate_rule.setL1TypeCode(SBML_COMPARTMENT_VOLUME_RULE)

		Rule.writeSbml(self, rate_rule, sbml_level, sbml_version)

		rate_rule.setVariable(self.__var.getSbmlId())

		if self.__definition.getInternalMathFormula() is not None:
			t_definition = MathFormula(self.__model, MathFormula.MATH_RATERULE)
			t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula())

			if self.getVariable().isConcentration():
				t_definition.setInternalMathFormula(
						SympyMul(t_definition.getInternalMathFormula(),
						SympyPow(self.getVariable().getCompartment().symbol.getInternalMathFormula(),
						SympyInteger(-1))))

			rate_rule.setMath(t_definition.getSbmlMathFormula(sbml_level, sbml_version))

	def copy(self, obj, sids_subs={}, symbols_subs={}, conversion_factors={}, time_conversion=None):

		Rule.copy(self, obj)

		if obj.getVariable().getSbmlId() in list(sids_subs.keys()):
			self.__var = self.__model.listOfVariables.getBySbmlId(sids_subs[obj.getVariable().getSbmlId()])
		else:
			self.__var = self.__model.listOfVariables.getBySbmlId(obj.getVariable().getSbmlId())

		self.getVariable().setRuledBy(self)

		if obj.getDefinition().getInternalMathFormula() is not None:
			t_convs = {}
			for var, conversion in list(conversion_factors.items()):
				t_convs.update({var: var/conversion})

			t_definition = unevaluatedSubs(obj.getDefinition().getInternalMathFormula(), symbols_subs)
			t_definition = unevaluatedSubs(t_definition, t_convs)

			t_var_symbol = unevaluatedSubs(obj.getVariable().symbol.getInternalMathFormula(), symbols_subs)

			if t_var_symbol in conversion_factors:
				t_definition *= conversion_factors[t_var_symbol]

			if time_conversion is not None:
				t_definition /= time_conversion.getInternalMathFormula()

			self.__definition.setInternalMathFormula(t_definition)

	def getVariable(self):
		return self.__var

	def setVariable(self, variable):

		if self.__var is not None:
			self.getVariable().unsetRuledBy()

		self.__var = variable
		self.getVariable().setRuledBy(self)

	def setPrettyPrintDefinition(self, definition, rawFormula=False):

		if self.getVariable().isConcentration() and not rawFormula:
			t_comp = self.getVariable().getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_RATERULE)
			t_math_formula.setPrettyPrintMathFormula(definition, rawFormula=rawFormula)
			self.__definition.setInternalMathFormula(
				t_math_formula.getInternalMathFormula()
				* t_comp.symbol.getInternalMathFormula())

		else:
			self.__definition.setPrettyPrintMathFormula(definition, rawFormula=rawFormula)

	def getPrettyPrintDefinition(self):

		if self.__definition.getInternalMathFormula() is not None:
			if self.getVariable().isConcentration():
				t_comp = self.getVariable().getCompartment()
				t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
				t_math_formula.setInternalMathFormula(
					self.__definition.getInternalMathFormula()/t_comp.symbol.getInternalMathFormula()
				)
				return t_math_formula.getPrettyPrintMathFormula()

			else:
				return self.__definition.getPrettyPrintMathFormula()

	def getRawDefinition(self, rawFormula=False):

		formula = self.__definition.getInternalMathFormula()

		if formula is not None:
			if self.getVariable().isConcentration() and not rawFormula:
				formula /= self.getVariable().getCompartment().symbol.getInternalMathFormula()

			if not rawFormula:
				subs = {}
				for species in self.__model.listOfSpecies:
					if species.isConcentration():
						subs.update({species.symbol.getInternalMathFormula(rawFormula=True): species.symbol.getInternalMathFormula()})
				formula = unevaluatedSubs(formula, subs)
		return formula

	def getDefinition(self, rawFormula=False):

		t_formula = MathFormula(self.__model, MathFormula.MATH_RATERULE)
		t_formula.setInternalMathFormula(self.getRawDefinition(rawFormula=rawFormula))
		return t_formula

	def setDefinition(self, definition):
		self.__definition = definition

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		self.__definition.renameSbmlId(old_sbml_id, new_sbml_id)

	def containsVariable(self, variable):
		if self.__definition.getInternalMathFormula() is not None:
			return (variable.symbol.getInternalMathFormula() in self.__definition.getInternalMathFormula().atoms()
					or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.__definition.getInternalMathFormula().atoms())
					or variable.symbol.getInternalMathFormula() == self.getVariable().symbol.getInternalMathFormula())
		else:
			return False

	def isValid(self):
		return (
			self.getVariable() is not None
			and self.__definition.getInternalMathFormula() is not None
			and self.__definition.getDeveloppedInternalMathFormula() is not None
		)