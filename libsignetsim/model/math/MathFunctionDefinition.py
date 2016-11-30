#!/usr/bin/env python
""" MathFunctionDefinition.py


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
from libsignetsim.settings.Settings import Settings

class MathFunctionDefinition(object):

	def __init__(self, model):
		self.definition = MathFormula(model, MathFormula.MATH_FUNCTION)


	def readSbml(self, sbml_function_definition, sbml_level, sbml_version):
		self.definition.readSbml(sbml_function_definition.getMath(), sbml_level, sbml_version)


	def writeSbml(self, sbml_function_definition, sbml_level, sbml_version):
		# print "poil"
		# print  self.definition.writeSbml(sbml_level, sbml_version)
		sbml_function_definition.setMath(self.definition.writeSbml(sbml_level, sbml_version))


	def getMathFormulaFunction(self):
		return self.definition.getMathFormula(MathFormula.MATH_INTERNAL).args[1]


	def getMathFormulaFunctionArguments(self):
		return self.definition.getMathFormula(MathFormula.MATH_INTERNAL).args[0]

	def copy(self, obj, prefix="", shift=0):
		self.definition.setInternalMathFormula(obj.definition.getInternalMathFormula())
		if prefix != "":
			self.definition.renameSbmlId(obj.getSbmlId(), prefix+obj.getSbmlId())
