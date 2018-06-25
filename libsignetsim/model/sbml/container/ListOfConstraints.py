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

from libsignetsim.model.sbml.container.ListOf import ListOf
from libsignetsim.model.sbml.container.HasIds import HasIds
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.model.sbml.Constraint import Constraint
from libsignetsim.settings.Settings import Settings


class ListOfConstraints(ListOf, HasIds, SbmlObject):
	""" Class for the listOfConstraints in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_list_of_constraints,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads a constraints' list from a sbml file """

		for constraint in sbml_list_of_constraints:
			t_constraint = Constraint(self.__model, self.nextId())
			t_constraint.readSbml(constraint, sbml_level, sbml_version)
			ListOf.add(self, t_constraint)

		SbmlObject.readSbml(self, sbml_list_of_constraints, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes a constraints' list to a sbml file """

		for constraint in self:
			constraint.writeSbml(sbml_model,sbml_level, sbml_version)

		if len(self) > 0:
			SbmlObject.writeSbml(self, sbml_model.getListOfConstraints(), sbml_level, sbml_version)
