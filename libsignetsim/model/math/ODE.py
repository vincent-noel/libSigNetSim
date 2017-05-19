#!/usr/bin/env python
""" ODE.py


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
from libsignetsim.model.math.sympy_shortcuts import SympyEqual
from sympy import srepr

class ODE(object):
	""" ODE class """

	def __init__ (self, model):
		""" Constructor of ode class """

		self.__model = model
		self.__variable = None
		self.__definition = MathFormula(self.__model)


	def new(self, variable, definition):

		self.__variable = variable
		self.__definition = definition


	def getVariable(self):
		return self.__variable

	def getDefinition(self):
		return self.__definition

	def setVariable(self, variable):
		self.__variable = variable

	def setDefinitionMath(self, definition):
		self.__definition.setInternalMathFormula(definition)

	def getFormula(self, rawFormula=True):

		t_definition = self.__definition.getInternalMathFormula(rawFormula=rawFormula)

		if not rawFormula and self.__variable.isSpecies() and self.__variable.isConcentration():
			t_definition /= self.__variable.getCompartment().symbol.getInternalMathFormula()

		return SympyEqual(
			self.__variable.symbol.getDerivative().getInternalMathFormula(rawFormula=rawFormula),
			t_definition
		)



	def __str__(self):

		return "%s = %s" % (
			str(self.__variable.symbol.getDerivative().getDeveloppedInternalMathFormula()),
			str(self.__definition.getDeveloppedInternalMathFormula())
		)