#!/usr/bin/env python
""" ListOfSpeciesReference.py


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

from libsignetsim.model.sbml.SpeciesReference import SpeciesReference
from libsignetsim.settings.Settings import Settings


class ListOfSpeciesReference(ListOf, HasIds, SbmlObject):
	""" Handles the list of species reference of a sbml model """

	def __init__ (self, model):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbmlListOfSpeciesReference,
					sbmlLevel=Settings.defaultSbmlLevel,
					sbmlVersion=Settings.defaultSbmlVersion):

		""" Read the list of species references from a sbml model """

		for sbmlSpeciesReference in sbmlListOfSpeciesReference:
			speciesReference = SpeciesReference(self.__model, self.nextId())
			speciesReference.readSbml(sbmlSpeciesReference, sbmlLevel, sbmlVersion)
			ListOf.add(self, speciesReference)

		SbmlObject.readSbml(self, sbmlListOfSpeciesReference, sbmlLevel, sbmlVersion)


	def writeSbml(self, sbmlReaction,
					sbmlLevel=Settings.defaultSbmlLevel,
					sbmlVersion=Settings.defaultSbmlVersion):

		""" Write the list of species references to a sbml model """

		for speciesReference in ListOf.values(self):
			speciesReference.writeSbml(sbmlReaction, sbmlLevel, sbmlVersion)

		SbmlObject.writeSbml(self, sbmlReaction, sbmlLevel, sbmlVersion)


	def new(self):
		""" Add a new species reference to the list and returns it """

		t_speciesReference = SpeciesReference(self.__model, self.nextId())
		ListOf.add(self, t_speciesReference)
		return t_speciesReference


	def add(self, species, stoichiometry=1):
		t_sr = self.new()
		t_sr.setSpecies(species)
		t_sr.setStoichiometry(stoichiometry)


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}):

		if len(self.keys()) > 0:
			t_shift = max(self.keys())+1
		else:
			t_shift = 0

		if obj not in deletions:
			SbmlObject.copy(self, obj, prefix, t_shift)
			for speciesReference in obj.values():
				if speciesReference not in deletions:
					t_sr = SpeciesReference(self.__model, (speciesReference.objId))

					if not speciesReference.isMarkedToBeReplaced:
						t_sr.copy(speciesReference, prefix, t_shift, subs, deletions, replacements)

					else:
						t_sr.copy(speciesReference.isMarkedToBeReplacedBy, prefix, t_shift, subs, deletions, replacements)

					if speciesReference.isMarkedToBeRenamed:
						t_sr.setSbmlId(speciesReference.getSbmlId(), model_wide=False)

					ListOf.add(self, t_sr)

	def hasVariableStoichiometry(self):

		for sr in self.values():
			if sr.isVariableStoichiometry():
				return True
		return False