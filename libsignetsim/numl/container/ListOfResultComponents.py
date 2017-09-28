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

from libsignetsim.numl.container.ListOf import ListOf
from libsignetsim.numl.ResultComponent import ResultComponent

from libsignetsim.settings.Settings import Settings

class ListOfResultComponents(ListOf, list):

	def __init__(self, document):

		ListOf.__init__(self, document)
		self.__document = document
		self.__resultComponentCounter = 0

	def createResultComponent(self):

		result_component = ResultComponent(self.__document)
		result_component.setId("result_component_%d" % self.__resultComponentCounter)
		ListOf.append(self, result_component)
		self.__resultComponentCounter += 1
		return result_component

	def readNuML(self, list_of_result_component, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		ListOf.readNuML(self, list_of_result_component, level, version)

		for result_component in list_of_result_component:
			t_result_component = ResultComponent(self.__document)
			t_result_component.readNuML(result_component, level, version)
			ListOf.append(self, t_result_component)

	def writeNuML(self, numl_document, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		ListOf.writeNuML(self, numl_document.getResultComponents(), level, version)

		for result_component in self:
			t_result_component = numl_document.createResultComponent()
			result_component.writeNuML(t_result_component, level, version)