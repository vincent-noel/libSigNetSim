#!/usr/bin/env python
""" RateRule.py


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
from libsignetsim.model.math.MathSymbol import MathSymbol
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
			self.__var = rate_rule.getVariable()
			self.getVariable().setRuledBy(self)


		self.__definition.readSbml(rate_rule.getMath())

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

		t_definition = MathFormula(self.__model, MathFormula.MATH_RATERULE)
		t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula())
		# t_variable = self.__var.symbol.getSbmlMathFormula(sbml_level, sbml_version).getName()

		if self.getVariable().isConcentration():
			t_definition.setInternalMathFormula(
					SympyMul(t_definition.getInternalMathFormula(),
					SympyPow(self.getVariable().getCompartment().symbol.getInternalMathFormula(),
					SympyInteger(-1))))

		rate_rule.setVariable(self.__var)
		rate_rule.setMath(t_definition.getSbmlMathFormula(sbml_level, sbml_version))

	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):

		Rule.copy(self, obj, prefix, shift, subs, deletions, conversions)

		t_symbol = SympySymbol(obj.getVariable().getSbmlId())
		if t_symbol in subs.keys():
			t_sbml_id = str(subs[t_symbol])
			tt_symbol = SympySymbol(t_sbml_id)

			if tt_symbol in replacements.keys():
				t_sbml_id = str(replacements[tt_symbol])
		else:
			t_sbml_id = prefix+obj.getVariable().getSbmlId()

		self.__var = t_sbml_id
		self.getVariable().setRuledBy(self)


		t_convs = {}
		for var, conversion in conversions.items():
			t_convs.update({var:var/conversion})

		t_var_symbol = unevaluatedSubs(obj.getVariable().symbol.getInternalMathFormula(), subs)
		t_var_symbol = unevaluatedSubs(t_var_symbol, replacements)

		t_definition = unevaluatedSubs(obj.getDefinition().getInternalMathFormula(), subs)
		t_definition = unevaluatedSubs(t_definition, replacements)
		t_definition = unevaluatedSubs(t_definition, t_convs)

		if t_var_symbol in conversions:
			t_definition *= conversions[t_var_symbol]

		if time_conversion is not None:
			t_definition /= time_conversion.getInternalMathFormula()

		self.__definition.setInternalMathFormula(t_definition)


	def getVariable(self):
		return self.__model.listOfVariables.getBySbmlId(self.__var)


	def setVariable(self, variable):

		if self.__var is not None:
			self.getVariable().unsetRuledBy()

		self.__var = variable.getSbmlId()
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


		if self.getVariable().isConcentration():
			t_comp = self.getVariable().getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
			t_math_formula.setInternalMathFormula(self.__definition.getInternalMathFormula()/t_comp.symbol.getInternalMathFormula())
			return t_math_formula.getPrettyPrintMathFormula()

		else:
			return self.__definition.getPrettyPrintMathFormula()


	def getRawDefinition(self, rawFormula=False):

		formula = self.__definition.getInternalMathFormula()

		if self.getVariable().isConcentration() and not rawFormula:
			formula /= self.getVariable().getCompartment().symbol.getInternalMathFormula()

		if not rawFormula:
			subs = {}
			for species in self.__model.listOfSpecies.values():
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
		# old_symbol = SympySymbol(old_sbml_id)
		#
		# if old_symbol in self.__definition.getInternalMathFormula().atoms():
		#
		# 	t_definition = unevaluatedSubs(
		# 		self.__definition.getInternalMathFormula(),
		# 		{old_symbol: SympySymbol(new_sbml_id)}
		# 	)
		#
		# 	self.__definition.setInternalMathFormula(t_definition)
		self.__definition.renameSbmlId(old_sbml_id, new_sbml_id)

	def containsVariable(self, variable):
		return (variable.symbol.getInternalMathFormula() in self.__definition.getInternalMathFormula().atoms()
				or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.__definition.getInternalMathFormula().atoms())
				or variable.symbol.getInternalMathFormula() == self.getVariable().symbol.getInternalMathFormula())
