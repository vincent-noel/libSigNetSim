#!/usr/bin/env python
""" ListOfSubmodels.py


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


from libsignetsim.model.container.ListOf import ListOf
from libsignetsim.model.container.HasIds import HasIds
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject

from libsignetsim.model.sbmlobject.SbmlSubModel import SbmlSubModel
from libsignetsim.settings.Settings import Settings

class ListOfSubmodels(ListOf, HasIds):#, SbmlObject):
	""" Class for the listOfModelDefinition in a sbml model """

	def __init__ (self, model):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		# SbmlObject.__init__(self, model)


	def readSbml(self, sbml_list_submodels,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads compartments' list from a sbml file """

		for i, submodel in enumerate(sbml_list_submodels):
			t_submodel = SbmlSubModel(self.__model, self.nextId())
			t_submodel.readSbml(submodel, sbml_level, sbml_version)
			ListOf.add(self, t_submodel)

		# SbmlObject.readSbml(self, sbml_list_submodels, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes compartments' list to a sbml file """

		for t_submodel in ListOf.values(self):
			t_submodel.writeSbml(sbml_model, sbml_level, sbml_version)

		# SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


	def new(self):
		""" Creates a new compartment """

		t_submodel = SbmlSubModel(self.__model, self.nextId())
		ListOf.add(self, t_submodel)
		return t_submodel


	def remove(self, sbml_obj):
		""" Remove an object from the list """

		# ListOf.remove(self, comp)
		dict.__delitem__(self, sbml_obj.objId)


	def removeById(self, obj_id):
		""" Remove an object from the list """
		dict.__delitem__(self, obj_id)

	def getSubmodels(self):

		res = []
		for submodel in ListOf.values(self):
			res.append(submodel.getModelObject())

		return res

	def getBySbmlIdRef(self, sbml_id_ref):
		return HasIds.getBySbmlId(self, sbml_id_ref)

	def getBySbmlId(self, sbml_id):
		for submodel in ListOf.values(self):
			if submodel.getModelObject().getSbmlId() == sbml_id:
				return submodel
