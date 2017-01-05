#!/usr/bin/env python
""" ListOfCFEs.py


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

from libsignetsim.model.math.CFE import CFE
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympyPiecewise, SympyITE, SympyInf, SympyNan, SympyEqual, SympySymbol
from libsignetsim.settings.Settings import Settings
from sympy import solve, sympify
from time import time
class ListOfCFEs(list):
	""" Sbml model class """


	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)
		self.developpedCFEs = []

	def build(self):

		if self.__model.listOfRules.hasAssignmentRule():
			for rule in self.__model.listOfRules.values():
				if rule.isAssignment():
					t_cfe = CFE(self.__model, CFE.ASSIGNMENT)
					t_cfe.new(rule.getVariable(), rule.getDefinition())

					list.append(self, t_cfe)

		for reaction in self.__model.listOfReactions.values():
			t_cfe = CFE(self.__model, CFE.REACTION)
			t_cfe.new(reaction, reaction.value)

			list.append(self, t_cfe)

		self.developCFEs()


	def developCFEs(self):

		t0 = time()
		self.developpedCFEs = []
		continueDevelop = True
		if len(self) > 0:

			system = []
			system_vars = []

			for t_cfe in self:
				if t_cfe.isAssignment():
					t_def = t_cfe.getDefinition().getDeveloppedInternalMathFormula()
					if t_def not in [SympyInf, -SympyInf, SympyNan]:
						t_equ = SympyEqual(
							t_cfe.getVariable().symbol.getInternalMathFormula(),
							t_def
						).evalf()

						if len(t_equ.atoms(SympyITE, SympyPiecewise)) > 0:
							continueDevelop = False

						system.append(t_equ)
						if len(t_def.atoms(SympySymbol)) > 0 and t_def.atoms(SympySymbol) != set([SympySymbol("_time_")]):
							# print t_def.atoms(SympySymbol)
							# print t_def.atoms(SympySymbol) == set([SympySymbol("_time_")])
							system_vars.append(t_cfe.getVariable().symbol.getInternalMathFormula())
						else:
							self.developpedCFEs.append(t_cfe)


				elif t_cfe.isReaction():
					self.developpedCFEs.append(t_cfe)

			# print system
			# print system_vars
			if len(system_vars) > 0 and continueDevelop:
				res = solve(system, system_vars)

				# print res

				if res is not True and len(res) > 0:

					if isinstance(res, dict):
						for var, value in res.items():
							t_var = self.__model.listOfVariables[str(var)]
							t_value = MathFormula(self.__model)
							t_value.setInternalMathFormula(value)
							t_cfe = CFE(self.__model)
							t_cfe.new(t_var, t_value)
							self.developpedCFEs.append(t_cfe)

					elif isinstance(res[0], dict):
						for var, value in res[0].items():
							t_var = self.__model.listOfVariables[str(var)]
							t_value = MathFormula(self.__model)
							t_value.setInternalMathFormula(value)
							t_cfe = CFE(self.__model)
							t_cfe.new(t_var, t_value)
							self.developpedCFEs.append(t_cfe)

					elif isinstance(res[0], tuple):
						for i_var, value in enumerate(res[0]):
							t_var = self.__model.listOfVariables[str(system_vars[i_var])]
							t_value = MathFormula(self.__model)
							t_value.setInternalMathFormula(value)
							t_cfe = CFE(self.__model)
							t_cfe.new(t_var, t_value)
							self.developpedCFEs.append(t_cfe)

					else:

						print "ERROR !!!!!!! The result of the solver for initial conditions is yet another unknown format !"
			else:
				self.developpedCFEs = self
		t1 = time()
		if Settings.verbose >= 1:
			print "> Finished developping closed forms (%.2gs)" % (t1-t0)

	def printCFEs(self):

		print "-----------------------------"
		for t_cfe in self:
			print ">> %s = %s" % (str(t_cfe.getVariable().symbol.getDeveloppedInternalMathFormula()),
								str(t_cfe.getDefinition().getDeveloppedInternalMathFormula()))
