#!/usr/bin/env python
""" MathEventTrigger.py


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
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.ModelException import ModelException

from libsbml import parseL3Formula

class MathEventTrigger(MathFormula):

    def __init__(self, model):

        self.__model = model
        MathFormula.__init__(self, model, MathFormula.MATH_EQUATION)


    def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}):
        t_convs = {}
        for var, conversion in conversions.items():
            t_convs.update({var:var/conversion})

        MathFormula.setInternalMathFormula(self, obj.getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs))

    def setPrettyPrintMathFormula(self, trigger):

        t_trigger = MathFormula(self.__model)
        t_trigger.readSbml(parseL3Formula(trigger), self.__model.sbmlLevel, self.__model.sbmlVersion)

        t_subs_mask = {}
        for t_var in self.__model.listOfSpecies.values():
            if t_var.isConcentration():
                t_subs_mask.update({t_var.symbol.getInternalMathFormula():SympySymbol("_speciesForcedConcentration_%s_" % str(t_var.symbol.getInternalMathFormula()))})

        self.setInternalMathFormula(t_trigger.getInternalMathFormula().subs(t_subs_mask))


    def getRootsFunctions(self):
        return self.generateRootsFunctions(self.getDeveloppedInternalMathFormula())


    def generateRootsFunctions(self, tree):

        if tree.func in [SympyAnd, SympyOr, SympyXor]:
            return (self.generateRootsFunctions(tree.args[0])
                    + self.generateRootsFunctions(tree.args[1]))

        else:
            if tree.func in [SympyLessThan, SympyStrictLessThan]:
                return ["(%s - %s)" % (self.writeCCode(tree.args[1]),
                                        self.writeCCode(tree.args[0]))]
            else:
                return ["(%s - %s)" % (self.writeCCode(tree.args[0]),
                                        self.writeCCode(tree.args[1]))]


    def getDeactivationCondition(self, shift=0):

            i_event = shift
            (res, i_event) = self.generateDeactivationCondition(self.getDeveloppedInternalMathFormula(), i_event)
            return res, i_event


    def generateDeactivationCondition(self, tree, i_event):

        res_i_event = i_event

        if tree.func == SympyAnd:
            (t_cond_0, res_i_event) = self.generateDeactivationCondition(tree.args[0], res_i_event)
            (t_cond_1, res_i_event) = self.generateDeactivationCondition(tree.args[1], res_i_event)
            return ("(%s || %s)" % (t_cond_0, t_cond_1) , res_i_event)

        elif tree.func == SympyOr:
            (t_cond_0, res_i_event) = self.generateDeactivationCondition(tree.args[0], res_i_event)
            (t_cond_1, res_i_event) = self.generateDeactivationCondition(tree.args[1], res_i_event)
            return ("(%s && %s)" % (t_cond_0, t_cond_1) , res_i_event)

        elif tree.func == SympyXor:
            (t_cond_0, res_i_event) = self.generateDeactivationCondition(tree.args[0], res_i_event)
            (t_cond_1, res_i_event) = self.generateDeactivationCondition(tree.args[1], res_i_event)
            return ("(%s && %s) || (!%s && !%s))" % (t_cond_0, t_cond_1, t_cond_0, t_cond_1) , res_i_event)

        else:
            return ("(data->roots_triggers[%d] == -1)" % res_i_event, res_i_event+1)


    def getActivationCondition(self, shift=0):

            i_event = shift
            (res, i_event) = self.generateActivationCondition(self.getDeveloppedInternalMathFormula(), i_event)
            return res, i_event


    def generateActivationCondition(self, tree, i_event):

        res_i_event = i_event

        if tree.func == SympyAnd:
            (t_cond_0, res_i_event) = self.generateActivationCondition(tree.args[0], res_i_event)
            (t_cond_1, res_i_event) = self.generateActivationCondition(tree.args[1], res_i_event)
            return ("(%s && %s)" % (t_cond_0, t_cond_1) , res_i_event)

        elif tree.func == SympyOr:
            (t_cond_0, res_i_event) = self.generateActivationCondition(tree.args[0], res_i_event)
            (t_cond_1, res_i_event) = self.generateActivationCondition(tree.args[1], res_i_event)
            return ("(%s || %s)" % (t_cond_0, t_cond_1) , res_i_event)

        elif tree.func == SympyXor:
            (t_cond_0, res_i_event) = self.generateActivationCondition(tree.args[0], res_i_event)
            (t_cond_1, res_i_event) = self.generateActivationCondition(tree.args[1], res_i_event)
            return ("(%s || %s) && (!(%s && %s))" % (t_cond_0, t_cond_1, t_cond_0, t_cond_1) , res_i_event)

        else:
            return ("(data->roots_triggers[%d] == 1)" % res_i_event, res_i_event+1)


    def nbRoots(self):
        return self.countRoots(self.getDeveloppedInternalMathFormula(), 0)


    def countRoots(self, tree, counter):

        res_counter = counter

        if tree.func in [SympyAnd, SympyOr, SympyXor]:
            res_counter = self.countRoots(tree.args[0], res_counter)
            res_counter = self.countRoots(tree.args[1], res_counter)
            return res_counter

        else:
            return res_counter + 1


    def getRootsOperator(self):
        return self.generateRootsOperator(self.getDeveloppedInternalMathFormula(), [])


    def generateRootsOperator(self, tree, t_list):

        if tree.func in [SympyAnd, SympyOr, SympyXor]:
            t_list += self.generateRootsOperator(tree.args[0], t_list)
            t_list += self.generateRootsOperator(tree.args[1], t_list)
            return t_list

        else:
            if tree.func in [SympyStrictGreaterThan, SympyStrictLessThan]:
                return [1]
            elif tree.func in [SympyGreaterThan, SympyLessThan]:
                return [0]
            elif tree.func == SympyEqual:
                return [2]
            elif tree.func == SympyUnequal:
                return [3]
            else:
                raise ModelException(ModelException.MATH_ERROR, "Unknown logical operator")

    def getOperator(self):
        return self.getInternalMathFormula().func