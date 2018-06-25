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
from PyDSTool.Toolbox import phaseplane as pp

from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from pprint import pformat


class PyDSToolModel(object):

	def __init__ (self, model):

		self.model = model

		self.systemParameters = None
		self.system = None

	def getSystem(self):
		return self.system

	def build(self, parameter, from_value, vars_to_keep=[]):

		parameter.setValue(from_value)
		self.model.build(vars_to_keep=vars_to_keep, reduce=True)
		self.buildDS()

	def buildDS(self):

		comp_subs = {}
		for comp in list(self.model.listOfCompartments):
			comp_subs.update({comp.symbol.getInternalMathFormula():comp.value.getInternalMathFormula()})

		parameters = {}
		variables = {}
		odes = {}

		subs_cfes = {}
		for cfe in self.model.getMathModel().listOfCFEs:
			t_definition = cfe.getDefinition().getDeveloppedInternalMathFormula()
			subs_cfes.update({cfe.getVariable().symbol.getInternalMathFormula(): t_definition})

		for variable in list(self.model.getMathModel().listOfVariables):

			if variable.isConstant():
				t_symbol = variable.symbol.getInternalMathFormula()
				t_value = self.model.listOfInitialConditions[t_symbol].getInternalMathFormula()
				parameters.update({str(t_symbol): str(t_value)})

			elif variable.isDerivative():
				t_symbol = variable.symbol.getInternalMathFormula()
				t_value = self.model.listOfInitialConditions[t_symbol].getInternalMathFormula()
				variables.update({str(t_symbol): str(t_value)})

		for ode in self.model.getMathModel().listOfODEs:
			t_ode = ode.getDefinition().getDeveloppedInternalMathFormula().subs(subs_cfes).subs(comp_subs)
			odes.update({str(ode.getVariable().symbol.getInternalMathFormula()): str(t_ode)})

		self.systemParameters = args(name=self.model.getSbmlId())
		self.systemParameters.pars = parameters
		self.systemParameters.varspecs = odes
		self.systemParameters.ics = variables
		self.system = Generator.Vode_ODEsystem(self.systemParameters)

	def __str__(self):

		res = "\n" + pformat(self.systemParameters.pars)
		res += "\n" + pformat(self.systemParameters.ics)
		res += "\n" + pformat(self.systemParameters.varspecs)
		res += "\n"

		return res