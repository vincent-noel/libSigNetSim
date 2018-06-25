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

		for model in self:
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
		for internal_model in self:
			res.append(internal_model)
		return res

	def resolveXPath(self, selector):

		if selector.startswith("modelDefinition") or selector.startswith("sbml:modelDefinition"):

			res_match = match(r'(.+)\[@(.+)=\'(.+)\'\]', selector)
			if res_match is not None:
				tokens = res_match.groups()

				if len(tokens) == 3:
					if tokens[1] == "id":
						return self.getBySbmlId(tokens[2])
					elif tokens[1] == "name":
						return self.getByName(tokens[2])

		# If not returned yet
		raise InvalidXPath(selector)


	def getByXPath(self, xpath):
		return self.resolveXPath(xpath[0]).getByXPath(xpath[1:])

	def setByXPath(self, xpath, value):
		self.resolveXPath(xpath[0]).setByXPath(xpath[1:], value)