#!/usr/bin/env python
""" ExternalModelDefinition.py




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

from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.settings.Settings import Settings

class ExternalModelDefinition(HasId, SbmlObject):

	def __init__(self, model, obj_id):

		self.__model = model

		self.objId = obj_id

		HasId.__init__(self, model)
		SbmlObject.__init__(self, model)
		self.__modelRef = None

		self.__source = None
		self.modelDefinition = None #Model(obj_id=self.objId, parent_doc=self.__model.parentDoc)



	def readSbml(self, sbml_model_definition,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasId.readSbml(self, sbml_model_definition, sbml_level, sbml_version)
		SbmlObject.readSbml(self, sbml_model_definition, sbml_level, sbml_version)

		if sbml_model_definition.isSetModelRef():
			self.__modelRef = sbml_model_definition.getModelRef()

		if sbml_model_definition.isSetSource():
			self.__source = sbml_model_definition.getSource()

		t_id_dep = self.__model.parentDoc.documentDependenciesPaths.index(self.__source)
		t_document = self.__model.parentDoc.documentDependencies[t_id_dep]

		if self.__modelRef is not None:
			self.modelDefinition = t_document.getSubmodel(self.__modelRef)
		else:
			self.modelDefinition = t_document.model


	def writeSbml(self, sbml_model_definition,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasId.writeSbml(self, sbml_model_definition, sbml_level, sbml_version)

		if self.__modelRef is not None:
			sbml_model_definition.setModelRef(self.__modelRef)

		if self.__source is not None:
			sbml_model_definition.setSource(self.__source)

		SbmlObject.writeSbml(self, sbml_model_definition, sbml_level, sbml_version)



	def getSource(self):
		return self.__source

	def setSource(self, source):
		self.__source = source
		self.updateModelDefinition()


	def hasModelRef(self):
		return self.__modelRef is not None

	def getModelRef(self):
		return self.__modelRef

	def setModelRef(self, model_ref):
		self.__modelRef = model_ref
		self.updateModelDefinition()


	def updateModelDefinition(self):

		self.__model.parentDoc.documentDependenciesPaths = None
		self.__model.parentDoc.loadExternalDocumentDependencies()

		t_id_dep = self.__model.parentDoc.documentDependenciesPaths.index(self.__source)
		t_document = self.__model.parentDoc.documentDependencies[t_id_dep]

		if self.__modelRef is not None:
			self.modelDefinition = t_document.getSubmodel(self.__modelRef)
		else:
			self.modelDefinition = t_document.model