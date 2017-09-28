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

from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.settings.Settings import Settings


class FunctionDefinition(HasId, SbmlObject):
	""" Function definition definition """

	def __init__ (self, model, obj_id):

		self.__model = model
		self.objId = obj_id

		HasId.__init__(self, model)
		SbmlObject.__init__(self, model)
		self.__definition = MathFormula(model, MathFormula.MATH_FUNCTION)

	def readSbml(self, sbml_function_definition, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads a function definition from a sbml file """

		HasId.readSbml(self, sbml_function_definition, sbml_level, sbml_version)
		SbmlObject.readSbml(self, sbml_function_definition, sbml_level, sbml_version)

		self.__definition.readSbml(sbml_function_definition.getMath(), sbml_level, sbml_version)

	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes a function definition to a sbml file """

		t_function_definition = sbml_model.createFunctionDefinition()
		HasId.writeSbml(self, t_function_definition, sbml_level, sbml_version)
		SbmlObject.writeSbml(self, t_function_definition, sbml_level, sbml_version)
		t_function_definition.setMath(self.__definition.writeSbml(sbml_level, sbml_version))


	def copy(self, obj, sids_subs={}):
		HasId.copy(self, obj, sids_subs=sids_subs)
		SbmlObject.copy(self, obj)
		self.__definition.setInternalMathFormula(obj.getDefinition().getInternalMathFormula())

	def getDefinition(self):
		return self.__definition
