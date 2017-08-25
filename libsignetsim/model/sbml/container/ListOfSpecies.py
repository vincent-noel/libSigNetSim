#!/usr/bin/env python
""" ListOfSpecies.py


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

from libsignetsim.model.sbml.Species import Species
from libsignetsim.model.ModelException import CannotDeleteException
from libsignetsim.settings.Settings import Settings


class ListOfSpecies(ListOf, HasIds, SbmlObject):

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_listOfSpecies,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		for sbml_species in sbml_listOfSpecies:
			t_species = Species(self.__model, self.nextId())
			t_species.readSbml(sbml_species, sbml_level, sbml_version)
			ListOf.add(self, t_species)

		SbmlObject.readSbml(self, sbml_listOfSpecies, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		for species in ListOf.values(self):
			species.writeSbml(sbml_model, sbml_level, sbml_version)

		SbmlObject.writeSbml(self, sbml_model.getListOfSpecies(), sbml_level, sbml_version)


	def new(self, name=None, compartment=None, value=0, unit=None,
			 constant=False, boundaryCondition=False, hasOnlySubstanceUnits=False):

		t_species = Species(self.__model, self.nextId())
		t_species.new(name, compartment, value, unit, constant,
							boundaryCondition, hasOnlySubstanceUnits)
		ListOf.add(self, t_species)
		return t_species

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factor=None):

		if obj not in deletions:

			SbmlObject.copy(self, obj)
			for species in obj.values():

				if species not in deletions:

					t_species = Species(self.__model, self.nextId())
					t_species.copy(
						species,
						sids_subs=sids_subs,
						symbols_subs=symbols_subs,
						usids_subs=usids_subs,
						conversion_factor=conversion_factor
					)
					ListOf.add(self, t_species)

	def nbFormulaInitialization(self):

		count = 0
		for species in ListOf.values(self):
			if ((species.isConcentration() or species.isDeclaredConcentration)
				and not self.__model.listOfInitialAssignments.hasInitialAssignment(species)):
				count += 1
		return count

	def hasBoundaryConditions(self):

		for species in ListOf.values(self):
			if species.boundaryCondition:
				return True

		return False


	def remove(self, species):
		""" Remove an object from the list """

		if species.isInReactions():
			raise CannotDeleteException("Species is used in reactions")
		elif species.isInRules():
			raise CannotDeleteException("Species in used in rules")

		self.__model.listOfVariables.removeVariable(species)
		# self.__model.listOfSbmlIds.removeSbmlId(species)
		ListOf.remove(self, species)


	def removeById(self, species_obj_id):
		""" Remove an object from the list """

		self.remove(self.getById(species_obj_id))

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		for obj in ListOf.values(self):
			Species.renameSbmlId(obj, old_sbml_id, new_sbml_id)
