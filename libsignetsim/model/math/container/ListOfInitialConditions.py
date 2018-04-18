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

from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyEqual

from sympy import pretty


class ListOfInitialConditions(dict):
	""" Sbml model class """

	def __init__(self, model):
		""" Constructor of model class """

		dict.__init__(self)
		self.__model = model

	def clear(self):
		dict.clear(self)

	def __str__(self):
		res = ""
		for var, value in dict.items(self):
			res += "%s : %s\n" % (var.symbol.getInternalMathFormula(), value.getDeveloppedInternalMathFormula())
		return res

	def pprint(self):

		for var, value in dict.items(self):
			var0 = SympySymbol("(" + str(var) + ")_0")
			print(pretty(SympyEqual(var0, value.getDeveloppedInternalMathFormula())))
			print("\n")