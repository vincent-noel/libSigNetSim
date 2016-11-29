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


from libsignetsim.model.sbmlobject.Rule import Rule
from libsignetsim.model.math.MathAssignmentRule import MathAssignmentRule
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings

from libsbml import SBML_SPECIES_CONCENTRATION_RULE, \
                    SBML_PARAMETER_RULE, \
                    SBML_COMPARTMENT_VOLUME_RULE
from sympy import Symbol

class AssignmentRule(Rule, MathAssignmentRule):


    def __init__ (self, model, objId):

        self.__model = model
        Rule.__init__(self, model, objId, Rule.RULE_ASSIGNMENT)
        MathAssignmentRule.__init__(self, model)

        self.__var = None


    def readSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

        Rule.readSbml(self, sbml_rule, sbml_level, sbml_version)

        if self.__model.listOfVariables.containsSbmlId(sbml_rule.getVariable()):
            self.__var = self.__model.listOfVariables[sbml_rule.getVariable()]
            self.__var.setRuledBy(self)

        MathAssignmentRule.readSbml(self, sbml_rule, sbml_level, sbml_version)


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
        MathAssignmentRule.writeSbml(self, sbml_rule, sbml_level, sbml_version)


    def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):

        Rule.copy(self, obj, prefix, shift)

        t_symbol = Symbol(obj.getVariable().getSbmlId())
        if t_symbol in subs.keys():
            t_sbml_id = str(subs[t_symbol])
            tt_symbol = Symbol(t_sbml_id)
            if tt_symbol in replacements.keys():
                t_sbml_id = str(replacements[tt_symbol])
        else:
            t_sbml_id = prefix+obj.getVariable().getSbmlId()

        self.__var = self.__model.listOfVariables[t_sbml_id]
        self.__var.setRuledBy(self)

        MathAssignmentRule.copy(self, obj, prefix, shift, subs, deletions, replacements, conversions, time_conversion)


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