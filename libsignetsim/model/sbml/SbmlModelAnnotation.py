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


from libsignetsim.model.sbml.SbmlModelHistory import SbmlModelHistory

from libsignetsim.settings.Settings import Settings
class SbmlModelAnnotation(object):


	def __init__(self):

		self.modelHistory = SbmlModelHistory(self)

	def readSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		self.modelHistory.readSbml(sbml_model, self.sbmlLevel, self.sbmlVersion)

	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		self.modelHistory.writeSbml(sbml_model, self.sbmlLevel, self.sbmlVersion)

	def getListOfSBOTermsDescriptions(self):

		res = []
		for object in self.listOfSbmlObjects:
			t_description = object.getAnnotation().getSBOTermDescription()
			if t_description is not None:
				res.append(t_description)

		return res
