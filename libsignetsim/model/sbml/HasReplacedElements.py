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
from libsignetsim.model.sbml.container.ListOfReplacedElements import ListOfReplacedElements
from libsignetsim.model.sbml.ReplacedBy import ReplacedBy


class HasReplacedElements(object):

	def __init__ (self, model):


		self.__model = model

		self.__hasReplacedElements = False
		self.__hasReplacedBy = False
		self.__listOfReplacedElements = None
		self.__replacedBy = None


	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		""" Reads a parameter from a sbml file """

		if self.__model.parentDoc.useCompPackage:


			t_object = sbml_object.getPlugin("comp")

			if t_object.getListOfReplacedElements() is not None and len(t_object.getListOfReplacedElements()) > 0:
				self.__hasReplacedElements = True
				self.__listOfReplacedElements = ListOfReplacedElements(self.__model, self)
				self.__listOfReplacedElements.readSbml(
						t_object.getListOfReplacedElements(),
						sbml_level, sbml_version)


			if t_object.isSetReplacedBy():
				self.__hasReplacedBy = True
				self.__replacedBy = ReplacedBy(self.__model, self)
				self.__replacedBy.readSbml(
						t_object.getReplacedBy(),
						sbml_level, sbml_version)


	def writeSbml(self, sbml_object,
						sbml_level=Settings.defaultSbmlLevel,
						sbml_version=Settings.defaultSbmlVersion):

		""" Writes a parameter to  a sbml file """

		if self.__hasReplacedElements:
			self.__listOfReplacedElements.writeSbml(sbml_object.getPlugin("comp"), sbml_level, sbml_version)

		if self.__hasReplacedBy:
			self.__replacedBy.writeSbml(sbml_object.getPlugin("comp"), sbml_level, sbml_version)

	def isModified(self):
		return False


	def hasReplacedElements(self):
		return self.__hasReplacedElements

	def getReplacedElements(self):
		if self.hasReplacedElements():
			return self.__listOfReplacedElements

	def getListOfReplacedElements(self):
		if self.hasReplacedElements():
			return self.__listOfReplacedElements

	def addReplacedElement(self):
		if not self.hasReplacedElements():
			self.__hasReplacedElements = True
			self.__listOfReplacedElements = ListOfReplacedElements(self.__model, self)
		return self.__listOfReplacedElements.new()

	def removeReplacedElement(self, re_object):

		t_replaced_element = self.__listOfReplacedElements.getByReplacedElementObject(re_object)
		if t_replaced_element is not None:
			self.__listOfReplacedElements.remove(t_replaced_element)
			if len(self.__listOfReplacedElements) == 0:
				self.__hasReplacedElements = False
				self.__listOfReplacedElements = None


	def isReplaced(self):
		return self.__hasReplacedBy

	def isReplacedBy(self):
		if self.isReplaced():
			return self.__replacedBy

	def getReplacedBy(self):
		if not self.isReplaced():
			self.__hasReplacedBy = True
			self.__replacedBy = ReplacedBy(self.__model, self)

		return self.__replacedBy

	def unsetReplacedBy(self):
		self.__hasReplacedBy = False
		self.__replacedBy = None


	def copy(self, obj, prefix="", shift=0):

		if obj.hasReplacedElements():
			self.__listOfReplacedElements = ListOfReplacedElements(self.__model, self)
			self.__listOfReplacedElements.copy(obj.getListOfReplacedElements(), prefix, shift)

		if obj.isReplaced():
			self.__replacedBy = ReplacedBy(self.__model, self)
			self.__replacedBy.copy(obj.isReplacedBy(), prefix, shift)
