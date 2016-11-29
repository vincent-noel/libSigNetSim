#!/usr/bin/env python
""" PyDSToolModel.py


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

from PyDSTool import args, Generator
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from sympy import simplify
class PyDSToolModel(object):

    def __init__ (self, model):

        self.model = model

        self.systemParameters = None
        self.system = None

    def getSystem(self):
        return self.system

    def build(self, vars_to_keep=[]):

        self.model.build(vars_to_keep=vars_to_keep)
        self.buildDS()


    def makeSubs(self, formula):

        t_atoms = formula.atoms(SympySymbol)
        t_subs = {}
        for atom in t_atoms:
            t_var = self.model.listOfVariables.getBySbmlId(str(atom))
            t_value = t_var.value.getInternalMathFormula()
            if len(t_value.atoms(SympySymbol)) > 0:
                t_value = self.makeSubs(t_value)
            t_subs.update({atom:t_value})

        return formula.subs(t_subs)


    def buildDS(self):

        parameters = {}
        variables = {}
        odes = {}
        subs = {}

        # Getting the list of local parameters
        local_params_subs = {}
        for reaction in self.model.listOfReactions.values():
            if len(reaction.listOfLocalParameters) > 0:
                for l_param in reaction.listOfLocalParameters.values():
                    t_name = str(l_param.symbol.getInternalMathFormula())
                    local_params_subs.update({t_name: t_name[1:]})

        if len(self.model.listOfCompartments) == 1:
            t_comp = self.model.listOfCompartments.values()[0]
            subs.update({t_comp.symbol.getInternalMathFormula():t_comp.value.getInternalMathFormula()})

        for variable in self.model.listOfVariables.values():
            if variable.isConstant():
                t_symbol = str(variable.symbol.getInternalMathFormula().subs(local_params_subs))

                t_raw_value = variable.value.getInternalMathFormula()
                if len(t_raw_value.atoms(SympySymbol)) > 0:
                    t_raw_value = self.makeSubs(t_raw_value)
                t_value = float(t_raw_value)

                parameters.update({t_symbol:t_value})

            if variable.isDerivative():
                t_symbol = variable.symbol.getInternalMathFormula()

                t_raw_value = variable.value.getInternalMathFormula()
                if len(t_raw_value.atoms(SympySymbol)) > 0:
                    t_raw_value = self.makeSubs(t_raw_value)
                t_value = float(t_raw_value)

                variables.update({str(t_symbol):t_value})

                t_vars = [var.getInternalMathFormula() for var in self.model.ODE_vars]
                t_index = t_vars.index(variable.symbol.getInternalMathFormula())
                t_ode = self.model.ODEs[t_index].getInternalMathFormula().subs(subs).subs(local_params_subs)
                odes.update({str(t_symbol):str(simplify(t_ode))})


        print odes
        print parameters


        self.systemParameters = args(name=self.model.getSbmlId())
        self.systemParameters.pars = parameters
        self.systemParameters.varspecs = odes
        self.systemParameters.ics = variables
        self.system = Generator.Vode_ODEsystem(self.systemParameters)
