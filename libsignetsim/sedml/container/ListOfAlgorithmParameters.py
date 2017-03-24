#!/usr/bin/env python
""" ListOfAlgorithmParameters.py


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
from libsignetsim.sedml.AlgorithmParameter import AlgorithmParameter
from libsignetsim.settings.Settings import Settings


class ListOfAlgorithmParameters(SedBase):

	def __init__(self, document):

		SedBase.__init__(self, document)

		self.__document = document
		self.listOfAlgorithmParameters = []

	def readSedml(self, list_of_algo_params, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, list_of_algo_params, level, version)

		for t_algo_param in list_of_algo_params:
			algo_param = AlgorithmParameter(self.__document)
			algo_param.readSedml(t_algo_param, level, version)
			self.listOfAlgorithmParameters.append(algo_param)

	def writeSedml(self, list_of_algo_params, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, list_of_algo_params, level, version)

		for t_algo_param in self.listOfAlgorithmParameters:
			algo_param = list_of_algo_params.createAlgorithmParameter()
			algo_param.writeSedml(t_algo_param, level, version)

