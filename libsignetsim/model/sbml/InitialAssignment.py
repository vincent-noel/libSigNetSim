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
from __future__ import print_function
from __future__ import division

from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger, SympyMul, SympyPow
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from sympy import pretty, Equality, Symbol


class InitialAssignment(SbmlObject, HasParentObj):
	""" Initial assignment definition """

	def __init__(self, model, parent_obj, obj_id, math_only=False):

		self.__model = model
		self.objId = obj_id

		HasParentObj.__init__(self, parent_obj)

		# For math submodels, where objects are not sbml objects
		self.mathOnly = math_only
		if not self.mathOnly:
			SbmlObject.__init__(self, model)

		self.__definition = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
		self.__var = None

	def readSbml(self, initial_assignment, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads an initial assignment from a sbml file """

		SbmlObject.readSbml(self, initial_assignment, sbml_level, sbml_version)

		if self.__model.listOfVariables.containsSbmlId(initial_assignment.getSymbol()):
			self.__var = self.__model.listOfVariables.getBySbmlId(initial_assignment.getSymbol())
			self.getVariable().setInitialAssignmentBy(self)

		self.__definition.readSbml(initial_assignment.getMath(), sbml_level, sbml_version)

		if self.__definition.getInternalMathFormula() is not None:

			if self.getVariable().isConcentration():
				self.__definition.setInternalMathFormula(
					SympyMul(self.__definition.getInternalMathFormula(),
							self.getVariable().getCompartment().symbol.getInternalMathFormula()))

	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an initial assignment to a sbml file """

		sbml_initial_assignment = sbml_model.createInitialAssignment()

		SbmlObject.writeSbml(self, sbml_initial_assignment, sbml_level, sbml_version)

		sbml_initial_assignment.setSymbol(self.__var.getSbmlId())

		if self.__definition.getInternalMathFormula() is not None:

			t_definition = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
			t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula())

			if self.getVariable().isConcentration():
				t_definition.setInternalMathFormula(
					SympyMul(self.__definition.getInternalMathFormula(),
							SympyPow(self.getVariable().getCompartment().symbol.getInternalMathFormula(),
										SympyInteger(-1))))

			sbml_initial_assignment.setMath(t_definition.getSbmlMathFormula(sbml_level, sbml_version))

	def copy(self, obj, sids_subs={}, symbols_subs={}, conversion_factors={}):
		SbmlObject.copy(self, obj)

		if obj.getVariable().getSbmlId() in list(sids_subs.keys()):
			self.__var = self.__model.listOfVariables.getBySbmlId(sids_subs[obj.getVariable().getSbmlId()])
		else:
			self.__var = self.__model.listOfVariables.getBySbmlId(obj.getVariable().getSbmlId())

		self.getVariable().setInitialAssignmentBy(self)

		t_convs = {}
		for var, conversion in list(conversion_factors.items()):
			t_convs.update({var: var/conversion})

		if obj.getDefinition() is not None:
			t_definition = unevaluatedSubs(obj.getDefinition().getInternalMathFormula(), symbols_subs)
			t_definition = unevaluatedSubs(t_definition, t_convs)

			t_var_symbol = unevaluatedSubs(obj.getVariable().symbol.getInternalMathFormula(), symbols_subs)

			if t_var_symbol in conversion_factors:
				t_definition *= conversion_factors[t_var_symbol]

			self.__definition.setInternalMathFormula(t_definition)

	def copySubmodel(self, obj):
		if obj.getDefinition() is not None:
			self.__definition.setInternalMathFormula(obj.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula())
		self.__var = self.__model.listOfVariables.getBySymbol(obj.getVariable().symbol.getSymbol())

	def getVariable(self):
		return self.__var

	def setVariable(self, variable):

		if self.__var is not None:
			self.getVariable().unsetInitialAssignmentBy()

		self.__var = variable
		self.getVariable().setInitialAssignmentBy(self)

	def getRawDefinition(self, rawFormula=False):

		# if self.__definition.getInternalMathFormula() is not None:
		formula = self.__definition.getInternalMathFormula()
		if formula is not None:
			if not rawFormula and self.getVariable().isConcentration():
				formula /= self.getVariable().getCompartment().symbol.getInternalMathFormula()

			if not rawFormula:
				subs = {}
				for species in self.__model.listOfSpecies:
					if species.isConcentration():
						subs.update({species.symbol.getInternalMathFormula(rawFormula=True): species.symbol.getInternalMathFormula()})
				formula = unevaluatedSubs(formula, subs)

		return formula

	def getDefinition(self, rawFormula=False):

		# if self.__definition is not None:
		math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
		math_formula.setInternalMathFormula(self.getRawDefinition(rawFormula=rawFormula))

		return math_formula

	def getRuleTypeDescription(self):
		return "Initial assignment"

	def setPrettyPrintDefinition(self, definition, rawFormula=False):

		if self.getVariable().isConcentration() and not rawFormula:
			t_comp = self.getVariable().getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
			t_math_formula.setPrettyPrintMathFormula(definition, rawFormula=rawFormula)
			self.__definition.setInternalMathFormula(
				t_math_formula.getInternalMathFormula() * t_comp.symbol.getInternalMathFormula())

		else:
			self.__definition.setPrettyPrintMathFormula(definition, rawFormula=rawFormula)

	def getPrettyPrintDefinition(self):

		if self.__definition.getInternalMathFormula() is not None:
			if self.getVariable().isSpecies() and not self.getVariable().hasOnlySubstanceUnits:
				t_comp = self.getVariable().getCompartment()
				t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
				t_math_formula.setInternalMathFormula(
					self.__definition.getInternalMathFormula()/t_comp.symbol.getInternalMathFormula()
				)
				return t_math_formula.getPrettyPrintMathFormula()

			else:
				return self.__definition.getPrettyPrintMathFormula()


	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		if self.__definition.getInternalMathFormula() is not None:
			self.__definition.renameSbmlId(old_sbml_id, new_sbml_id)


	def containsVariable(self, variable):

		if self.__definition.getInternalMathFormula() is not None:
			return (variable.symbol.getInternalMathFormula() in self.__definition.getInternalMathFormula().atoms()
					or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.__definition.getInternalMathFormula().atoms())
					or variable.symbol.getInternalMathFormula() == self.getVariable().symbol.getInternalMathFormula())
		else:
			return False

	def getByXPath(self, xpath):

		if len(xpath) == 0:
			return self

		if len(xpath) > 1:
			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@value":
			return self.getValue()

		elif xpath[0] == "@name":
			return self.getName()

		elif xpath[0] == "@id":
			return self.getSbmlId()


	def getXPath(self, attribute=None):

		xpath = "sbml:initialAssignment"
		xpath += "[@metaid='%s']" % self.getMetaId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])

	def pprint(self):
		print(
			pretty(
				Equality(
					Symbol(str(self.getVariable().symbol.getDeveloppedInternalMathFormula()) + "_0"),
					self.getDefinition().getDeveloppedInternalMathFormula()
				)
			)

		)

	def isValid(self):

		return (
			self.getVariable() is not None
			and self.__definition.getInternalMathFormula() is not None
			and self.__definition.getDeveloppedInternalMathFormula() is not None
		)