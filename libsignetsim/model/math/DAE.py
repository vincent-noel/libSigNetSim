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

#from builtins import str
from builtins import object
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyEqual, SympyInteger
from sympy import solve, srepr, pretty


class DAE(object):
	""" DAE class """

	def __init__ (self, model):
		""" Constructor of ode class """
		self.__model = model
		self.__definition = None

	def new(self, definition):
		self.__definition = definition

	def getDefinition(self):
		return self.__definition

	def getFormula(self, rawFormula=True, developped=False):

		if developped:
			t_definition = self.__definition.getDeveloppedInternalMathFormula(rawFormula=rawFormula)
		else:
			t_definition = self.__definition.getInternalMathFormula(rawFormula=rawFormula)

		return SympyEqual(
			t_definition,
			SympyInteger(0)
		)

	def __str__(self):
		return "%s = 0" % str(self.__definition.getDeveloppedInternalMathFormula())

	def pprint(self):
		print(
			pretty(
				SympyEqual(
					self.__definition.getDeveloppedInternalMathFormula(),
					SympyInteger(0)
				)
			)

		)

	def solve(self):

		to_solve = []
		for var in self.__definition.getDeveloppedInternalMathFormula().atoms(SympySymbol):
			variable = self.__model.listOfVariables.getBySymbol(var)

			if variable is not None and variable.isAlgebraic():
				to_solve.append(var)

		return (to_solve[0], solve(self.__definition.getDeveloppedInternalMathFormula(), to_solve))

	def isValid(self):

		return self.__definition.getInternalMathFormula() != MathFormula.ZERO
