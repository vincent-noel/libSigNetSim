#!/usr/bin/env python
""" ListOfDAEs.py


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
from libsignetsim.model.math.DAE import DAE
from libsignetsim.model.math.sympy_shortcuts import SympyEqual, SympyInteger
from sympy import solve


class ListOfDAEs(list):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)


	def build(self):

		for rule in self.__model.listOfRules.values():
			if rule.isAlgebraic():
				self.__model.hasDAEs = True
				t_dae = DAE(self.__model)
				t_dae.new(rule.getDefinition())
				list.append(self, t_dae)


	def solveInitialConditions(self, tmin=0):

		system = []
		system_vars = []

		t_subs = {}
		for var, val in self.__model.solvedInitialConditions.items():
			t_subs.update({var.symbol.getInternalMathFormula():val.getInternalMathFormula()})

		for dae in self:
			t_formula = MathFormula(self.__model)
			t_formula.setInternalMathFormula(dae.getDefinition().getInternalMathFormula())
			t_formula.setInternalMathFormula(t_formula.getDeveloppedInternalMathFormula().subs(t_subs))

			system.append(
				SympyEqual(
					t_formula.getFinalMathFormula(),
					SympyInteger(0)
				)
			)

		system_vars = []
		for var in self.__model.listOfVariables.values():
			if var.value.getInternalMathFormula() is None and var.isAlgebraic():
				system_vars.append(var.symbol.getInternalMathFormula())


		if len(system_vars) > 0:
			res = solve(system, system_vars)

			if res is not True and len(res) > 0:
				if isinstance(res, dict):
					for var, value in res.items():
						t_var = self.__model.listOfVariables[str(var)]
						t_value = MathFormula(self.__model)
						t_value.setInternalMathFormula(value)
						self.__model.solvedInitialConditions.update({t_var:t_value})

				elif isinstance(res[0], dict):
					for var, value in res[0].items():
						t_var = self.__model.listOfVariables[str(var)]
						t_value = MathFormula(self.__model)
						t_value.setInternalMathFormula(value)
						self.__model.solvedInitialConditions.update({t_var:t_value})
				elif isinstance(res[0], tuple):
					for i_var, value in enumerate(res[0]):
						t_var = self.__model.listOfVariables[str(system_vars[i_var])]
						t_value = MathFormula(self.__model)
						t_value.setInternalMathFormula(value)
						self.__model.solvedInitialConditions.update({t_var:t_value})
