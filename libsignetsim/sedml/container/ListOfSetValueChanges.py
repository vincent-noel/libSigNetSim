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

from libsignetsim.sedml.SetValue import SetValue

from libsignetsim.settings.Settings import Settings


class ListOfSetValueChanges(ListOf):

	def __init__(self, document, repeated_task):

		ListOf.__init__(self, document)

		self.__document = document
		self.__repeatedTask = repeated_task
		self.__setValueCounter = 0

	def new(self, set_value_id=None):

		t_set_value_id = set_value_id
		if t_set_value_id is None:
			t_set_value_id = "%s_setvalue_%d" % (self.__repeatedTask.getId(), self.__setValueCounter)

		set_value = SetValue(self.__document, self.__repeatedTask)
		set_value.setId(t_set_value_id)
		ListOf.append(self, set_value)
		self.__setValueCounter += 1
		return set_value

	def createSetValue(self, set_value_id=None):
		return self.new(set_value_id)

	def readSedml(self, list_of_changes, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_changes, level, version)

		for change in list_of_changes:
			t_change = SetValue(self.__document, self.__repeatedTask)
			t_change.readSedml(change, level, version)
			ListOf.append(self, t_change)
			self.__setValueCounter += 1

	def writeSedml(self, list_of_changes, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_changes, level, version)

		for change in self:
			t_change = list_of_changes.createSetValue()
			change.writeSedml(t_change, level, version)

	def getValueChanges(self):

		value_changes = {}

		for change in self:
			value_changes.update(change.getValueChange())

		return value_changes