#!/usr/bin/env python
""" ListOfVariables.py


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

from libsignetsim.sedml.container.ListOf import ListOf
from libsignetsim.sedml.Variable import Variable
from libsignetsim.settings.Settings import Settings


class ListOfVariables(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)

		self.__document = document

	def readSedml(self, list_of_variables, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_variables, level, version)

		for t_var in list_of_variables:
			var = Variable(self.__document)
			var.readSedml(t_var, level, version)
			ListOf.append(self, var)

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