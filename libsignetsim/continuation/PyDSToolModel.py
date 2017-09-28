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

from PyDSTool import args, Generator


class PyDSToolModel(object):

	def __init__ (self, model):

		self.model = model

		self.systemParameters = None
		self.system = None

	def getSystem(self):
		return self.system

	def build(self, parameter, from_value, vars_to_keep=[]):
		self.model.build(vars_to_keep=vars_to_keep)

		self.model.buildReducedModel(vars_to_keep=vars_to_keep)
		self.buildDS(parameter, from_value)

	def buildDS(self, parameter, from_value):

		comp_subs = {}
		for comp in self.model.listOfCompartments.values():
			comp_subs.update({comp.symbol.getInternalMathFormula():comp.value.getInternalMathFormula()})

		parameters = {}
		variables = {}
		odes = {}

		subs_cfes = {}
		for cfe in self.model.getMathModel().listOfCFEs:
			subs_cfes.update({cfe.getVariable().symbol.getInternalMathFormula(): cfe.getDefinition().getInternalMathFormula()})
		for variable in self.model.getMathModel().listOfVariables.values():
			if variable.isConstant():
				t_symbol = variable.symbol.getInternalMathFormula()#.subs(local_params_subs))
				t_value = self.model.solvedInitialConditions[t_symbol].getInternalMathFormula()
				if str(variable.symbol.getInternalMathFormula()) == parameter:
					t_value = from_value
				parameters.update({str(t_symbol): float(t_value)})

			if variable.isDerivative():
				t_symbol = variable.symbol.getInternalMathFormula()
				t_value = self.model.solvedInitialConditions[t_symbol].getInternalMathFormula()
				variables.update({str(t_symbol): float(t_value)})

		for ode in self.model.getMathModel().listOfODEs:
			odes.update({str(ode.getVariable().symbol.getInternalMathFormula()): str(ode.getDefinition().getDeveloppedInternalMathFormula().subs(subs_cfes).subs(comp_subs))})

		print odes
		print variables
		print parameters

		self.systemParameters = args(name=self.model.getSbmlId())
		self.systemParameters.pars = parameters
		self.systemParameters.varspecs = odes
		self.systemParameters.ics = variables
		self.system = Generator.Vode_ODEsystem(self.systemParameters)
