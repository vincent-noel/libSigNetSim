#!/usr/bin/env python
""" AlgebraicRule.py


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


from libsignetsim.model.sbmlobject.Rule import Rule
from libsignetsim.model.math.MathAlgebraicRule import MathAlgebraicRule
from libsignetsim.settings.Settings import Settings

class AlgebraicRule(Rule, MathAlgebraicRule):
	""" Class for rate rules """

	def __init__ (self, model, objId):

		Rule.__init__(self, model, objId, Rule.RULE_ALGEBRAIC)
		MathAlgebraicRule.__init__(self, model)


	def readSbml(self, sbml_rule,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		Rule.readSbml(self, sbml_rule, sbml_level, sbml_version)
		MathAlgebraicRule.readSbml(self, sbml_rule, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		sbml_rule = sbml_model.createAlgebraicRule()
		Rule.writeSbml(self, sbml_rule, sbml_level, sbml_version)
		MathAlgebraicRule.writeSbml(self, sbml_rule, sbml_level, sbml_version)


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):
		Rule.copy(self, obj, prefix, shift)
		MathAlgebraicRule.copy(self, obj, prefix, shift, subs, deletions, replacements, conversions)

	def getExpression(self):
		return self.getPrettyPrintDefinition()


	def setExpression(self, string):
		self.setPrettyPrintDefinition(string)
