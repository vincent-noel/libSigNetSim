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
from libsignetsim.sedml.AlgorithmParameter import AlgorithmParameter
from libsignetsim.settings.Settings import Settings


class ListOfAlgorithmParameters(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)

		self.__document = document
		# self.listOfAlgorithmParameters = []

	def readSedml(self, list_of_algo_params, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_algo_params, level, version)

		for t_algo_param in list_of_algo_params:
			algo_param = AlgorithmParameter(self.__document)
			algo_param.readSedml(t_algo_param, level, version)
			ListOf.append(self, algo_param)

	def writeSedml(self, list_of_algo_params, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_algo_params, level, version)

		for t_algo_param in self:
			algo_param = list_of_algo_params.createAlgorithmParameter()
			t_algo_param.writeSedml(algo_param, level, version)

	def hasRelTol(self):

		for param in self:
			if param.isRelTol():
				return True
		return False

	def hasAbsTol(self):

		for param in self:
			if param.isAbsTol():
				return True
		return False


	def getRelTol(self):

		for param in self:
			if param.isRelTol():
				return float(param.getValue())

	def getAbsTol(self):

		for param in self:
			if param.isAbsTol():
				return float(param.getValue())

	def setRelTol(self, rel_tol):

		param = AlgorithmParameter(self.__document)
		param.setRelTol(rel_tol)
		ListOf.append(self, param)

	def setAbsTol(self, abs_tol):

		param = AlgorithmParameter(self.__document)
		param.setAbsTol(abs_tol)
		ListOf.append(self, param)