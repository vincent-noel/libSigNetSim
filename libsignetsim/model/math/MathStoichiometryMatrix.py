#!/usr/bin/env python
""" MathStoichiometryMatrix.py


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


from sympy import simplify, diff, solve, zeros


class MathStoichiometryMatrix(object):
    """ Sbml model class """

    def __init__ (self):
        """ Constructor of model class """

        self.stoichiometryMatrix = None


    def buildStoichiometryMatrix(self, including_fast_reactions=True):

        matrix = None
        for i, reaction in enumerate(self.listOfReactions.values()):
            if (not reaction.fast) or including_fast_reactions:

                if matrix is None:
                    matrix = reaction.getStoichiometryMatrix_v2()
                else:
                    matrix  += reaction.getStoichiometryMatrix_v2()

        self.stoichiometryMatrix = matrix


    def getSimpleStoichiometryMatrix(self):

        if self.stoichiometryMatrix is None:
            self.buildStoichiometryMatrix()

        matrix = None
        if self.stoichiometryMatrix != None:
            for i, reaction in enumerate(self.stoichiometryMatrix):

                t_reaction = zeros(1,len(self.listOfSpecies))


                for j, t_formula in enumerate(reaction):
                    t_reaction[j] = t_formula.getDeveloppedInternalMathFormula()


                if matrix is None:
                    matrix = t_reaction
                else:
                    matrix = matrix.col_join(t_reaction)

            return matrix