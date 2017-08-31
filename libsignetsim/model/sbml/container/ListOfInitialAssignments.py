#!/usr/bin/env python
""" ListOfInitialAssignments.py


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


from libsignetsim.model.sbml.container.ListOf import ListOf
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.model.sbml.InitialAssignment import InitialAssignment
from libsignetsim.settings.Settings import Settings


class ListOfInitialAssignments(ListOf, SbmlObject):
	""" Class for the listOfInitialAssignments in a sbml model """

	def __init__ (self, model):

		self.__model = model
		ListOf.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_list_of_ia,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads initial assignments' list from a sbml file """

		for init_ass in sbml_list_of_ia:
			t_init_ass = InitialAssignment(self.__model, self.nextId())
			t_init_ass.readSbml(init_ass, sbml_level, sbml_version)
			ListOf.add(self, t_init_ass)

		SbmlObject.readSbml(self, sbml_list_of_ia, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes initial assignments' list to a sbml file """

		for initial_assignment in ListOf.values(self):
			initial_assignment.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(ListOf.values(self)):
			SbmlObject.writeSbml(self, sbml_model.getListOfInitialAssignments(), sbml_level, sbml_version)


	def new(self, variable=None, expression=None, rawFormula=False):

		if (variable is not None and expression is not None):
			t_initial_assignment = InitialAssignment(self.__model, self.nextId())
			t_initial_assignment.setVariable(variable)
			t_initial_assignment.setPrettyPrintDefinition(expression, rawFormula=rawFormula)
			ListOf.add(self, t_initial_assignment)
			return t_initial_assignment


	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, conversion_factors={}):

		if obj not in deletions:

			SbmlObject.copy(self, obj)

			for init_ass in obj.values():
				if init_ass not in deletions:

					t_init_ass = InitialAssignment(self.__model, self.nextId())
					t_init_ass.copy(init_ass, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factors=conversion_factors)
					ListOf.add(self, t_init_ass)

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		for obj in ListOf.values(self):
			obj.renameSbmlId(old_sbml_id, new_sbml_id)


	def hasInitialAssignment(self, variable):

		for obj in ListOf.values(self):
			if obj.getVariable().getSbmlId() == variable.getSbmlId():
				return True


	def containsVariable(self, variable):

		for init_ass in ListOf.values(self):
			if init_ass.containsVariable(variable):
				return True
		return False


	def remove(self, init_assignment):
		""" Remove an initial assignment from the list """

		init_assignment.variable.unsetRuledBy()
		ListOf.remove(self, init_assignment)


	def removeById(self, obj_id):
		""" Remove an initial assignment from the list """

		self.remove(self.getById(obj_id))
