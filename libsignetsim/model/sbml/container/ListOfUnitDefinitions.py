#!/usr/bin/env python
""" ListOfUnitDefinitions.py


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

from libsignetsim.model.sbml.UnitDefinition import UnitDefinition
from libsignetsim.settings.Settings import Settings
from copy import deepcopy

class ListOfUnitDefinitions(ListOf, HasIds, SbmlObject):

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_unitDefinitions,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		for unitDefinition in sbml_unitDefinitions:
			t_unitDefinition = UnitDefinition(self.__model, self.nextId())
			t_unitDefinition.readSbml(unitDefinition, sbml_level, sbml_version)
			ListOf.add(self, t_unitDefinition)

		SbmlObject.readSbml(self, sbml_unitDefinitions, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		for unitDefinition in ListOf.values(self):
			unitDefinition.writeSbml(sbml_model, sbml_level, sbml_version)

		SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


	def new(self):

		t_unitDefinition = UnitDefinition(self.__model, self.nextId())
		ListOf.add(self, t_unitDefinition)
		return t_unitDefinition


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}):


		if len(self.keys()) > 0:
			t_shift = max(self.keys())+1
		else:
			t_shift = 0


		if obj not in deletions:

			SbmlObject.copy(self, obj, prefix, t_shift)

			for unit_definition in obj.values():
				if unit_definition not in deletions:

					obj_id = unit_definition.objId + t_shift
					t_definition = UnitDefinition(self.__model, obj_id)

					# if not unit_definition.isMarkedToBeReplaced:
					t_definition.copy(unit_definition, prefix, t_shift)
					# else:
					#     t_definition.copy(unit_definition.isMarkedToBeReplacedBy, prefix, t_shift)
					#
					# if unit_definition.isMarkedToBeRenamed:
					#     t_definition.setSbmlId(unit_definition.getSbmlId(), model_wide=False)

					ListOf.add(self, t_definition)


	def getAmountUnit(self, unit, compartment_unit):

		new_unit = deepcopy(unit)
		new_comp_unit = deepcopy(compartment_unit)
		new_comp_unit.listOfUnits[0].exponent *= -1

		new_unit_list = []
		for t_units in new_unit.listOfUnits:
			if not t_units.isEqual(new_comp_unit.listOfUnits[0]):
				new_unit_list.append(t_units)

		new_unit.listOfUnits = new_unit_list


		if not self.containsUnits(new_unit):
			ListOf.add(self, new_unit)
			return new_unit
		else:

			return self.getExistingUnits(new_unit)
		# return new_unit


	def getConcentrationUnit(self, unit, compartment_unit):

		new_unit = deepcopy(unit)
		new_comp_unit = deepcopy(compartment_unit)
		new_comp_unit.listOfUnits[0].exponent = new_comp_unit.listOfUnits[0].exponent * -1
		new_unit.listOfUnits = new_unit.listOfUnits + new_comp_unit.listOfUnits

		if not self.containsUnits(new_unit):
			ListOf.add(self, new_unit)
			return new_unit
		else:
			# We return the one already in the list, not the computed one
			return self.getExistingUnits(new_unit)


	def getExistingUnits(self, units):

		for t_unit in ListOf.values(self):
			if units.isEqual(t_unit):
				return t_unit


	def containsUnits(self, units):

		for t_unit in ListOf.values(self):
			if units.isEqual(t_unit):
				return True

		return False

	def isUnitIdAvailable(self, unit_id):
		return unit_id not in ListOf.keys(self)
