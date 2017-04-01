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
from re import match

class XPath(object):

	def __init__(self, document):
		self.__document = document

		self.__path = None
		self.__refType = None
		self.__ref = None

	def readSedml(self, xpath, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		self.__path = xpath.split('/')
		if self.__path[0] == "" and self.__path[1] == "sbml:sbml" and self.__path[2] == "sbml:model":

			ind_last_token = len(self.__path) - 1
			res_match = match(r"(sbml:[a-zA-Z]+)\[@([a-zA-Z]+)=\'(.*)\'\]", self.__path[ind_last_token])

			self.__path[ind_last_token] = res_match.groups()[0]
			self.__refType = res_match.groups()[1]
			self.__ref = res_match.groups()[2]

	def getModelObject(self, sbml_model):

		ind_last_token = len(self.__path) - 1

		t_container = None
		if self.__path[ind_last_token] == "sbml:species":
			t_container = sbml_model.listOfSpecies

		elif self.__path[ind_last_token] == "sbml:compartment":
			t_container = sbml_model.listOfCompartments

		elif self.__path[ind_last_token] == "sbml:parameter":
			t_container = sbml_model.listOfParameters

		if t_container is not None:
			if self.__refType == "id":
				return t_container.getBySbmlId(self.__ref)

			elif self.__refType == "name":
				return t_container.getByName(self.__ref)

	def setModelObject(self, object):

		self.__path = ["", "sbml:sbml", "sbml:model"]

		if object.getModel().sbmlLevel == 1:
			self.__refType = "name"
			self.__ref = object.getName()
		else:
			self.__refType = "id"
			self.__ref = object.getSbmlId()

		if isinstance(object, Compartment):
			self.__path += ["sbml:listOfCompartments", "sbml:compartment"]

		elif isinstance(object, Species):
			self.__path += ["sbml:listOfSpecies", "sbml:species"]

		elif isinstance(object, Parameter):
			self.__path += ["sbml:listOfParameters", "sbml:parameter"]

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		return self.getXPath()

	def getXPath(self):
		if self.__path is not None:
			return "/".join(self.__path) + ("[@%s='%s']" % (self.__refType, self.__ref))
