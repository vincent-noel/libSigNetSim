#!/usr/bin/env python
""" MathModel.py


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

from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from libsignetsim.cwriter.CModelWriter import CModelWriter
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger, SympyFloat


from libsignetsim.model.ModelException import MathException
from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from time import time


from libsignetsim.model.math.container.ListOfODEs import ListOfODEs
from libsignetsim.model.math.container.ListOfCFEs import ListOfCFEs
from libsignetsim.model.math.container.ListOfDAEs import ListOfDAEs
from libsignetsim.model.math.MathSlowModel import MathSlowModel
from libsignetsim.model.math.container.ListOfConservationLaws import ListOfConservationLaws

class MathModel(CModelWriter):
	""" Sbml model class """

	def __init__ (self, obj_id=0):
		""" Constructor of model class """

		CModelWriter.__init__(self, obj_id)

		self.listOfODEs = ListOfODEs(self)
		self.listOfCFEs = ListOfCFEs(self)
		self.listOfDAEs = ListOfDAEs(self)

		self.solvedInitialConditions = None
		self.hasDAEs = False
		self.slowModel = None

		self.stoichiometryMatrix = MathStoichiometryMatrix(self)
		self.listOfConservationLaws = ListOfConservationLaws(self)

		self.nbOdes = None
		self.nbAssignments = None
		self.nbConstants = None
		self.nbAlgebraics = None

		self.variablesOdes = None
		self.variablesAssignment = None
		self.variablesConstant = None
		self.variablesAlgebraic = None
		self.__upToDate = False


	def isUpToDate(self):
		return self.__upToDate

	def setUpToDate(self, value):
		self.__upToDate = value


	def getMathModel(self):

		if self.slowModel is not None:
			return self.slowModel

		else:
			return self



	def buildModel(self, vars_to_keep=[], dont_reduce=False, tmin=0):

		# print "Building CFEs"
		self.listOfCFEs.build()
		# print "Building ODEs"
		self.listOfODEs.build()
		# print "Building DAEss"
		self.listOfDAEs.build()

		# self.solveInitialConditions(tmin)
		self.solveSimpleInitialConditions(tmin)

		if len(self.listOfDAEs) > 0:
			self.listOfDAEs.solveInitialConditions(tmin)

		if self.listOfReactions.hasFastReaction():
			self.slowModel = MathSlowModel(self)
			self.slowModel.build()

	def prettyPrint(self):

		print "\n> Full system : "

		self.listOfCFEs.prettyPrint()
		self.listOfDAEs.prettyPrint()
		self.listOfODEs.prettyPrint()
		# self.printConservationLaws()

		print "-----------------------------"


	def solveSimpleInitialConditions(self, tmin):
		""" Initial conditions are a mess between values, initial assignments,
			and assignment rules. We actually need to solve them to make sure
			all dependencies are respected

			Unfortunately, this can be quite costly for large system
			So we'll try to just solve the minimum for C simulations

			"""

		DEBUG = False

		t0 = time()

		init_cond = {}
		if tmin == 0:
			init_cond = {SympySymbol("_time_"): SympyInteger(tmin)}
		else:
			init_cond = {SympySymbol("_time_"): SympyFloat(tmin)}

		for init_ass in self.listOfInitialAssignments.values():
			t_var = init_ass.getVariable().symbol.getInternalMathFormula()
			t_value = init_ass.getDefinition().getDeveloppedInternalMathFormula()
			init_cond.update({t_var:t_value})

		if DEBUG:
			print init_cond

		for rule in self.listOfRules.values():
			if rule.isAssignment():
				t_var = rule.getVariable().symbol.getInternalMathFormula()

				if t_var not in init_cond.keys():
					t_value = rule.getDefinition().getDeveloppedInternalMathFormula()
					init_cond.update({t_var:t_value})

		if DEBUG:
			print init_cond

		for var in self.listOfVariables.values():
			t_var = var.symbol.getInternalMathFormula()

			if t_var not in init_cond.keys():
				t_value = var.value.getDeveloppedInternalMathFormula()
				if t_value is not None:
					init_cond.update({t_var:t_value})
				elif not var.isAlgebraic():
					init_cond.update({t_var:SympyFloat(0.0)})

		if DEBUG:
			print init_cond


		crossDependencies = True
		passes = 1
		while crossDependencies:
			if DEBUG:
				print "PASS : %d" % passes
			crossDependencies = False
			for t_var in init_cond.keys():
				t_def = init_cond[t_var]
				if len(t_def.atoms(SympySymbol).intersection(set(init_cond.keys()))) > 0:
					crossDependencies = True
					if DEBUG:
						print "\n> " + str(t_var) + " : " + str(t_def)
						# raise MathException("Dependencies")
					for match in t_def.atoms(SympySymbol).intersection(set(init_cond.keys())):
						if match == t_var:
							raise MathException("Initial values : self dependency is bad")
						if DEBUG:
							print ">> " + str(match) + " : " + str(init_cond[match])

						# t_formula = selfMathFormula()
						t_def = unevaluatedSubs(t_def, {match:init_cond[match]})
						init_cond.update({t_var:t_def})
						# t_cfe.setDefinitionMath(t_cfe.getDefinition().getInternalMathFormula().subs(self.getBySymbol(match).getSubs()))
						# t_subs = {tt_cfe.getVariable().symbol.getInternalMathFormula():tt_cfe.getV
					if DEBUG:
						if len(t_def.atoms(SympySymbol).intersection(set(init_cond.keys()))) == 0:
							print "> " + str(t_var) + " : " + str(t_def) + " [OK]"
						else:
							print "> " + str(t_var) + " : " + str(t_def) + " [ERR]"
			passes += 1
			if passes >= 100:
				raise MathException("Initial values : Probable circular dependencies")

			if DEBUG:
				print ""

		if DEBUG:
			print init_cond.keys()
			print self.listOfVariables.symbols()
			print self.listOfVariables.keys()

		# Trying to put zero as default for variables without values (aka biomodels 113)
		# But we should also replace that value in the initial conds, so prbalbly we should set it to zero
		# at the very beginning.
		# TODO this week end !
		# for var in self.listOfVariables.values():
		# 	if not var.symbol.getInternalMathFormula() in init_cond.keys() and not var.isAlgebraic():
		# 		# raise MathException("Lacks an initial condition : %s" % var.getSbmlId())
		# 		print "Lacks an initial condition : %s. Set it to zero" % var.getSbmlId()
		# 		init_cond.update({var.symbol.getInternalMathFormula():SympyFloat(0.0)})

		self.solvedInitialConditions = {}
		for var, value in init_cond.items():
			t_var = self.listOfVariables.getBySymbol(var)
			if t_var is not None:
				t_value = MathFormula(self)
				t_value.setInternalMathFormula(value.doit())
				self.solvedInitialConditions.update({t_var:t_value})


		for var in self.listOfVariables.values():
			if not var in self.solvedInitialConditions.keys() and not var.isAlgebraic():
				# raise MathException("Lacks an initial condition : %s" % var.getSbmlId())
				print "Lacks an initial condition : %s" % var.getSbmlId()
				# t_formula = MathFormula(self)
				# t_formula.setInternalMathFormula(SympyFloat(0.0))
				# self.solvedInitialConditions.update({var:t_formula})


		if Settings.verbose >= 1:
			print "> Finished calculating initial conditions (%.2gs)" % (time()-t0)


	#
	# def buildReducedSystem(self, vars_to_keep=[]):
	#
	# 	reduced_odes = []
	# 	reduced_odes_vars = []
	# 	reduced_odes_der_vars = []
	# 	reduced_odes_symbols = []
	#
	# 	self.findReducibleVariables(vars_to_keep=vars_to_keep)
	#
	# 	# print self.reducibleVariables
	# 	t_reducible_vars = [var for var in self.reducibleVariables.keys()]
	# 	t_reducible_values = [var for var in self.reducibleVariables.values()]
	#
	# 	if len(self.reducibleVariables) > 0:
	#
	# 		for i, ode_var in enumerate(self.ODE_vars):
	# 			if ode_var.getInternalMathFormula() in t_reducible_vars:
	#
	# 				t_cfe = t_reducible_values[t_reducible_vars.index(ode_var.getInternalMathFormula())]
	# 				t_formula = MathFormula(self)
	# 				t_formula.setInternalMathFormula(t_cfe)
	# 				self.CFEs.append(t_formula)
	#
	# 				self.CFE_vars.append(ode_var)
	# 				self.CFE_types.append(MathCFEs.SOLVED)
	#
	# 				#Now changing the variable type
	# 				t_var = self.listOfVariables[str(ode_var.getInternalMathFormula())]
	# 				self.listOfVariables.changeVariableType(t_var, Variable.VAR_ASS)
	#
	# 			else:
	# 				reduced_odes.append(self.ODEs[i])
	# 				reduced_odes_vars.append(ode_var)
	# 				reduced_odes_der_vars.append(self.ODE_der_vars[i])
	# 				reduced_odes_symbols.append(self.ODE_symbols[i])
	#
	# 		self.ODEs = reduced_odes
	# 		self.ODE_vars = reduced_odes_vars
	# 		self.ODE_der_vars = reduced_odes_der_vars
	# 		self.ODE_symbols = reduced_odes_symbols
	#
	# 		self.developCFEs()
