#!/usr/bin/env python
""" EventAssignment.py


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


from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathEventAssignment import MathEventAssignment
from libsignetsim.model.math.MathEventTrigger import MathEventTrigger
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.sbmlobject.HasId import HasId
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject

from libsignetsim.settings.Settings import Settings
from sympy import Symbol


class EventAssignment(MathEventAssignment, SbmlObject):
    """ Class definition for event assignments """

    def __init__(self, model, obj_id, event=None):

        self.__model = model
        self.objId = obj_id
        SbmlObject.__init__(self, model)
        MathEventAssignment.__init__(self, model)
        self.event = event
        self.__var = None


    def readSbml(self, sbml_event_assignment, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
        """ Reads event assignment from a sbml file """

        SbmlObject.readSbml(self, sbml_event_assignment, sbml_level, sbml_version)
        self.__var = self.__model.listOfVariables[sbml_event_assignment.getVariable()]
        self.__var.addEventAssignmentBy(self.event)
        MathEventAssignment.readSbml(self, sbml_event_assignment, sbml_level, sbml_version)

    def writeSbml(self, sbml_event, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
        """ Writes event assignemnt to a sbml file """

        sbml_event_assignment = sbml_event.createEventAssignment()
        SbmlObject.writeSbml(self, sbml_event_assignment, sbml_level, sbml_version)
        MathEventAssignment.writeSbml(self, sbml_event_assignment, sbml_level, sbml_version)


    def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):
        SbmlObject.copy(self, obj, prefix, shift)

        t_symbol = Symbol(obj.getVariable().getSbmlId())
        if t_symbol in subs.keys():
            t_sbml_id = str(subs[t_symbol])
            tt_symbol = Symbol(t_sbml_id)
            if tt_symbol in replacements.keys():
                t_sbml_id = str(replacements[tt_symbol])
        else:
            t_sbml_id = prefix+obj.getVariable().getSbmlId()

        self.__var = self.__model.listOfVariables[t_sbml_id]
        self.__var.addEventAssignmentBy(self.event)
        MathEventAssignment.copy(self, obj, prefix, shift, subs, deletions, replacements, conversions, time_conversion)

    def getVariable(self):
        return self.__var

    def getVariableMath(self):
        return self.variable


    def setVariable(self, variable):

        if self.__var is not None:
            self.__var.removeEventAssignmentBy(self.event)

        self.__var = variable
        self.__var.addEventAssignmentBy(self.event)
        self.variable.setInternalVariable(variable.symbol.getInternalMathFormula())

    def getAssignment(self):

        return self.definition.getPrettyPrintMathFormula()

    def getAssignmentMath(self):

        return self.definition

    def setAssignment(self, value):

        self.definition.setPrettyPrintMathFormula(str(value))