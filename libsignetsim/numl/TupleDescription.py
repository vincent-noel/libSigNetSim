#!/usr/bin/env python
""" TupleDescription.py


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

from libsignetsim.numl.DimensionDescription import DimensionDescription
from libsignetsim.settings.Settings import Settings

class TupleDescription (DimensionDescription):

	def __init__(self, document, name=None):
		DimensionDescription.__init__(self, document, name)
		self.__document = document
		self.__atomicDescriptions = []

	def readNuML(self, tuple_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		DimensionDescription.readNuML(tuple_description, level, version)
		for atomic_description in tuple_description.getAtomicDescriptions():
			pass

	def writeNuML(self, tuple_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		pass