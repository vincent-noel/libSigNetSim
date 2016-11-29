#!/usr/bin/env python
""" InitialAssignment.py


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


from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject
from libsignetsim.model.math.MathInitialAssignment import MathInitialAssignment
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.settings.Settings import Settings
from sympy import Symbol

class InitialAssignment(SbmlObject, MathInitialAssignment):
    """ Initial assignment definition """

    def __init__ (self, model, obj_id):

        self.model = model
        self.objId = obj_id

        SbmlObject.__init__(self, model)
        MathInitialAssignment.__init__(self, model)

        self.__var = None


    def readSbml(self, initial_assignment, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
        """ Reads an initial assignment from a sbml file """

        SbmlObject.readSbml(self, initial_assignment, sbml_level, sbml_version)

        if self.model.listOfVariables.containsSbmlId(initial_assignment.getSymbol()):
            self.__var = self.model.listOfVariables[initial_assignment.getSymbol()]
            self.__var.setInitialAssignmentBy(self)

        MathInitialAssignment.readSbml(self, initial_assignment, sbml_level, sbml_version)


    def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
        """ Writes an initial assignment to a sbml file """

        sbml_initial_assignment = sbml_model.createInitialAssignment()

        SbmlObject.writeSbml(self, sbml_initial_assignment, sbml_level, sbml_version)
        MathInitialAssignment.writeSbml(self, sbml_initial_assignment, sbml_level, sbml_version)


    def copy(self, obj, prefix="", shift="", subs={}, deletions=[], replacements={}, conversions=[]):
        SbmlObject.copy(self, obj, prefix, shift)

        t_symbol = Symbol(obj.getVariable().getSbmlId())

        # print "LIst of variables"
        # print self.model.listOfVariables.keys()
        if t_symbol in subs.keys():
            t_sbml_id = str(subs[t_symbol])
            tt_symbol = Symbol(t_sbml_id)
            if tt_symbol in replacements.keys():
                t_sbml_id = str(replacements[tt_symbol])
        else:
            t_sbml_id = prefix+obj.getVariable().getSbmlId()

        self.__var = self.model.listOfVariables[t_sbml_id]
        self.__var.setInitialAssignmentBy(self)
        MathInitialAssignment.copy(self, obj, prefix, shift, subs, deletions, replacements, conversions)




    def getVariable(self):

        return self.__var


    def getVariableMath(self):

        return self.variable

    def setVariable(self, variable):

        if self.__var is not None:
            self.var.unsetInitialAssignmentBy()

        self.__var = var
        self.__var.setInitialAssignmentBy(self)
        self.variable.setInternalVariable(variable.symbol.getInternalMathFormula())


    def getExpression(self):

        return self.definition.getPrettyPrintMathFormula()

    def getExpressionMath(self):

        return self.definition

    def setExpression(self, string):

        self.definition.setPrettyPrintMathFormula(string)


    def getRuleTypeDescription(self):
        return "Initial assignment"