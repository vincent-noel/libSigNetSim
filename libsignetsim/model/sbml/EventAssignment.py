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
from __future__ import division

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import SympyInteger, SympyMul, SympyPow
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs


class EventAssignment(SbmlObject):
	""" Class definition for event assignments """

	def __init__(self, model, obj_id, event=None, math_only=False):

		self.__model = model
		self.objId = obj_id
		self.event = event
		self.__var = None
		self.__definition = MathFormula(model, MathFormula.MATH_EVENTASSIGNMENT)

		# For math submodels, where objects are not sbml objects
		self.mathOnly = math_only
		if not self.mathOnly:
			SbmlObject.__init__(self, model)

	def readSbml(self, sbml_event_assignment, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads event assignment from a sbml file """

		SbmlObject.readSbml(self, sbml_event_assignment, sbml_level, sbml_version)
		self.__var = self.__model.listOfVariables.getBySbmlId(sbml_event_assignment.getVariable())
		self.getVariable().addEventAssignmentBy(self.event)

		if sbml_event_assignment.getMath() is not None:
			self.__definition.readSbml(sbml_event_assignment.getMath())

			if self.getVariable().isConcentration():
				t_comp = self.getVariable().getCompartment()
				self.__definition.setInternalMathFormula(
						SympyMul(self.__definition.getInternalMathFormula(),
									t_comp.symbol.getInternalMathFormula()))

	def writeSbml(self, sbml_event, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes event assignemnt to a sbml file """

		sbml_event_assignment = sbml_event.createEventAssignment()
		SbmlObject.writeSbml(self, sbml_event_assignment, sbml_level, sbml_version)

		sbml_event_assignment.setVariable(self.__var.getSbmlId())

		if self.__definition.getInternalMathFormula() is not None:
			t_definition = MathFormula(self.__model, MathFormula.MATH_EVENTASSIGNMENT)
			t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula())

			if self.getVariable().isConcentration():
				t_comp = self.getVariable().getCompartment()
				t_definition.setInternalMathFormula(
					SympyMul(t_definition.getInternalMathFormula(),
								SympyPow(t_comp.symbol.getInternalMathFormula(),
									SympyInteger(-1))))

			sbml_event_assignment.setMath(t_definition.getSbmlMathFormula())


	def copy(self, obj, sids_subs={}, symbols_subs={}, conversion_factors={}, time_conversion=None):

		if not self.mathOnly:
			SbmlObject.copy(self, obj)

		if obj.getVariable().getSbmlId() in list(sids_subs.keys()):
			self.__var = self.__model.listOfVariables.getBySbmlId(sids_subs[obj.getVariable().getSbmlId()])
		else:
			self.__var = self.__model.listOfVariables.getBySbmlId(obj.getVariable().getSbmlId())

		self.getVariable().addEventAssignmentBy(self.event)

		if obj.getDefinition().getInternalMathFormula() is not None:

			t_convs = {}
			for var, conversion in list(conversion_factors.items()):
				t_convs.update({var: var/conversion})

			t_definition = unevaluatedSubs(obj.getDefinition().getInternalMathFormula(rawFormula=False), symbols_subs)
			t_definition = unevaluatedSubs(t_definition, t_convs)

			t_var_symbol = unevaluatedSubs(obj.getVariable().symbol.getInternalMathFormula(), symbols_subs)

			if t_var_symbol in conversion_factors:
				t_definition *= conversion_factors[t_var_symbol]

			self.__definition.setInternalMathFormula(t_definition)

	def copySubmodel(self, obj):
		self.__var = self.__model.listOfVariables.getBySymbol(obj.getVariable().symbol.getSymbol())
		if obj.getDefinition().getInternalMathFormula() is not None:
			self.__definition.setInternalMathFormula(obj.getDefinition().getDeveloppedInternalMathFormula())

	def getVariable(self):
		return self.__var

	def getVariableMath(self):
		return self.getVariable().symbol

	def setVariable(self, variable):
		if self.__var is not None:
			self.getVariable().removeEventAssignmentBy(self.event)

		self.__var = variable
		self.getVariable().addEventAssignmentBy(self.event)

	def getPrettyPrintAssignment(self):
		if self.__definition.getInternalMathFormula() is not None:
			return self.__definition.getPrettyPrintMathFormula()

	def getAssignmentMath(self):
		return self.__definition

	def setPrettyPrintAssignment(self, value, rawFormula=False):
		self.__definition.setPrettyPrintMathFormula(str(value), rawFormula)

	def getDefinition(self):
		return self.__definition

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		self.__definition.renameSbmlId(old_sbml_id, new_sbml_id)

	def isValid(self):
		return (
			self.__definition is not None
			and self.__definition.getInternalMathFormula() is not None
			and self.__definition.getDeveloppedInternalMathFormula() is not None
		)
