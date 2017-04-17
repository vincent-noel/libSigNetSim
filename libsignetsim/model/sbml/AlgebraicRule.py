#!/usr/bin/env python
""" AlgebraicRule.py


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


from libsignetsim.model.sbml.Rule import Rule
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula

from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyEqual

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


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[],
				replacements={}, conversions={}, time_conversion=None):

		Rule.copy(self, obj, prefix, shift)
		t_definition = obj.getDefinition().getInternalMathFormula().subs(subs).subs(replacements)
		self.__definition.setInternalMathFormula(t_definition)

	def getRawDefinition(self, rawFormula=False):

		formula = self.__definition.getInternalMathFormula()
		if not rawFormula:
			subs = {}
			for species in self.__model.listOfSpecies.values():
				if species.isConcentration():
					subs.update({species.symbol.getInternalMathFormula(rawFormula=True): species.symbol.getInternalMathFormula()})
			formula = formula.subs(subs)

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
		return self.__definition.getPrettyPrintMathFormula()


	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)

		if old_symbol in self.__definition.getInternalMathFormula().atoms():
			t_definition = MathFormula(self.__model, MathFormula.MATH_ALGEBRAICRULE)
			t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula.subs(old_symbol, SympySymbol(new_sbml_id)))


	def containsVariable(self, variable):
		return (variable.symbol.getInternalMathFormula() in self.__definition.getInternalMathFormula().atoms()
				or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.__definition.getInternalMathFormula().atoms()))
