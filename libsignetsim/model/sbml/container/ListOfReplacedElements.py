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

from libsignetsim.model.sbml.container.ListOf import ListOf
from libsignetsim.model.sbml.SimpleSbmlObject import SimpleSbmlObject

from libsignetsim.model.sbml.ReplacedElement import ReplacedElement
from libsignetsim.settings.Settings import Settings

class ListOfReplacedElements(ListOf):#, SimpleSbmlObject):
	""" Class for the listOfModelDefinition in a sbml model """

	def __init__ (self, model, parent_obj):

		self.__model = model
		self.__parentObj = parent_obj
		ListOf.__init__(self, model)
		# SimpleSbmlObject.__init__(self, model)


	def readSbml(self, sbml_list_re,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads compartments' list from a sbml file """

		for re in sbml_list_re:
			t_re = ReplacedElement(self.__model, self.__parentObj, self.nextId())
			t_re.readSbml(re, sbml_level, sbml_version)
			ListOf.add(self, t_re)


	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes compartments' list to a sbml file """

		for t_replaced_element in self:
			t_replaced_element.writeSbml(sbml_object, sbml_level, sbml_version)

	def new(self):
		""" Creates a new compartment """

		t_replaced_element = ReplacedElement(self.__model, self.__parentObj, self.nextId())
		ListOf.add(self, t_replaced_element)
		return t_replaced_element

	def copy(self, obj, prefix="", shift=0):

		for replaced_element in obj:
			t_re = ReplacedElement(self.__model, self.__parentObj, (replaced_element.objId + shift))
			t_re.copy(replaced_element, prefix, shift)
			ListOf.add(self, t_re)

	def remove(self, obj):
		""" 
			Remove an object from the list 
			Using list base method to avoid having to remove it from the listOfSbmlObjects (it's not there) 
		"""
		list.remove(self, obj)

	def getByReplacedElementObject(self, re_object):

		for replacement_element in self:
			if replacement_element.getReplacedElementObject() == re_object:
				return replacement_element

	def containsSubmodel(self, submodel_ref):

		for replaced_element in self:
			if replaced_element.getSubmodelRef() == submodel_ref:
				return True

		return False