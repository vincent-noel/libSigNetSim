#!/usr/bin/env python
""" SbmlModelDefinition.py




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
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject

from libsignetsim.model.Model import Model
from libsignetsim.settings.Settings import Settings

class SbmlModelDefinition(HasId, SbmlObject):

    def __init__(self, model, obj_id):

        self.__model = model
        self.objId = obj_id

        HasId.__init__(self, model)
        SbmlObject.__init__(self, model)

        self.modelDefinition = Model(obj_id=self.objId, parent_doc=self.__model.parentDoc)


    def readSbml(self, sbml_model_definition,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):

        HasId.readSbml(self, sbml_model_definition, sbml_level, sbml_version)
        self.modelDefinition.readSbml(sbml_model_definition, sbml_level, sbml_version)
        SbmlObject.readSbml(self, sbml_model_definition, sbml_level, sbml_version)


    def writeSbml(self, sbml_model_definition,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):

        HasId.writeSbml(self, sbml_model_definition, sbml_level, sbml_version)
        self.modelDefinition.writeSbml(sbml_model_definition, sbml_level, sbml_version)
        SbmlObject.writeSbml(self, sbml_model_definition, sbml_level, sbml_version)