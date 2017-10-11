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

from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.settings.Settings import Settings
from re import match


class ExternalModelDefinition(HasId, SbmlObject, HasParentObj):

	def __init__(self, model, obj_id, parent_obj):

		self.__model = model

		self.objId = obj_id
		HasParentObj.__init__(self, parent_obj)
		HasId.__init__(self, model)
		SbmlObject.__init__(self, model)
		self.__modelRef = None

		self.__source = None
		self.modelDefinition = None

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
		t_document.setParentObj(self)

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

	# def resolveXPath(self, selector):
	#
	# 	if not (selector.startswith("externalModelDefinition") or selector.startswith("sbml:externalModelDefinition")):
	# 		raise InvalidXPath(selector)
	#
	# 	if "[@" in selector:
	# 		res_match = match(r'(.*)\[@(.*)=(.*)\]', selector)
	# 		if res_match is None:
	# 			raise InvalidXPath(selector)
	#
	# 		tokens = res_match.groups()
	# 		if len(tokens) != 3:
	# 			raise InvalidXPath(selector)
	#
	# 		object = None
	# 		if tokens[1] == "id":
	# 			object = self.getBySbmlId(tokens[2][1:-1])
	# 		elif tokens[1] == "name":
	# 			object = self.getByName(tokens[2][1:-1])
	#
	# 		if object is not None:
	# 			return object
	# 	else:
	#
	#
	# 	# If not returned yet
	# 	raise InvalidXPath(selector)
	#
	def getByXPath(self, xpath):
		return self.modelDefinition.parentDoc.getByXPath("/".join(xpath))

	def setByXPath(self, xpath, object):
		self.modelDefinition.parentDoc.setByXPath("/".join(xpath), object)

	def getXPath(self, attribute=None):

		xpath = "sbml:externalModelDefinition"
		if self.__model.sbmlLevel == 1:
			xpath += "[@name='%s']" % self.getSbmlId()
		else:
			xpath += "[@id='%s']" % self.getSbmlId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])