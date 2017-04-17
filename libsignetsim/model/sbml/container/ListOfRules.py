#!/usr/bin/env python
""" ListOfRules.py


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

		for rule in ListOf.values(self):
			rule.writeSbml(sbml_model, sbml_level, sbml_version)

		SbmlObject.writeSbml(self, sbml_model, sbml_level, sbml_version)


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):


		if len(self.keys()) > 0:
			t_shift = max(self.keys())+1
		else:
			t_shift = 0

		if obj not in deletions:
			SbmlObject.copy(self, obj, prefix, t_shift)

			for sbml_rule in obj.values():

				if sbml_rule not in deletions:
					t_obj_id = t_shift + sbml_rule.objId

					if sbml_rule.isAssignment():
						t_rule = AssignmentRule(self.__model, t_obj_id)
					elif sbml_rule.isRate():
						t_rule = RateRule(self.__model, t_obj_id)
					elif sbml_rule.isAlgebraic():
						t_rule = AlgebraicRule(self.__model, t_obj_id)
					else:
						t_rule = Rule(self.__model, t_obj_id)

					if not sbml_rule.isMarkedToBeReplaced:
						t_rule.copy(sbml_rule, prefix, t_shift, subs,
											deletions, replacements,
											conversions, time_conversion)
					else:
						t_rule.copy(sbml_rule.isMarkedToBeReplacedBy,
											prefix, t_shift, subs, deletions,
											replacements, conversions,
											time_conversion)

					if sbml_rule.isMarkedToBeRenamed:
						t_rule.setSbmlId(sbml_rule.getSbmlId(),
											model_wide=False)

					ListOf.add(self, t_rule)




	def getByVariable(self, variable, pos=0):
		""" Finds rules by variable """
		return [r for _, r in ListOf.items(self) if r.variable.getSbmlMathFormula() == variable][pos]


	# def getSpeciesAssignmentRules(self):
	#     """ Finds rules for species assignment """
	#     return [r for _, r in self.items()
	#             if r.isAssignment == True and r.isSpeciesAssignment == True]


	def hasAssignmentRule(self):
		""" Checks if there is at least one algebraic rule """
		for rule in ListOf.values(self):
			if rule.isAssignment():
				return True
		return False

	def hasAlgebraicRule(self):
		""" Checks if there is at least one algebraic rule """
		for rule in ListOf.values(self):
			if rule.isAlgebraic():
				return True

		if self.__model.listOfReactions.hasFastReaction():
			return True
		return False

	def countAlgebraicRules(self):
		nb = 0
		for rule in ListOf.values(self):
			if rule.isAlgebraic():
				nb += 1

		return nb

	def algebraicContainsVariable(self, variable):
		for rule in ListOf.values(self):
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
		return t_rule


	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		for rule in ListOf.values(self):
			# if rule.rule_type == Rule.RULE_RATE:
			rule.renameSbmlId(old_sbml_id, new_sbml_id)


	def containsVariable(self, variable):

		for rule in ListOf.values(self):
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
