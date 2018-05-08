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

from libsignetsim.model.math.MathException import MathException
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyEqual, SympyInteger, SympyFloat
from libsignetsim.settings.Settings import Settings

from sympy import pretty
from time import time


class ListOfInitialConditions(dict):
	""" Sbml model class """

	def __init__(self, model):
		""" Constructor of model class """

		dict.__init__(self)
		self.__model = model

	def clear(self):
		dict.clear(self)

	def __str__(self):
		res = ""
		for var, value in dict.items(self):
			res += "%s : %s\n" % (var.symbol.getInternalMathFormula(), value.getDeveloppedInternalMathFormula())
		return res

	def pprint(self):

		for var, value in dict.items(self):
			var0 = SympySymbol("(" + str(var) + ")_0")
			print(pretty(SympyEqual(var0, value.getDeveloppedInternalMathFormula())))
			print("\n")


	def solve(self, tmin):
		""" Initial conditions are a mess between values, initial assignments,
			and assignment rules. We actually need to solve them to make sure
			all dependencies are respected

			Unfortunately, this can be quite costly for large system
			So we'll try to just solve the minimum for C simulations

			"""

		DEBUG = False

		t0 = time()

		if tmin == 0:
			init_cond = {SympySymbol("_time_"): SympyInteger(tmin)}
		else:
			init_cond = {SympySymbol("_time_"): SympyFloat(tmin)}

		for init_ass in self.__model.listOfInitialAssignments:
			if init_ass.isValid():
				t_var = init_ass.getVariable().symbol.getSymbol()
				t_value = init_ass.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula()
				init_cond.update({t_var: t_value})

		if DEBUG:
			print(init_cond)

		for rule in self.__model.listOfRules:
			if rule.isAssignment() and rule.isValid():
				t_var = rule.getVariable().symbol.getSymbol()
				if t_var not in list(init_cond.keys()):
					t_value = rule.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula()
					init_cond.update({t_var: t_value})

		if DEBUG:
			print(init_cond)

		for var in self.__model.listOfVariables:
			t_var = var.symbol.getSymbol()
			if t_var not in list(init_cond.keys()):
				t_value = var.value.getDeveloppedInternalMathFormula()
				if t_value is not None:
					init_cond.update({t_var: t_value})
				elif not var.isAlgebraic():
					init_cond.update({t_var: SympyFloat(0.0)})

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

		# self.listOfInitialConditions = {}
		dict.clear(self)
		for var, value in list(init_cond.items()):
			if var != SympySymbol("_time_"):
				t_var = self.__model.listOfVariables.getBySymbol(var)
				if t_var is not None:
					t_value = MathFormula(self.__model)
					t_value.setInternalMathFormula(value.doit())
					dict.update(self, {t_var.symbol.getSymbol(): t_value})

		if DEBUG:
			print("> Final listOfInitialConditions")
			print(dict.keys(self))

		for var in self.__model.listOfVariables:
			if not var.symbol.getSymbol() in dict.keys(self) and not var.isAlgebraic():
				print("Lacks an initial condition : %s" % var.getSbmlId())

		if Settings.verbose >= 1:
			print("> Finished calculating initial conditions (%.2gs)" % (time()-t0))
