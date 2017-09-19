#!/usr/bin/env python
""" XPath.py


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

	def getModelObject(self, sbml_model):

		return sbml_model.parentDoc.getByXPath(self.__rawXPath)

	def changeModelObject(self, sbml_model, value):
		sbml_model.parentDoc.setByXPath(self.__rawXPath, value)

	def setModelObject(self, object, attribute=None):

		self.__rawXPath = "sbml:sbml/sbml:model/"

		if isinstance(object, Compartment):
			self.__rawXPath += "sbml:listOfCompartments/sbml:compartment"

		elif isinstance(object, Species):
			self.__rawXPath += "sbml:listOfSpecies/sbml:species"

		elif isinstance(object, Parameter):
			self.__rawXPath += "sbml:listOfParameters/sbml:parameter"

		elif isinstance(object, Reaction):
			self.__rawXPath += "sbml:listOfReactions/sbml:reaction"

		if object.getModel().sbmlLevel == 1:
			self.__rawXPath += "[@name='%s']" % object.getName()
		else:
			self.__rawXPath += "[@id='%s']" % object.getSbmlId()

		if attribute is not None:
			self.__rawXPath += "/@%s" % attribute

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		return self.__rawXPath

	def getXPath(self):
		return self.__rawXPath
