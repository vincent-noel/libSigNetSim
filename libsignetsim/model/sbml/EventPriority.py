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
from __future__ import division

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.sbml.SimpleSbmlObject import SimpleSbmlObject
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs


class EventPriority(SimpleSbmlObject, MathFormula):
	""" Events priority's definition """

	def __init__(self, model, math_only=False):

		self.__model = model
		MathFormula.__init__(self, model, MathFormula.MATH_PRIORITY)

		self.mathOnly = math_only
		if not self.mathOnly:
			SimpleSbmlObject.__init__(self, model)

	def readSbml(self, sbml_priority,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads an event priority definition from a sbml file """

		SimpleSbmlObject.readSbml(self, sbml_priority, sbml_level, sbml_version)
		MathFormula.readSbml(self, sbml_priority.getMath(), sbml_level, sbml_version)


	def writeSbml(self, sbml_event,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes an event priority definition to a sbml file """

		sbml_priority = sbml_event.createPriority()
		SimpleSbmlObject.writeSbml(self, sbml_priority, sbml_level, sbml_version)
		sbml_priority.setMath(MathFormula.writeSbml(self, sbml_level, sbml_version))


	def copy(self, obj, symbols_subs={}, conversion_factors={}):

		if not self.mathOnly:
			SimpleSbmlObject.copy(self, obj)

		t_convs = {}
		for var, conversion in list(conversion_factors.items()):
			t_convs.update({var: var/conversion})

		t_formula = unevaluatedSubs(obj.getInternalMathFormula(rawFormula=False), symbols_subs)
		t_formula = unevaluatedSubs(t_formula, t_convs)
		MathFormula.setInternalMathFormula(self, t_formula)



	def copySubmodel(self, obj):
		MathFormula.setInternalMathFormula(self, obj.getDeveloppedInternalMathFormula())

