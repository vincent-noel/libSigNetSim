#!/usr/bin/env python
""" CFE.py


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
from sympy import simplify, srepr

class CFE(object):
	""" CFE class """

	ASSIGNMENT          = 0
	REACTION            = 1
	SOLVED              = 2

	def __init__ (self, model, cfe_type=SOLVED):
		""" Constructor of ode class """

		self.__model = model
		self.__type = cfe_type
		self.__variable = None
		self.__definition = None

	def new(self, variable, definition):

		self.__variable = variable

		# print "Simplifying %s..." % str(definition.getDeveloppedInternalMathFormula())
		# self.__definition = simplify(definition.getInternalMathFormula())
		self.__definition = definition


	def getVariable(self):
		return self.__variable

	def getDefinition(self):
		return self.__definition

	def isAssignment(self):
		return self.__type == self.ASSIGNMENT

	def isReaction(self):
		return self.__type == self.REACTION

	def setDefinition(self, definition):
		self.__definition = definition

	def setDefinitionMath(self, math):
		self.__definition.setInternalMathFormula(math)

	def getSubs(self):
		# print ">>>before simplify : %s" % self.__definition.getInternalMathFormula()
		# print "\n\n>>>after simplify : %s" % simplify(self.__definition.getInternalMathFormula())
		#
		# return {self.__variable.symbol.getInternalMathFormula():simplify(self.__definition.getInternalMathFormula())}
		return {self.__variable.symbol.getInternalMathFormula():self.__definition.getDeveloppedInternalMathFormula()}

	def __str__(self):
		return "%s = %s" % (str(self.getVariable().symbol.getDeveloppedInternalMathFormula()),
							str(self.getDefinition().getDeveloppedInternalMathFormula()))
