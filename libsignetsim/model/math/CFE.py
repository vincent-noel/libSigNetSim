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


from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympyEqual
from sympy import simplify, pretty


class CFE(object):
	""" CFE class """

	ASSIGNMENT          = 0
	REACTION            = 1
	SOLVED              = 2

	def __init__(self, model, cfe_type=SOLVED):
		""" Constructor of ode class """

		self.__model = model
		self.__type = cfe_type
		self.__variable = None
		self.__definition = MathFormula(self.__model)

	def new(self, variable, definition):
		self.__variable = variable
		self.__definition = definition

	def getVariable(self):
		return self.__variable

	def getDefinition(self):
		return self.__definition

	def isAssignment(self):
		return self.__type == self.ASSIGNMENT

	def isReaction(self):
		return self.__type == self.REACTION

	def setVariable(self, variable):
		self.__variable = variable

	def setDefinition(self, definition):
		self.__definition = definition

	def setDefinitionMath(self, math):
		self.__definition.setInternalMathFormula(math)

	def getSubs(self):
		return {self.__variable.symbol.getInternalMathFormula():self.__definition.getDeveloppedInternalMathFormula()}

	def __str__(self):
		return "%s = %s" % (
			str(self.getVariable().symbol.getDeveloppedInternalMathFormula()),
			str(self.getDefinition().getDeveloppedInternalMathFormula())
		)

	def pprint(self):
		print(
			pretty(
				SympyEqual(
					self.getVariable().symbol.getDeveloppedInternalMathFormula(),
					self.getDefinition().getDeveloppedInternalMathFormula()
				)
			)
		)

	def getFormula(self, rawFormula=True, developped=False):

		if developped:
			t_definition = self.__definition.getDeveloppedInternalMathFormula(rawFormula=rawFormula)
		else:
			t_definition = self.__definition.getInternalMathFormula(rawFormula=rawFormula)

		if not rawFormula:
			if self.__variable.isSpecies() and self.__variable.isConcentration():
				t_definition /= self.__variable.getCompartment().symbol.getInternalMathFormula()
			elif self.__variable.isReaction() and len(self.__variable.listOfReactants) > 0:
				t_definition /= self.__variable.listOfReactants[0].getSpecies().getCompartment().symbol.getInternalMathFormula()

		return SympyEqual(
			self.__variable.symbol.getInternalMathFormula(rawFormula=rawFormula, developped=developped),
			t_definition
		)
