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

from libsignetsim.model.sbml.FunctionDefinition import FunctionDefinition
from libsignetsim.settings.Settings import Settings


class ListOfFunctionDefinitions(ListOf, HasIds, SbmlObject):
	""" Class for the listOfFunctionDefinitions in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_functions,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads the list of events from a sbml model """

		for function in sbml_functions:
			t_function = FunctionDefinition(self.__model, self.nextId())
			t_function.readSbml(function, sbml_level, sbml_version)
			ListOf.add(self, t_function)

		SbmlObject.readSbml(self, sbml_functions, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
						sbml_level=Settings.defaultSbmlLevel,
						sbml_version=Settings.defaultSbmlVersion):
		""" Writes the list of events to a sbml model """

		for function_definition in self:
			function_definition.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self) > 0:
			SbmlObject.writeSbml(self, sbml_model.getListOfFunctionDefinitions(), sbml_level, sbml_version)


	def copy(self, obj, deletions=[], sids_subs={}):

		if obj not in deletions:
			SbmlObject.copy(self, obj)
			for function_definition in obj:
				if function_definition not in deletions:
					t_function = FunctionDefinition(self.__model, self.nextId())
					t_function.copy(function_definition, sids_subs=sids_subs)
					ListOf.add(self, t_function)



	# We should overload remove to check if the functions are not used before deleting them
