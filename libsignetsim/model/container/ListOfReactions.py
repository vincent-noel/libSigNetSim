#!/usr/bin/env python
""" ListOfReactions.py


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
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.model.sbml.Reaction import Reaction
from libsignetsim.settings.Settings import Settings

class ListOfReactions(ListOf, HasIds, SbmlObject):
	""" Class for the list of reactions in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_listOfReactions,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads a list of reactions from a sbml file """

		for sbml_reaction in sbml_listOfReactions:
			t_reaction = Reaction(self.__model, self.nextId())
			ListOf.add(self, t_reaction)
			t_reaction.readSbml(sbml_reaction, sbml_level, sbml_version)

		SbmlObject.readSbml(self, sbml_listOfReactions, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes a list of reactions from a sbml file """

		for reaction in ListOf.values(self):
			reaction.writeSbml(sbml_model, sbml_level, sbml_version)

		SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


	def new(self, name=None):

		t_reaction = Reaction(self.__model, self.nextId())
		t_reaction.new(name)
		ListOf.add(self, t_reaction)
		return t_reaction


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[],
				replacements={}, conversions={},
				extent_conversion=None, time_conversion=None):

		if len(self.keys()) > 0:
			t_shift = max(self.keys())+1
		else:
			t_shift = 0


		if obj not in deletions:
			SbmlObject.copy(self, obj, prefix, t_shift)
			for reaction in obj.values():
				if reaction not in deletions:
					t_obj_id = reaction.objId + t_shift
					t_reaction = Reaction(self.__model, t_obj_id)

					if not reaction.isMarkedToBeReplaced:
						t_reaction.copy(reaction, prefix, t_shift, subs,
											deletions, replacements,
											conversions, extent_conversion,
											time_conversion)
					else:
						t_reaction.copy(reaction.isMarkedToBeReplacedBy,
											prefix, t_shift, subs, deletions,
											replacements, conversions,
											extent_conversion,
											time_conversion)

					if reaction.isMarkedToBeRenamed:
						t_reaction.setSbmlId(reaction.getSbmlId(),
											model_wide=False)

					ListOf.add(self, t_reaction)


	def remove(self, reaction):

		self.__model.listOfVariables.removeVariable(reaction)
		ListOf.remove(self, reaction)


	def containsLocalParameterSbmlId(self, sbml_id):

		for reaction in ListOf.values(self):
			if reaction.listOfLocalParameters.containsSbmlId(sbml_id):
				return True
		return False


	def getLocalParameterReactionIdBySbmlId(self, sbml_id):

		for reaction in ListOf.values(self):
			if reaction.listOfLocalParameters.containsSbmlId(sbml_id):
				return reaction.objId
		return -1


	def getLocalParameterIdBySbmlId(self, sbml_id):

		for reaction in ListOf.values(self):
			if reaction.listOfLocalParameters.containsSbmlId(sbml_id):
				return reaction.listOfLocalParameters.getBySbmlId(sbml_id).objId
		return -1

	def countLocalParameters(self):

		nb_local_parameters = 0
		for reaction in ListOf.values(self):
			nb_local_parameters += len(reaction.listOfLocalParameters)

		return nb_local_parameters

	def hasFastReaction(self):

		for reaction in ListOf.values(self):
			if reaction.fast:
				return True
		return False

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		for obj in ListOf.values(self):
			obj.renameSbmlId(old_sbml_id, new_sbml_id)
