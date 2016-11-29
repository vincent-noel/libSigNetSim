#!/usr/bin/env python
""" HasId.py


	This file is the parent class for all objects having ids/names


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


from libsignetsim.settings.Settings import Settings
from string import punctuation
from sympy import Symbol

class HasId(object):

    def __init__(self, model):

        self.__model = model

        self.__sbmlId = None
        self.__name = None


    def new(self, name=None, sbml_id=None):

        if name is None:
            self.newName()
        else:
            self.__name = name

        if sbml_id is not None:
            self.__sbmlId = sbml_id

    def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}):

        self.__sbmlId = prefix + obj.getSbmlId()
        self.setName(obj.getName())


    def newName(self):


            if self.isSpecies():
                self.__name = "Species %d" % self.objId
            elif self.isParameter():
                self.__name = "Parameter %d" % self.objId
            elif self.isCompartment():
                self.__name = "Compartment %d" % self.objId
            elif self.isReaction():
                self.__name = "Reaction %d" % self.objId

            else:
                self.__name = ""



    def readSbml(self, sbml_variable,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):

        if sbml_level >= 2:
            self.__sbmlId = sbml_variable.getId()
        else:
            self.__sbmlId = sbml_variable.getName()

        if sbml_variable.isSetName():
            self.__name = sbml_variable.getName()



    def writeSbml(self, sbml_variable,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):

        if self.__sbmlId is not None:
            if sbml_level >= 2:
                sbml_variable.setId(self.__sbmlId)
            else:
                sbml_variable.setName(self.__sbmlId)

        if self.__name is not None:
            sbml_variable.setName(self.__name)


    def getNameOrSbmlId(self):

        if self.getName() is None:
            return self.getSbmlId()
        else:
            return self.getName()


    def getSbmlId(self):
        return self.__sbmlId

    def getName(self):
        return self.__name

    def setSbmlId(self, sbml_id, prefix="", model_wide=True):

        t_sbml_id = prefix + sbml_id.strip()
        if self.__sbmlId is not None and self.__sbmlId != t_sbml_id:
            if model_wide:
                print "renaming model wide : %s to %s" % (self.__sbmlId, t_sbml_id)
                self.__model.renameSbmlId(self.__sbmlId, t_sbml_id)
            else:
                self.__model.listOfVariables.renameSbmlId(self.__sbmlId, t_sbml_id)

        self.__sbmlId = t_sbml_id

    def setName(self, name):
        self.__name = name

    def getIdFromName(self, name):

        res_sbml_id = name.replace(" ", "_")
        res_sbml_id = res_sbml_id.replace("-", "_")
        forbidden_chars = list(set(punctuation) - set('_'))
        for t_char in forbidden_chars:
            res_sbml_id = res_sbml_id.replace(t_char,"")
        return res_sbml_id