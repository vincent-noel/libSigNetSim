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

from libsignetsim.model.sbml.Port import Port
from libsignetsim.settings.Settings import Settings

class ListOfPorts(ListOf, HasIds):#, SbmlObject):
    """ Class for the listOfModelDefinition in a sbml model """

    def __init__ (self, model=None):

        self.__model = model
        ListOf.__init__(self, model)
        HasIds.__init__(self, model)
        # SbmlObject.__init__(self, model)


    def readSbml(self, sbml_list_ports,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):
        """ Reads compartments' list from a sbml file """

        for port in sbml_list_ports:
            t_port = Port(self.__model, self.nextId())
            t_port.readSbml(port, sbml_level, sbml_version)
            ListOf.add(self, t_port)

        # SbmlObject.readSbml(self, sbml_list_ports, sbml_level, sbml_version)


    def writeSbml(self, sbml_model,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):
        """ Writes compartments' list to a sbml file """

        for t_port in self:
            sbml_port = sbml_model.createPort()
            t_port.writeSbml(sbml_port, sbml_level, sbml_version)

        # SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


    def new(self):
        """ Creates a new compartment """

        t_port = Port(self.__model, self.nextId())
        # t_deletion.new(name, sbml_id)
        ListOf.add(self, t_port)
        return t_port


    def remove(self, comp):
        """ Remove an object from the list """

        ListOf.remove(self, comp)


    def removeById(self, obj_id):
        """ Remove an object from the list """
        self.remove(self.getById(obj_id))