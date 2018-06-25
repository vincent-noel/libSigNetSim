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
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.ModelException import SbmlException
from libsignetsim.model.math.MathException import MathException
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyEqual, SympyUnequal, SympyGreaterThan, SympyLessThan,
	SympyStrictGreaterThan, SympyStrictLessThan, SympyAnd, SympyOr, SympyXor, SympyTrue, SympyFalse
)

from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

from libsbml import parseL3Formula
from sympy import srepr, simplify


class EventTrigger(MathFormula, SbmlObject):
	""" Events definition """

	def __init__(self, model, math_only=False):

		self.__model = model

		MathFormula.__init__(self, model, MathFormula.MATH_EQUATION)
		self.initialValue = False
		self.isPersistent = True
		self.mathOnly = math_only
		if not self.mathOnly:
			SbmlObject.__init__(self, model)

	def readSbml(self, sbml_trigger, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads an event definition from a sbml file """

		SbmlObject.readSbml(self, sbml_trigger, sbml_level, sbml_version)
		MathFormula.readSbml(self, sbml_trigger.getMath(), sbml_level, sbml_version)
		MathFormula.setInternalMathFormula(self, MathFormula.ensureBool(self, MathFormula.getInternalMathFormula(self)))
		if sbml_level >= 3:
			self.isPersistent = sbml_trigger.getPersistent()
			self.initialValue = sbml_trigger.getInitialValue()

	def writeSbml(self, sbml_event, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an event definition to a sbml file """

		sbml_trigger = sbml_event.createTrigger()
		SbmlObject.writeSbml(self, sbml_trigger, sbml_level, sbml_version)

		sbml_trigger.setMath(MathFormula.writeSbml(self, sbml_level, sbml_version))

		if sbml_level >= 3:
			sbml_trigger.setPersistent(self.isPersistent)
			sbml_trigger.setInitialValue(self.initialValue)

		sbml_event.setTrigger(sbml_trigger)

	def copy(self, obj, symbols_subs={}, conversion_factors={}):

		if not self.mathOnly:
			SbmlObject.copy(self, obj)

		t_convs = {}
		for var, conversion in list(conversion_factors.items()):
			t_convs.update({var: var/conversion})

		t_formula = unevaluatedSubs(obj.getInternalMathFormula(rawFormula=False), symbols_subs)
		t_formula = unevaluatedSubs(t_formula, t_convs)
		MathFormula.setInternalMathFormula(self, t_formula)

		self.initialValue = obj.initialValue
		self.isPersistent = obj.isPersistent

	def copySubmodel(self, obj):

		MathFormula.setInternalMathFormula(self, obj.getDeveloppedInternalMathFormula())
		self.initialValue = obj.initialValue
		self.isPersistent = obj.isPersistent

	def setPrettyPrintMathFormula(self, string, rawFormula=False):
		""" Sets the formula for substance. If forcedConcentration, the species are replaced by their concentration"""

		sbml_formula = parseL3Formula(str(string))
		if sbml_formula is None:
			raise SbmlException("MathFormula : Unable to parse math formula")

		MathFormula.readSbml(self, sbml_formula, self.sbmlLevel, self.sbmlVersion)
		if not rawFormula:
			t_subs_mask = {}
			for t_var in self.__model.listOfSpecies:
				if t_var.isConcentration():
					t_symbol = SympySymbol("_speciesForcedConcentration_%s_" % str(t_var.symbol.getInternalMathFormula()))
					t_subs_mask.update({t_var.symbol.getInternalMathFormula(): t_symbol})

			MathFormula.setInternalMathFormula(self, MathFormula.getInternalMathFormula(self).subs(t_subs_mask))

	def getRootsFunctions(self):
		return self.generateRootsFunctions(simplify(MathFormula.getDeveloppedInternalMathFormula(self)))

	def generateRootsFunctions(self, tree):

		if tree.func in [SympyAnd, SympyOr, SympyXor]:
			return (
				self.generateRootsFunctions(tree.args[0])
				+ self.generateRootsFunctions(tree.args[1])
			)

		elif tree == SympyTrue:
			return ["(1)"]

		elif tree == SympyFalse:
			return ["(0)"]

		else:
			if tree.func in [SympyLessThan, SympyStrictLessThan]:
				return ["(%s - %s)" % (
					MathFormula.writeCCode(self, tree.args[1]),
					MathFormula.writeCCode(self, tree.args[0])
				)]
			else:

				return ["(%s - %s)" % (
					MathFormula.writeCCode(self, tree.args[0]),
					MathFormula.writeCCode(self, tree.args[1])
				)]

	def getDeactivationCondition(self, shift=0):

			i_event = shift
			(res, i_event) = self.generateDeactivationCondition(MathFormula.getDeveloppedInternalMathFormula(self), i_event)
			return res, i_event

	def generateDeactivationCondition(self, tree, i_event):

		res_i_event = i_event

		if tree.func == SympyAnd:
			(t_cond_0, res_i_event) = self.generateDeactivationCondition(tree.args[0], res_i_event)
			(t_cond_1, res_i_event) = self.generateDeactivationCondition(tree.args[1], res_i_event)
			return ("(%s || %s)" % (t_cond_0, t_cond_1) , res_i_event)

		elif tree.func == SympyOr:
			(t_cond_0, res_i_event) = self.generateDeactivationCondition(tree.args[0], res_i_event)
			(t_cond_1, res_i_event) = self.generateDeactivationCondition(tree.args[1], res_i_event)
			return ("(%s && %s)" % (t_cond_0, t_cond_1) , res_i_event)

		elif tree.func == SympyXor:
			(t_cond_0, res_i_event) = self.generateDeactivationCondition(tree.args[0], res_i_event)
			(t_cond_1, res_i_event) = self.generateDeactivationCondition(tree.args[1], res_i_event)
			return ("(%s && %s) || (!%s && !%s))" % (t_cond_0, t_cond_1, t_cond_0, t_cond_1) , res_i_event)

		else:
			return ("(data->roots_triggers[%d] == -1)" % res_i_event, res_i_event+1)

	def getActivationCondition(self, shift=0):

			i_event = shift
			(res, i_event) = self.generateActivationCondition(
								simplify(MathFormula.getDeveloppedInternalMathFormula(self)),
								i_event)
			return res, i_event

	def generateActivationCondition(self, tree, i_event):

		res_i_event = i_event

		if tree.func == SympyAnd:
			(t_cond_0, res_i_event) = self.generateActivationCondition(tree.args[0], res_i_event)
			(t_cond_1, res_i_event) = self.generateActivationCondition(tree.args[1], res_i_event)
			return ("(%s && %s)" % (t_cond_0, t_cond_1) , res_i_event)

		elif tree.func == SympyOr:
			(t_cond_0, res_i_event) = self.generateActivationCondition(tree.args[0], res_i_event)
			(t_cond_1, res_i_event) = self.generateActivationCondition(tree.args[1], res_i_event)
			return ("(%s || %s)" % (t_cond_0, t_cond_1) , res_i_event)

		elif tree.func == SympyXor:
			(t_cond_0, res_i_event) = self.generateActivationCondition(tree.args[0], res_i_event)
			(t_cond_1, res_i_event) = self.generateActivationCondition(tree.args[1], res_i_event)
			return ("(%s || %s) && (!(%s && %s))" % (t_cond_0, t_cond_1, t_cond_0, t_cond_1) , res_i_event)

		else:
			return ("(data->roots_triggers[%d] == 1)" % res_i_event, res_i_event+1)

	def nbRoots(self):
		return self.countRoots(simplify(MathFormula.getDeveloppedInternalMathFormula(self)), 0)

	def countRoots(self, tree, counter):

		res_counter = counter

		if tree.func in [SympyAnd, SympyOr, SympyXor]:
			res_counter = self.countRoots(tree.args[0], res_counter)
			res_counter = self.countRoots(tree.args[1], res_counter)
			return res_counter

		else:
			return res_counter + 1

	def getRootsOperator(self):
		return self.generateRootsOperator(simplify(MathFormula.getDeveloppedInternalMathFormula(self)), [])

	def generateRootsOperator(self, tree, t_list):

		if tree.func in [SympyAnd, SympyOr, SympyXor]:
			t_list += self.generateRootsOperator(tree.args[0], t_list)
			t_list += self.generateRootsOperator(tree.args[1], t_list)
			return t_list

		else:
			if tree.func in [SympyStrictGreaterThan, SympyStrictLessThan]:
				return [1]
			elif tree.func in [SympyGreaterThan, SympyLessThan]:
				return [0]
			elif tree.func == SympyEqual:
				return [2]
			elif tree.func == SympyUnequal:
				return [3]
			elif tree == SympyTrue or tree == SympyFalse:
				return [3]
			else:
				raise MathException("Event Trigger : Unknown logical operator %s" % srepr(tree.func))

	def getOperator(self):
		return MathFormula.getInternalMathFormula(self).func

	def isValid(self):
		return MathFormula.getInternalMathFormula(self) is not None