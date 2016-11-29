#!/usr/bin/env python
""" HasUnits.py


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


from libsignetsim.model.sbmlobject.UnitDefinition import UnitDefinition
from libsignetsim.settings.Settings import Settings

class HasUnits(object):


    def __init__ (self, model):

        self.__model = model
        self.__unit = None
        self.__builtinUnit = False


    def readSbml(self, sbml_object, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
        """ Reads a parameter from a sbml file """
        if sbml_object.isSetUnits():
            if self.__model.listOfUnitDefinitions.containsSbmlId(sbml_object.getUnits()):
                self.__unit = sbml_object.getUnits()
            elif sbml_level < 3:
                self.__builtinUnit = True
                self.__unit = sbml_object.getUnits()


    def writeSbml(self, sbml_object, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
        """ Writes a parameter to  a sbml file """

        if self.__unit is not None:
            if self.__builtinUnit is False:
                sbml_object.setUnits(self.__unit)
            if self.__builtinUnit is True and sbml_level < 3:
                sbml_object.setUnits(self.__unit)


    def new(self, unit=None):

        self.setUnits(unit)


    def setUnits(self, unit, prefix=""):
        if unit is not None:
            self.__unit = prefix + unit.getSbmlId()


    def getUnits(self):
        if self.__unit is not None:
            if self.__builtinUnit:
                return self.__unit
            else:
                return self.__model.listOfUnitDefinitions.getBySbmlId(self.__unit)
        else:
            return None


    def setUnitId(self, unit_id, prefix=""):
        if unit_id is not None:
            self.__unit = prefix + unit_id

    def getUnitId(self):
        return self.__unit

    def hasUnits(self):
        return self.__unit is not None


    def setDefaultVolumeUnit(self):
        self.__unit = "volume"


    def copy(self, obj, prefix="", shift=0):
        self.setUnitId(obj.getUnitId(), prefix)