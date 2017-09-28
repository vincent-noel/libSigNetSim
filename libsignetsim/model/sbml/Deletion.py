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


"""

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.HasRef import HasRef


class Deletion(HasId, HasRef):

	def __init__(self, model, obj_id, parent_submodel):

		self.__model = model
		self.objId = obj_id
		self.parentSubmodel = parent_submodel

		HasId.__init__(self, model)
		HasRef.__init__(self, model)

	def readSbml(self, sbml_deletion, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		HasId.readSbml(self, sbml_deletion, sbml_level, sbml_version)
		HasRef.readSbml(self, sbml_deletion, sbml_level, sbml_version)

	def writeSbml(self, sbml_deletion, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		HasId.writeSbml(self, sbml_deletion, sbml_level, sbml_version)
		HasRef.writeSbml(self, sbml_deletion, sbml_level, sbml_version)

	def getDeletionObject(self):

		if self.hasIdRef():
			return self.parentSubmodel.getModelObject().listOfVariables.getBySbmlId(self.getIdRef())

		elif self.hasPortRef():
			return self.parentSubmodel.getModelObject().listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

		elif self.hasMetaIdRef():
			return self.parentSubmodel.getModelObject().listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

	def getDeletionObjectFromInstance(self, model_instance):

		if self.hasIdRef():
			if self.hasSBaseRef():
				tt_model = self.parentSubmodel.getModelObject().listOfSubmodels.getBySbmlId(self.getIdRef()).getModelObject()
				tt_instance = model_instance.getSubmodelInstance(self.getIdRef())
				t_object = tt_model.listOfSbmlObjects.getByMetaId(self.getSBaseRef().getRef(tt_model))
				return model_instance.listOfSbmlObjects.getByMetaId(tt_instance.objectsDictionnary[t_object.getMetaId()])

			else:
				t_object = self.parentSubmodel.getModelObject().listOfVariables.getBySbmlId(self.getIdRef())
				return model_instance.listOfSbmlObjects.getByMetaId(
					model_instance.objectsDictionnary[t_object.getMetaId()])

		elif self.hasPortRef():
			t_object = self.parentSubmodel.getModelObject().listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()
			return model_instance.listOfSbmlObjects.getByMetaId(model_instance.objectsDictionnary[t_object.getMetaId()])

		elif self.hasMetaIdRef():
			t_object = self.parentSubmodel.getModelObject().listOfSbmlObjects.getByMetaId(self.getMetaIdRef())
			return model_instance.listOfSbmlObjects.getByMetaId(model_instance.objectsDictionnary[t_object.getMetaId()])

