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

from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.Unit import Unit
from libsignetsim.settings.Settings import Settings

from libsbml import UNIT_KIND_AMPERE, UNIT_KIND_AVOGADRO, UNIT_KIND_BECQUEREL,\
	UNIT_KIND_CANDELA, UNIT_KIND_COULOMB, UNIT_KIND_DIMENSIONLESS,\
	UNIT_KIND_FARAD, UNIT_KIND_GRAM, UNIT_KIND_GRAY, UNIT_KIND_HENRY,\
	UNIT_KIND_HERTZ, UNIT_KIND_ITEM, UNIT_KIND_JOULE, UNIT_KIND_KATAL,\
	UNIT_KIND_KELVIN, UNIT_KIND_KILOGRAM, UNIT_KIND_LITRE, UNIT_KIND_LUMEN,\
	UNIT_KIND_LUX, UNIT_KIND_METRE, UNIT_KIND_MOLE, UNIT_KIND_NEWTON,\
	UNIT_KIND_OHM, UNIT_KIND_PASCAL, UNIT_KIND_RADIAN, UNIT_KIND_SECOND,\
	UNIT_KIND_SIEMENS, UNIT_KIND_SIEVERT, UNIT_KIND_STERADIAN, UNIT_KIND_TESLA,\
	UNIT_KIND_VOLT, UNIT_KIND_WATT, UNIT_KIND_WEBER, UNIT_KIND_INVALID

class UnitDefinition(HasId, SbmlObject):


	def __init__ (self, model, objId=0):

		self.__model = model
		self.objId = objId

		SbmlObject.__init__(self, model)
		HasId.__init__(self, model)

		self.listOfUnits = []

	def defaultConcentrationUnit(self):

		HasId.setName(self, "nanomolars")
		HasId.setSbmlId(self, "nanomolars")

		t_unit = Unit(self.__model, len(self.listOfUnits))
		t_unit.new(UNIT_KIND_MOLE, 1, -9)

		self.listOfUnits.append(t_unit)

		t_unit = Unit(self.__model, len(self.listOfUnits))
		t_unit.new(UNIT_KIND_LITRE, -1)

		self.listOfUnits.append(t_unit)

	def defaultAmountUnit(self):

		HasId.setName(self, "nanomoles")
		HasId.setSbmlId(self, "nanomoles")

		t_unit = Unit(self.__model, len(self.listOfUnits))
		t_unit.new(UNIT_KIND_MOLE, 1, -9)

		self.listOfUnits.append(t_unit)


	def defaultTimeUnits(self):

		HasId.setName(self, "seconds")
		HasId.setSbmlId(self, "seconds")

		t_unit = Unit(self.__model, len(self.listOfUnits))
		t_unit.new(UNIT_KIND_SECOND)

		self.listOfUnits.append(t_unit)

	def defaultCompartmentUnits(self):

		HasId.setName(self, "litres")
		HasId.setSbmlId(self, "litres")

		t_unit = Unit(self.__model, len(self.listOfUnits))
		t_unit.new(UNIT_KIND_LITRE)

		self.listOfUnits.append(t_unit)



	def isEqual(self, other_units):

		if len(self.listOfUnits) == len(other_units.listOfUnits):
			found = False
			for i, t_unit in enumerate(self.listOfUnits):
				found = False

				for t_other_unit in other_units.listOfUnits:

					if t_unit.isEqual(t_other_unit):
						found = True
				if found == False:
					return False
			if found == True:

				return True
			else:

				return False
		else:
			return False


	def copy(self, obj, usids_subs={}):

		HasId.copy(self, obj, sids_subs=usids_subs)

		for unit in obj.listOfUnits:
			t_unit = Unit(self.__model, len(self.listOfUnits))
			t_unit.copy(unit)
			self.listOfUnits.append(t_unit)


	def readSbml(self, unitDefinition, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		SbmlObject.readSbml(self, unitDefinition, sbml_level, sbml_version)
		HasId.readSbml(self, unitDefinition, sbml_level, sbml_version)

		for unit in unitDefinition.getListOfUnits():
			t_unit = Unit(self.__model, len(self.listOfUnits))
			t_unit.readSbml(unit, sbml_level, sbml_version)
			self.listOfUnits.append(t_unit)


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		t_unitDefinition = sbml_model.createUnitDefinition()
		SbmlObject.writeSbml(self, t_unitDefinition, sbml_level, sbml_version)
		HasId.writeSbml(self, t_unitDefinition, sbml_level, sbml_version)

		for unit in self.listOfUnits:
			unit.writeSbml(t_unitDefinition, sbml_level, sbml_version)


	def __str__(self):

		return self.getName() + " (" + self.printUnitDefinition() + ")"

	def printUnitDefinition(self):

		if len(self.listOfUnits) > 0:
			t_unit = ""
			i_unit = 0
			for unit in self.listOfUnits:
				if unit.exponent > 0:
					if i_unit > 0:
						t_unit += "."
					t_unit += str(unit)
					i_unit += 1

			for unit in self.listOfUnits:
				if unit.exponent < 0:
					if i_unit > 0:
						t_unit += "."
					t_unit += str(unit)
					i_unit += 1

			return t_unit
		else:
			return "UNDEFINED"



	def newUnit(self):
		self.listOfUnits.append(Unit(self.__model, len(self.listOfUnits)))
		return self.listOfUnits[len(self.listOfUnits)-1]

	def deleteUnit(self, objId):
		self.listOfUnits.remove(self.listOfUnits[objId])
