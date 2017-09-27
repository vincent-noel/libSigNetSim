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

""" Range.py

	This file ...

"""

from libsignetsim.sedml.HasId import HasId
from libsignetsim.settings.Settings import Settings


class Range(HasId):

	def __init__(self, document):

		HasId.__init__(self, document)
		self.__document = document

	def readSedml(self, abstract_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		HasId.readSedml(self, abstract_range, level, version)

	def writeSedml(self, abstract_range, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		HasId.writeSedml(self, abstract_range, level, version)
