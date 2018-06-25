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

from libsignetsim.model.sbml.Rule import Rule
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula

from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyEqual
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

class AlgebraicRule(Rule):
	""" Class for rate rules """

	def __init__ (self, model, objId):

		self.__model = model
		Rule.__init__(self, model, objId, Rule.RULE_ALGEBRAIC)
		self.__definition = MathFormula(model,
										MathFormula.MATH_ALGEBRAICRULE)


	def readSbml(self, sbml_rule,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		Rule.readSbml(self, sbml_rule, sbml_level, sbml_version)
		self.__definition.readSbml(sbml_rule.getMath(), sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		sbml_rule = sbml_model.createAlgebraicRule()
		Rule.writeSbml(self, sbml_rule, sbml_level, sbml_version)
		sbml_rule.setMath(self.__definition.getSbmlMathFormula(sbml_level,
																sbml_version))


	def copy(self, obj, symbols_subs={}):

		Rule.copy(self, obj)

		t_definition = unevaluatedSubs(obj.getDefinition().getInternalMathFormula(), symbols_subs)
		self.__definition.setInternalMathFormula(t_definition)

	def getRawDefinition(self, rawFormula=False):

		formula = self.__definition.getInternalMathFormula()
		if formula is not None and not rawFormula:
			subs = {}
			for species in self.__model.listOfSpecies:
				if species.isConcentration():
					subs.update({species.symbol.getInternalMathFormula(rawFormula=True): species.symbol.getInternalMathFormula()})
			formula = unevaluatedSubs(formula, subs)

		return formula


	def getDefinition(self, rawFormula=False):

		math_formula = MathFormula(self.__model)
		math_formula.setInternalMathFormula(self.getRawDefinition(rawFormula=rawFormula))

		return math_formula


	# def setDefinition(self, definition):
	# 	self.__definition = definition

	def setPrettyPrintDefinition(self, definition, rawFormula=False):
		self.__definition.setPrettyPrintMathFormula(definition, rawFormula=rawFormula)

	def getPrettyPrintDefinition(self):
		if self.__definition.getInternalMathFormula() is not None:
			return self.__definition.getPrettyPrintMathFormula()


	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		self.__definition.renameSbmlId(old_sbml_id, new_sbml_id)

	def containsVariable(self, variable):
		if self.__definition .getInternalMathFormula() is not None:
			return (variable.symbol.getInternalMathFormula() in self.__definition.getInternalMathFormula().atoms()
					or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.__definition.getInternalMathFormula().atoms()))
		else:
			return False

	def isValid(self):
		return (
			self.__definition.getInternalMathFormula() is not None
			and self.__definition.getDeveloppedInternalMathFormula() is not None
		)