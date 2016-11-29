#!/usr/bin/env python
""" MathODEs.py


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


class MathODEs(object):
    """ Sbml model class """

    def __init__ (self):
        """ Constructor of model class """


        # Ordinary differential equations
        self.ODEs = []
        self.ODE_vars = []
        self.ODE_der_vars = []
        self.ODE_symbols = []


    def getCODE(self, ind):
        return self.ODEs[ind].getCMathFormula()

    def getODEs(self, forcedConcentration=False):

        res = []
        for ind, ode in enumerate(self.ODEs):
            res.append(SympyEqual(self.ODE_der_vars[ind].getFinalMathFormula(forcedConcentration), ode.getFinalMathFormula(forcedConcentration)))
        return res

    def getODE(self, ind, forcedConcentration=False):
        return SympyEqual(self.ODE_der_vars[ind].getFinalMathFormula(forcedConcentration), self.ODEs[ind].getFinalMathFormula(forcedConcentration))

    def getODE_concentrations(self, forcedConcentration=False):

        res = []
        for ind, ode in enumerate(self.ODEs):
            if len(self.listOfCompartments.keys()) == 1:
                t_comp = self.listOfCompartments.values()[0]
                t_ode = ode.getDeveloppedInternalMathFormula()
                # t_ode = ode.godeetDeveloppedInternalMathFormula().subs({t_comp.symbol.getInternalMathFormula():t_comp.value.getInternalMathFormula()})

            else:
                t_ode = ode.getDeveloppedInternalMathFormula().subs(self.listOfVariables.getAmountsToConcentrations())
            t_formula = MathFormula(self)
            t_formula.setInternalMathFormula(t_ode)
            res.append(SympyEqual(self.ODE_der_vars[ind].getFinalMathFormula(forcedConcentration), t_formula.getFinalMathFormula(forcedConcentration)))
        return res

    def getODE_concentration(self, ind, forcedConcentration=False):
        t_ode = self.ODEs[ind].getDeveloppedInternalMathFormula().subs(self.listOfVariables.getAmountsToConcentrations())
        t_formula = MathFormula(self)
        t_formula.setInternalMathFormula(t_ode)
        return SympyEqual(self.ODE_der_vars[ind].getFinalMathFormula(forcedConcentration), t_formula.getFinalMathFormula(forcedConcentration))

    def buildODEs(self, including_fast_reactions=True):

        self.ODEs = []
        self.ODE_vars = []
        self.ODE_der_vars = []
        self.ODE_symbols = []
        for variable in self.listOfVariables.values():
            if (((variable.isCompartment() or variable.isParameter() or variable.isStoichiometry()) and variable.isRateRuled())
                or (variable.isSpecies() and not variable.constant and (variable.isRateRuled() or (variable.isInReactions(including_fast_reactions) and not variable.isAssignmentRuled())))):

                self.addODE(variable, including_fast_reactions)


    def addODE(self, variable, including_fast_reactions=True):

        t_variable = MathFormula(self, MathFormula.MATH_VARIABLE)
        t_variable.setInternalMathFormula(variable.symbol.getInternalMathFormula())
        self.ODE_vars.append(t_variable)

        t_variable_ode = MathFormula(self)
        t_variable_ode.setInternalMathFormula(variable.getODE(including_fast_reactions, MathFormula.MATH_DEVINTERNAL))
        self.ODEs.append(t_variable_ode)

        t_variable_derivative = MathFormula(self)
        t_variable_derivative.setInternalMathFormula(variable.symbol.getMathFormulaDerivative(MathFormula.MATH_DEVINTERNAL))
        self.ODE_der_vars.append(t_variable_derivative)

        t_variable_symbols = MathFormula(self)
        t_variable_symbols.setInternalMathFormula(variable.getODE(including_fast_reactions, MathFormula.MATH_DEVINTERNAL, symbols=True))
        self.ODE_symbols.append(t_variable_symbols)


    def printODEs(self):

        print "-----------------------------"
        for i_equ, equ in enumerate(self.ODEs):
            t_equ = equ.getDeveloppedInternalMathFormula()
            print ">> %s = %s" % (str(self.ODE_der_vars[i_equ].getDeveloppedInternalMathFormula()),
                                str(t_equ))
                                # equ.getFinalMathFormula()))



    def developODEs(self):

        # Here we just develop the expression,
        # so that the whole system is here
        # Just to be sure not to get any ordering constraints
        # In two passes, not sure it's the right thing to do, but it works

        for i_ode, t_ode in enumerate(self.ODEs):
            tt_ode = t_ode.getDeveloppedInternalMathFormula()
            # print "> CFE #%d : %s" % (i_cfe, str(tt_cfe))
            for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
                if t_cfe_var.getInternalMathFormula() in tt_ode.atoms(SympySymbol) and i_cfe_var < i_ode:
                    tt_ode = tt_ode.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
            self.ODEs[i_ode].setInternalMathFormula(tt_ode)


        for i_ode, t_ode in enumerate(self.ODEs):

            tt_ode = t_ode.getDeveloppedInternalMathFormula()

            for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
                if t_cfe_var.getInternalMathFormula() in tt_ode.atoms(SympySymbol):
                    tt_ode = tt_ode.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
            self.ODEs[i_ode].setInternalMathFormula(tt_ode)
            # self.ODEs[i_ode].setInternalMathFormula(simplify(tt_ode))