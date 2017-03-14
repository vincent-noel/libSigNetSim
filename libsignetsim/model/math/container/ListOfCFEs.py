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
from sympy import solve, sympify, srepr
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

		# print "Starting to develop CFEs"
		# self.prettyPrint()
		self.developCFEs()
		# self.prettyPrint()

		# print "Done developping CFEs"


	def developCFEs(self):

		DEBUG = False
		t0 = time()
		self.developpedCFEs = []
		continueDevelop = True
		if len(self) > 0:

			cfe_vars = []
			for t_cfe in self:
				# if t_cfe.isAssignment():
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
							t_cfe.setDefinitionMath(t_cfe.getDefinition().getInternalMathFormula().subs(self.getBySymbol(match).getSubs()))
							# t_subs = {tt_cfe.getVariable().symbol.getInternalMathFormula():tt_cfe.getV
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
			#
			# cfe_subs = {}
			# for t_cfe in self:
			# 	# if t_cfe.isAssignment():
			# 	cfe_vars.append(t_cfe.getVariable().symbol.getInternalMathFormula())
			# 	cfe_subs.update({t_cfe.getVariable().symbol.getInternalMathFormula(): t_cfe.getDefinition().getInternalMathFormula()})
			#
			# # self.prettyPrint()
			#
			# for t_cfe in self:
			# 	t_def = t_cfe.getDefinition().getInternalMathFormula()
			# 	if len(t_def.atoms(SympySymbol).intersection(set(cfe_vars))) > 0:
			# 		t_cfe.setDefinitionMath(t_def.subs(cfe_subs))
			#
			# # self.prettyPrint()
			#
			#
			# system = []
			# system_vars = []
			#
			# print cfe_vars
			# for t_cfe in self:
			# 	# if t_cfe.isAssignment():
			# 		t_def = t_cfe.getDefinition().getInternalMathFormula()
			# 		if len(t_def.atoms(SympySymbol).intersection(set(cfe_vars))) > 0:
			# 			print ">> " + str(t_cfe)
			# 			for match in t_def.atoms(SympySymbol).intersection(set(cfe_vars)):
			# 				print ">> " + str(self.getBySymbol(match))
			# 				tt_cfe = self.getBySymbol(match)
			# 				system.append(SympyEqual(
			# 					tt_cfe.getVariable().symbol.getInternalMathFormula(),
			# 					tt_cfe.getDefinition().getInternalMathFormula()
			# 				))
			# 			system.append(SympyEqual(
			# 				t_cfe.getVariable().symbol.getInternalMathFormula(),
			# 				t_cfe.getDefinition().getInternalMathFormula()
			# 			))
			# 			system_vars.append(t_cfe.getVariable().symbol.getInternalMathFormula())
						# raise MathException("Cfes not completely developped")
					# # print "def : %s" % str(t_def)
					# # print "test = %s" % str(t_def not in [SympyInf, -SympyInf, SympyNan])
					# if (t_def not in [SympyInf, -SympyInf, SympyNan]
					# 	and len(t_def.atoms(SympyITE, SympyPiecewise)) > 0):
					# 	t_equ = SympyEqual(
					# 		t_cfe.getVariable().symbol.getInternalMathFormula(),
					# 		t_def
					# 	)
					#
					# 	if (len(t_def.atoms(SympySymbol)) > 0
					# 			and t_def.atoms(SympySymbol) != set([SympySymbol("_time_")])
					# 			and len(t_def.atoms(SympySymbol).intersection(set(cfe_vars))) > 0):
					# 		# print t_def.atoms(SympySymbol)
					# 		# print len(t_def.atoms(SympySymbol).intersection(set(cfe_vars)))
					# 		# print ""
					# 		system_vars.append(t_cfe.getVariable().symbol.getInternalMathFormula())
					# 		system.append(t_equ)
						# else:
						# 	self.developpedCFEs.append(t_cfe)
			#
			#
			# 	# elif t_cfe.isReaction():
			# 	# 	self.developpedCFEs.append(t_cfe)
			# print "> System to solve :"
			# for equ in system:
			# 	print ">> %s == %s" % (str(equ.args[0]), str(equ.args[1]))
			# print "> Solve variables :"
			# for var in system_vars:
			# 	print ">> %s" % var
			# start_solve = time()
			#
			# res = solve(system, system_vars)
			#
			# print "> Pure solving : %.2gs" % (time()-start_solve)
			# print "-"*25
			# print ">> %s" % res

			#
			# for equ in system:
			# 	print str(equ)
			# print system_vars
			# if len(system_vars) > 0 and continueDevelop:
			# 	res = solve(system, system_vars)
			# #
			# 	print res
			#
			# 	if res is not True and len(res) > 0:
			#
			# 		if isinstance(res, dict):
			# 			for var, value in res.items():
			# 				t_var = self.__model.listOfVariables[str(var)]
			# 				t_value = MathFormula(self.__model)
			# 				t_value.setInternalMathFormula(value)
			# 				t_cfe = CFE(self.__model)
			# 				t_cfe.new(t_var, t_value)
			# 				self.developpedCFEs.append(t_cfe)
			#
			# 		elif isinstance(res[0], dict):
			# 			for var, value in res[0].items():
			# 				t_var = self.__model.listOfVariables[str(var)]
			# 				t_value = MathFormula(self.__model)
			# 				t_value.setInternalMathFormula(value)
			# 				t_cfe = CFE(self.__model)
			# 				t_cfe.new(t_var, t_value)
			# 				self.developpedCFEs.append(t_cfe)
			#
			# 		elif isinstance(res[0], tuple):
			# 			for i_var, value in enumerate(res[0]):
			# 				t_var = self.__model.listOfVariables[str(system_vars[i_var])]
			# 				t_value = MathFormula(self.__model)
			# 				t_value.setInternalMathFormula(value)
			# 				t_cfe = CFE(self.__model)
			# 				t_cfe.new(t_var, t_value)
			# 				self.developpedCFEs.append(t_cfe)
			#
			# 		else:
			#
			# 			print "ERROR !!!!!!! The result of the solver for initial conditions is yet another unknown format !"
			# else:
			# 	self.developpedCFEs = self
		t1 = time()
		if Settings.verbose >= 1:
			print "> Finished developping closed forms (%.2gs)" % (t1-t0)

	def prettyPrint(self):

		print "-----------------------------"
		for t_cfe in self:
			print ">> " + str(t_cfe)


	def getByVariable(self, variable):

		for cfe in self:
			if variable == cfe.getVariable():
				return cfe

	def getBySymbol(self, symbol):
		for cfe in self:
			if symbol == cfe.getVariable().symbol.getInternalMathFormula():
				return cfe
