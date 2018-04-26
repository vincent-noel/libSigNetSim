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
from libsignetsim.sedml.UniformRange import UniformRange
from libsignetsim.sedml.VectorRange import VectorRange
from libsignetsim.sedml.FunctionalRange import FunctionalRange


from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_RANGE_UNIFORMRANGE, SEDML_RANGE_VECTORRANGE, SEDML_RANGE_FUNCTIONALRANGE
from six.moves import reload_module
reload_module(libsbml)


class ListOfRanges(ListOf):

	def __init__(self, document, repeated_task):

		ListOf.__init__(self, document)
		self.__document = document
		self.__repeatedTask = repeated_task
		self.__rangeCounter = 0

	def new(self, range_type, range_id=None):

		t_range_id = range_id
		if t_range_id is None:
			t_range_id = "%s_range_%d" % (self.__repeatedTask.getId(), self.__rangeCounter)

		if range_type == SEDML_RANGE_UNIFORMRANGE:
			t_range = UniformRange(self.__document)
			t_range.setId(t_range_id)
			ListOf.append(self, t_range)
			self.__rangeCounter += 1
			return t_range

		elif range_type == SEDML_RANGE_VECTORRANGE:
			t_range = VectorRange(self.__document)
			t_range.setId(t_range_id)
			ListOf.append(self, t_range)
			self.__rangeCounter += 1
			return t_range

		elif range_type == SEDML_RANGE_FUNCTIONALRANGE:
			t_range = FunctionalRange(self.__document)
			t_range.setId(t_range_id)
			ListOf.append(self, t_range)
			self.__rangeCounter += 1
			return t_range

	def createUniformRange(self, range_id=None):
		return self.new(SEDML_RANGE_UNIFORMRANGE, range_id)

	def createVectorRange(self, range_id=None):
		return self.new(SEDML_RANGE_VECTORRANGE, range_id)

	def createFunctionalRange(self, range_id=None):
		return self.new(SEDML_RANGE_FUNCTIONALRANGE, range_id)

	def readSedml(self, list_of_ranges, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_ranges, level, version)

		for tt_range in list_of_ranges:

			if tt_range.getTypeCode() == SEDML_RANGE_UNIFORMRANGE:
				t_range = UniformRange(self.__document)
				t_range.readSedml(tt_range, level, version)
				ListOf.append(self, t_range)
				self.__rangeCounter += 1

			elif tt_range.getTypeCode() == SEDML_RANGE_VECTORRANGE:
				t_range = VectorRange(self.__document)
				t_range.readSedml(tt_range, level, version)
				ListOf.append(self, t_range)
				self.__rangeCounter += 1

			elif tt_range.getTypeCode() == SEDML_RANGE_FUNCTIONALRANGE:
				t_range = FunctionalRange(self.__document)
				t_range.readSedml(tt_range, level, version)
				ListOf.append(self, t_range)
				self.__rangeCounter += 1

	def writeSedml(self, list_of_ranges, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_ranges, level, version)

		for tt_range in self:

			if isinstance(tt_range, UniformRange):
				t_range = list_of_ranges.createUniformRange()
				tt_range.writeSedml(t_range, level, version)

			elif isinstance(tt_range, VectorRange):
				t_range = list_of_ranges.createVectorRange()
				tt_range.writeSedml(t_range, level, version)

			elif isinstance(tt_range, FunctionalRange):
				t_range = list_of_ranges.createFunctionalRange()
				tt_range.writeSedml(t_range, level, version)

	def getByRangeId(self, range_id):

		for t_range in self:
			if t_range.getId() == range_id:
				return t_range
