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

from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.HasId import HasId
from libsignetsim.sedml.XPath import XPath
from libsignetsim.settings.Settings import Settings


class Change(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__target = XPath(self.__document)

	def readSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, change, level, version)
		HasId.readSedml(self, change, level, version)

		if change.isSetTarget():
			self.__target.readSedml(change.getTarget(), level, version)

	def writeSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, change, level, version)
		HasId.writeSedml(self, change, level, version)

		if self.__target.getXPath() is not None:
			change.setTarget(self.__target.writeSedml(level, version))

	def getTarget(self):
		return self.__target

	def setTarget(self, target):
		self.__target.setModelObject(target)


