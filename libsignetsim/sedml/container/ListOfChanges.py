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

from libsignetsim.sedml.container.ListOf import ListOf

from libsignetsim.sedml.ChangeAttribute import ChangeAttribute
from libsignetsim.sedml.ComputeChange import ComputeChange
from libsignetsim.sedml.AddXML import AddXML
from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_CHANGE_ATTRIBUTE, SEDML_CHANGE_COMPUTECHANGE, SEDML_CHANGE_ADDXML
from six.moves import reload_module
reload_module(libsbml)

class ListOfChanges(ListOf):

	def __init__(self, document, model):

		ListOf.__init__(self, document)

		self.__document = document
		self.__model = model
		self.__changeCounter = 0

	def new(self, change_type, change_id=None):
		t_change_id = change_id
		if t_change_id is None:
			t_change_id = "%s_change_%d" % (self.__model.getId(), self.__changeCounter)

		if change_type == SEDML_CHANGE_ATTRIBUTE:
			t_change = ChangeAttribute(self.__document)
			t_change.setId(t_change_id)
			ListOf.append(self, t_change)
			self.__changeCounter += 1
			return t_change

		elif change_type == SEDML_CHANGE_COMPUTECHANGE:
			t_change = ComputeChange(self.__document)
			t_change.setId(t_change_id)
			ListOf.append(self, t_change)
			self.__changeCounter += 1
			return t_change

		elif change_type == SEDML_CHANGE_ADDXML:
			t_change = AddXML(self.__document)
			t_change.setId(t_change_id)
			ListOf.append(self, t_change)
			self.__changeCounter += 1
			return t_change

	def createChangeAttribute(self, change_id=None):
		return self.new(SEDML_CHANGE_ATTRIBUTE, change_id)

	def createComputeChange(self, change_id=None):
		return self.new(SEDML_CHANGE_COMPUTECHANGE, change_id)

	def createAddXML(self, change_id=None):
		return self.new(SEDML_CHANGE_ADDXML, change_id)

	def readSedml(self, list_of_changes, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_changes, level, version)

		for change in list_of_changes:

			if change.getTypeCode() == SEDML_CHANGE_ATTRIBUTE:
				t_change = ChangeAttribute(self.__document)
				t_change.readSedml(change, level, version)
				ListOf.append(self, t_change)
				self.__changeCounter += 1

			elif change.getTypeCode() == SEDML_CHANGE_COMPUTECHANGE:
				t_change = ComputeChange(self.__document)
				t_change.readSedml(change, level, version)
				ListOf.append(self, t_change)
				self.__changeCounter += 1

			elif change.getTypeCode() == SEDML_CHANGE_ADDXML:
				t_change = AddXML(self.__document)
				t_change.readSedml(change, level, version)
				ListOf.append(self, t_change)
				self.__changeCounter += 1

	def writeSedml(self, list_of_changes, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_changes, level, version)

		for change in self:
			if isinstance(change, ChangeAttribute):
				t_change = list_of_changes.createChangeAttribute()
				change.writeSedml(t_change, level, version)

			elif isinstance(change, ComputeChange):
				t_change = list_of_changes.createComputeChange()
				change.writeSedml(t_change, level, version)

			elif isinstance(change, AddXML):
				t_change = list_of_changes.createAddXML()
				change.writeSedml(t_change, level, version)

	def applyChanges(self, sbml_model):

		for change in self:
			if isinstance(change, ChangeAttribute) or isinstance(change, ComputeChange):
				change.applyChange(sbml_model)

	def applyXMLChanges(self, sbml_tree):
		for change in self:
			if isinstance(change, AddXML):
				change.applyChange(sbml_tree)

	def nbXMLChanges(self):

		counter = 0
		for change in self:
			if isinstance(change, AddXML):
				counter += 1
		return counter