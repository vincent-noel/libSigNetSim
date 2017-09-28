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

from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.sbml.SbmlVariable import SbmlVariable
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.ModelException import SbmlException

class Variable(SbmlVariable, MathVariable):

	def __init__(self, model, sbml_type, is_from_reaction=None):

		self.__model = model

		SbmlVariable.__init__(self, model, sbml_type, is_from_reaction)
		MathVariable.__init__(self, model, is_from_reaction)

	def new(self, string, sbml_type=SbmlVariable.PARAMETER):
		SbmlVariable.new(self, string, sbml_type)
		MathVariable.new(self, string)

	def copy(self, obj, sids_subs={}, symbols_subs={}, conversion_factor=None):
		SbmlVariable.copy(self, obj, sids_subs=sids_subs)
		MathVariable.copy(self, obj, symbols_subs=symbols_subs, conversion_factor=conversion_factor)

	def readSbml(self, sbml_variable,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		SbmlVariable.readSbml(self, sbml_variable, sbml_level, sbml_version)
		MathVariable.readSbml(self, sbml_variable, sbml_level, sbml_version)

	def writeSbml(self, sbml_variable,
						sbml_level=Settings.defaultSbmlLevel,
						sbml_version=Settings.defaultSbmlVersion):

		SbmlVariable.writeSbml(self, sbml_variable, sbml_level, sbml_version)
		MathVariable.writeSbml(self, sbml_variable, sbml_level, sbml_version)

	def setSbmlId(self, sbml_id, prefix="", model_wide=True):

		if sbml_id is not None:
			t_sbml_id = prefix + sbml_id
			if t_sbml_id == self.getSbmlId():
				pass

			elif not self.__model.listOfVariables.containsSbmlId(t_sbml_id) or (self.isParameter() and self.isLocalParameter()):
				SbmlVariable.setSbmlId(self, t_sbml_id, prefix, model_wide)
				MathVariable.setSbmlId(self, t_sbml_id, prefix)

			else:
				raise SbmlException("Identifier %s already exist" % sbml_id)

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		""" Function to rename a sbml id which could be countained
			in the variable, aka in the value
		"""
		SbmlVariable.renameSbmlId(self, new_sbml_id)
		MathVariable.renameSbmlId(self, old_sbml_id, new_sbml_id)

	def renameSymbol(self, old_sbml_id, new_sbml_id):
		SbmlVariable.renameSbmlId(self, new_sbml_id)
		MathVariable.renameSymbol(self, old_sbml_id, new_sbml_id)

	def isInAlgebraicRules(self):
		return self.__model.listOfRules.algebraicContainsVariable(self)
