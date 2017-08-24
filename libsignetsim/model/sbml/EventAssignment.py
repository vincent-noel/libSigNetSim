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
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger, SympyMul, SympyPow
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs


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
		self.__var = sbml_event_assignment.getVariable()
		self.getVariable().addEventAssignmentBy(self.event)

		if sbml_event_assignment.getMath() is not None:
			self.__definition.readSbml(sbml_event_assignment.getMath())
		else:
			self.__definition = None

		if self.getVariable().isConcentration():
			t_comp = self.getVariable().getCompartment()
			self.__definition.setInternalMathFormula(
					SympyMul(self.__definition.getInternalMathFormula(),
								t_comp.symbol.getInternalMathFormula()))


	def writeSbml(self, sbml_event, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes event assignemnt to a sbml file """

		sbml_event_assignment = sbml_event.createEventAssignment()
		SbmlObject.writeSbml(self, sbml_event_assignment, sbml_level, sbml_version)

		if self.__definition is not None:
			t_definition = MathFormula(self.__model, MathFormula.MATH_EVENTASSIGNMENT)
			t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula())

		# t_variable = self.__var.symbol.getSbmlMathFormula(sbml_level, sbml_version).getName()

		if self.getVariable().isConcentration():
			t_comp = self.getVariable().getCompartment()
			t_definition.setInternalMathFormula(
				SympyMul(t_definition.getInternalMathFormula(),
							SympyPow(t_comp.symbol.getInternalMathFormula(),
								SympyInteger(-1))))


		sbml_event_assignment.setVariable(self.__var)
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

		self.__var = t_sbml_id
		self.getVariable().addEventAssignmentBy(self.event)

		t_convs = {}
		for var, conversion in conversions.items():
			t_convs.update({var:var/conversion})

		t_definition = unevaluatedSubs(obj.getDefinition().getInternalMathFormula(), subs)
		t_definition = unevaluatedSubs(t_definition, replacements)
		t_definition = unevaluatedSubs(t_definition, t_convs)

		t_var_symbol = unevaluatedSubs(obj.getVariable().symbol.getInternalMathFormula(), subs)
		t_var_symbol = unevaluatedSubs(t_var_symbol, replacements)

		if t_var_symbol in conversions:
			t_definition *= conversions[t_var_symbol]

		self.__definition.setInternalMathFormula(t_definition)


	def getVariable(self):
		return self.__model.listOfVariables.getBySbmlId(self.__var)

	def getVariableMath(self):
		return self.getVariable().symbol


	def setVariable(self, variable):

		if self.__var is not None:
			self.getVariable().removeEventAssignmentBy(self.event)

		self.__var = variable.getSbmlId()
		self.getVariable().addEventAssignmentBy(self.event)


	def getPrettyPrintAssignment(self):

		return self.__definition.getPrettyPrintMathFormula()

	def getAssignmentMath(self):

		return self.__definition

	def setPrettyPrintAssignment(self, value, rawFormula=False):

		self.__definition.setPrettyPrintMathFormula(str(value), rawFormula)

	def getDefinition(self):

		return self.__definition

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		self.__definition.renameSbmlId(old_sbml_id, new_sbml_id)
		if self.__var == old_sbml_id:
			self.__var = new_sbml_id