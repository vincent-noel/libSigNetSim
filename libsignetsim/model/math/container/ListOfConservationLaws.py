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

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.ConservationLaw import ConservationLaw
from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyInf, SympyNan, SympyAdd, SympyEqual, SympyStrictLessThan
)
from sympy import solve, Lambda, flatten
from time import time

class ListOfConservationLaws(list):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """


		list.__init__(self)
		self.__model = model


	def hasConservationLaws(self):
		return len(self) > 0

	def clear(self):
		del self[:]
	
	def build(self, stoichiometry_matrix=None):

		DEBUG = False

		del self[:]

		if stoichiometry_matrix is None:
			stoichiometry_matrix = self.__model.stoichiometryMatrix
		if stoichiometry_matrix.hasNullSpace():
			for i, t_res in enumerate(stoichiometry_matrix.getSimpleNullspace()):
				t_law = MathFormula.ZERO
				t_value = MathFormula.ZERO

				unknowns = []
				t_vars = []
				nb_vars = 0

				for ii, tt_res in enumerate(t_res):

					tt_symbol = stoichiometry_matrix.listOfSpecies[ii]
					t_species = self.__model.listOfVariables.getBySymbol(tt_symbol)
					tt_symbol_formula = tt_symbol

					if t_species.isSpecies() and not t_species.hasOnlySubstanceUnits:
						tt_symbol_formula /= t_species.getCompartment().symbol.getSymbol()

					if tt_symbol in self.__model.solvedInitialConditions.keys():
						tt_value = self.__model.solvedInitialConditions[tt_symbol].getDeveloppedInternalMathFormula()
						if t_species.isSpecies() and not t_species.hasOnlySubstanceUnits:
							tt_value /= t_species.getCompartment().symbol.getSymbol()

					else:
						t_unknown = SympySymbol("_%s_0_" % str(tt_symbol))
						tt_value = t_unknown

						tt_unknown = MathFormula(self.__model, MathFormula.MATH_VARIABLE)
						tt_unknown.setInternalMathFormula(t_unknown)
						unknowns.append(tt_unknown)

					if tt_res == SympyInteger(1):
						t_law += tt_symbol_formula
						t_value += tt_value
						nb_vars += 1

					elif tt_res == SympyInteger(-1):
						t_law -= tt_symbol_formula
						t_value -= tt_value
						nb_vars += 1

					else:
						t_law += tt_res * tt_symbol_formula
						t_value += tt_res * tt_value
						nb_vars += 1

					t_vars.append(tt_symbol)

				if nb_vars > 1:
					t_vars = []
					for t_atom in t_law.atoms(SympySymbol):

						if not self.__model.listOfVariables.getBySymbol(t_atom).isCompartment():
							t_vars.append(t_atom)

					t_lhs = MathFormula(self.__model)
					t_lhs.setInternalMathFormula(t_law)

					t_rhs = MathFormula(self.__model)
					t_rhs.setInternalMathFormula(t_value)

					if DEBUG:
						print "New conservation law : "
						print "%s = %s" % (str(t_law), str(t_value))
					t_conservation_law = ConservationLaw(self.__model)
					t_conservation_law.new(t_lhs, t_rhs, t_vars)
					list.append(self, t_conservation_law)
				else:
					t_vars = []
					for t_atom in t_law.atoms(SympySymbol):

						if not self.__model.listOfVariables.getBySymbol(t_atom).isCompartment():
							t_vars.append(t_atom)

					t_lhs = MathFormula(self.__model)
					t_lhs.setInternalMathFormula(t_law)

					t_rhs = MathFormula(self.__model)
					t_rhs.setInternalMathFormula(t_value)

					if DEBUG:
						print "New conservation law : "
						print "%s = %s" % (str(t_law), str(t_value))
					t_conservation_law = ConservationLaw(self.__model)
					t_conservation_law.new(t_lhs, t_rhs, [t_vars])
					list.append(self, t_conservation_law)


	def __str__(self):
		res = ""
		for law in self:
			res += "%s\n" % law
		return res