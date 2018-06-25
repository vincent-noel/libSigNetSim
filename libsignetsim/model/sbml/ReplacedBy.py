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
from libsignetsim.model.sbml.HasRef import HasRef

class ReplacedBy(HasRef):

	def __init__(self, model, parent_obj):

		self.__model = model
		self.__parentObj = parent_obj
		HasRef.__init__(self, model)
		self.__submodelRef = None



	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasRef.readSbml(self, sbml_object, sbml_level, sbml_version)
		if sbml_object.isSetSubmodelRef():
			self.__submodelRef = sbml_object.getSubmodelRef()


	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		sbml_rb = sbml_object.createReplacedBy()
		HasRef.writeSbml(self, sbml_rb, sbml_level, sbml_version)
		if self.__submodelRef is not None:
			sbml_rb.setSubmodelRef(self.__submodelRef)

	def setSubmodelRef(self, submodel_ref):
		self.__submodelRef = submodel_ref


	def getSubmodelRef(self):
		return self.__submodelRef

	def hasModelRef(self):
		return self.__submodelRef is not None

	def getReplacingElementObjectFromInstance(self, model_instance):

		# Now choosing the right model
		if self.hasModelRef():

			if self.getSubmodelRef() == self.__model.getSbmlId():
				tt_model = self.__model
				tt_instance = model_instance

			else:
				tt_model = self.__model.listOfSubmodels.getBySbmlId(self.getSubmodelRef()).getModelObject()
				tt_instance = model_instance.getSubmodelInstance(self.getSubmodelRef())

			if self.hasIdRef():

				if self.hasSBaseRef():

					ttt_model = tt_model.listOfSubmodels.getBySbmlId(self.getIdRef()).getModelObject()
					ttt_instance = tt_instance.getSubmodelInstance(self.getIdRef())
					refs = self.getSBaseRef().getRef(ttt_model)
					obj_dicts = [ttt_instance.objectsDictionnary]
					while len(refs) > 1:
						ttt_model = ttt_model.listOfSubmodels.getBySbmlId(refs[0]).getModelObject()
						ttt_instance = ttt_instance.getSubmodelInstance(refs[0])
						obj_dicts.append(ttt_instance.objectsDictionnary)
						refs = refs[-1:]

					t_object = ttt_model.listOfSbmlObjects.getByMetaId(refs[0])
					ttt_metaid = ttt_instance.objectsDictionnary[t_object.getMetaId()]
					obj_dicts.pop()

					while len(obj_dicts) > 0:
						ttt_metaid = obj_dicts[-1][ttt_metaid]
						obj_dicts.pop()

					tt_metaid = tt_instance.objectsDictionnary[ttt_metaid]

					return tt_instance.listOfSbmlObjects.getByMetaId(tt_metaid)
				else:
					t_object = tt_model.listOfVariables.getBySbmlId(self.getIdRef())


			elif self.hasPortRef():
				t_object = tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

			elif self.hasMetaId():
				t_object = tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

			return tt_instance.listOfSbmlObjects.getByMetaId(
				tt_instance.objectsDictionnary[t_object.getMetaId()]
			)

	def getReplacingElementObject(self):

		# Now choosing the right model
		if self.hasModelRef():

			if self.getSubmodelRef() == self.__model.getSbmlId():
				tt_model = self.__model

			else:
				tt_model = self.__model.listOfSubmodels.getBySbmlId(self.getSubmodelRef()).getModelObject()

			if self.hasIdRef():

				if self.hasSBaseRef():

					ttt_model = tt_model.listOfSubmodels.getBySbmlId(self.getIdRef()).getModelObject()
					refs = self.getSBaseRef().getRef(ttt_model)

					while len(refs) > 1:
						ttt_model = ttt_model.listOfSubmodels.getBySbmlId(refs[0]).getModelObject()
						refs = refs[-1:]

					return ttt_model.listOfSbmlObjects.getByMetaId(refs[0])

				else:
					return tt_model.listOfVariables.getBySbmlId(self.getIdRef())


			elif self.hasPortRef():
				return tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

			elif self.hasMetaId():
				return tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())


	def renameSbmlId(self, old_sbml_id, new_sbml_id, submodel_ref=None):

		if self.hasIdRef() and self.getIdRef() == old_sbml_id:
			self.setIdRef(new_sbml_id)

	def getParentObject(self):
		return self.__parentObj