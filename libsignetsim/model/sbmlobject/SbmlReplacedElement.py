#!/usr/bin/env python
""" SbmlReplacedElement.py




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


from libsignetsim.model.sbmlobject.HasRef import HasRef

class SbmlReplacedElement(HasRef):

    def __init__(self, model, obj_id):

        self.__model = model
        self.objId = obj_id
        HasRef.__init__(self, model)
        self.__submodelRef = None
        self.__deletion = None
        self.__conversionFactor = None


    def readSbml(self, sbml_replaced_element,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):


        HasRef.readSbml(self, sbml_replaced_element, sbml_level, sbml_version)
        if sbml_replaced_element.isSetSubmodelRef():
            self.__submodelRef = sbml_replaced_element.getSubmodelRef()

        if sbml_replaced_element.isSetDeletion():
            self.__deletion = sbml_replaced_element.getDeletion()

        if sbml_replaced_element.isSetConversionFactor():
            self.__conversionFactor = sbml_replaced_element.getConversionFactor()


    def writeSbml(self, sbml_object,
                    sbml_level=Settings.defaultSbmlLevel,
                    sbml_version=Settings.defaultSbmlVersion):

        sbml_replaced_element = sbml_object.createReplacedElement()

        HasRef.writeSbml(self, sbml_replaced_element, sbml_level, sbml_version)
        if self.__submodelRef is not None:
            sbml_replaced_element.setSubmodelRef(self.__submodelRef)

        if self.__deletion is not None:
            sbml_replaced_element.setDeletion(self.__deletion)

        if self.__conversionFactor is not None:
            sbml_replaced_element.setConversionFactor(self.__conversionFactor)

    def copy(self, obj, prefix="", shift=0):

        HasRef.copy(self, obj, prefix, shift)
        self.setSubmodelRef(obj.getSubmodelRef())
        self.setDeletion(obj.getDeletion())
        self.setConversionFactor(obj.getConversionFactor(), prefix)


    def getDeletion(self):
        return self.__deletion

    def setDeletion(self, deletion):
        self.__deletion = deletion

    def getConversionFactor(self):
        return self.__conversionFactor

    def setConversionFactor(self, conversion_factor, prefix=""):
        if conversion_factor is not None:
            self.__conversionFactor = prefix + conversion_factor

    def getSubmodelRef(self):
        return self.__submodelRef

    def hasModelRef(self):
        return self.__submodelRef is not None

    def setSubmodelRef(self, submodel_ref):
        self.__submodelRef = submodel_ref



    def getReplacedElementMetaId(self, model_instances=None):

        # Now choosing the right model
        if self.hasModelRef():

            if self.getSubmodelRef() == self.__model.getSbmlId():
                tt_model = self.__model
            else:
                tt_model = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef()).getModelObject()

            if self.hasIdRef():
                if self.hasSBaseRef():
                    ttt_model = tt_model.listOfSubmodels.getBySbmlIdRef(self.getIdRef()).getModelObject()
                    refs = self.getSBaseRef().getRef(ttt_model)

                    t_ref = self.getIdRef()
                    while len(refs) > 1:
                        t_ref = "%s__%s" % (t_ref, refs[0])
                        ttt_model = ttt_model.listOfSubmodels.getBySbmlIdRef(refs[0]).getModelObject()
                        refs = refs[-1:]

                    t_object = ttt_model.listOfSbmlObjects[refs[0]]
                    return "%s__%s" % (t_ref, t_object.getMetaId())

                else:
                    t_object = tt_model.listOfVariables[self.getIdRef()]

            elif self.hasPortRef():
                t_object = tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

            elif self.hasMetaIdRef():
                t_object = tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

            elif self.__deletion is not None:
                t_submodel = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef())

                if self.__deletion in t_submodel.listOfDeletions.sbmlIds():

                    t_deletion = t_submodel.listOfDeletions.getBySbmlId(self.__deletion)

                    if t_deletion.hasIdRef():
                        t_object = tt_model.listOfVariables[t_deletion.getIdRef()]

                    elif t_deletion.hasPortRef():
                        t_object = tt_model.listOfPorts.getBySbmlId(t_deletion.getPortRef()).getRefObject()

                    elif t_deletion.hasMetaIdRef():
                        t_object = tt_model.listOfSbmlObjects.getByMetaId(t_deletion.getMetaIdRef())

            return t_object.getMetaId()

    def getReplacedElementSubmodelAndObject(self):

        submodel = []
        res = None
        # Now choosing the right model
        if self.hasModelRef():

            if self.getSubmodelRef() == self.__model.getSbmlId():
                tt_model = self.__model
            else:
                tt_model = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef()).getModelObject()

            submodel.append(self.getSubmodelRef())

            if self.hasIdRef():
                if self.hasSBaseRef():
                    ttt_model = tt_model.listOfSubmodels.getBySbmlIdRef(self.getIdRef()).getModelObject()
                    refs = self.getSBaseRef().getRef(ttt_model)

                    submodel.append(self.getIdRef())
                    while len(refs) > 1:
                        submodel.append(res[0])
                        ttt_model = ttt_model.listOfSubmodels.getBySbmlIdRef(refs[0]).getModelObject()
                        refs = refs[-1:]

                    res = ttt_model.listOfSbmlObjects[refs[0]]

                else:

                    res = tt_model.listOfVariables[self.getIdRef()]

            elif self.hasPortRef():
                res = tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

            elif self.hasMetaIdRef():
                res = tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

            elif self.__deletion is not None:
                t_submodel = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef())

                if self.__deletion in t_submodel.listOfDeletions.sbmlIds():

                    t_deletion = t_submodel.listOfDeletions.getBySbmlId(self.__deletion)

                    if t_deletion.hasIdRef():
                        res = tt_model.listOfVariables[t_deletion.getIdRef()]

                    elif t_deletion.hasPortRef():
                        res = tt_model.listOfPorts.getBySbmlId(t_deletion.getPortRef()).getRefObject()

                    elif t_deletion.hasMetaIdRef():
                        res = tt_model.listOfSbmlObjects.getByMetaId(t_deletion.getMetaIdRef())

            return (submodel, res)



    def getReplacedElementObject(self):

        res = None
        # Now choosing the right model
        if self.hasModelRef():

            if self.getSubmodelRef() == self.__model.getSbmlId():
                tt_model = self.__model
            else:
                tt_model = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef()).getModelObject()

            if self.hasIdRef():
                if self.hasSBaseRef():
                    ttt_model = tt_model.listOfSubmodels.getBySbmlIdRef(self.getIdRef()).getModelObject()
                    refs = self.getSBaseRef().getRef(ttt_model)

                    while len(refs) > 1:
                        ttt_model = ttt_model.listOfSubmodels.getBySbmlIdRef(refs[0]).getModelObject()
                        refs = refs[-1:]

                    res = ttt_model.listOfSbmlObjects[refs[0]]

                else:

                    res = tt_model.listOfVariables[self.getIdRef()]

            elif self.hasPortRef():
                res = tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

            elif self.hasMetaIdRef():
                res = tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

            elif self.__deletion is not None:
                t_submodel = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef())

                if self.__deletion in t_submodel.listOfDeletions.sbmlIds():

                    t_deletion = t_submodel.listOfDeletions.getBySbmlId(self.__deletion)

                    if t_deletion.hasIdRef():
                        res = tt_model.listOfVariables[t_deletion.getIdRef()]

                    elif t_deletion.hasPortRef():
                        res = tt_model.listOfPorts.getBySbmlId(t_deletion.getPortRef()).getRefObject()

                    elif t_deletion.hasMetaIdRef():
                        res = tt_model.listOfSbmlObjects.getByMetaId(t_deletion.getMetaIdRef())

            return res