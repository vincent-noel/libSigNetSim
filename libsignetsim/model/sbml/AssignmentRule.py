#!/usr/bin/env python
""" AssignmentRule.py


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
from libsignetsim.model.math.sympy_shortcuts import  (
SympySymbol, SympyInteger, SympyMul, SympyPow)

from libsbml import SBML_SPECIES_CONCENTRATION_RULE, \
					SBML_PARAMETER_RULE, \
					SBML_COMPARTMENT_VOLUME_RULE


class AssignmentRule(Rule):


	def __init__ (self, model, objId):

		self.__model = model
		Rule.__init__(self, model, objId, Rule.RULE_ASSIGNMENT)
		self.variable = MathSymbol(model)
		self.definition = MathFormula(model, MathFormula.MATH_ASSIGNMENTRULE)
		self.__var = None


	def readSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		Rule.readSbml(self, sbml_rule, sbml_level, sbml_version)

		if self.__model.listOfVariables.containsSbmlId(sbml_rule.getVariable()):
			self.__var = self.__model.listOfVariables[sbml_rule.getVariable()]
			self.__var.setRuledBy(self)

		self.variable.readSbml(sbml_rule.getVariable(), sbml_level, sbml_version)
		self.definition.readSbml(sbml_rule.getMath(), sbml_level, sbml_version)

		if self.getVariable().isConcentration():
			self.definition.setInternalMathFormula(
					SympyMul(self.definition.getInternalMathFormula(),
						self.getVariable().getCompartment().symbol.getInternalMathFormula()))
		# MathAssignmentRule.readSbml(self, sbml_rule, sbml_level, sbml_version)


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		sbml_rule = sbml_model.createAssignmentRule()

		if sbml_level < 2:
			if self.__var.isSpecies():
				sbml_rule.setL1TypeCode(SBML_SPECIES_CONCENTRATION_RULE)
			elif self.__var.isParameter():
				sbml_rule.setL1TypeCode(SBML_PARAMETER_RULE)
			elif self.__var.isCompartment():
				sbml_rule.setL1TypeCode(SBML_COMPARTMENT_VOLUME_RULE)

		Rule.writeSbml(self, sbml_rule, sbml_level, sbml_version)
		t_definition = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
		t_definition.setInternalMathFormula(self.definition.getInternalMathFormula())
		t_variable = self.variable.getSbmlMathFormula(sbml_level, sbml_version).getName()

		if self.getVariable().isConcentration():
			t_definition.setInternalMathFormula(
					SympyMul(self.definition.getInternalMathFormula(),
							 SympyPow(self.getVariable().getCompartment().symbol.getInternalMathFormula(),
										SympyInteger(-1))))

		sbml_rule.setVariable(t_variable)
		sbml_rule.setMath(t_definition.getSbmlMathFormula(sbml_level, sbml_version))

		# MathAssignmentRule.writeSbml(self, sbml_rule, sbml_level, sbml_version)


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):

		Rule.copy(self, obj, prefix, shift)

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

		t_definition = obj.definition.getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs)

		t_var_symbol = obj.variable.getInternalMathFormula().subs(subs).subs(replacements)
		if t_var_symbol in conversions:
			t_definition *= conversions[t_var_symbol]

		self.definition.setInternalMathFormula(t_definition)
		self.variable.setInternalMathFormula(t_var_symbol)
		# MathAssignmentRule.copy(self, obj, prefix, shift, subs, deletions, replacements, conversions, time_conversion)


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
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
			t_math_formula.setPrettyPrintMathFormula(definition)
			self.definition.setInternalMathFormula(t_math_formula.getInternalMathFormula()*t_comp.symbol.getInternalMathFormula())

		else:
			self.definition.setPrettyPrintMathFormula(definition)


	def setPrettyPrintVariable(self, variable):
		self.variable.setPrettyPrintMathFormula(variable)


	def getPrettyPrintDefinition(self):

		if self.getVariable().isConcentration():
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

		t_formula = self.getDefinition(MathFormula.MATH_INTERNAL, forcedConcentration)

		# print "yeah, that one !!"
		# print t_formula
		if forcedConcentration:
			for species in self.__model.listOfSpecies.values():
				if species.isConcentration():
					t_fc = SympySymbol("_speciesForcedConcentration_%s_" % str(species.symbol.getInternalMathFormula()))
					t_species = SympySymbol(species.getSbmlId())
					t_formula = t_formula.subs({ t_fc : t_species })
					# t_formula.setInternalMathFormula(t_internal)

		return t_formula


	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)

		if self.variable.getInternalMathFormula() == old_symbol:
			self.variable.setInternalMathFormula(SympySymbol(new_sbml_id))

		if old_symbol in self.definition.getInternalMathFormula().atoms():
			self.definition.setInternalMathFormula(self.definition.getInternalMathFormula().subs(old_symbol, SympySymbol(new_sbml_id)))


	def containsVariable(self, variable):
		return (variable.symbol.getInternalMathFormula() in self.definition.getInternalMathFormula().atoms()
				or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.definition.getInternalMathFormula().atoms())
				or variable.symbol.getInternalMathFormula() == self.variable.getInternalMathFormula())
