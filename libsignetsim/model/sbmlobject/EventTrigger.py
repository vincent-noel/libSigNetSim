#!/usr/bin/env python
""" EventTrigger.py


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
from libsignetsim.model.sbmlobject.EventAssignment import EventAssignment
from libsignetsim.model.math.MathEventTrigger import MathEventTrigger
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.sbmlobject.HasId import HasId
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import  (
	SympySymbol, SympyInteger, SympyFloat, SympyRational, SympyAtom,
	SympyOne, SympyNegOne, SympyZero, SympyPi, SympyE, SympyExp1, SympyHalf,
	SympyInf, SympyNan, SympyAdd, SympyMul, SympyPow,
	SympyFunction, SympyUndefinedFunction, SympyLambda, SympyDerivative,
	SympyCeiling, SympyFloor, SympyAbs, SympyLog, SympyExp, SympyPiecewise,
	SympyFactorial, SympyRoot, SympyAcos, SympyAsin, SympyAtan, SympyAcosh,
	SympyAsinh, SympyAtanh, SympyCos, SympySin, SympyTan, SympyAcot,
	SympyAcoth, SympyCosh, SympySinh, SympyTanh, SympySec, SympyCsc,
	SympyCot, SympyCoth, SympyAcsc, SympyAsec,
	SympyEqual, SympyUnequal, SympyGreaterThan, SympyLessThan,
	SympyStrictGreaterThan, SympyStrictLessThan,
	SympyAnd, SympyOr, SympyXor, SympyNot, SympyTrue, SympyFalse,
	SympyMax, SympyMin)

class EventTrigger(MathEventTrigger):
	""" Events definition """

	def __init__ (self, model):

		self.__model = model

		MathEventTrigger.__init__(self, model)

		self.initialValue = True
		self.isPersistent = True


	def readSbml(self, sbml_trigger, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads an event definition from a sbml file """

		MathEventTrigger.readSbml(self, sbml_trigger.getMath(), sbml_level, sbml_version)

		if sbml_level >= 3:
			self.isPersistent = sbml_trigger.getPersistent()
			self.initialValue = sbml_trigger.getInitialValue()


	def writeSbml(self, sbml_event, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an event definition to a sbml file """

		sbml_trigger = sbml_event.createTrigger()
		sbml_trigger.setMath(MathEventTrigger.writeSbml(self, sbml_level, sbml_version))

		if sbml_level >= 3:
			sbml_trigger.setPersistent(self.isPersistent)
			sbml_trigger.setInitialValue(self.initialValue)

		sbml_event.setTrigger(sbml_trigger)


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}):

		MathEventTrigger.copy(self, obj, prefix, shift, subs, deletions, replacements, conversions)
		self.initialValue = obj.initialValue
		self.isPersistent = obj.isPersistent

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		old_symbol = SympySymbol(old_sbml_id)
		if old_symbol in self.getInternalMathFormula().atoms():
			self.setInternalMathFormula(
				self.getInternalMathFormula().subs(
					old_symbol,
					SympySymbol(new_sbml_id)
				)
			)
