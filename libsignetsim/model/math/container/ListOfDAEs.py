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
from __future__ import print_function

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.DAE import DAE
from libsignetsim.model.math.CFE import CFE
from libsignetsim.model.math.sympy_shortcuts import SympyEqual, SympyInteger, SympySymbol, SympyFloat
from libsignetsim.model.math.MathException import MathException
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

from sympy import solve, srepr
from time import time

class ListOfDAEs(list):
	""" Sbml model class """

	def __init__(self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)

	def build(self):

		for rule in self.__model.listOfRules:
			if rule.isAlgebraic() and rule.isValid():
				# self.__model.hasDAEs = True
				t_dae = DAE(self.__model)
				t_dae.new(rule.getDefinition(rawFormula=True))
				list.append(self, t_dae)

	def solveInitialConditions(self, tmin=0):

		DEBUG = False
		system = []

		subs = {SympySymbol('time'): SympyFloat(tmin)}
		for var, val in list(self.__model.listOfInitialConditions.items()):
			if not self.__model.listOfVariables.getBySymbol(var).isAlgebraic():
				subs.update({var: val.getInternalMathFormula()})

		for dae in self:
			system.append(
				SympyEqual(
					unevaluatedSubs(dae.getDefinition().getDeveloppedInternalMathFormula(), subs),
					SympyInteger(0)
				)
			)

		system_vars = []
		for var in self.__model.listOfVariables:
			if var.isAlgebraic():
				system_vars.append(var.symbol.getInternalMathFormula())

		if DEBUG:
			print(system)
			print(system_vars)

		all_true = True
		for equ in system:
			if equ != True:
				all_true = False

		if len(system_vars) > 0 and not all_true:

			init_cond = {}
			res = solve(system, system_vars, manual=True)

			if DEBUG:
				print(res)

			if res is not True and len(res) > 0:
				if isinstance(res, dict):
					for var, value in list(res.items()):
						init_cond.update({var: value})

				elif isinstance(res[0], dict):
					for var, value in list(res[0].items()):
						init_cond.update({var: value})

				elif isinstance(res[0], tuple):
					for i_var, value in enumerate(res[0]):
						init_cond.update({system_vars[i_var]: value})

			if DEBUG:
				print(init_cond)

			t0 = time()

			if tmin == 0:
				init_cond.update({SympySymbol("_time_"): SympyInteger(tmin)})
			else:
				init_cond.update({SympySymbol("_time_"): SympyFloat(tmin)})

			for init_ass in self.__model.listOfInitialAssignments:
				if init_ass.isValid():
					t_var = init_ass.getVariable().symbol.getSymbol()
					t_value = init_ass.getDefinition().getDeveloppedInternalMathFormula()
					init_cond.update({t_var:t_value})

			if DEBUG:
				print(init_cond)

			for rule in self.__model.listOfRules:
				if rule.isAssignment() and rule.isValid():
					t_var = rule.getVariable().symbol.getSymbol()

					if t_var not in list(init_cond.keys()):
						t_value = rule.getDefinition().getDeveloppedInternalMathFormula()
						init_cond.update({t_var: t_value})

			if DEBUG:
				print(init_cond)

			for var in self.__model.listOfVariables:
				t_var = var.symbol.getSymbol()

				if t_var not in list(init_cond.keys()):
					t_value = var.value.getDeveloppedInternalMathFormula()
					if t_value is not None:
						init_cond.update({t_var: t_value})
					else:
						print("WTF %s" % var.getSbmlId())
			if DEBUG:
				print(init_cond)


			crossDependencies = True
			passes = 1
			while crossDependencies:
				if DEBUG:
					print("PASS : %d" % passes)
				crossDependencies = False
				for t_var in list(init_cond.keys()):
					t_def = init_cond[t_var]
					if len(t_def.atoms(SympySymbol).intersection(set(init_cond.keys()))) > 0:
						crossDependencies = True
						if DEBUG:
							print("\n> " + str(t_var) + " : " + str(t_def))

						for match in t_def.atoms(SympySymbol).intersection(set(init_cond.keys())):
							if match == t_var:
								raise MathException("Initial values : self dependency is bad")
							if DEBUG:
								print(">> " + str(match) + " : " + str(init_cond[match]))

							t_def = unevaluatedSubs(t_def, {match: init_cond[match]})
							init_cond.update({t_var: t_def})

						if DEBUG:
							if len(t_def.atoms(SympySymbol).intersection(set(init_cond.keys()))) == 0:
								print("> " + str(t_var) + " : " + str(t_def) + " [OK]")
							else:
								print("> " + str(t_var) + " : " + str(t_def) + " [ERR]")
				passes += 1
				if passes >= 100:
					raise MathException("Initial values : Probable circular dependencies")

				if DEBUG:
					print("")

			if DEBUG:
				print(list(init_cond.keys()))
				print(self.__model.listOfVariables.symbols())

			self.__model.listOfInitialConditions = {}
			for var, value in list(init_cond.items()):
				t_var = self.__model.listOfVariables.getBySymbol(var)
				if t_var is not None:
					t_value = MathFormula(self.__model)
					t_value.setInternalMathFormula(value)
					self.__model.listOfInitialConditions.update({t_var.symbol.getSymbol(): t_value})

			for var in self.__model.listOfVariables:
				if not var.symbol.getSymbol() in list(self.__model.listOfInitialConditions.keys()):
					print("Lacks an initial condition : %s" % var.getSbmlId())

	def solveDAEs(self):

		for i, dae in enumerate(self):
			if dae.isValid():
				var, res = dae.solve()

				if len(res) > 0:
					t_var = self.__model.listOfVariables.getBySymbol(var)
					t_formula = MathFormula(self.__model)

					if isinstance(res[0], dict):
						t_formula.setInternalMathFormula(list(res[0].values())[0])
					else:
						t_formula.setInternalMathFormula(res[0])

					cfe = CFE(self.__model)
					cfe.new(t_var, t_formula)
					self.__model.listOfCFEs.append(cfe)
					self.__model.listOfVariables.changeVariableType(t_var, MathVariable.VAR_ASS)
					list.__delitem__(self, i)

		self.__model.listOfCFEs.developCFEs()

	def __str__(self):

		res = ""
		for dae in self:
			res += str(dae) + "\n"

		return res


	def pprint(self):

		for dae in self:
			dae.pprint()
			print("\n")