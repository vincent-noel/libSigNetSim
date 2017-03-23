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

from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.DataGenerator import DataGenerator
from libsignetsim.settings.Settings import Settings


class ListOfDataGenerators(SedBase):

	def __init__(self, document):

		SedBase.__init__(self, document)
		self.__document = document
		self.listOfDataGenerators = []

	def readSedml(self, list_of_data_generators, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, list_of_data_generators, level, version)

		for t_data_generator in list_of_data_generators:

			data_generator = DataGenerator(self.__document)
			data_generator.readSedml(t_data_generator, level, version)
			self.listOfDataGenerators.append(data_generator)