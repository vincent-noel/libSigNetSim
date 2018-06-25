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

from libsignetsim.model.sbml.container.ListOf import ListOf
from libsignetsim.model.sbml.container.HasIds import HasIds
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasParentObj import HasParentObj

from libsignetsim.model.sbml.Species import Species
from libsignetsim.model.ModelException import CannotDeleteException, InvalidXPath
from libsignetsim.settings.Settings import Settings

from re import match

class ListOfSpecies(ListOf, HasIds, SbmlObject, HasParentObj):

	def __init__ (self, model, parent_obj):

		self.__model = model

		HasParentObj.__init__(self, parent_obj)
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_listOfSpecies,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		for sbml_species in sbml_listOfSpecies:
			t_species = Species(self.__model, self, self.nextId())
			t_species.readSbml(sbml_species, sbml_level, sbml_version)
			ListOf.add(self, t_species)

		SbmlObject.readSbml(self, sbml_listOfSpecies, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		for species in self:
			species.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self) > 0:
			SbmlObject.writeSbml(self, sbml_model.getListOfSpecies(), sbml_level, sbml_version)


	def new(self, name=None, compartment=None, value=0, unit=None,
			 constant=False, boundaryCondition=False, hasOnlySubstanceUnits=False):

		t_species = Species(self.__model, self, self.nextId())
		t_species.new(name, compartment, value, unit, constant,
							boundaryCondition, hasOnlySubstanceUnits)
		ListOf.add(self, t_species)
		return t_species

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factor=None):

		if obj not in deletions:

			SbmlObject.copy(self, obj)
			for species in obj:

				if species not in deletions:

					t_species = Species(self.__model, self, self.nextId())
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
		for species in self:
			if ((species.isConcentration() or species.isDeclaredConcentration)
				and not self.__model.listOfInitialAssignments.hasInitialAssignment(species)):
				count += 1
		return count

	def hasBoundaryConditions(self):

		for species in self:
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
		for obj in self:
			Species.renameSbmlId(obj, old_sbml_id, new_sbml_id)



	def resolveXPath(self, selector):

		if not (selector.startswith("species") or selector.startswith("sbml:species")):
			raise InvalidXPath(selector)

		res_match = match(r'(.*)\[@(.*)=(.*)\]', selector)
		if res_match is None:
			raise InvalidXPath(selector)

		tokens = res_match.groups()
		if len(tokens) != 3:
			raise InvalidXPath(selector)

		object = None
		if tokens[1] == "id":
			object = self.getBySbmlId(tokens[2][1:-1])
		elif tokens[1] == "name":
			object = self.getByName(tokens[2][1:-1])
		elif tokens[1] == "metaid":
			object = self.getByMetaId(tokens[2][1:-1])

		if object is not None:
			return object

		# If not returned yet
		raise InvalidXPath(selector)

	def getByXPath(self, xpath):
		return self.resolveXPath(xpath[0]).getByXPath(xpath[1:])

	def setByXPath(self, xpath, object):
		self.resolveXPath(xpath[0]).setByXPath(xpath[1:], object)

	def getXPath(self):
		return "/".join([self.getParentObj().getXPath(), "sbml:listOfSpecies"])



