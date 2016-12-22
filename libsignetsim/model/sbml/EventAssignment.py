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
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyMul, SympyPow)


class EventAssignment(SbmlObject):
	""" Class definition for event assignments """

	def __init__(self, model, obj_id, event=None):

		self.__model = model
		self.objId = obj_id
		SbmlObject.__init__(self, model)
		self.event = event
		self.__var = None
		self.__definition = MathFormula(model, MathFormula.MATH_EVENTASSIGNMENT)


	def readSbml(self, sbml_event_assignment, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads event assignment from a sbml file """

		SbmlObject.readSbml(self, sbml_event_assignment, sbml_level, sbml_version)
		self.__var = self.__model.listOfVariables[sbml_event_assignment.getVariable()]
		self.__var.addEventAssignmentBy(self.event)

		self.__definition.readSbml(sbml_event_assignment.getMath())

		if self.__var.isConcentration():
			t_comp = self.__var.getCompartment()
			self.__definition.setInternalMathFormula(
					SympyMul(self.__definition.getInternalMathFormula(),
								t_comp.symbol.getInternalMathFormula()))


	def writeSbml(self, sbml_event, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes event assignemnt to a sbml file """

		sbml_event_assignment = sbml_event.createEventAssignment()
		SbmlObject.writeSbml(self, sbml_event_assignment, sbml_level, sbml_version)

		t_definition = MathFormula(self.__model, MathFormula.MATH_EVENTASSIGNMENT)
		t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula())
		t_variable = self.__var.symbol.getSbmlMathFormula(sbml_level, sbml_version).getName()

		if self.__var.isConcentration():
			t_comp = self.__var.getCompartment()
			t_definition.setInternalMathFormula(
				SympyMul(t_definition.getInternalMathFormula(),
							SympyPow(t_comp.symbol.getInternalMathFormula(),
								SympyInteger(-1))))


		sbml_event_assignment.setVariable(t_variable)
		sbml_event_assignment.setMath(t_definition.getSbmlMathFormula())


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):
		SbmlObject.copy(self, obj, prefix, shift)

		t_symbol = SympySymbol(obj.getVariable().getSbmlId())
		if t_symbol in subs.keys():
			t_sbml_id = str(subs[t_symbol])
			tt_symbol = SympySymbol(t_sbml_id)
			if tt_symbol in replacements.keys():
				t_sbml_id = str(replacements[tt_symbol])
		else:
			t_sbml_id = prefix+obj.getVariable().getSbmlId()

		self.__var = self.__model.listOfVariables[t_sbml_id]
		self.__var.addEventAssignmentBy(self.event)

		t_convs = {}
		for var, conversion in conversions.items():
			t_convs.update({var:var/conversion})

		t_definition = obj.getDefinition().getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs)

		t_var_symbol = obj.getVariable().symbol.getInternalMathFormula().subs(subs).subs(replacements)
		if t_var_symbol in conversions:
			t_definition *= conversions[t_var_symbol]

		self.__definition.setInternalMathFormula(t_definition)


	def getVariable(self):
		return self.__var

	def getVariableMath(self):
		return self.__var.symbol


	def setVariable(self, variable):

		if self.__var is not None:
			self.__var.removeEventAssignmentBy(self.event)

		self.__var = variable
		self.__var.addEventAssignmentBy(self.event)


	def getAssignment(self):

		return self.__definition.getPrettyPrintMathFormula()

	def getAssignmentMath(self):

		return self.__definition

	def setAssignment(self, value):

		self.__definition.setPrettyPrintMathFormula(str(value))

	def getDefinition(self):

		return self.__definition

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)

		if old_symbol in self.__definition.getInternalMathFormula().atoms():
			t_definition = self.__definition.getInternalMathFormula.subs(
												old_symbol,
												SympySymbol(new_sbml_id)
			)
			self.__definition.setInternalMathFormula(t_definition)
