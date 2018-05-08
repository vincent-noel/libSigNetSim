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


from libsignetsim.model.math.sympy_shortcuts import SympyEqual, SympyInteger
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from sympy import pretty


class ConservationLaw(object):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		self.LHS = None
		self.RHS = None
		self.vars = []

	def new(self, lhs, rhs, vars):

		self.LHS = lhs
		self.RHS = rhs
		self.vars = vars

	def pprint(self):

		print("%s" % pretty(
			SympyEqual(
				self.LHS.getDeveloppedInternalMathFormula(),
				self.RHS.getDeveloppedInternalMathFormula()
			)
		))


	def __str__(self):
		return ">> %s == %s" % (
			self.LHS.getDeveloppedInternalMathFormula(),
			self.RHS.getDeveloppedInternalMathFormula()
		)


	def getFormula(self, rawFormula=True):

		if not rawFormula:

			comp_symbols = {}
			for comp in self.__model.listOfCompartments:
				comp_symbols.update({comp.symbol.getInternalMathFormula(): SympyInteger(1)})

			return SympyEqual(
				unevaluatedSubs(self.LHS.getInternalMathFormula(), comp_symbols),
				unevaluatedSubs(self.RHS.getInternalMathFormula(), comp_symbols)
			)
		else:
			return SympyEqual(
				self.LHS.getDeveloppedInternalMathFormula(),
				self.RHS.getDeveloppedInternalMathFormula()
			)

	def getNbVars(self):
		return len(self.vars)