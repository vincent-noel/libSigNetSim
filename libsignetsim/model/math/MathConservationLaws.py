#!/usr/bin/env python
""" MathConservationLaws.py


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
from libsignetsim.settings.Settings import Settings
from sympy import simplify, diff, solve, srepr, linsolve
from time import time
# from sympy.solvers.solveset import nonlinsolve
class MathConservationLaws(object):
    """ Sbml model class """

    def __init__ (self):
        """ Constructor of model class """

        self.LHSs = []
        self.RHSs = []
        self.RHS_concentrations = []
        self.vars = []

        self.LHSs_v2 = []
        self.RHSs_v2 = []
        self.RHS_concentrations_v2 = []

        self.reducibleVariables = []
        self.reducibleVariablesConcentrations = []


    def hasConservationLaws(self):
        return len(self.LHSs) > 0

    def buildConservationLaws(self):

        self.LHSs = []
        self.RHSs = []
        self.vars = []
        # self.LHS_signs = []
        self.LHS_vars = []

        t_stoichiometry = self.getSimpleStoichiometryMatrix()

        # print t_stoichiometry
        if t_stoichiometry is not None and len(t_stoichiometry) > 0:

            for i, t_res in enumerate(t_stoichiometry.nullspace()):
                t_law = MathFormula.ZERO
                t_value = MathFormula.ZERO

                unknowns = []
                # t_signs = []
                t_vars = []
                for ii, tt_res in enumerate(t_res):

                    t_species = self.listOfSpecies.values()[ii]
                    # print "\nSpecies %s" % t_species.getSbmlId()

                    # Getting symbol
                    tt_symbol = t_species.symbol.getInternalMathFormula()
                    # if t_species.isConcentration():
                    #     tt_symbol /= t_species.getCompartment().symbol.getInternalMathFormula()


                    # Getting value
                    if t_species.hasInitialAssignment():
                        tt_value = t_species.hasInitialAssignmentBy().getExpressionMath().getDeveloppedInternalMathFormula()

                        for tt_species in self.listOfSpecies.values():
                            ttt_symbol = tt_species.symbol.getInternalMathFormula()
                            ttt_value = tt_species.value.getInternalMathFormula()
                            if ttt_symbol in tt_value.atoms(SympySymbol) and ttt_value is not None:
                                tt_value = tt_value.subs(ttt_symbol, ttt_value)

                        if t_species.isConcentration():
                            tt_value /= t_species.getCompartment().symbol.getInternalMathFormula()

                        if SympySymbol("_time_") in tt_value.atoms():
                            tt_value = tt_value.subs(SympySymbol("_time_"), 0)

                    elif t_species.value.getInternalMathFormula() is not None:
                        tt_value =  t_species.getMathValue().getInternalMathFormula()
                        if t_species.isConcentration():
                            tt_value /= t_species.getCompartment().symbol.getInternalMathFormula()

                    else:
                        t_unknown = SympySymbol("_%s_0_" % str(tt_symbol))
                        tt_value = t_unknown

                        tt_unknown = MathFormula(self, MathFormula.MATH_VARIABLE)
                        tt_unknown.setInternalMathFormula(t_unknown)
                        unknowns.append(tt_unknown)

                    if t_species.isConcentration():
                        tt_value *= t_species.getCompartment().symbol.getInternalMathFormula()

                    # print "  > symbol = %s" % str(tt_symbol)
                    # print "  > value = %s" % str(tt_value)
                    # Building law
                    if tt_res == SympyInteger(1):
                        t_law += tt_symbol
                        t_value += tt_value
                        # t_signs.append(1)

                    elif tt_res == SympyInteger(-1):
                        t_law -= tt_symbol
                        t_value -= tt_value
                        # t_signs.append(-1)

                    else:
                        t_law += tt_res * tt_symbol
                        t_value += tt_res * tt_value
                        # t_signs.append(0)


                    t_vars.append(tt_symbol)

                if t_law.func == SympyAdd:
                    for t_atom in t_law.atoms(SympySymbol):
                        if self.listOfVariables[str(t_atom)].isDerivative():
                            t_var = MathFormula(self, MathFormula.MATH_VARIABLE)
                            t_var.setInternalMathFormula(t_atom)
                            self.vars.append(t_var)


                    t_lhs = MathFormula(self)
                    t_lhs.setInternalMathFormula(t_law)
                    self.LHSs.append(t_lhs)

                    t_rhs = MathFormula(self)
                    t_rhs.setInternalMathFormula(t_value)
                    self.RHSs.append(t_rhs)

                    #
                    # print "New conservation law : "
                    # print "%s = %s" % (str(t_law), str(t_value))

                    self.LHS_vars.append(t_vars)



    def findConservationLaws(self):

        t0 = time()
        self.buildConservationLaws()
        t1 = time()

        if Settings.verbose:
            print "  > Raw conservation laws built (%.2gs)" % (t1-t0)

        # t_laws = [law.getInternalMathFormula() for law in self.LHSs]
        # t_vals = [val.getInternalMathFormula() for val in self.RHSs]

        t_laws, t_vals = self.getRealConservationLaws()

        self.LHSs_v2 = []
        for t_law in t_laws:
            t_formula = MathFormula(self)
            t_formula.setInternalMathFormula(t_law)
            # print "LHS : %s" % str(t_law)
            self.LHSs_v2.append(t_formula)

        self.RHSs_v2 = []
        for i_val, t_val in enumerate(t_vals):
            t_formula = MathFormula(self)
            t_formula.setInternalMathFormula(t_val)
            # print "RHS : %s" % str(t_val)
            self.RHSs_v2.append(t_formula)

            # print "  >> Real conservation law : "
            # print "%s = %s" % (str(self.LHSs_v2[i_val].getInternalMathFormula()), str(t_val))


        t2 = time()
        if Settings.verbose:
            print "  > Real conservation laws built (%.2gs)" % (t2-t1)



    def printConservationLaws(self, forcedConcentration=False):

        print "-----------------------------"
        for i, equ in enumerate(self.RHSs_v2):
            print ">> %s" % str(SympyEqual(
                            self.LHSs_v2[i].getDeveloppedInternalMathFormula(),
                            equ.getDeveloppedInternalMathFormula()))


    def getConservationLaws(self, forcedConcentration=False):

        res = []
        for i, equ in enumerate(self.LHSs_v2):

            if len(self.listOfCompartments.keys()) == 1:
                t_comp = self.listOfCompartments.values()[0]
                t_equ = equ.getDeveloppedInternalMathFormula().subs({t_comp.symbol.getInternalMathFormula():t_comp.value.getInternalMathFormula()})
                # t_cfe = self.CFEs[i].getDeveloppedInternalMathFormula().subs({t_comp.symbol.getInternalMathFormula():t_comp.value.getInternalMathFormula()})
            else:
                t_equ = equ.getDeveloppedInternalMathFormula().subs(self.listOfVariables.getAmountsToConcentrations())
            t_formula = MathFormula(self)
            t_formula.setInternalMathFormula(simplify(SympyEqual(t_equ, self.RHSs_v2[i].getDeveloppedInternalMathFormula())))

            res.append(t_formula.getFinalMathFormula(forcedConcentration))

        return res


    def getRealConservationLaws(self, forcedConcentration=False):

        f_laws = []
        f_values = []
        tofix_laws = []
        tofix_values = []

        for i, law in enumerate(self.LHSs):
            t_law = law.getInternalMathFormula()
            if not self.isSumOfPositiveTerms(t_law):
                tofix_laws.append(t_law)
                tofix_values.append(self.RHSs[i].getInternalMathFormula())
            else:
                f_laws.append(t_law)
                f_values.append(self.RHSs[i].getInternalMathFormula())


        for i_law, law in enumerate(tofix_laws):

            t_neg_terms = self.getNegativeTerms(law)
            t_vars = []
            for neg_term in t_neg_terms:
                t_vars.append(neg_term.args[1])

            t_laws = [SympyEqual(tt_law, tofix_values[ii_law]) for ii_law, tt_law in enumerate(tofix_laws) if tt_law != law]
            t_laws += [SympyEqual(tt_law, f_values[ii_law]) for ii_law, tt_law in enumerate(f_laws)]

            sol = solve(t_laws, t_vars)

            tofix_laws[i_law] = law.subs(sol)


        # print tofix_laws

        return (f_laws+tofix_laws, f_values+tofix_values)


    def isSumOfPositiveTerms(self, formula):

        if formula.func == SympyAdd:
            for arg in formula.args:
                if arg.func == SympyMul:
                    for mul_arg in arg.args:
                        if self.isNegativeTerm(mul_arg):
                            return False

        return True


    def getNegativeTerms(self, formula):
        res = []
        if formula.func == SympyAdd:
            for arg in formula.args:
                if arg.func == SympyMul:
                    # print srepr(arg)
                    for mul_arg in arg.args:
                        if self.isNegativeTerm(mul_arg):
                            res.append(arg)

        return res



    def isNegativeTerm(self, formula):

        return (formula == SympyInteger(-1)
                or (formula.func == SympyInteger and int(formula) < 0)
                or (formula.func == SympyFloat and float(formula) < 0)
        )


    def findReducibleVariables(self, vars_to_keep=[]):

        odes_vars_in_laws = []
        for law in self.LHSs_v2:
            t_vars = []
            for var in law.getDeveloppedInternalMathFormula().atoms(SympySymbol):
                t_variable = self.listOfVariables[str(var)]
                if t_variable.isDerivative() and not t_variable.isCompartment():
                    t_vars.append(var)
            odes_vars_in_laws.append(t_vars)


        system = []
        for i, law in enumerate(self.LHSs_v2):
            t_law = law.getDeveloppedInternalMathFormula()
            t_value = self.RHSs_v2[i].getDeveloppedInternalMathFormula()
            system.append(SympyEqual(t_law, t_value))


        vars_to_extract = []
        for i, ode_var in enumerate(odes_vars_in_laws):

            j=0
            while j < len(ode_var) and (
                (len(vars_to_extract) > 0 and ode_var[j] in vars_to_extract)
                or (len(vars_to_keep) > 0 and str(ode_var[j]) in vars_to_keep)):
                j += 1

            if j < len(ode_var):
                vars_to_extract.append(ode_var[j])

        # print [equ for equ in system]
        # print vars_to_extract[1]

        # print solve(system, vars_to_extract[1])
        solutions = solve(system, vars_to_extract)
        # print solutions
        if len(solutions) > 0:
            self.reducibleVariables = solutions
        else:
            self.reducibleVariables = {}