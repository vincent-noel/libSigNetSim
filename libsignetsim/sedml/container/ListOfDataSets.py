#!/usr/bin/env python
""" ListOfDataSets.py


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
from libsignetsim.sedml.DataSet import DataSet
from libsignetsim.settings.Settings import Settings

class ListOfDataSets(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)

		self.__document = document

	def readSedml(self, list_of_data_sets, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_data_sets, level, version)

		for t_data_set in list_of_data_sets:
			data_set = DataSet(self.__document)
			data_set.readSedml(t_data_set, level, version)
			ListOf.append(self, data_set)

	def writeSedml(self, list_of_data_sets, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_data_sets, level, version)

		for t_data_set in self:
			data_set = list_of_data_sets.createDataSet()
			t_data_set.writeSedml(data_set, level, version)

	def build(self):

		for data_set in self:
			data_set.build()

	def getData(self):

		data = {}

		for data_set in self:
			data.update(data_set.getData())

		return data
