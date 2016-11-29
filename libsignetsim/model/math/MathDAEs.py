#!/usr/bin/env python
""" MathDAEs.py


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
from libsignetsim.model.math.sympy_shortcuts import  (
    SympySymbol, SympyInteger, SympyFloat, SympyRational, SympyAtom,
    SympyOne, SympyNegOne, SympyZero, SympyPi, SympyE, SympyExp1, SympyHalf,
    SympyInf, SympyNan, SympyAdd, SympyMul, SympyPow,
    SympyFunction, SympyUndefinedFunction, SympyLambda, SympyDerivative,
    SympyCeiling, SympyFloor, SympyAbs, SympyLog, SympyExp, SympyPiecewise,
    SympyFactorial, SympyRoot, SympyAcos, SympyAsin, SympyAtan, SympyAcosh,
    SympyAsinh, SympyAtanh, SympyCos, SympySin, SympyTan, SympyAcot,
    SympyAcoth, SympyCosh, SympySinh, SympyTanh, SympySec, SympyCsc,
    SympyCot, SympyCoth, SympyAcsc, SympyAsec,
    SympyEqual, SympyUnequal, SympyGreaterThan, SympyLessThan,
    SympyStrictGreaterThan, SympyStrictLessThan,
    SympyAnd, SympyOr, SympyXor, SympyNot, SympyTrue, SympyFalse,
    SympyMax, SympyMin)
from sympy import simplify, diff, solve


class MathDAEs(object):
    """ Sbml model class """

    def __init__ (self):
        """ Constructor of model class """

        self.hasDAEs = False
        self.init_conditions_solved = False

        # Differential algebraic equations
        self.DAEs = []
        self.DAE_concentrations = []
        self.DAE_symbols = []
        self.DAE_vars = []



    def getCDAE(self, ind):
        return self.DAEs[ind].getCMathFormula()


    def getDAEs(self, forcedConcentration=False):
        res = []
        for dae in self.DAEs:
            res.append(dae.getFinalMathFormula(forcedConcentration))
        return res

    def getDAE_concentrations(self, forcedConcentration=False):
        res = []
        for dae in self.DAE_concentrations:
            res.append(dae.getFinalMathFormula(forcedConcentration))
        return res

    def buildDAEs(self):

        self.DAEs = []
        self.DAE_concentrations = []
        self.DAE_symbols = []
        self.DAE_vars = []

        for rule in self.listOfRules.values():
            if rule.isAlgebraic():
                # print rule.definition.getDeveloppedInternalMathFormula()
                self.addDAE(rule)


    def addDAE(self, rule):

        dae_definition = rule.getExpressionMath().getDeveloppedInternalMathFormula()
        t_atoms = []
        for t_atom in dae_definition.atoms(SympySymbol):
            if t_atom != MathFormula.t:
                res_atom = MathFormula(self, MathFormula.MATH_VARIABLE)
                res_atom.setInternalMathFormula(t_atom)
                t_atoms.append(res_atom)


        t_vars = []
        for t_atom in dae_definition.atoms(SympySymbol):
            if t_atom != MathFormula.t and self.listOfVariables[str(t_atom)].isDerivative():
                res_atom = MathFormula(self, MathFormula.MATH_VARIABLE)
                res_atom.setInternalMathFormula(t_atom)
                t_vars.append(res_atom)


        t_definition = MathFormula(self)
        t_definition.setInternalMathFormula(dae_definition)
        self.DAEs.append(t_definition)

        dae_conc_definition = rule.getExpressionMath(forcedConcentration=True).getInternalMathFormula()
        t_conc_definition = MathFormula(self)
        t_conc_definition.setInternalMathFormula(dae_conc_definition)
        self.DAE_concentrations.append(t_conc_definition)

        self.DAE_symbols += t_atoms
        self.DAE_vars += t_vars



    def printDAEs(self):

        print "-----------------------------"
        for dae_equ in self.DAEs:
            print ">> %s" % str(SympyEqual(dae_equ.getFinalMathFormula(),
                                            SympyInteger(0)))