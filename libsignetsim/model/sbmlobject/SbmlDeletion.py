#!/usr/bin/env python
""" SbmlDeletion.py




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
from libsignetsim.model.sbmlobject.HasId import HasId
from libsignetsim.model.sbmlobject.HasRef import HasRef

class SbmlDeletion(HasId, HasRef):

    def __init__(self, model, obj_id, parent_submodel):

        self.__model = model
        self.objId = obj_id
        self.parentSubmodel = parent_submodel

        HasId.__init__(self, model)
        HasRef.__init__(self, model)



    def readSbml(self, sbml_deletion,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):

        HasId.readSbml(self, sbml_deletion, sbml_level, sbml_version)
        HasRef.readSbml(self, sbml_deletion, sbml_level, sbml_version)



    def writeSbml(self, sbml_deletion,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):

        # sbml_deletion = sbml_object.createDeletion()
        HasId.writeSbml(self, sbml_deletion, sbml_level, sbml_version)
        HasRef.writeSbml(self, sbml_deletion, sbml_level, sbml_version)




    def getDeletionObject(self):

        # print self.__model.getNameOrSbmlId()
        t_model = self.parentSubmodel.getModelObject()

        # print t_model.getNameOrSbmlId()
        if self.hasIdRef():
            # if self.hasSBaseRef():
            #     ttt_model = self.__model.listOfSubmodels.getBySbmlIdRef(self.getIdRef()).getModelObject()
            #     refs = self.getSBaseRef().getRef(ttt_model)
            #
            #     t_ref = self.getIdRef()
            #     while len(refs) > 1:
            #         t_ref = "%s__%s" % (t_ref, refs[0])
            #         ttt_model = ttt_model.listOfSubmodels.getBySbmlIdRef(refs[0]).getModelObject()
            #         refs = refs[-1:]
            #
            #     t_object = ttt_model.listOfSbmlObjects[refs[0]]
            #     return "%s__%s" % (t_ref, t_object.getMetaId())
            #
            # else:
            return self.parentSubmodel.getModelObject().listOfVariables[self.getIdRef()]

        elif self.hasPortRef():
            return self.parentSubmodel.getModelObject().listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

        elif self.hasMetaIdRef():
            return self.parentSubmodel.getModelObject().listOfSbmlObjects.getByMetaId(self.getMetaIdRef())
        #
        # elif self.__deletion is not None:
        #     t_submodel = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef())
        #
        #     if self.__deletion in t_submodel.listOfDeletions.sbmlIds():
        #
        #         t_deletion = t_submodel.listOfDeletions.getBySbmlId(self.__deletion)
        #
        #         if t_deletion.hasIdRef():
        #             t_object = tt_model.listOfVariables[t_deletion.getIdRef()]
        #
        #         elif t_deletion.hasPortRef():
        #             t_object = tt_model.listOfPorts.getBySbmlId(t_deletion.getPortRef()).getRefObject()
        #
        #         elif t_deletion.hasMetaIdRef():
        #             t_object = tt_model.listOfSbmlObjects.getByMetaId(t_deletion.getMetaIdRef())