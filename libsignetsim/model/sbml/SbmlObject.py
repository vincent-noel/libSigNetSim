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

from libsignetsim.model.sbml.SimpleSbmlObject import SimpleSbmlObject
from libsignetsim.model.sbml.HasReplacedElements import HasReplacedElements

from libsignetsim.settings.Settings import Settings


class SbmlObject(SimpleSbmlObject, HasReplacedElements):

	def __init__(self, model):

		self.__model = model
		SimpleSbmlObject.__init__(self, model)
		HasReplacedElements.__init__(self, model)
		self.isMarkedToBeReplaced = False
		self.isMarkedToBeReplacedBy = None
		self.isMarkedToBeDeleted = False
		self.isMarkedToBeRenamed = False
		self.hasConversionFactor = None

	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasReplacedElements.readSbml(self, sbml_object, sbml_level, sbml_version)
		SimpleSbmlObject.readSbml(self, sbml_object, sbml_level, sbml_version)

	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasReplacedElements.writeSbml(self, sbml_object, sbml_level, sbml_version)
		SimpleSbmlObject.writeSbml(self, sbml_object, sbml_level, sbml_version)

	def copy(self, obj, prefix="", shift=0):
		SimpleSbmlObject.copy(self, obj)

	def getModel(self):
		return self.__model
