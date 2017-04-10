#!/usr/bin/env python
""" SbmlModelAnnotation.py


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

