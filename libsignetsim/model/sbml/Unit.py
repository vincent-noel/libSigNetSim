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


class Unit(object):

	unit_id = {UNIT_KIND_AMPERE: "ampere",
						UNIT_KIND_AVOGADRO: "avogadro",
						UNIT_KIND_BECQUEREL: "becquerel",
						UNIT_KIND_CANDELA: "candela",
						UNIT_KIND_COULOMB: "coulomb",
						UNIT_KIND_DIMENSIONLESS: "dimensionless",
						UNIT_KIND_FARAD: "farad",
						UNIT_KIND_GRAM: "gram",
						UNIT_KIND_GRAY: "gray",
						UNIT_KIND_HENRY: "henry",
						UNIT_KIND_HERTZ: "hertz",
						UNIT_KIND_ITEM: "thing",
						UNIT_KIND_JOULE: "joule",
						UNIT_KIND_KATAL: "katal",
						UNIT_KIND_KELVIN: "kelvin",
						UNIT_KIND_KILOGRAM: "kilogram",
						UNIT_KIND_LITRE: "litre",
						UNIT_KIND_LUMEN: "lumen",
						UNIT_KIND_LUX: "lux",
						UNIT_KIND_METRE: "metre",
						UNIT_KIND_MOLE: "mole",
						UNIT_KIND_NEWTON: "newton",
						UNIT_KIND_OHM: "ohm",
						UNIT_KIND_PASCAL: "pascal",
						UNIT_KIND_RADIAN: "radian",
						UNIT_KIND_SECOND: "second",
						UNIT_KIND_SIEMENS: "siemens",
						UNIT_KIND_SIEVERT: "sievert",
						UNIT_KIND_STERADIAN: "steradian",
						UNIT_KIND_TESLA: "tesla",
						UNIT_KIND_VOLT: "volt",
						UNIT_KIND_WATT: "watt",
						UNIT_KIND_WEBER: "weber",
						UNIT_KIND_INVALID: "invalid"
	}


	def __init__(self, model=None, objId=None):

		self.__model = model
		self.objId = objId
		self.kind = UNIT_KIND_MOLE
		self.exponent = 1
		self.scale = 0
		self.multiplier = 1


	def new(self, kind = UNIT_KIND_MOLE, exponent=1, scale=1, multiplier=1):

		self.kind = kind
		self.exponent = exponent
		self.scale = scale
		self.multiplier = multiplier


	def copy(self, obj, prefix="", shift=0):

		self.kind = obj.kind
		self.exponent = obj.exponent
		self.scale = obj.scale
		self.multiplier = obj.multiplier


	def isEqual(self, other_unit):

		return (self.exponent == other_unit.exponent
			and self.multiplier*(10**self.scale) == other_unit.multiplier*(10**other_unit.scale))


	def readSbml(self, unit, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		self.kind = int(unit.getKind())

		if unit.isSetExponent():
			self.exponent = int(unit.getExponent())

		if unit.isSetScale():
			self.scale = int(unit.getScale())

		if unit.isSetMultiplier():
			self.multiplier = float(unit.getMultiplier())


	def writeSbml(self, unitDefinition, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		t_unit = unitDefinition.createUnit()

		t_unit.setKind(self.kind)

		if self.exponent != 1 or sbml_level == 3:
			t_unit.setExponent(self.exponent)

		if self.scale != 0 or sbml_level == 3:
			t_unit.setScale(self.scale)

		if self.multiplier != 1 or sbml_level == 3:
			t_unit.setMultiplier(self.multiplier)


	def setKind(self, kind):
		self.kind = kind


	def setExponent(self, exponent):
		self.exponent = exponent


	def setScale(self, scale):
		self.scale = scale

	def __str__(self):
		t_str = ""
		if self.multiplier != 1:
			t_str += "(%g." % self.multiplier

		if self.scale == -3:
			t_str += "m"
		elif self.scale == -6:
			t_str += "u"
		elif self.scale == -9:
			t_str += "n"
		elif self.scale == +3:
			t_str += "k"
		elif self.scale == +6:
			t_str += "M"
		elif self.scale == +9:
			t_str += "G"

		t_str += self.unit_id[self.kind] + ("^" + str(self.exponent) if self.exponent != 1 else "")

		if self.multiplier != 1:
			t_str += ")"
		return t_str

	def getKind(self):
		return self.kind

	def getKindName(self):
		return self.unit_id[self.kind]

	def getExponent(self):
		return self.exponent

	def getScale(self):
		return self.scale

	def getMultiplier(self):
		return self.multiplier
