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
from libsignetsim.model.ModelException import CannotDeleteException, InvalidXPath
from libsignetsim.model.sbml.Parameter import Parameter
from libsignetsim.settings.Settings import Settings

from re import match


class ListOfParameters(ListOf, HasIds, SbmlObject, HasParentObj):
	""" Class for the ListOfParameters in a sbml model """

	def __init__ (self, model, parent_obj, are_local_parameters=False, reaction=None):

		self.__model = model

		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)
		HasParentObj.__init__(self, parent_obj)

		self.are_local_parameters = are_local_parameters
		self.reaction = reaction


	def readSbml(self, sbml_list_of_parameters, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion, reaction=None):
		""" Reads parameters' list from a sbml file """

		for sbml_parameter in sbml_list_of_parameters:
			t_parameter = Parameter(self.__model, self, self.nextId(),
									local_parameter=self.are_local_parameters,
									reaction=self.reaction)
			t_parameter.readSbml(sbml_parameter, sbml_level, sbml_version)
			ListOf.add(self, t_parameter)

		SbmlObject.readSbml(self, sbml_list_of_parameters, sbml_level, sbml_version)


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes parameters' list to a sbml file """

		for parameter in self:
			parameter.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self) > 0:
			SbmlObject.writeSbml(self, sbml_model.getListOfParameters(), sbml_level, sbml_version)


	def new(self, parameter=None, value=None):
		""" Creates new parameter """

		t_parameter = Parameter(self.__model, self, self.nextId(),
								local_parameter=self.are_local_parameters,
								reaction=self.reaction)
		t_parameter.new(parameter, value=value)
		ListOf.add(self, t_parameter)
		return t_parameter


	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factor=None):

		if obj not in deletions:

			SbmlObject.copy(self, obj)

			for parameter in obj:

				if parameter not in deletions:
					t_parameter = Parameter(
						self.__model, self, self.nextId(),
						local_parameter=parameter.localParameter,
						reaction=parameter.reaction
					)

					t_parameter.copy(
						parameter,
						sids_subs=sids_subs,
						symbols_subs=symbols_subs,
						usids_subs=usids_subs,
						conversion_factor=conversion_factor
					)

					ListOf.add(self, t_parameter)


	def remove(self, parameter, full_remove=True):
		""" Remove an object from the list """

		if full_remove:
			if parameter.isInRules():
				raise CannotDeleteException("Parameter in used in rules")

			if parameter.isInReactionsRates():
				raise CannotDeleteException("Parameter in used in reactions")

			self.__model.listOfVariables.removeVariable(parameter)

		ListOf.remove(self, parameter, full_remove=full_remove)


	def removeById(self, parameter_obj_id):
		""" Remove an object from the list """

		self.remove(self.getById(parameter_obj_id))


	def resolveXPath(self, selector):

		if not (selector.startswith("parameter") or selector.startswith("sbml:parameter")):
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
		if len(xpath) > 0:
			return self.resolveXPath(xpath[0]).getByXPath(xpath[1:])
		else:
			return self

	def setByXPath(self, xpath, object):
		self.resolveXPath(xpath[0]).setByXPath(xpath[1:], object)

	def getXPath(self):
		return "/".join([self.getParentObj().getXPath(), "sbml:listOfParameters"])

	def addXML(self, xml_node):
		t_parameter = Parameter(self.__model, self, self.nextId(),
								local_parameter=self.are_local_parameters,
								reaction=self.reaction)
		t_parameter.readXML(xml_node)
		ListOf.add(self, t_parameter)