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


"""

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.HasRef import HasRef

class Port(HasId, HasRef):

	def __init__(self, model, obj_id):

		self.__model = model
		self.objId = obj_id
		HasId.__init__(self, model)
		HasRef.__init__(self, model)



	def readSbml(self, sbml_port,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasId.readSbml(self, sbml_port, sbml_level, sbml_version)
		HasRef.readSbml(self, sbml_port, sbml_level, sbml_version)



	def writeSbml(self, sbml_port,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasId.writeSbml(self, sbml_port, sbml_level, sbml_version)
		HasRef.writeSbml(self, sbml_port, sbml_level, sbml_version)
