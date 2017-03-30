#!/usr/bin/env python
""" ListOfRanges.py


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
from libsignetsim.sedml.UniformRange import UniformRange
from libsignetsim.sedml.VectorRange import VectorRange
from libsignetsim.sedml.FunctionalRange import FunctionalRange


from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_RANGE_UNIFORMRANGE, SEDML_RANGE_VECTORRANGE, SEDML_RANGE_FUNCTIONALRANGE
reload(libsbml)


class ListOfRanges(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)
		self.__document = document

	def readSedml(self, list_of_ranges, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_ranges, level, version)

		for tt_range in list_of_ranges:

			if tt_range.getTypeCode() == SEDML_RANGE_UNIFORMRANGE:
				t_range = UniformRange(self.__document)
				t_range.readSedml(tt_range, level, version)
				ListOf.append(self, t_range)

			elif tt_range.getTypeCode() == SEDML_RANGE_VECTORRANGE:
				t_range = VectorRange(self.__document)
				t_range.readSedml(tt_range, level, version)
				ListOf.append(self, t_range)

			elif tt_range.getTypeCode() == SEDML_RANGE_FUNCTIONALRANGE:
				t_range = FunctionalRange(self.__document)
				t_range.readSedml(tt_range, level, version)
				ListOf.append(self, t_range)

	def writeSedml(self, list_of_ranges, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_ranges, level, version)

		for tt_range in self:

			if isinstance(tt_range, UniformRange):
				t_range = list_of_ranges.createUniformRange()
				t_range.writeSedml(tt_range, level, version)

			elif isinstance(tt_range, VectorRange):
				t_range = list_of_ranges.createVectorRange()
				t_range.writeSedml(tt_range, level, version)

			elif isinstance(tt_range, FunctionalRange):
				t_range = list_of_ranges.createFunctionalRange()
				t_range.writeSedml(tt_range, level, version)
