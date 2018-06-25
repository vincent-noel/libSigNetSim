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

		for unitDefinition in self:
			unitDefinition.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self) > 0:
			SbmlObject.writeSbml(self, sbml_model.getListOfUnitDefinitions(), sbml_level, sbml_version)


	def new(self):

		t_unitDefinition = UnitDefinition(self.__model, self.nextId())
		ListOf.add(self, t_unitDefinition)
		return t_unitDefinition


	def copy(self, obj, deletions=[], usids_subs={}):

		if obj not in deletions:

			SbmlObject.copy(self, obj)

			for unit_definition in obj:
				if unit_definition not in deletions:

					t_definition = UnitDefinition(self.__model, self.nextId())
					t_definition.copy(unit_definition, usids_subs=usids_subs)
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

		for t_unit in self:
			if units.isEqual(t_unit):
				return t_unit


	def containsUnits(self, units):

		for t_unit in self:
			if units.isEqual(t_unit):
				return True

		return False

	def isUnitIdAvailable(self, unit_id):
		return unit_id not in HasIds.sbmlIds(self)
