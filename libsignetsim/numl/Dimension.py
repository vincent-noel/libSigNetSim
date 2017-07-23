#!/usr/bin/env python
""" Dimension.py


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
from libsignetsim.numl.NMBase import NMBase
from libsignetsim.settings.Settings import Settings

class Dimension (NMBase):

	def __init__(self, document, result_component, description=None):
		NMBase.__init__(self, document)

		self.__document = document
		self.__resultComponent = result_component
		self.__description = description

	def readNuML(self, dimension, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		# self.__description = dimension.getDescription()
		pass
	def writeNuML(self, dimension, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		pass

	def getResultComponent(self):
		return self.__resultComponent

	def getDescription(self):
		return self.__description
