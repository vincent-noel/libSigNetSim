#!/usr/bin/env python
""" MathAlgebraicRule.py


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


class MathAlgebraicRule(object):

    def __init__(self, model):

        self.__model = model
        self.definition = MathFormula(model, MathFormula.MATH_ALGEBRAICRULE)


    def readSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

        self.definition.readSbml(sbml_rule.getMath(), sbml_level, sbml_version)


    def writeSbml(self, sbml_rule, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

        sbml_rule.setMath(self.definition.getSbmlMathFormula(sbml_level, sbml_version))



    def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversions={}, time_conversion=None):
        self.definition.setInternalMathFormula(obj.definition.getInternalMathFormula().subs(subs).subs(replacements))


    def setPrettyPrintDefinition(self, definition):

        self.definition.setPrettyPrintMathFormula(definition)
        self.definition.setInternalMathFormula(SympyEqual(self.definition.getInternalMathFormula(), MathFormula.ZERO))

    def getPrettyPrintDefinition(self):

        return self.definition.getPrettyPrintMathFormula()


    def getExpressionMath(self, forcedConcentration=False):

        if forcedConcentration:
            t_formula = MathFormula(self.__model)
            t_formula.setInternalMathFormula(self.definition.getInternalMathFormula())

            for species in self.__model.listOfSpecies.values():
                if species.isConcentration():
                    t_internal = MathFormula.getInternalMathFormula(t_formula)
                    t_fc = SympySymbol("_speciesForcedConcentration_%s_" % str(species.symbol.getInternalMathFormula()))
                    t_species = SympySymbol(species.getSbmlId())
                    t_internal = t_internal.subs({ t_fc : t_species })
                    t_formula.setInternalMathFormula(t_internal)

            return t_formula
        else:
            return self.definition

    def renameSbmlId(self, old_sbml_id, new_sbml_id):
        old_symbol = SympySymbol(old_sbml_id)

        if old_symbol in self.definition.getInternalMathFormula().atoms():
            t_definition = MathFormula(self.__model, MathFormula.MATH_ALGEBRAICRULE)
            t_definition.setInternalMathFormula(self.definition.getInternalMathFormula.subs(old_symbol, SympySymbol(new_sbml_id)))

    def containsVariable(self, variable):
        return (variable.symbol.getInternalMathFormula() in self.definition.getInternalMathFormula().atoms()
                or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.definition.getInternalMathFormula().atoms()))