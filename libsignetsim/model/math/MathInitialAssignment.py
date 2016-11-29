#!/usr/bin/env python
""" MathInitialAssignment.py


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
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.settings.Settings import Settings
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

class MathInitialAssignment(object):

    def __init__(self, model):

        self.__model = model
        self.variable = MathSymbol(model)
        self.definition = MathFormula(model, MathFormula.MATH_ASSIGNMENTRULE)

    def readSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

        self.variable.readSbml(sbml_rule.getSymbol(), sbml_level, sbml_version)
        self.definition.readSbml(sbml_rule.getMath(), sbml_level, sbml_version)

        if self.getVariable().isConcentration():
            self.definition.setInternalMathFormula(
                SympyMul(self.definition.getInternalMathFormula(),
                        self.getVariable().getCompartment().symbol.getInternalMathFormula()))


    def writeSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

        t_definition = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
        t_definition.setInternalMathFormula(self.definition.getInternalMathFormula())
        t_variable = self.variable.getSbmlMathFormula(sbml_level, sbml_version).getName()

        if self.getVariable().isConcentration():
            t_definition.setInternalMathFormula(
                SympyMul(self.definition.getInternalMathFormula(),
                        SympyPow(self.getVariable().getCompartment().symbol.getInternalMathFormula(),
                                    SympyInteger(-1))))


        sbml_rule.setSymbol(t_variable)
        sbml_rule.setMath(t_definition.getSbmlMathFormula(sbml_level, sbml_version))


    def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):

        t_convs = {}
        for var, conversion in conversions.items():
            t_convs.update({var:var/conversion})

        t_definition = obj.definition.getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs)

        t_var_symbol = obj.variable.getInternalMathFormula().subs(subs).subs(replacements)
        if t_var_symbol in conversions:
            t_definition *= conversions[t_var_symbol]

        self.variable.setInternalVariable(t_var_symbol)
        self.definition.setInternalMathFormula(t_definition)

        # if prefix != "":
        #     self.variable.subs(obj.getModel().listOfVariables.subsToFlatten())
        #     self.definition.subs(obj.getModel().listOfVariables.subsToFlatten())

        # self.variable.subs(subs)
        # self.definition.subs(subs)
        # print self.variable.getInternalMathFormula()
        # print self.definition.getInternalMathFormula()

    def setPrettyPrintDefinition(self, definition):

        variable = self.__model.listOfVariables[str(self.variable.getInternalMathFormula())]

        if variable.isSpecies() and not variable.hasOnlySubstanceUnits:
            t_comp = variable.getCompartment()
            t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
            t_math_formula.setPrettyPrintMathFormula(definition)
            self.definition.setInternalMathFormula(t_math_formula.getInternalMathFormula()*t_comp.symbol.getInternalMathFormula())

        else:
            self.definition.setPrettyPrintMathFormula(definition)


    def setPrettyPrintVariable(self, variable):

        self.variable.setPrettyPrintMathFormula(variable)


    def getPrettyPrintDefinition(self):

        variable = self.__model.listOfVariables[str(self.variable.getInternalMathFormula())]

        if variable.isSpecies() and not variable.hasOnlySubstanceUnits:
            t_comp = variable.getCompartment()
            t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
            t_math_formula.setInternalMathFormula(self.definition.getInternalMathFormula()/t_comp.symbol.getInternalMathFormula())
            return t_math_formula.getPrettyPrintMathFormula()

        else:
            return self.definition.getPrettyPrintMathFormula()


    def setVariable(self, variable):

        self.variable.setInternalMathFormula(variable.symbol.getInternalMathFormula())


    def renameSbmlId(self, old_sbml_id, new_sbml_id):
        old_symbol = SympySymbol(old_sbml_id)

        if self.variable.getInternalMathFormula() == old_symbol:
            self.variable.setInternalMathFormula(SympySymbol(new_sbml_id))

        if old_symbol in self.definition.getInternalMathFormula().atoms():
            self.definition.setInternalMathFormula(self.definition.getInternalMathFormula.subs(old_symbol, SympySymbol(new_sbml_id)))


    def containsVariable(self, variable):
        return (variable.symbol.getInternalMathFormula() in self.definition.getInternalMathFormula().atoms()
                or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.definition.getInternalMathFormula().atoms())
                or variable.symbol.getInternalMathFormula() == self.variable.getInternalMathFormula())