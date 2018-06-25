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
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger
from sympy import simplify, diff, solve


class MathJacobianMatrix(object):


	""" Sbml model class """

	def __init__ (self):
		""" Constructor of model class """

		self.interactionMatrix = None
		self.jacobianMatrix = None


	def buildJacobianMatrix(self, including_fast_reactions=True):

		self.interactionMatrix = []
		self.jacobianMatrix = []

		for ode in self.ODEs:

			partial_ders = []
			signs = []

			for var in self.ODE_vars:

				t_part_der = diff(ode.getDeveloppedInternalMathFormula(), var.getDeveloppedInternalMathFormula())
				t_part_der_formula = MathFormula(self)
				t_part_der_formula.setInternalMathFormula(t_part_der)
				partial_ders.append(t_part_der_formula)

				if t_part_der == MathFormula.ZERO:
					signs.append(0)

				else:
					for atom in t_part_der.atoms(SympySymbol):
						t_part_der = t_part_der.subs({atom: SympyInteger(1)})

					if t_part_der > MathFormula.ZERO:
						signs.append(1)
					elif t_part_der < MathFormula.ZERO:
						signs.append(-1)
					else:
						signs.append(2)

			self.jacobianMatrix.append(partial_ders)
			self.interactionMatrix.append(signs)
