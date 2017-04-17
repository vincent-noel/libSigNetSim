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
from libsignetsim.model.math.sympy_shortcuts import SympyPiecewise, SympyITE, SympyInf, SympyNan, SympyEqual, SympySymbol, SympyPow
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.ModelException import MathException
from sympy import solve, sympify, srepr, simplify
from time import time

class ListOfCFEs(list):
	""" Sbml model class """


	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)

	def build(self):

		for rule in self.__model.listOfRules.values():
			if rule.isAssignment():
				t_cfe = CFE(self.__model, CFE.ASSIGNMENT)
				t_cfe.new(rule.getVariable(), rule.getDefinition(rawFormula=True))
				list.append(self, t_cfe)

		for reaction in self.__model.listOfReactions.values():
			t_cfe = CFE(self.__model, CFE.REACTION)
			t_cfe.new(reaction, reaction.value)
			list.append(self, t_cfe)

		self.developCFEs()


	def developCFEs(self):

		DEBUG = False

		if DEBUG:
			print self

		t0 = time()

		if len(self) > 0:

			cfe_vars = []
			for t_cfe in self:
				cfe_vars.append(t_cfe.getVariable().symbol.getInternalMathFormula())

			crossDependencies = True
			passes = 1

			while crossDependencies:

				if DEBUG:
					print "PASS : %d" % passes

				crossDependencies = False
				for t_cfe in self:
					t_def = t_cfe.getDefinition().getInternalMathFormula()
					if len(t_def.atoms(SympySymbol).intersection(set(cfe_vars))) > 0:

						crossDependencies = True

						if DEBUG:
							print "\n> " + str(t_cfe)

						for match in t_def.atoms(SympySymbol).intersection(set(cfe_vars)):
							if match == t_cfe.getVariable().symbol:
								raise MathException("Developping CFEs : self dependency is bad")

							if DEBUG:
								print ">> " + str(self.getBySymbol(match))

							t_cfe.setDefinitionMath(t_cfe.getDefinition().simpleSubsDevelopped(self.getBySymbol(match).getSubs()))

						if DEBUG:
							if len(t_cfe.getDefinition().getInternalMathFormula().atoms(SympySymbol).intersection(set(cfe_vars))) == 0:
								print "> " + str(t_cfe) + " [OK]"

							else:
								print "> " + str(t_cfe) + " [ERR]"

				passes += 1
				if passes >= 100:
					raise MathException("Developping CFEs : Probable circular dependencies")

				if DEBUG:
					print ""

		t1 = time()
		if Settings.verbose >= 1:
			print "> Finished developping closed forms (%.2gs)" % (t1-t0)

	def __str__(self):

		res = ""
		for t_cfe in self:
			res += str(t_cfe) + "\n"

		return res


	def getByVariable(self, variable):

		for cfe in self:
			if variable == cfe.getVariable():
				return cfe

	def getBySymbol(self, symbol):
		for cfe in self:
			if symbol == cfe.getVariable().symbol.getInternalMathFormula():
				return cfe
