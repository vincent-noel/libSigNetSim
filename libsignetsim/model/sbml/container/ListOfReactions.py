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
from libsignetsim.model.sbml.Reaction import Reaction
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.settings.Settings import Settings

from re import match


class ListOfReactions(ListOf, HasIds, SbmlObject, HasParentObj):
	""" Class for the list of reactions in a sbml model """

	def __init__ (self, model, parent_obj):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)
		HasParentObj.__init__(self, parent_obj)

	def readSbml(self, sbml_listOfReactions,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads a list of reactions from a sbml file """

		for sbml_reaction in sbml_listOfReactions:
			t_reaction = Reaction(self.__model, self, self.nextId())
			ListOf.add(self, t_reaction)
			t_reaction.readSbml(sbml_reaction, sbml_level, sbml_version)

		SbmlObject.readSbml(self, sbml_listOfReactions, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes a list of reactions from a sbml file """

		for reaction in self:
			reaction.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self):
			SbmlObject.writeSbml(self, sbml_model.getListOfReactions(), sbml_level, sbml_version)

	def new(self, name=None):

		t_reaction = Reaction(self.__model, self, self.nextId())
		t_reaction.new(name)
		ListOf.add(self, t_reaction)
		return t_reaction

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factors={},
				extent_conversion=None, time_conversion=None):

		if obj not in deletions:
			SbmlObject.copy(self, obj)
			for reaction in obj:
				if reaction not in deletions:

					t_reaction = Reaction(self.__model, self, self.nextId())
					t_reaction.copy(
						reaction,
						deletions=deletions,
						sids_subs=sids_subs,
						symbols_subs=symbols_subs,
						usids_subs=usids_subs,
						conversion_factors=conversion_factors,
						extent_conversion=extent_conversion,
						time_conversion=time_conversion
					)
					ListOf.add(self, t_reaction)

	def remove(self, reaction):

		self.__model.listOfVariables.removeVariable(reaction)
		ListOf.remove(self, reaction)

	def containsVariable(self, variable):
		for reaction in self:
			if reaction.containsVariable(variable):
				return True
		return False

	def containsLocalParameterSbmlId(self, sbml_id):

		for reaction in self:
			if reaction.listOfLocalParameters.containsSbmlId(sbml_id):
				return True
		return False


	def getLocalParameterReactionIdBySbmlId(self, sbml_id):

		for reaction in self:
			if reaction.listOfLocalParameters.containsSbmlId(sbml_id):
				return reaction.objId
		return -1


	def getLocalParameterIdBySbmlId(self, sbml_id):

		for reaction in self:
			if reaction.listOfLocalParameters.containsSbmlId(sbml_id):
				return reaction.listOfLocalParameters.getBySbmlId(sbml_id).objId
		return -1

	def countLocalParameters(self):

		nb_local_parameters = 0
		for reaction in self:
			nb_local_parameters += len(reaction.listOfLocalParameters)

		return nb_local_parameters

	def hasFastReaction(self):

		for reaction in self:
			if reaction.fast:
				return True
		return False

	def hasVariableStoichiometry(self):

		for reaction in self:
			if reaction.hasVariableStoichiometry():
				return True
		return False

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		for obj in self:
			obj.renameSbmlId(old_sbml_id, new_sbml_id)



	def resolveXPath(self, selector):

		if not (selector.startswith("reaction") or selector.startswith("sbml:reaction")):
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
		return "/".join([self.getParentObj().getXPath(), "sbml:listOfReactions"])

