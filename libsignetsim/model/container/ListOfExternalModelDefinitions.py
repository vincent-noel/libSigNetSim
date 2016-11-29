#!/usr/bin/env python
""" ListOfExternalModelDefinitions.py


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
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject

from libsignetsim.model.sbmlobject.SbmlExternalModelDefinition import SbmlExternalModelDefinition
from libsignetsim.settings.Settings import Settings

class ListOfExternalModelDefinitions(ListOf, HasIds):#, SbmlObject):
    """ Class for the listOfExternalModelDefinition in a sbml model """

    def __init__ (self, model=None):

        self.__model = model
        ListOf.__init__(self, model)
        HasIds.__init__(self, model)
        # SbmlObject.__init__(self, model)


    def readSbml(self, sbml_external_models,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):
        """ Reads external model definitions' list from a sbml file """

        for model in sbml_external_models:
            t_model = SbmlExternalModelDefinition(self.__model, self.nextId())
            t_model.readSbml(model, sbml_level, sbml_version)
            ListOf.add(self, t_model)

        # SbmlObject.writeSbml(self, sbml_external_models, sbml_level, sbml_version)


    def writeSbml(self, sbml_document,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):
        """ Writes external model definitions' list to a sbml file """

        for model in ListOf.values(self):
            sbml_emd = sbml_document.createExternalModelDefinition()
            model.writeSbml(sbml_emd, sbml_level, sbml_version)

        # SbmlObject.writeSbml(self, sbml_document, sbml_level, sbml_version)


    def new(self):
        """ Creates a new external model definition """

        t_model = SbmlExternalModelDefinition(self.__model, self.nextId())
        ListOf.add(self, t_model)
        return t_model


    def remove(self, comp):
        """ Remove an object from the list """

        dict.__delitem__(self, comp.objId)
        # ListOf.remove(self, comp)


    def removeById(self, obj_id):
        """ Remove an object from the list """
        dict.__delitem__(self, obj_id)
        # self.remove(self.getById(obj_id))


    def getListOfModelDefinitions(self):
        res = []
        for external_model in ListOf.values(self):
            res.append(external_model)
        return res