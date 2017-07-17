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
from libsignetsim.sedml.SedmlException import SedmlUnknownXPATH
from re import match

class XPath(object):

	VALUE = "value"
	NAME = "name"
	ID = "id"
	METAID = "metaid"


	def __init__(self, document):

		self.__document = document

		self.__path = None

		self.__containers = None
		self.__variable = None
		self.__attribute = None

		self.__varType = None
		self.__refType = None
		self.__ref = None


	def readSedml(self, xpath, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if xpath is not None:
			# print xpath
			t_path = xpath.split('/')

			last_ind = len(t_path)-1
			if t_path[last_ind].startswith("@"):
				self.__attribute = t_path[last_ind][1:]
				# self.__path = self.__path[:-1]
				last_ind -= 1

			self.readRef(t_path[last_ind])
		#
		#
		# if self.__path[-1].startswith("descendant::*"):
		#
		#
		# if self.__path[0] == "" and self.__path[1] in ["sbml:sbml", "sbml"] and self.__path[2] == ["sbml:model", "model"]:
		# 	self.__preambule = ["", "sbml:sbml", "sbml:model"]
		#
		#
		# 	if self.__path[3].startswith("descendant::*"):
		# 		# Then we'll get it via listOfVariables, or listOfSbmlObjects I guess
		# 		self.__containers = ["descendant::*"]
		# 	elif ":" in self.__path[3] and
		#
		#
		#
		#
		#
		# 		ind_last_token = len(self.__path) - 1
		#
		# 		if self.__path[ind_last_token].startswith("@"):
		# 			self.__attribute = self.__path[ind_last_token][1:]
		# 			self.__path = self.__path[:-1]
		# 			ind_last_token -= 1
		#
		# 		print self.__path[ind_last_token]
		# 		last_token =
		# 		if self.__path[ind_last_token].startswith("sbml:"):
		#
		# 		res_match = match(r"(sbml:[a-zA-Z]+)\[@([a-zA-Z]+)=[\'\"](.*)[\'\"]\]", self.__path[ind_last_token])
		#
		# 		print res_match.groups()
		# 		self.__path[ind_last_token] = res_match.groups()[0]
		# 		self.__refType = res_match.groups()[1]
		# 		self.__ref = res_match.groups()[2]

	def readRef(self, string):

		res_match = match(r"([a-zA-Z\:\*]+)\[@([a-zA-Z]+)=[\'\"](.*)[\'\"]\]", string)

		# print res_match.groups()
		self.__varType = res_match.groups()[0]
		if self.__varType != "descendant::*" and ":" not in self.__varType:
			self.__varType = "sbml:" + self.__varType

		self.__refType = res_match.groups()[1]
		self.__ref = res_match.groups()[2]

	def getModelObject(self, sbml_model):

		# print self.__path
		# ind_last_token = len(self.__path) - 1
		# if self.__attribute is not None:
		# 	ind_last_token -= 1

		t_container = None
		# if self.__path[ind_last_token] == "sbml:species":
		if self.__varType == "descendant::*":
			if self.__refType == "id":
				t_container = sbml_model.listOfVariables
			else:
				t_container = sbml_model.listOfSbmlObjects

		elif self.__varType.endswith(":species"):
			t_container = sbml_model.listOfSpecies

		elif self.__varType.endswith(":compartment"):
			t_container = sbml_model.listOfCompartments

		elif self.__varType.endswith(":parameter"):
			t_container = sbml_model.listOfParameters

		if t_container is not None:
			if self.__refType == "id":
				return t_container.getBySbmlId(self.__ref)

			elif self.__refType == "name":
				return t_container.getByName(self.__ref)

	def setModelObject(self, object, attribute=None):

		# self.__path = ["", "sbml:sbml", "sbml:model"]
		# print type(object)
		# print object.getSbmlId()

		if object.getModel().sbmlLevel == 1:
			self.__refType = "name"
			self.__ref = object.getName()
		else:
			self.__refType = "id"
			self.__ref = object.getSbmlId()

		if isinstance(object, Compartment):
			self.__varType = "sbml:compartment"

		elif isinstance(object, Species):
			self.__varType = "sbml:species"

		elif isinstance(object, Parameter):
			# print "YEAH PARAMETEr"
			self.__varType = "sbml:parameter"

		# else:
		# 	print type(object)
		self.__attribute = attribute

	def writeSedml(self, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		return self.getXPath()

	def getXPath(self):

		if self.__varType is not None and self.__refType is not None and self.__ref is not None:
			# print "%s (%s)" % (self.__ref, self.__varType)
			str = "/sbml:sbml/sbml:model"
			if self.__varType == "descendant::*":
				str += "/" + self.__varType

			else:
				if self.__varType.endswith(":species"):
					str += "/sbml:listOfSpecies/sbml:species"

				elif self.__varType.endswith(":compartment"):
					str += "/sbml:listOfCompartments/sbml:compartment"

				elif self.__varType.endswith(":parameter"):
					str += "/sbml:listOfParameters/sbml:parameter"


			str += ("[@%s='%s']" % (self.__refType, self.__ref))
			if self.__attribute is not None:
				str += "/@%s" % self.__attribute

			return str

	def getAttribute(self):
		return self.__attribute

	def getTargetName(self):
		return self.__ref