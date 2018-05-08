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
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.Compartment import Compartment
from libsignetsim.model.ModelException import CannotDeleteException, InvalidXPath
from libsignetsim.settings.Settings import Settings

from re import match


class ListOfCompartments(ListOf, HasIds, SbmlObject, HasParentObj):
	""" Class for the listOfCompartments in a sbml model """

	def __init__ (self, model, parent_obj):

		self.__model = model

		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)
		HasParentObj.__init__(self, parent_obj)

	def readSbml(self, sbml_compartments,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads compartments' list from a sbml file """

		for compartment in sbml_compartments:
			t_compartment = Compartment(self.__model, self, self.nextId())
			t_compartment.readSbml(compartment, sbml_level, sbml_version)
			ListOf.add(self, t_compartment)

		SbmlObject.readSbml(self, sbml_compartments, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes compartments' list to a sbml file """

		for compartment in self:
			compartment.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self) > 0:
			SbmlObject.writeSbml(self, sbml_model.getListOfCompartments(), sbml_level, sbml_version)


	def new(self, name=None, sbml_id=None, value=1, constant=True, unit=None):
		""" Creates a new compartment """

		t_compartment = Compartment(self.__model, self, self.nextId())
		t_compartment.new(name, sbml_id, value, constant, unit)
		ListOf.add(self, t_compartment)
		return t_compartment

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factors=None):

		if obj not in deletions:

			SbmlObject.copy(self, obj)

			for compartment in obj:
				if compartment not in deletions:

					t_compartment = Compartment(self.__model, self, self.nextId())
					t_compartment.copy(
						compartment,
						sids_subs=sids_subs,
						symbols_subs=symbols_subs,
						usids_subs=usids_subs,
						conversion_factors=conversion_factors
					)
					ListOf.add(self, t_compartment)


	def remove(self, comp):
		""" Remove an object from the list """

		t_nb_species = comp.getNbSpecies()
		if t_nb_species > 0:
			message = "Compartment contains %d species" % t_nb_species
			raise CannotDeleteException(message)

		self.__model.listOfVariables.removeVariable(comp)
		ListOf.remove(self, comp)


	def removeById(self, obj_id):
		""" Remove an object from the list """
		self.remove(ListOf.getById(self, obj_id))


	def resolveXPath(self, selector):

		if not (selector.startswith("compartment") or selector.startswith("sbml:compartment")):
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
		return "/".join([self.getParentObj().getXPath(), "sbml:listOfCompartments"])
