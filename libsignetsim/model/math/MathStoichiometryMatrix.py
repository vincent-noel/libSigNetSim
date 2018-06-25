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


from libsignetsim.settings.Settings import Settings
from sympy import pretty
from time import time


class MathStoichiometryMatrix(object):
	""" Sbml model class """

	def __init__(self, model):
		""" Constructor of model class """

		self.__model = model
		self.stoichiometryMatrix = None

	def __str__(self):
		return pretty(self.stoichiometryMatrix)

	def pprint(self):
		print(pretty(self.stoichiometryMatrix))

	def build(self, including_fast_reactions=True, including_slow_reactions=True, include_variable_stoichiometry=False):

		t0 = time()

		subs = {}
		for var, value in list(self.__model.listOfInitialConditions.items()):
			subs.update({var: value.getInternalMathFormula()})

		matrix = None
		for i, reaction in enumerate(self.__model.listOfReactions):

			reaction_matrix = reaction.getStoichiometryMatrix(subs,
					including_fast_reactions=including_fast_reactions,
					including_slow_reactions=including_slow_reactions,
					include_variable_stoichiometry=include_variable_stoichiometry
			)

			if matrix is None:
				matrix = reaction_matrix
			else:
				matrix = matrix.row_join(reaction_matrix)

		self.stoichiometryMatrix = matrix

		if Settings.verboseTiming >= 2:
			print("reaction matrix built in %.2gs" % (time()-t0))

	def getStoichiometryMatrix(self, including_fast_reactions=True, including_slow_reactions=True, include_variable_stoichiometry=False):

		if self.stoichiometryMatrix is None:
			self.build(including_fast_reactions, including_slow_reactions, include_variable_stoichiometry)
		return self.stoichiometryMatrix
