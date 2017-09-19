#!/usr/bin/env python
""" ListOfModelDefinitions.py


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
from libsignetsim.model.sbml.ModelDefinition import ModelDefinition
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.settings.Settings import Settings

from re import match


class ListOfModelDefinitions(ListOf, HasIds):
	""" Class for the listOfModelDefinition in a sbml model """

	def __init__ (self, model):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)

	def readSbml(self, sbml_external_models,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads compartments' list from a sbml file """

		for model in sbml_external_models:
			t_model = ModelDefinition(self.__model, self.nextId())
			t_model.readSbml(model, sbml_level, sbml_version)
			ListOf.add(self, t_model)

	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes compartments' list to a sbml file """

		for model in ListOf.values(self):
			sbml_md = sbml_model.createModelDefinition()
			model.writeSbml(sbml_md, sbml_level, sbml_version)


	def new(self, name=None, sbml_id=None):
		""" Creates a new compartment """

		t_model = ModelDefinition(self.__model, self.nextId())
		ListOf.add(self, t_model)
		return t_model

	def remove(self, comp):
		""" Remove an object from the list """
		dict.__delitem__(self, comp.objId)

	def removeById(self, obj_id):
		""" Remove an object from the list """
		dict.__delitem__(self, obj_id)

	def getListOfModelDefinitions(self):
		res = []
		for internal_model in ListOf.values(self):
			res.append(internal_model)
		return res


	def getByXPath(self, xpath):

		first = xpath[0]
		xpath.pop(0)

		if first.startswith("modelDefinition") or first.startswith("sbml:modelDefinition"):

			res_match = match(r'(.+)\[@(.+)=(.+)\]', first)
			if res_match is not None:
				tokens = res_match.groups()

				if len(tokens) == 3:
					if tokens[1] == "id":
						return self.getBySbmlId(tokens[2][1:-1]).getByXPath(xpath)
					elif tokens[1] == "name":
						return self.getByName(tokens[2][1:-1]).getByXPath(xpath)

		# If not returned yet
		raise InvalidXPath(first)