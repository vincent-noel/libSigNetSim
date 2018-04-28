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


from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.Species import Species
from libsignetsim.model.sbml.Compartment import Compartment
from libsignetsim.model.sbml.Parameter import Parameter
from libsignetsim.model.sbml.Reaction import Reaction

class XPath(object):

	VALUE = "value"
	NAME = "name"
	ID = "id"
	METAID = "metaid"


	def __init__(self, document):
		self.__document = document
		self.__rawXPath = None

	def readSedml(self, xpath, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		self.__rawXPath = xpath

	def isModelObject(self):
		return not self.__rawXPath.startswith("#")

	def isSedmlObject(self):
		return self.__rawXPath.startswith("#")

	def getModelObject(self, sbml_model, instance=False):
		if self.isModelObject():
			return sbml_model.parentDoc.getByXPath(self.__rawXPath, instance)

	def changeModelObject(self, sbml_model, value):
		if self.isModelObject():
			sbml_model.parentDoc.setByXPath(self.__rawXPath, value, instance=True)

	def setModelObject(self, object, attribute=None):
		self.__rawXPath = object.getXPath()
		if attribute is not None:
			self.__rawXPath += "/@%s" % attribute

	def getSedmlObject(self):
		if self.isSedmlObject():
			return self.__document.listOfIds.getById(self.__rawXPath[1:])

	def setSedmlObject(self, object, attribute=None):
		self.__rawXPath = "#%s" % object.getId()

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		return self.__rawXPath

	def getXPath(self):
		return self.__rawXPath

	def getParentXPath(self):
		paths = self.__rawXPath.split("/")[:-1]
		return "/".join(paths)

	def getElementXPath(self):
		return self.__rawXPath.split("/")[-1]

	def getElementTag(self):
		element = self.__rawXPath.split("/")[-1]
		if ":" in element:
			return element.split(":")[-1]
		else:
			return element

	def getXPathWithoutPrefixes(self):
		paths = self.__rawXPath.split("/")
		res = []
		for path in paths:
			if ":" in path:
				res.append(path.split(":")[1])
			else:
				res.append(path)
		return "/".join(res)