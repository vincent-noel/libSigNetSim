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
# from libsignetsim.model.math.MathRateRule import MathRateRule
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsbml import SBML_SPECIES_CONCENTRATION_RULE,\
					SBML_PARAMETER_RULE,\
					SBML_COMPARTMENT_VOLUME_RULE

from libsignetsim.model.math.sympy_shortcuts import  (
	SympySymbol, SympyInteger, SympyMul, SympyPow)
# from sympy import Symbol
# class RateRule(Rule, MathRateRule):
class RateRule(Rule):
	""" Class for rate rules """

	def __init__ (self, model, obj_id):

		self.__model = model
		Rule.__init__(self, model, obj_id, Rule.RULE_RATE)
		# MathRateRule.__init__(self, model)
		self.variable = MathSymbol(model)
		self.definition = MathFormula(model, MathFormula.MATH_RATERULE)
		self.__var = None


	def readSbml(self, rate_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		Rule.readSbml(self, rate_rule, sbml_level, sbml_version)

		if self.__model.listOfVariables.containsSbmlId(rate_rule.getVariable()):
			self.__var = self.__model.listOfVariables[rate_rule.getVariable()]
			self.__var.setRuledBy(self)

		self.variable.readSbml(rate_rule.getVariable())
		self.definition.readSbml(rate_rule.getMath())

		if self.getVariable().isConcentration():
			self.definition.setInternalMathFormula(
					SympyMul(self.definition.getInternalMathFormula(),
					self.getVariable().getCompartment().symbol.getInternalMathFormula()))
		# MathRateRule.readSbml(self, sbml_rule, sbml_level, sbml_version)

	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		rate_rule = sbml_model.createRateRule()
		if sbml_level < 2:

			if self.__var.isSpecies():
				rate_rule.setL1TypeCode(SBML_SPECIES_CONCENTRATION_RULE)
			elif self.__var.isParameter():
				rate_rule.setL1TypeCode(SBML_PARAMETER_RULE)
			elif self.__var.isCompartment():
				rate_rule.setL1TypeCode(SBML_COMPARTMENT_VOLUME_RULE)

		Rule.writeSbml(self, rate_rule, sbml_level, sbml_version)
		# MathRateRule.writeSbml(self, sbml_rule, sbml_level, sbml_version)

		t_definition = MathFormula(self.__model, MathFormula.MATH_RATERULE)
		t_definition.setInternalMathFormula(self.definition.getInternalMathFormula())
		t_variable = self.variable.getSbmlMathFormula(sbml_level, sbml_version).getName()

		if self.getVariable().isConcentration():
			t_definition.setInternalMathFormula(
					SympyMul(t_definition.getInternalMathFormula(),
					SympyPow(self.getVariable().getCompartment().symbol.getInternalMathFormula(),
					SympyInteger(-1))))

		rate_rule.setVariable(t_variable)
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

		self.__var = self.__model.listOfVariables[t_sbml_id]
		self.__var.setRuledBy(self)


		t_convs = {}
		for var, conversion in conversions.items():
			t_convs.update({var:var/conversion})
		t_var_symbol = obj.variable.getInternalMathFormula().subs(subs).subs(replacements)

		t_definition = obj.definition.getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs)

		if t_var_symbol in conversions:
			t_definition *= conversions[t_var_symbol]

		if time_conversion is not None:
			t_definition /= time_conversion.getInternalMathFormula()

		self.variable.setInternalMathFormula(t_var_symbol)
		self.definition.setInternalMathFormula(t_definition)

		# MathRateRule.copy(self, obj, prefix, shift, subs, deletions, replacements, conversions, time_conversion)



	def getVariable(self):
		return self.__var

	def getVariableMath(self):
		return self.variable

	def setVariable(self, variable):

		if self.__var is not None:
			self.__var.unsetRuledBy()

		self.__var = variable
		self.__var.setRuledBy(self)
		self.variable.setInternalVariable(variable.symbol.getInternalMathFormula())


	def getExpression(self):
		return self.getPrettyPrintDefinition()

	def getExpressionMath(self):
		return self.definition

	def setExpression(self, string):
		self.setPrettyPrintDefinition(string)


	def setPrettyPrintDefinition(self, definition):

		if self.getVariable().isConcentration():
			t_comp = self.getVariable().getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_RATERULE)
			t_math_formula.setPrettyPrintMathFormula(definition)
			self.definition.setInternalMathFormula(
				t_math_formula.getInternalMathFormula()
				* t_comp.symbol.getInternalMathFormula())

		else:
			self.definition.setPrettyPrintMathFormula(definition)


	def setPrettyPrintVariable(self, variable):

		self.variable.setPrettyPrintMathFormula(variable)


	def getPrettyPrintDefinition(self):


		if self.getVariable().isConcentration():
			# variable = self.var #self.__model.listOfVariables[str(self.variable.getInternalMathFormula())]
			t_comp = self.getVariable().getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
			t_math_formula.setInternalMathFormula(self.definition.getInternalMathFormula()/t_comp.symbol.getInternalMathFormula())
			return t_math_formula.getPrettyPrintMathFormula()

		else:
			return self.definition.getPrettyPrintMathFormula()


	def getDefinition(self, math_type=MathFormula.MATH_INTERNAL, forcedConcentration=False):

		if self.getVariable().isConcentration() and forcedConcentration:
			return (self.definition.getInternalMathFormula()
						/ self.getVariable().getCompartment().symbol.getInternalMathFormula())
		else:
			return self.definition.getInternalMathFormula()

	def getInternalDefinition(self, forcedConcentration=False):
		return self.getDefinition(MathFormula.MATH_INTERNAL, forcedConcentration)



	def setVariable(self, variable):

		self.variable.setInternalMathFormula(variable.symbol.getInternalMathFormula())


	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)

		if self.variable.getInternalMathFormula() == old_symbol:
			self.variable.setInternalMathFormula(SympySymbol(new_sbml_id))

		if old_symbol in self.definition.getInternalMathFormula().atoms():

			t_definition = self.definition.getInternalMathFormula()
			t_definition = t_definition.subs(old_symbol, SympySymbol(new_sbml_id))

			self.definition.setInternalMathFormula(t_definition)

	def containsVariable(self, variable):
		return (variable.symbol.getInternalMathFormula() in self.definition.getInternalMathFormula().atoms()
				or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.definition.getInternalMathFormula().atoms())
				or variable.symbol.getInternalMathFormula() == self.variable.getInternalMathFormula())
