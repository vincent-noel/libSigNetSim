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

from libsignetsim.model.sbml.EventAssignedVariable import EventAssignedVariable
from libsignetsim.model.sbml.InitiallyAssignedVariable import InitiallyAssignedVariable
from libsignetsim.model.sbml.RuledVariable import RuledVariable
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasUnits import HasUnits


class ConservedMoiety(Variable, SbmlObject, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable,
						HasUnits):

	def __init__(self, model):

		SbmlObject.__init__(self, model)
		InitiallyAssignedVariable.__init__(self, model)
		RuledVariable.__init__(self, model)
		EventAssignedVariable.__init__(self, model)
		HasUnits.__init__(self, model)
		Variable.__init__(self, model, Variable.CONSERVED_MOIETY)

		self.__model = model

	def copy(self, parameter, sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factor=None):

		SbmlObject.copy(self, parameter)
		HasUnits.copy(self, parameter, usids_subs=usids_subs)
		Variable.copy(self, parameter, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factor=conversion_factor)

	def new(self, name, value, unit=None):
		""" Creates new compartment with default options """

		SbmlObject.new(self)
		Variable.new(self, name, Variable.CONSERVED_MOIETY)
		HasUnits.new(self, unit)

		self.value.setInternalMathFormula(value)
		self.__model.listOfVariables.changeVariableType(self, Variable.VAR_CST)
