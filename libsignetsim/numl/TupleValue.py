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

from libsignetsim.numl.Dimension import Dimension
from libsignetsim.settings.Settings import Settings

class TupleValue (Dimension):

	def __init__(self, document, description):
		Dimension.__init__(self, document, description)
		self.__document = document

	def readNuML(self, tuple_value, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		Dimension.readNuML(tuple_value, level, version)

	def writeNuML(self, tuple_value, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		pass