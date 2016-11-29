#!/usr/bin/env python
""" UnitDefinition.py


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


from libsignetsim.model.sbmlobject.HasId import HasId
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

class UnitDefinition(HasId):


    def __init__ (self, model, objId):

        self.__model = model
        self.objId = objId

        HasId.__init__(self, model)
        self.listOfUnits = []


    def defaultConcentrationUnit(self):

        HasId.setName(self, "nanomolars")
        HasId.setSbmlId(self, "nmol/L")

        t_unit = Unit(self.__model, len(self.listOfUnits))
        t_unit.new(UNIT_KIND_MOLE, 1, -9)

        self.listOfUnits.append(t_unit)

        t_unit = Unit(self.__model, len(self.listOfUnits))
        t_unit.new(UNIT_KIND_LITRE, -1)

        self.listOfUnits.append(t_unit)

    def defaultAmountUnit(self):

        HasId.setName(self, "nanomoles")
        HasId.setSbmlId(self, "nmol")

        t_unit = Unit(self.__model, len(self.listOfUnits))
        t_unit.new(UNIT_KIND_MOLE, 1, -9)

        self.listOfUnits.append(t_unit)


    def defaultTimeUnits(self):

        HasId.setName(self, "seconds")
        HasId.setSbmlId(self, "s")

        t_unit = Unit(self.__model, len(self.listOfUnits))
        t_unit.new(UNIT_KIND_SECOND)

        self.listOfUnits.append(t_unit)

    def defaultCompartmentUnits(self):

        HasId.setName(self, "litres")
        HasId.setSbmlId(self, "L")

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


    def copy(self, obj, prefix="", shift=0):

        HasId.copy(self, obj, prefix, shift)

        for unit in obj.listOfUnits:
            t_unit = Unit(self.__model, unit.objId)
            t_unit.copy(unit, prefix, shift)
            self.listOfUnits.append(t_unit)


    def readSbml(self, unitDefinition, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

        HasId.readSbml(self, unitDefinition, sbml_level, sbml_version)

        for unit in unitDefinition.getListOfUnits():
            t_unit = Unit(self.__model, len(self.listOfUnits))
            t_unit.readSbml(unit, sbml_level, sbml_version)
            self.listOfUnits.append(t_unit)


    def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

        t_unitDefinition = sbml_model.createUnitDefinition()

        HasId.writeSbml(self, t_unitDefinition, sbml_level, sbml_version)

        for unit in self.listOfUnits:
            unit.writeSbml(t_unitDefinition, sbml_level, sbml_version)


    def prettyPrint(self):

        return self.getName() + " (" + self.printUnitDefinition() + ")"

    def printUnitDefinition(self):

        if len(self.listOfUnits) > 0:
            t_unit = ""
            i_unit = 0
            for unit in self.listOfUnits:
                if unit.exponent > 0:
                    if i_unit > 0:
                        t_unit += "."
                    t_unit += unit.printUnit()
                    i_unit += 1

            for unit in self.listOfUnits:
                if unit.exponent < 0:
                    if i_unit > 0:
                        t_unit += "."
                    t_unit += unit.printUnit()
                    i_unit += 1

            return t_unit
        else:
            return "UNDEFINED"
    #
    #
    # def printUnitDefinition(self):
    #
    #     if len(self.listOfUnits) > 0:
    #         t_unit = ""
    #         for i_unit, unit in enumerate(self.listOfUnits):
    #
    #             if i_unit > 0:
    #                 t_unit += "."
    #             t_unit += unit.printUnit()
    #
    #         return t_unit
    #     else:
    #         return "UNDEFINED"


    def newUnit(self):
        self.listOfUnits.append(Unit(self.__model, len(self.listOfUnits)))


    def deleteUnit(self, objId):
        self.listOfUnits.remove(self.listOfUnits[objId])



class Unit():

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


    def printUnit(self):
        t_str = ""
        if self.multiplier != 1:
            t_str += "(%g." % self.multiplier

        if self.scale == -3:
            t_str = "m"
        elif self.scale == -6:
            t_str = "u"
        elif self.scale == -9:
            t_str = "n"
        elif self.scale == +3:
            t_str = "k"
        elif self.scale == +6:
            t_str = "M"
        elif self.scale == +9:
            t_str = "G"

        t_str += self.unit_id[self.kind] + ("^" + str(self.exponent) if self.exponent != 1 else "")

        if self.multiplier != 1:
            t_str += ")"
        return t_str