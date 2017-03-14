#!/usr/bin/env python
""" ListOfCompartments.py


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
from libsignetsim.model.sbml.container.HasIds import HasIds
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.Compartment import Compartment
from libsignetsim.model.ModelException import CannotDeleteException
from libsignetsim.settings.Settings import Settings

class ListOfCompartments(ListOf, HasIds, SbmlObject):
	""" Class for the listOfCompartments in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_compartments,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads compartments' list from a sbml file """

		for compartment in sbml_compartments:
			t_compartment = Compartment(self.__model, self.nextId())
			t_compartment.readSbml(compartment, sbml_level, sbml_version)
			ListOf.add(self, t_compartment)

		SbmlObject.readSbml(self, sbml_compartments, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes compartments' list to a sbml file """

		for compartment in ListOf.values(self):
			compartment.writeSbml(sbml_model, sbml_level, sbml_version)

		SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


	def new(self, name=None, sbml_id=None, size=1, constant=True, unit=None):
		""" Creates a new compartment """

		t_compartment = Compartment(self.__model, self.nextId())
		t_compartment.new(name, sbml_id, size, constant, unit)
		ListOf.add(self, t_compartment)
		return t_compartment

	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}):

		if len(self.keys()) > 0:
			t_shift = max(self.keys())+1
		else:
			t_shift = 0

		if obj not in deletions:

			SbmlObject.copy(self, obj, prefix, t_shift)

			for compartment in obj.values():
				if compartment not in deletions:

					obj_id = compartment.objId + t_shift
					t_compartment = Compartment(self.__model, obj_id)

					if not compartment.isMarkedToBeReplaced:
						t_compartment.copy(compartment, prefix, t_shift, subs, deletions, replacements)
					else:
						t_compartment.copy(compartment.isMarkedToBeReplacedBy, prefix, t_shift, subs, deletions, replacements)

					if compartment.isMarkedToBeRenamed:
						t_compartment.setSbmlId(compartment.getSbmlId(), model_wide=False)

					ListOf.add(self, t_compartment)


	def remove(self, comp):
		""" Remove an object from the list """

		# t_id = comp.getSbmlId()
		t_nb_species = comp.getNbSpecies()
		if t_nb_species > 0:
			message = "Compartment contains %d species" % t_nb_species
			raise CannotDeleteException(message)

		self.__model.listOfVariables.removeVariable(comp)
		ListOf.remove(self, comp)


	def removeById(self, obj_id):
		""" Remove an object from the list """
		self.remove(ListOf.getById(self, obj_id))
