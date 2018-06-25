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

from libsignetsim.model.sbml.Deletion import Deletion
from libsignetsim.settings.Settings import Settings

class ListOfDeletions(ListOf, HasIds):#, SbmlObject):
	""" Class for the listOfModelDefinition in a sbml model """

	def __init__ (self, model, parent_submodel):

		self.__model = model
		self.__parentSubmodel = parent_submodel
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		# SbmlObject.__init__(self, model)

	def readSbml(self, sbml_list_deletions,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads compartments' list from a sbml file """

		for deletion in sbml_list_deletions:
			t_deletion = Deletion(self.__model, self.nextId(), self.__parentSubmodel)
			t_deletion.readSbml(deletion, sbml_level, sbml_version)
			ListOf.add(self, t_deletion)

		# SbmlObject.readSbml(self, sbml_list_deletions, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes compartments' list to a sbml file """

		for t_deletion in self:
			sbml_deletion = sbml_model.createDeletion()
			t_deletion.writeSbml(sbml_deletion, sbml_level, sbml_version)

		# SbmlObject.writeSbml(sbml_model)


	def new(self):
		""" Creates a new compartment """

		t_deletion = Deletion(self.__model, self.nextId(), self.__parentSubmodel)
		ListOf.add(self, t_deletion)
		return t_deletion


	def remove(self, deletion):
		""" Remove an object from the list """
		ListOf.remove(self, deletion)

	def removeById(self, obj_id):
		""" Remove an object from the list """
		self.remove(self.getById(obj_id))


	def getDeletedMetaIds(self):

		objs = []
		for deletion in self:
			objs.append(deletion.getRefObject().getMetaId())

		return objs
