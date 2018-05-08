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
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.model.sbml.Rule import Rule
from libsignetsim.model.sbml.AssignmentRule import AssignmentRule
from libsignetsim.model.sbml.RateRule import RateRule
from libsignetsim.model.sbml.AlgebraicRule import AlgebraicRule
from libsignetsim.settings.Settings import Settings
from libsbml import RULE_TYPE_SCALAR, RULE_TYPE_RATE

class ListOfRules(ListOf, SbmlObject):
	""" Container for the rules of a sbml model"""

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		SbmlObject.__init__(self, model)

	def readSbml(self, sbml_listOfRules,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		""" Reads rules' list from a sbml file """

		for sbml_rule in sbml_listOfRules:
			if sbml_level >= 2:
				if sbml_rule.isAssignment():
					t_rule = AssignmentRule(self.__model, self.nextId())
				elif sbml_rule.isRate():
					t_rule = RateRule(self.__model, self.nextId())
				elif sbml_rule.isAlgebraic():
					t_rule = AlgebraicRule(self.__model, self.nextId())
				else:
					t_rule = Rule(self.__model, self.nextId())
			else:
				if sbml_rule.getType() == RULE_TYPE_SCALAR:
					t_rule = AssignmentRule(self.__model, self.nextId())
				elif sbml_rule.getType() == RULE_TYPE_RATE:
					t_rule = RateRule(self.__model, self.nextId())
				else:
					t_rule = AlgebraicRule(self.__model, self.nextId())

			t_rule.readSbml(sbml_rule, sbml_level, sbml_version)
			ListOf.add(self, t_rule)

		SbmlObject.readSbml(self, sbml_listOfRules, sbml_level, sbml_version)

	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		""" Writes rules' list to a sbml file """

		for rule in self:
			rule.writeSbml(sbml_model, sbml_level, sbml_version)

		if len(self):
			SbmlObject.writeSbml(self, sbml_model.getListOfRules(), sbml_level, sbml_version)

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, conversion_factors={}, time_conversion=None):

		if obj not in deletions:
			SbmlObject.copy(self, obj)

			for sbml_rule in obj:

				if sbml_rule not in deletions:

					if sbml_rule.isAssignment():
						t_rule = AssignmentRule(self.__model, self.nextId())
						t_rule.copy(sbml_rule, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factors=conversion_factors)
					elif sbml_rule.isRate():
						t_rule = RateRule(self.__model, self.nextId())
						t_rule.copy(sbml_rule, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factors=conversion_factors, time_conversion=time_conversion)
					elif sbml_rule.isAlgebraic():
						t_rule = AlgebraicRule(self.__model, self.nextId())
						t_rule.copy(sbml_rule, symbols_subs=symbols_subs)

					ListOf.add(self, t_rule)

	def getByVariable(self, variable, pos=0):
		""" Finds rules by variable """
		return [r for r in self if r.variable.getSbmlMathFormula() == variable][pos]

	def hasAssignmentRule(self):
		""" Checks if there is at least one algebraic rule """
		for rule in self:
			if rule.isAssignment():
				return True
		return False

	def hasAlgebraicRule(self):
		""" Checks if there is at least one algebraic rule """
		for rule in self:
			if rule.isAlgebraic():
				return True

		if self.__model.listOfReactions.hasFastReaction():
			return True
		return False

	def countAlgebraicRules(self):
		nb = 0
		for rule in self:
			if rule.isAlgebraic():
				nb += 1

		return nb

	def algebraicContainsVariable(self, variable):
		for rule in self:
			if rule.isAlgebraic():
				if rule.containsVariable(variable):
					return True
		return False

	def newAlgebraicRule(self, expression=None, rawFormula=False):
		return self.new(Rule.RULE_ALGEBRAIC, expression=expression, rawFormula=rawFormula)

	def newAssignmentRule(self, variable=None, expression=None, rawFormula=False):
		return self.new(Rule.RULE_ASSIGNMENT, variable=variable, expression=expression, rawFormula=rawFormula)

	def newRateRule(self, variable=None, expression=None, rawFormula=False):
		return self.new(Rule.RULE_RATE, variable=variable, expression=expression, rawFormula=rawFormula)

	def new(self, rule_type, variable=None, expression=None, rawFormula=False):

		t_rule = None

		if rule_type == Rule.RULE_ALGEBRAIC:
			t_rule = AlgebraicRule(self.__model, self.nextId())
			if expression is not None:
				t_rule.setPrettyPrintDefinition(expression, rawFormula=rawFormula)

		elif rule_type == Rule.RULE_ASSIGNMENT:
			t_rule = AssignmentRule(self.__model, self.nextId())
			if (variable is not None and expression is not None):
				t_rule.setVariable(variable)
				t_rule.setPrettyPrintDefinition(expression, rawFormula=rawFormula)

		elif rule_type == Rule.RULE_RATE:
			t_rule = RateRule(self.__model, self.nextId())
			if (variable is not None and expression is not None):
				t_rule.setVariable(variable)
				t_rule.setPrettyPrintDefinition(expression, rawFormula=rawFormula)

		ListOf.add(self, t_rule)
		SbmlObject.new(t_rule)
		return t_rule

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		for rule in self:
			rule.renameSbmlId(old_sbml_id, new_sbml_id)

	def containsVariable(self, variable):

		for rule in self:
			if rule.containsVariable(variable):
				return True
		return False

	def remove(self, rule):
		""" Remove a rule from the list """

		if rule.isAssignment() or rule.isRate():
			rule.getVariable().unsetRuledBy()

		ListOf.remove(self, rule)

	def removeById(self, rule_obj_id):
		""" Remove a rule from the list """

		self.remove(self.getById(rule_obj_id))
