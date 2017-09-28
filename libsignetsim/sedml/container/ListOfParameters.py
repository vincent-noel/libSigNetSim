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
from libsignetsim.sedml.Parameter import Parameter
from libsignetsim.settings.Settings import Settings


class ListOfParameters(ListOf):

	def __init__(self, document, parent):

		ListOf.__init__(self, document)

		self.__document = document
		self.__parent = parent
		self.__parameterCounter = 0

	def new(self, parameter_id=None):

		if parameter_id is None:
			parameter_id = "%s_parameter_%d" % self.__parameterCounter

		t_parameter = Parameter(self.__document)
		t_parameter.setId(parameter_id)
		ListOf.append(self, t_parameter)
		self.__parameterCounter += 1
		return t_parameter
	def createParameter(self, parameter_id=None):
		return self.new(parameter_id)

	def readSedml(self, list_of_parameters, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_parameters, level, version)

		for t_parameter in list_of_parameters:
			parameter = Parameter(self.__document)
			parameter.readSedml(t_parameter, level, version)
			ListOf.append(self, parameter)
			self.__parameterCounter += 1

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