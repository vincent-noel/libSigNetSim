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
from libsignetsim.model.ModelException import CannotDeleteException, InvalidXPath
from libsignetsim.model.sbml.SubModel import SubModel
from libsignetsim.settings.Settings import Settings
from re import match


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
			t_submodel = SubModel(self.__model, self.nextId())
			t_submodel.readSbml(submodel, sbml_level, sbml_version)
			ListOf.add(self, t_submodel)

		# SbmlObject.readSbml(self, sbml_list_submodels, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes compartments' list to a sbml file """

		for t_submodel in self:
			t_submodel.writeSbml(sbml_model, sbml_level, sbml_version)

		# SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


	def new(self):
		""" Creates a new compartment """

		t_submodel = SubModel(self.__model, self.nextId())
		ListOf.add(self, t_submodel)
		return t_submodel


	def remove(self, sbml_obj):
		""" Remove an object from the list """

		for object in self.__model.listOfSbmlObjects:
			if object.hasReplacedElements() and object.getListOfReplacedElements().containsSubmodel(sbml_obj.getSbmlId()):
				raise CannotDeleteException("Submodel %s is used. Please remove the substitutions first" % sbml_obj.getNameOrSbmlId())

		list.remove(self, sbml_obj)

	def removeById(self, obj_id):
		""" Remove an object from the list """
		self.remove(self.getById(obj_id))

	def getSubmodels(self):

		res = []
		for submodel in self:
			res.append(submodel.getModelObject())

		return res

	def getBySbmlId(self, sbml_id_ref):
		return HasIds.getBySbmlId(self, sbml_id_ref)

	def getBySbmlIdRef(self, sbml_id):
		for submodel in self:
			if submodel.getModelObject().getSbmlId() == sbml_id:
				return submodel

	def resolveXPath(self, selector):

		if not (selector.startswith("submodel") or selector.startswith("sbml:submodel")):
			raise InvalidXPath(selector)

		res_match = match(r'(.*)\[@(.*)=\'(.*)\'\]', selector)
		if res_match is None:
			raise InvalidXPath(selector)


		tokens = res_match.groups()
		if len(tokens) != 3:
			raise InvalidXPath(selector)

		object = None
		if tokens[1] == "id":
			object = HasIds.getBySbmlId(self, tokens[2])
		elif tokens[1] == "name":
			object = HasIds.getByName(self, tokens[2])

		if object is not None:
			return object

		# If not returned yet
		raise InvalidXPath(selector)

	def getByXPath(self, xpath):
		return self.resolveXPath(xpath[0]).getByXPath(xpath[1:])

	def setByXPath(self, xpath, object):
		self.resolveXPath(xpath[0]).setByXPath(xpath[1:], object)
