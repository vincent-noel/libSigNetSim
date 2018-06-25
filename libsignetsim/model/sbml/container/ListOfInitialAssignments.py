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
from __future__ import print_function

from libsignetsim.model.sbml.container.ListOf import ListOf
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.model.sbml.InitialAssignment import InitialAssignment

from libsignetsim.settings.Settings import Settings
from re import match

class ListOfInitialAssignments(ListOf, SbmlObject, HasParentObj):
	""" Class for the listOfInitialAssignments in a sbml model """

	def __init__(self, model, parent_obj, math_only=False):

		self.__model = model
		ListOf.__init__(self, model)
		HasParentObj.__init__(self, parent_obj)

		# For math submodels, where objects are not sbml objects
		self.mathOnly = math_only
		if not math_only:
			SbmlObject.__init__(self, model)

	def readSbml(self, sbml_list_of_ia,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads initial assignments' list from a sbml file """

		for init_ass in sbml_list_of_ia:
			t_init_ass = InitialAssignment(self.__model, self, self.nextId())
			t_init_ass.readSbml(init_ass, sbml_level, sbml_version)
			ListOf.add(self, t_init_ass)

		SbmlObject.readSbml(self, sbml_list_of_ia, sbml_level, sbml_version)

	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes initial assignments' list to a sbml file """

		for initial_assignment in self:
			initial_assignment.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self) > 0:
			SbmlObject.writeSbml(self, sbml_model.getListOfInitialAssignments(), sbml_level, sbml_version)

	def new(self, variable=None, expression=None, rawFormula=False):

		if (variable is not None and expression is not None):
			t_initial_assignment = InitialAssignment(self.__model, self, self.nextId())
			t_initial_assignment.setVariable(variable)
			t_initial_assignment.setPrettyPrintDefinition(expression, rawFormula=rawFormula)
			ListOf.add(self, t_initial_assignment)
			return t_initial_assignment

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, conversion_factors={}):

		if obj not in deletions:

			SbmlObject.copy(self, obj)

			for init_ass in obj:
				if init_ass not in deletions:

					t_init_ass = InitialAssignment(self.__model, self, self.nextId())
					t_init_ass.copy(init_ass, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factors=conversion_factors)
					ListOf.add(self, t_init_ass)

	def copySubmodel(self, obj):

		for init_ass in obj:
			t_init_ass = InitialAssignment(self.__model, self, init_ass.objId, math_only=self.mathOnly)
			t_init_ass.copySubmodel(init_ass)
			ListOf.add(self, t_init_ass)

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		for obj in self:
			obj.renameSbmlId(old_sbml_id, new_sbml_id)


	def hasInitialAssignment(self, variable):

		for obj in self:
			if obj.getVariable().getSbmlId() == variable.getSbmlId():
				return True

	def containsVariable(self, variable):

		for init_ass in self:
			if init_ass.containsVariable(variable):
				return True
		return False

	def remove(self, init_assignment):
		""" Remove an initial assignment from the list """

		init_assignment.getVariable().unsetRuledBy()
		ListOf.remove(self, init_assignment)

	def removeById(self, obj_id):
		""" Remove an initial assignment from the list """

		self.remove(self.getById(obj_id))

	def resolveXPath(self, selector):

		if not (selector.startswith("initialAssignment") or selector.startswith("sbml:initialAssignment")):
			raise InvalidXPath(selector)

		res_match = match(r'(.*)\[@(.*)=(.*)\]', selector)
		if res_match is None:
			raise InvalidXPath(selector)

		tokens = res_match.groups()
		if len(tokens) != 3:
			raise InvalidXPath(selector)

		object = None
		if tokens[1] == "metaid":
			object = self.getByMetaId(tokens[2][1:-1])

		if object is not None:
			return object

		# If not returned yet
		raise InvalidXPath(selector)

	def getByXPath(self, xpath):
		if len(xpath) > 0:
			return self.resolveXPath(xpath[0]).getByXPath(xpath[1:])
		else:
			return self

	def setByXPath(self, xpath, object):
		self.resolveXPath(xpath[0]).setByXPath(xpath[1:], object)

	def getXPath(self):
		return "/".join([self.getParentObj().getXPath(), "sbml:listOfInitialAssignments"])

	def pprint(self):

		for ode in self:
			ode.pprint()
			print("\n")
