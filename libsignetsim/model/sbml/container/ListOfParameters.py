#!/usr/bin/env python
""" ListOfParameters.py


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
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.model.sbml.Parameter import Parameter
from libsignetsim.settings.Settings import Settings


class ListOfParameters(ListOf, HasIds, SbmlObject):
	""" Class for the ListOfParameters in a sbml model """

	def __init__ (self, model, are_local_parameters=False, reaction=None):

		self.__model = model

		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)

		self.are_local_parameters = are_local_parameters
		self.reaction = reaction


	def readSbml(self, sbml_list_of_parameters, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion, reaction=None):
		""" Reads parameters' list from a sbml file """

		for sbml_parameter in sbml_list_of_parameters:
			t_parameter = Parameter(self.__model, self.nextId(),
									local_parameter=self.are_local_parameters,
									reaction=self.reaction)
			t_parameter.readSbml(sbml_parameter, sbml_level, sbml_version)
			ListOf.add(self, t_parameter)

		SbmlObject.readSbml(self, sbml_list_of_parameters, sbml_level, sbml_version)


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes parameters' list to a sbml file """

		for parameter in ListOf.values(self):
			parameter.writeSbml(sbml_model, sbml_level, sbml_version)

		SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


	def new(self, parameter=None):
		""" Creates new parameter """

		t_parameter = Parameter(self.__model, self.nextId(),
								local_parameter=self.are_local_parameters,
								reaction=self.reaction)
		t_parameter.new(parameter)
		ListOf.add(self, t_parameter)
		return t_parameter


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}):

		if len(self.keys()) > 0:
			t_shift = max(self.keys())+1
		else:
			t_shift = 0


		if obj not in deletions:

			SbmlObject.copy(self, obj, prefix, t_shift)

			for parameter in obj.values():

				if parameter not in deletions:
					obj_id = parameter.objId + t_shift
					t_parameter = Parameter(self.__model, obj_id,
									local_parameter=parameter.localParameter,
									reaction=parameter.reaction)

					if not parameter.isMarkedToBeReplaced:
						t_parameter.copy(parameter, prefix, t_shift, subs, deletions, replacements)
					else:
						t_parameter.copy(parameter.isMarkedToBeReplacedBy, prefix, t_shift, subs, deletions, replacements)


					if parameter.isMarkedToBeRenamed:
						t_parameter.setSbmlId(parameter.getSbmlId(), model_wide=False)

					ListOf.add(self, t_parameter)


	def remove(self, parameter):
		""" Remove an object from the list """

		if parameter.isInRules():
			raise ModelException(ModelException.SBML_ERROR, "Parameter in used in rules")

		self.__model.listOfVariables.removeVariable(parameter)
		# self.model.listOfSbmlIds.removeSbmlId(parameter)
		ListOf.remove(self, parameter)


	def removeById(self, parameter_obj_id):
		""" Remove an object from the list """

		self.remove(self.getById(parameter_obj_id))
