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
from libsignetsim.sedml.DataSet import DataSet
from libsignetsim.settings.Settings import Settings

class ListOfDataSets(ListOf):

	def __init__(self, document, report):

		ListOf.__init__(self, document)

		self.__document = document
		self.__report = report
		self.__dataSetCounter = 0

	def new(self, data_set_id=None):

		t_data_set_id = data_set_id
		if t_data_set_id is None:
			t_data_set_id = "%s_dataset_%d" % (self.__report.getId(), self.__dataSetCounter)

		data_set = DataSet(self.__document)
		data_set.setId(t_data_set_id)
		ListOf.append(self, data_set)
		self.__dataSetCounter += 1
		return data_set

	def createDataSet(self, data_set_id=None):
		return self.new(data_set_id)

	def readSedml(self, list_of_data_sets, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_data_sets, level, version)

		for t_data_set in list_of_data_sets:
			data_set = DataSet(self.__document)
			data_set.readSedml(t_data_set, level, version)
			ListOf.append(self, data_set)
			self.__dataSetCounter += 1

	def writeSedml(self, list_of_data_sets, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_data_sets, level, version)

		for t_data_set in self:
			data_set = list_of_data_sets.createDataSet()
			t_data_set.writeSedml(data_set, level, version)

	def getData(self):

		data = {}

		for data_set in self:
			data.update(data_set.getData())

		return data

	def getDataToGenerate(self):

		data = []
		for data_set in self:
			data.append(data_set.getDataToGenerate())

		return list(set(data))