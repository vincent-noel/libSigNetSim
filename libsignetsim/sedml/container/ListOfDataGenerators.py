#!/usr/bin/env python
""" ListOfDataGenerators.py


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
from libsignetsim.sedml.DataGenerator import DataGenerator
from libsignetsim.settings.Settings import Settings


class ListOfDataGenerators(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)
		self.__document = document
		self.__dataGeneratorCounter = 0

	def new(self, data_generator_id=None):

		t_data_generator_id = data_generator_id
		if t_data_generator_id is None:
			t_data_generator_id = "datagenerator_%d" % self.__dataGeneratorCounter

		data_generator = DataGenerator(self.__document)
		data_generator.setId(t_data_generator_id)
		ListOf.append(self, data_generator)
		self.__dataGeneratorCounter += 1
		return data_generator


	def createDataGenerator(self, data_generator_id=None):
		return self.new(data_generator_id)


	def readSedml(self, list_of_data_generators, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_data_generators, level, version)

		for t_data_generator in list_of_data_generators:

			data_generator = DataGenerator(self.__document)
			data_generator.readSedml(t_data_generator, level, version)
			ListOf.append(self, data_generator)
			self.__dataGeneratorCounter += 1

	def writeSedml(self, list_of_data_generators, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_data_generators, level, version)

		for t_data_generator in self:
			data_generator = list_of_data_generators.createDataGenerator()
			t_data_generator.writeSedml(data_generator, level, version)

	def getDataGenerator(self, data_reference):

		for data_generator in self:
			if data_generator.getId() == data_reference:
				return data_generator