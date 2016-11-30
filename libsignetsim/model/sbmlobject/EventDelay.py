#!/usr/bin/env python
""" EventDelay.py


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


from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject
from libsignetsim.settings.Settings import Settings

class EventDelay(SbmlObject, MathFormula):
	""" Events priority's definition """

	def __init__ (self, model):

		self.__model = model
		SbmlObject.__init__(self, model)
		MathFormula.__init__(self, model)


	def readSbml(self, sbml_delay,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads an event priority definition from a sbml file """

		SbmlObject.readSbml(self, sbml_delay, sbml_level, sbml_version)
		MathFormula.readSbml(self, sbml_delay.getMath(), sbml_level, sbml_version)


	def writeSbml(self, sbml_event,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes an event priority definition to a sbml file """

		sbml_delay = sbml_event.createDelay()
		SbmlObject.writeSbml(self, sbml_delay, sbml_level, sbml_version)
		sbml_delay.setMath(MathFormula.writeSbml(self, sbml_level, sbml_version))




	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):

		SbmlObject.copy(self, obj, prefix, shift)

		t_convs = {}
		for var, conversion in conversions.items():
			t_convs.update({var:var/conversion})

		t_formula = obj.getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs)
		if time_conversion is not None:
			t_formula *= time_conversion.getInternalMathFormula()

		self.setInternalMathFormula(t_formula)


	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		old_symbol = SympySymbol(old_sbml_id)
		if old_symbol in self.getInternalMathFormula().atoms():
			self.setInternalMathFormula(
				self.getInternalMathFormula().subs(
					old_symbol,
					SympySymbol(new_sbml_id)
				)
			)
