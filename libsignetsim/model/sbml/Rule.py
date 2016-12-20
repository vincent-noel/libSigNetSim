#!/usr/bin/env python
""" Rule.py


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


from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.settings.Settings import Settings


class Rule(SbmlObject):

	RULE_ALGEBRAIC              =   0
	RULE_ASSIGNMENT             =   1
	RULE_RATE                   =   2
	RULE_UNKNOWN                =   3
	RULE_SPECIES_CONCENTRATION  =   4
	RULE_COMPARTMENT_VOLUME     =   5
	RULE_PARAMETER              =   6

	ruleTypes = {RULE_ALGEBRAIC: "Algebraic rule",
				 RULE_ASSIGNMENT: "Assignment rule",
				 RULE_RATE: "Rate rule",
				 RULE_SPECIES_CONCENTRATION: "Species concentration rule",
				 RULE_COMPARTMENT_VOLUME: "Compartment volume rule",
				 RULE_PARAMETER: "Parameter rule"}


	def __init__ (self, model, objId, rule_type=None):

		self.__model = model
		self.objId = objId

		SbmlObject.__init__(self, model)

		self.ruleType = rule_type

		# self.variable = MathSymbol(model)
		# self.definition = MathFormula(model)


	def readSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		SbmlObject.readSbml(self, sbml_rule, sbml_level, sbml_version)

	def writeSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		SbmlObject.writeSbml(self, sbml_rule, sbml_level, sbml_version)

	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], conversions={}):

		SbmlObject.copy(self, obj, prefix, shift)
		self.ruleType = obj.ruleType

	def isAssignment(self):

		return self.ruleType == self.RULE_ASSIGNMENT


	def isRate(self):

		return self.ruleType == self.RULE_RATE

	def isAlgebraic(self):

		return self.ruleType == self.RULE_ALGEBRAIC


	def getType(self):

		return self.ruleType


	def getRuleType(self):

		return self.ruleType

	def getRuleTypeDescription(self):

		return self.ruleTypes[self.ruleType]
