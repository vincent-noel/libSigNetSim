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

from libsignetsim.model.math.ODE import ODE

class ListOfODEs(list):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)

	def build(self, including_fast_reactions=True):

		self[:] = []
		for variable in self.__model.listOfVariables:
			if variable.isDerivative():
				t_ode = ODE(self.__model)
				t_ode.new(variable,	variable.getODE(including_fast_reactions, rawFormula=True))
				list.append(self, t_ode)

	def getByVariable(self, variable):

		for ode in self:
			if ode.getVariable() == variable:
				return ode

	def __str__(self):

		res = ""
		for ode in self:
			res += str(ode) + "\n"
		return res

	def pprint(self):

		for ode in self:
			ode.pprint()
			print("\n")

