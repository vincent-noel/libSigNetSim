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


from libsbml import formulaToString
from libsignetsim.settings.Settings import Settings

class Constraint(object):
	""" Constraint definition """

	def __init__ (self, model, obj_id):

		self.model = model
		self.objId = obj_id
		self.sbmlId = None

		self.math = None
		self.message = None


	def readSbml(self, constraint, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads constraint from a sbml file """

		self.sbmlId = constraint.getId()
		self.math = formulaToString(constraint.getMath())
		self.message = constraint.getMessage()


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes constraint to a sbml file """

		sbml_constraint = sbml_model.createConstraint()
		sbml_constraint.setId(self.sbmlId)
		sbml_constraint.setMath(self.math)
		sbml_constraint.setMessage(self.message)
