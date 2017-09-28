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
from libsignetsim.sedml.Variable import Variable
from libsignetsim.settings.Settings import Settings


class ListOfVariables(ListOf):

	def __init__(self, document, parent):

		ListOf.__init__(self, document)

		self.__document = document
		self.__parent = parent
		self.__variableCounter = 0

	def new(self, variable_id=None):

		t_variable_id = variable_id
		if t_variable_id is None:
			t_variable_id = "%s_variable_%d" % (self.__parent.getId(), self.__variableCounter)

		variable = Variable(self.__document)
		variable.setId(t_variable_id)
		self.__variableCounter += 1
		ListOf.append(self, variable)
		return variable

	def createVariable(self, variable_id=None):
		return self.new(variable_id)

	def readSedml(self, list_of_variables, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_variables, level, version)

		for t_var in list_of_variables:
			var = Variable(self.__document)
			var.readSedml(t_var, level, version)
			ListOf.append(self, var)
			self.__variableCounter += 1

	def writeSedml(self, list_of_variables, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_variables, level, version)

		for t_var in self:
			var = list_of_variables.createVariable()
			t_var.writeSedml(var, level, version)

	def getData(self):

		data = {}
		for variable in self:
			data.update(variable.getData())

		return data

	def getTasksToRun(self):

		tasks = []
		for variable in self:
			tasks.append(variable.getTask())

		return list(set(tasks))