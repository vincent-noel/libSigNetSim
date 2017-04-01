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
from libsignetsim.sedml.Parameter import Parameter
from libsignetsim.settings.Settings import Settings


class ListOfParameters(ListOf):

	def __init__(self, document, parent):

		ListOf.__init__(self, document)

		self.__document = document
		self.__parent = parent

	def readSedml(self, list_of_parameters, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_parameters, level, version)

		for t_parameter in list_of_parameters:
			parameter = Parameter(self.__document)
			parameter.readSedml(t_parameter, level, version)
			ListOf.append(self, parameter)

	def writeSedml(self, list_of_parameters, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_parameters, level, version)

		for t_parameter in self:
			parameter = list_of_parameters.createParameter()
			t_parameter.writeSedml(parameter, level, version)

	def getSubs(self):

		data = {}
		for parameter in self:
			data.update(parameter.getSub())

		return data