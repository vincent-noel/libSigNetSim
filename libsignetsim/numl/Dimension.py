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

""" Dimension.py

	This file ...

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
		NMBase.readNuML(self, dimension, level, version)

	def writeNuML(self, dimension, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		NMBase.writeNuML(self, dimension, level, version)

	def getResultComponent(self):
		return self.__resultComponent

	def getDescription(self):
		return self.__description
