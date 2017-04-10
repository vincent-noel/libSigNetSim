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
from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyFloat, SympyRational, SympyAtom,
	SympyOne, SympyNegOne, SympyZero, SympyPi, SympyE, SympyExp1, SympyHalf,
	SympyInf, SympyNan, SympyAdd, SympyMul, SympyPow,
	SympyFunction, SympyUndefinedFunction, SympyLambda, SympyDerivative,
	SympyCeiling, SympyFloor, SympyAbs, SympyLog, SympyExp, SympyPiecewise,
	SympyFactorial, SympyRoot, SympyAcos, SympyAsin, SympyAtan, SympyAcosh,
	SympyAsinh, SympyAtanh, SympyCos, SympySin, SympyTan, SympyAcot,
	SympyAcoth, SympyCosh, SympySinh, SympyTanh, SympySec, SympyCsc,
	SympyCot, SympyCoth, SympyAcsc, SympyAsec,
	SympyEqual, SympyUnequal, SympyGreaterThan, SympyLessThan,
	SympyStrictGreaterThan, SympyStrictLessThan,
	SympyAnd, SympyOr, SympyXor, SympyNot, SympyTrue, SympyFalse,
	SympyMax, SympyMin)


from libsignetsim.model.ModelException import MathException
from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.MathJacobianMatrix import MathJacobianMatrix
from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from libsignetsim.model.Variable import Variable
from sympy import simplify, diff, solve, zeros, solveset, linsolve, srepr
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

		# MathConservationLaws.__init__(self)
		# MathJacobianMatrix.__init__(self)
		self.stoichiometryMatrix = MathStoichiometryMatrix(self)
		self.listOfConservationLaws = ListOfConservationLaws(self)
		# self.listOfFinalVariables = ListOfVariables(self)

		self.nbOdes = None
		self.nbAssignments = None
		self.nbConstants = None
		self.nbAlgebraics = None

		self.variablesOdes = None
		self.variablesAssignment = None
		self.variablesConstant = None
		self.variablesAlgebraic = None
		self.__upToDate = False

		# self.stoichiometryMatrix = None


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
		self.solveSimpleInitialConditions_v2(tmin)

		if len(self.listOfDAEs) > 0:
			self.listOfDAEs.solveInitialConditions_v2(tmin)

		if self.listOfReactions.hasFastReaction():
			self.slowModel = MathSlowModel(self)
			self.slowModel.build()

		# print len(self.getMathModel().listOfCFEs)

		# print self.listOfVariables.keys()
		# print [var.value.getInternalMathFormula() for var in self.listOfVariables.values()]
		# self.prettyPrint()



		# self.buildStoichiometryMatrix()
		# self.listOfConservationLaws.buildConservationLaws()
		# self.listOfConservationLaws.printConservationLaws()



		# print self.listOfSpecies.hasBoundaryConditions()
		# print dont_reduce

		# if self.listOfReactions.hasFastReaction():
		# 	self.buildSlowSubstem()
		#
		# elif (len(self.listOfEvents) == 0 and len(self.listOfReactions) > 0
		# 	and not self.listOfSpecies.hasBoundaryConditions()
		# 	and not dont_reduce):
		#
		# 	t1 = time()
		#
		# 	self.buildStoichiometryMatrix()
		#
		# 	t1a = time()
		# 	if Settings.verbose:
		# 		print "> Stoichiometry matrix built (%.2gs)" % (t1a-t1)
		#
		# 	self.findConservationLaws()
		#
		# 	t2 = time()
		# 	if Settings.verbose:
		# 		print "> Conservation laws found (%.2gs)" % (t2-t1a)
		#
		#
		# 	# print vars_to_keep
		# 	self.buildReducedSystem(vars_to_keep=vars_to_keep)
		# 	self.developODEs()
		# 	if Settings.verbose:
		# 		print "> Model reduced (%.2gs)" % (time()-t2)

#        self.buildJacobianMatrix()
		# self.printSystem()




	def prettyPrint(self):

		print "\n> Full system : "

		self.listOfCFEs.prettyPrint()
		self.listOfDAEs.prettyPrint()
		self.listOfODEs.prettyPrint()
		# self.printConservationLaws()

		print "-----------------------------"


	def solveSimpleInitialConditions_v2(self, tmin):
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


		# if Settings.verbose >= 1:
		# 	print "> Finished calculating initial conditions (%.2gs)" % (time()-t0)



	def solveSimpleInitialConditions(self, tmin):
		""" Initial conditions are a mess between values, initial assignments,
			and assignment rules. We actually need to solve them to make sure
			all dependencies are respected

			Unfortunately, this can be quite costly for large system
			So we'll try to just solve the minimum for C simulations

			"""

		DEBUG_LOG = False
		t0 = time()

		subs_t0 = {}
		if tmin == 0:
			subs_t0 = {SympySymbol("_time_"): SympyInteger(tmin)}
		else:
			subs_t0 = {SympySymbol("_time_"): SympyFloat(tmin)}


		# Here we build a subs dictionnary for the special case which are the constant compartments
		compartments = {}
		for compartment in self.listOfCompartments.values():
			t_symbol = compartment.symbol.getInternalMathFormula()
			if compartment.hasInitialAssignment():
				t_initass = compartment.hasInitialAssignmentBy()
				compartments.update({t_symbol:t_initass.getDefinition().getInternalMathFormula()})

			elif compartment.isAssignment():
				t_cfe = self.listOfCFEs.getByVariable(compartment)
				compartments.update({t_symbol:t_cfe.getDefinition().getInternalMathFormula()})

			elif compartment.isConstant() and compartment.value.getInternalMathFormula() is not None:
				compartments.update({t_symbol:compartment.value.getInternalMathFormula().subs(subs_t0)})


		constants = {}
		for var in self.listOfVariables.values():
			if (var.isConstant() or var.isDerivative()) and not var.hasInitialAssignment():
				if var.isSpecies() and var.isConcentration():
					constants.update({var.symbol.getInternalMathFormula(): var.value.getDeveloppedInternalMathFormula().subs(subs_t0).subs(compartments)})
				else:
					constants.update({var.symbol.getInternalMathFormula(): var.value.getDeveloppedInternalMathFormula().subs(subs_t0)})

		if DEBUG_LOG:
			print constants


		initially_assigned = {}
		for var in self.listOfVariables.values():
			t_value = None
			if (not var.isReaction() and var.hasInitialAssignment()):
				t_value = var.hasInitialAssignmentBy().getDefinition().getDeveloppedInternalMathFormula()
				initially_assigned.update({var.symbol.getInternalMathFormula(): t_value.subs(subs_t0).subs(compartments).subs(constants)})

			elif (not var.isReaction() and var.isAssignment()):
				t_value = self.listOfCFEs.getByVariable(var).getDefinition().getDeveloppedInternalMathFormula()
				initially_assigned.update({var.symbol.getInternalMathFormula(): t_value.subs(subs_t0).subs(compartments).subs(constants)})
		if DEBUG_LOG:
			print initially_assigned

		self.solvedInitialConditions = {}

		for var in self.listOfVariables.values():
			t_symbol = var.symbol.getInternalMathFormula()

			if t_symbol in constants.keys():
				t_formula = MathFormula(self)
				t_formula.setInternalMathFormula(constants[t_symbol].subs(constants))
				self.solvedInitialConditions.update({var:t_formula})

			elif t_symbol in initially_assigned.keys():
				t_formula = MathFormula(self)
				t_formula.setInternalMathFormula(initially_assigned[t_symbol].subs(constants).subs(initially_assigned))
				self.solvedInitialConditions.update({var:t_formula})

			else:
				t_formula = MathFormula(self)
				t_formula.setInternalMathFormula(SympyInteger(0))
				self.solvedInitialConditions.update({var:t_formula})


		if DEBUG_LOG:
			for key, value in self.solvedInitialConditions.items():
				print "%s : %s" % (
					key.getSbmlId(),
					str(value.getInternalMathFormula())
				)

		system = []
		system_vars = []

		for key, value in self.solvedInitialConditions.items():
			if len(value.getInternalMathFormula().atoms(SympySymbol)) > 0:
				system_vars.append(key.symbol.getInternalMathFormula())

			if key.symbol.getInternalMathFormula() == SympySymbol("MPF") or key.symbol.getInternalMathFormula() == SympySymbol("SPF"):
				system.append(SympyEqual(key.symbol.getInternalMathFormula(), value.getInternalMathFormula().doit()))

		if DEBUG_LOG:
			print "> System to solve :"
			for equ in system:
				print ">> %s == %s" % (srepr(equ.args[0]), srepr(equ.args[1]))
			print ">> %s" % system_vars
			start_solve = time()

		res = solve(system, system_vars)

		if DEBUG_LOG:
			print "> Pure solving : %.2gs" % (time()-start_solve)
			print "-"*25
			print ">> %s" % res
		if Settings.verboseTiming >= 2:
			print "> Finished calculating initial conditions (%.2gs)" % (time()-t0)


	def solveInitialConditions(self, tmin):
		""" Initial conditions are a mess between values, initial assignments,
			and assignment rules. We actually need to solve them to make sure
			all dependencies are respected

			So the idea is to build a system with all the assignment rules, the
			initial assigments, and the initial values, and solve it for the
			variables whose initial value depends on other variables

			"""

		DEBUG_LOG = False

		t0 = time()
		self.solvedInitialConditions = {}

		variables = self.listOfVariables.values()
		system = []
		system_vars = []

		# for var in self.listOfVariables.values():
		# 	print "%s : %s" % (var.getSbmlId(), str(var.symbol.getInternalMathFormula()))

		# TODO: Those are initial values, so the time needs to be set to the
		# starting time. that's why we have this tmin argument since the
		# build() call. Maybe the computing of the initial conditions
		# should be a separate call
		if tmin == 0:
			subs = {SympySymbol("_time_"): SympyInteger(tmin)}
		else:
			subs = {SympySymbol("_time_"): SympyFloat(tmin)}


		# Here we build a subs dictionnary for the special case which are the constant compartments
		subs_comp = {}
		for compartment in self.listOfCompartments.values():
			if compartment.isConstant():
				subs_comp.update({compartment.symbol.getInternalMathFormula():compartment.value.getInternalMathFormula()})


		#First of all, let's look at the constant cases :
		for t_var in self.listOfVariables.values():
			if not (t_var.isReaction() or t_var.isAssignmentRuled() or t_var.hasInitialAssignment() or t_var.isAlgebraic()):
			# Here we can be more restrictive, since only assigments rules matter for IC. Rate rules shouldn't
			# if not (t_var.isReaction() or t_var.isRuled() or t_var.hasInitialAssignment() or t_var.isAlgebraic()):
				if t_var.value.getInternalMathFormula() is not None:
					t_def = t_var.value.getDeveloppedInternalMathFormula().subs(subs)

					if t_var.isConcentration():
						t_def = t_def.subs(subs_comp)

					if len(t_def.atoms(SympySymbol)) == 0:
						variables.remove(t_var)
						t_formula = MathFormula(self)
						t_formula.setInternalMathFormula(t_def)
						self.solvedInitialConditions.update({t_var: t_formula})
						# subs.update({t_var.symbol.getInternalMathFormula():t_def})


					# else:
					# 	print "There is something wrong with %s (value is %s, pre subs is %s)" % (t_var.symbol.getInternalMathFormula(), t_def, t_var.value.getDeveloppedInternalMathFormula())

		nb_simples = len(self.listOfVariables.keys())-len(variables)
		# if DEBUG_LOG:
		# 	print "\n> %d variables out of %d were simple cases" % (nb_simples, len(self.listOfVariables))
		# 	print [var.symbol.getInternalMathFormula() for var in list(set(self.listOfVariables.values()).difference(set(variables)))]




		for t_cfe in self.listOfCFEs:
			if t_cfe.getVariable() in variables:
				variables.remove(t_cfe.getVariable())
				t_def = t_cfe.getDefinition().getDeveloppedInternalMathFormula().subs(subs)
				if t_def not in [SympyInf, -SympyInf, SympyNan]:
					t_equ = SympyEqual(
						t_cfe.getVariable().symbol.getInternalMathFormula(),
						t_def.doit()
					)
					if len(t_def.atoms(SympySymbol)) > 0:
						# if DEBUG_LOG:
						# 	print "Adding %s (From unsolvable CFE : %s)" % (t_equ, t_def)
						system.append(t_equ)
						system_vars.append(t_cfe.getVariable().symbol.getInternalMathFormula())
					else:
						t_formula = MathFormula(self)
						t_formula.setInternalMathFormula(t_def)
						self.solvedInitialConditions.update({t_cfe.getVariable(): t_formula})
						# subs.update({t_var.symbol.getInternalMathFormula():t_def})



		nb_found_bycfe = len(self.listOfVariables)-len(variables)-nb_simples

		# if DEBUG_LOG:
		# 	print "\n> %d initial values found after reading CFEs (%d left)" % (nb_found_bycfe, len(self.listOfVariables) - len(self.solvedInitialConditions))
		# 	print [var.getSbmlId() for var in self.solvedInitialConditions.keys()]
		# 	print "\n>> System vars : "
		# 	print system_vars
		#
		# 	print "\n> Subs pre initial assignments"
		# 	print subs

		for t_init in self.listOfInitialAssignments.values():
			if t_init.getVariable() in variables:
				variables.remove(t_init.getVariable())
				t_def = t_init.getDefinition().getDeveloppedInternalMathFormula().subs(subs)
				if t_def not in [SympyInf, -SympyInf, SympyNan]:
					t_equ = SympyEqual(
						t_init.getVariable().symbol.getInternalMathFormula(),
						t_def.doit()
					)
					if len(t_def.atoms(SympySymbol)) > 0:
						# print "Adding %s (From InitAss)" % t_equ

						system.append(t_equ)
						system_vars.append(t_init.getVariable().symbol.getInternalMathFormula())

					else:
						t_formula = MathFormula(self)
						t_formula.setInternalMathFormula(t_def)
						self.solvedInitialConditions.update({t_init.getVariable(): t_formula})
						# subs.update({t_init.getVariable().symbol.getInternalMathFormula():t_def})

				else:
					t_formula = MathFormula(self)
					t_formula.setInternalMathFormula(t_def)
					self.solvedInitialConditions.update({t_init.getVariable(): t_formula})
					# subs.update({t_init.getVariable().symbol.getInternalMathFormula():t_def})

		# if DEBUG_LOG:
		# 	print "\n> Solved initial conditions after reading initial assignments"
		# 	print [var.getSbmlId() for var in self.solvedInitialConditions.keys()]


		for t_var in self.listOfVariables.values():
			if t_var.isReaction():
				t_formula = MathFormula(self)
				t_formula.setInternalMathFormula(SympyInteger(0))
				self.solvedInitialConditions.update({t_var: t_formula})


		for var in self.listOfVariables.values():
			if var not in self.solvedInitialConditions.keys():

				print var.symbol.getInternalMathFormula()
				print type(var)


		for t_var in self.listOfVariables.values():
			# if not t_var.isReaction() and t_var in variables:
			if t_var in variables:
				variables.remove(t_var)
				if t_var.value.getInternalMathFormula() is not None:
					t_def = t_var.value.getDeveloppedInternalMathFormula()#.subs(subs)
					# print "simple values ? : %s = %s" % (t_var.symbol.getInternalMathFormula(), t_def)

					if t_def not in [SympyInf, -SympyInf, SympyNan]:
						t_equ = SympyEqual(
							t_var.symbol.getInternalMathFormula(),
							t_def.doit()
						)
						if len(t_equ.atoms(SympySymbol)) > 0:
							system.append(t_equ)
							system_vars.append(t_var.symbol.getInternalMathFormula())
						else:
							t_formula = MathFormula(self)
							t_formula.setInternalMathFormula(t_def)
							self.solvedInitialConditions.update({t_var: t_formula})

					# else:
					# 	t_formula = MathFormula(self)
					# 	t_formula.setInternalMathFormula(t_def)
					# 	self.solvedInitialConditions.update({t_var: t_formula})


		if DEBUG_LOG:
			print "\n> Solved initial conditions after constructing the system"
			print [var.getSbmlId() for var in self.solvedInitialConditions.keys()]
		subs = {}
		# if tmin == 0:
		# 	subs = {SympySymbol("_time_"): SympyInteger(tmin)}
		# else:
		# 	subs = {SympySymbol("_time_"): SympyFloat(tmin)}

		for var, value in self.solvedInitialConditions.items():
			# print value.getInternalMathFormula()
			# if len(value.getInternalMathFormula().atoms(SympySymbol)) == 0:
				subs.update({var.symbol.getInternalMathFormula(): value.getInternalMathFormula()})


		t_system = []
		for equ in system:
			if len(equ.atoms(SympySymbol)) > 0:
				t_equ = equ.subs(subs)

				if len(t_equ.atoms(SympySymbol)) == 0:
					t_var = self.listOfVariables[str(t_equ.args[0])]
					t_value = MathFormula(self)
					t_value.setInternalMathFormula(t_equ.args[1])
					self.solvedInitialConditions.update({t_var:t_value})
				else:
					# print "here we replace %s" % str(t_equ.args[0])
					t_system.append(t_equ)
				# if equ
			else:
				t_var = self.listOfVariables[str(t_equ.args[0])]
				t_value = MathFormula(self)
				t_value.setInternalMathFormula(t_equ.args[1])
				self.solvedInitialConditions.update({t_var:t_value})

		system = t_system

		# for var, value in self.solvedInitialConditions.items():
		# 	# print value.getInternalMathFormula()
		# 	# if len(value.getInternalMathFormula().atoms(SympySymbol)) == 0:
		# 		subs.update({var.symbol.getInternalMathFormula(): value.getInternalMathFormula()})
		#
		#
		# print "\npoil before sub"
		# t_system = []
		# for equ in system:
		# 	if len(equ.atoms(SympySymbol)) > 0:
		# 		t_equ = equ.subs(subs)
		#
		# 		if len(t_equ.atoms(SympySymbol)) == 0:
		# 			t_var = self.listOfVariables[str(t_equ.args[0])]
		# 			t_value = MathFormula(self)
		# 			t_value.setInternalMathFormula(t_equ.args[1])
		# 			self.solvedInitialConditions.update({t_var:t_value})
		# 		else:
		# 			t_system.append(t_equ)
		# 			print "here we replace %s" % str(t_equ.args[0])
		# 		# if equ
		# 	else:
		# 		t_var = self.listOfVariables[str(t_equ.args[0])]
		# 		t_value = MathFormula(self)
		# 		t_value.setInternalMathFormula(t_equ.args[1])
		# 		self.solvedInitialConditions.update({t_var:t_value})
		#
		# system = t_system
		#
		# for var, value in self.solvedInitialConditions.items():
		# 	# print value.getInternalMathFormula()
		# 	# if len(value.getInternalMathFormula().atoms(SympySymbol)) == 0:
		# 		subs.update({var.symbol.getInternalMathFormula(): value.getInternalMathFormula()})
		#
		#
		# print "\npoil before sub"
		# t_system = []
		# for equ in system:
		# 	if len(equ.atoms(SympySymbol)) > 0:
		# 		t_equ = equ.subs(subs)
		#
		# 		if len(t_equ.atoms(SympySymbol)) == 0:
		# 			t_var = self.listOfVariables[str(t_equ.args[0])]
		# 			t_value = MathFormula(self)
		# 			t_value.setInternalMathFormula(t_equ.args[1])
		# 			self.solvedInitialConditions.update({t_var:t_value})
		# 		else:
		# 			print "here we replace %s" % str(t_equ.args[0])
		# 			t_system.append(t_equ)
		# 		# if equ
		# 	else:
		# 		t_var = self.listOfVariables[str(t_equ.args[0])]
		# 		t_value = MathFormula(self)
		# 		t_value.setInternalMathFormula(t_equ.args[1])
		# 		self.solvedInitialConditions.update({t_var:t_value})
		#
		# system = t_system

		# retursn
		# print "possible subs"
		# print subs
		if DEBUG_LOG:
			print "> Precomputed initial values"
			print [var.getSbmlId() for var in self.solvedInitialConditions.keys()]
			print [var.getSbmlId() for var in self.listOfVariables.values()]
			for key, value in self.solvedInitialConditions.items():
				print ">> %s : %s" % (
					key.symbol.getDeveloppedInternalMathFormula(),
					str(value.getDeveloppedInternalMathFormula())
				)
			print "> System to solve :"
			print ">> %s" % system
			print ">> %s" % system_vars
		# return

		start_solve = time()
		res = solve(system, system_vars)
		if Settings.verboseTiming >= 2:
			print "> Pure solving : %.2gs" % (time()-start_solve)
		if DEBUG_LOG:
			print "-"*25
			print ">> %s" % res

		if res is not True and len(res) > 0:
			if isinstance(res, dict):
				for var, value in res.items():
					t_var = self.listOfVariables[str(var)]
					t_value = MathFormula(self)
					t_value.setInternalMathFormula(value)
					self.solvedInitialConditions.update({t_var:t_value})

			elif isinstance(res[0], dict):
				for var, value in res[0].items():
					t_var = self.listOfVariables[str(var)]
					t_value = MathFormula(self)
					t_value.setInternalMathFormula(value)
					self.solvedInitialConditions.update({t_var:t_value})

			elif isinstance(res[0], tuple):
				for i_var, value in enumerate(res[0]):
					t_var = self.listOfVariables[str(system_vars[i_var])]
					t_value = MathFormula(self)
					t_value.setInternalMathFormula(value)
					self.solvedInitialConditions.update({t_var:t_value})

			else:
				print "ERROR !!!!!!! The result of the solver for initial conditions is yet another unknown format !"

		subs = {}
		for var, value in self.solvedInitialConditions.items():
			# if len(value.getInternalMathFormula().atoms(SympySymbol)) == 0:
				subs.update({var.symbol.getInternalMathFormula(): value.getInternalMathFormula()})


		#
		# # print "final subs"
		# # print subs
		#
		# final = {}
		# for var, value in self.solvedInitialConditions.items():
		# 	# if len(value.getInternalMathFormula().atoms(SympySymbol)) > 0:
		# 	t_formula = MathFormula(self)
		# 	t_formula.setInternalMathFormula(value.getInternalMathFormula().subs(subs))
		# 	final.update({var: t_formula})
		#
		# self.solvedInitialConditions = final
		#
		# # for key, value in self.solvedInitialConditions.items():
		# # 	print "%s : %s" % (
		# # 		key.getSbmlId(),
		# # 		str(value.getDeveloppedInternalMathFormula())
		# # 	)
		#
		# for var in self.listOfVariables.values():
		# 	if var not in self.solvedInitialConditions.keys() and var.value.getInternalMathFormula() is not None:
		# 		# print var.symbol.getInternalMathFormula()
		# 		t_value = MathFormula(self)
		# 		t_value.setInternalMathFormula(var.value.getDeveloppedInternalMathFormula())
		# 		self.solvedInitialConditions.update({var:t_value})
		#
		# subs = {}
		#
		# if tmin == 0:
		# 	subs = {SympySymbol("_time_"): SympyInteger(tmin)}
		# else:
		# 	subs = {SympySymbol("_time_"): SympyFloat(tmin)}
		# for var, value in self.solvedInitialConditions.items():
		# 	if value.getInternalMathFormula() is not None:
		# 		subs.update({var.symbol.getInternalMathFormula(): value.getInternalMathFormula()})
		#
		# # print "last subs"
		# # print subs



		# for t_cfe in self.listOfCFEs:
		#
		# 	# print var.symbol.getInternalMathFormula()
		# 	t_value = MathFormula(self)
		# 	t_value.setInternalMathFormula(t_cfe.getDefinition().getDeveloppedInternalMathFormula().subs(subs))
		# 	self.solvedInitialConditions.update({t_cfe.getVariable():t_value})



		if Settings.verboseTiming >= 2:
			print "> Finished calculating initial conditions (%.2gs)" % (time()-t0)


		# for key, value in self.solvedInitialConditions.items():
		# 	print "%s : %s" % (
		# 		key.getSbmlId(),
		# 		str(value.getDeveloppedInternalMathFormula())
		# 	)
	#
	# def buildSlowSubstem(self):
	#
	# 	self.fastLaws = []
	# 	self.fastLaws_vars = []
	# 	self.fastStoichiometryMatrix = None
	# 	self.fastConservationLaws = []
	#
	#
	# 	for reaction in self.listOfReactions.values():
	# 		if reaction.fast:
	# 			self.fastLaws.append(reaction.kineticLaw.getFinalMathFormula())
	#
	# 			for reactant in reaction.listOfReactants.values():
	# 				self.fastLaws_vars.append(reactant.getSpecies().symbol.getFinalMathFormula())
	#
	# 			for product in reaction.listOfProducts.values():
	# 				self.fastLaws_vars.append(product.getSpecies().symbol.getFinalMathFormula())
	#
	# 			t_sto_matrix = reaction.getStoichiometryMatrix_v2()
	#
	# 			for t_stoi_reaction in t_sto_matrix:
	# 				t_reaction = zeros(1,len(self.listOfSpecies))
	# 				for j, t_formula in enumerate(t_stoi_reaction):
	#
	# 					t_reaction[j] = t_formula.getDeveloppedInternalMathFormula()
	#
	# 				if self.fastStoichiometryMatrix is None:
	# 					self.fastStoichiometryMatrix = t_reaction
	# 				else:
	# 					self.fastStoichiometryMatrix = self.fastStoichiometryMatrix.col_join(t_reaction)
	#
	#
	#
	# 	if len(self.fastLaws) > 0:
	#
	# 		for i, t_res in enumerate(self.fastStoichiometryMatrix.nullspace()):
	#
	# 			t_law = MathFormula.ZERO
	# 			t_value = MathFormula.ZERO
	# 			t_vars = []
	#
	# 			for ii, tt_res in enumerate(t_res):
	#
	# 				t_species = self.listOfSpecies.values()[ii]
	#
	# 				# Getting symbol
	# 				tt_symbol = t_species.symbol.getFinalMathFormula()
	# 				if t_species.isConcentration():
	# 					tt_symbol /= t_species.getCompartment().symbol.getFinalMathFormula()
	#
	#
	# 				# Getting value
	# 				if t_species.hasInitialAssignment():
	# 					tt_value = t_species.hasInitialAssignmentBy().getExpressionMath().getFinalMathFormula()
	#
	# 					for tt_species in self.listOfSpecies.values():
	# 						ttt_symbol = tt_species.symbol.getFinalMathFormula()
	# 						ttt_value = tt_species.value.getFinalMathFormula()
	# 						if ttt_symbol in tt_value.atoms(SympySymbol) and ttt_value is not None:
	# 							tt_value = tt_value.subs(ttt_symbol, ttt_value)
	#
	# 					if t_species.isConcentration():
	# 						tt_value /= t_species.getCompartment().symbol.getFinalMathFormula()
	#
	# 					if SympySymbol("_time_") in tt_value.atoms():
	# 						tt_value = tt_value.subs(SympySymbol("_time_"), 0)
	#
	# 				elif t_species.value.getFinalMathFormula() is not None:
	# 					tt_value =  t_species.getMathValue().getFinalMathFormula()
	# 					if t_species.isConcentration():
	# 						tt_value /= t_species.getCompartment().symbol.getFinalMathFormula()
	#
	#
	# 				# Building law and total value
	# 				if tt_res == SympyInteger(1):
	# 					t_law += tt_symbol
	# 					t_value += tt_value
	#
	# 				elif tt_res == SympyInteger(-1):
	# 					t_law -= tt_symbol
	# 					t_value -= tt_value
	#
	# 				else:
	# 					t_law += tt_res * tt_symbol
	# 					t_value += tt_res * tt_value
	#
	# 			if t_law.func == SympyAdd:
	# 				# print "New fast conservation law : %s" % str(SympyEqual(t_law, t_value))
	# 				self.fastConservationLaws.append(SympyEqual(t_law, t_value))
	#
	#
	# 		self.buildODEs(including_fast_reactions=False)
	#
	# 		t_ode_vars = [ode_var.getFinalMathFormula() for ode_var in self.ODE_vars]
	# 		# print t_ode_vars
	# 		# print self.fastLaws_vars
	# 		variables_fast_only = list(set(self.fastLaws_vars) - set(t_ode_vars))
	# 		variables_mixtes = list(set(self.fastLaws_vars).intersection(set(t_ode_vars)))
	#
	# 		# print "Mixed variables : %s" % str(variables_mixtes)
	# 		# print "Fast variables : %s" % str(variables_fast_only)
	#
	# 		for fast_law in self.fastLaws:
	# 			t_dae = MathFormula(self)
	# 			t_dae.setFinalMathFormula(fast_law)
	# 			self.DAEs.append(t_dae)
	#
	# 		for dae_var in variables_fast_only:
	# 			t_dae_var = MathFormula(self, MathFormula.MATH_VARIABLE)
	# 			t_dae_var.setFinalMathFormula(dae_var)
	# 			self.DAE_vars.append(t_dae_var)
	# 			self.DAE_symbols.append(t_dae_var)
	#
	# 			t_var = self.listOfVariables[str(t_dae_var.getInternalMathFormula())]
	# 			self.listOfVariables.changeVariableType(t_var, MathVariable.VAR_DAE)
	#
	# 		self.DAE_vars = list(set(self.DAE_vars))
	# 		self.DAE_symbols = list(set(self.DAE_symbols))
	#
	# 		t_fast_cons_laws = [law for law in self.fastConservationLaws]
	# 		t_fast_vars = [var for var in self.fastLaws_vars]
	# 		# print "Fast conservation law, checking initial conditions"
	# 		# print t_fast_cons_laws
	# 		# print t_fast_vars
	# 		# (ss,vv)= self.loadKnownInitialValues(t_fast_cons_laws, t_fast_vars, force=True)
	# 		# if len(ss) > 0:
	#
	# 		containsBoundaryConditions = False
	# 		for var in variables_mixtes:
	# 			t_var = self.listOfVariables[str(var.func)]
	# 			# print "mixed : " + t_var.getSbmlId()
	# 			if t_var.isSpecies() and t_var.boundaryCondition:
	# 				containsBoundaryConditions = True
	# 				break
	#
	# 		# print containsBoundaryConditions
	# 		if not containsBoundaryConditions:
	#
	# 			f_vars = [dae for dae in self.fastLaws_vars]
	# 			f_system = [SympyEqual(dae.getFinalMathFormula(), MathFormula.ZERO) for i, dae in enumerate(self.DAEs)]
	# 			f_system += self.fastConservationLaws
	#
	#
	# 			if len(f_system) > 0:
	# 				(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, exclude_list=f_vars, force=True)
	# 				solved_variables = self.solveSystem(f_system, f_vars)
	#
	# 				self.saveFoundInitialValues(solved_variables)
	#
	# 		else:
	# 			f_vars = [dae for dae in self.fastLaws_vars]
	# 			f_system = [SympyEqual(dae.getFinalMathFormula(), MathFormula.ZERO) for i, dae in enumerate(self.DAEs)]
	# 			# f_system += self.fastConservationLaws
	#
	#
	# 			if len(f_system) > 0:
	# 				(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, exclude_list=variables_fast_only, force=True)
	# 				solved_variables = self.solveSystem(f_system, variables_fast_only)
	#
	# 				self.saveFoundInitialValues(solved_variables)
	#
	#
	#
	# 		print "\n> Fist we solve the value of the mixed variables in the fast system"
	#
	# 		system = [SympyEqual(diff(law,MathFormula.t), SympyInteger(0)) for law in self.fastLaws]
	# 		variables = [diff(var,MathFormula.t) for var in self.fastLaws_vars]
	# 		# unknowns = [diff(var, MathFormula.t) for var in variables_fast_only]
	#
	#
	#
	# 		# Then we remove the fast variables from the conservation laws
	# 		t_der_cons = []
	# 		t_der_cons_vars = []
	# 		for i, law in enumerate(self.LHSs_v2):
	#
	# 			containsFastSubsystem = True
	#
	# 			for var in self.DAE_vars:
	# 				if not (var.getFinalMathFormula() in law.getFinalMathFormula().atoms(SympyFunction)):
	# 					containsFastSubsystem = False
	#
	# 			if containsFastSubsystem:
	#
	# 				t_der_cons_law = SympyEqual(
	# 					diff(law.getFinalMathFormula(), MathFormula.t),
	# 					MathFormula.ZERO)
	#
	# 				t_der_cons.append(t_der_cons_law)
	#
	#
	# 		f_der_mixed = [diff(var, MathFormula.t) for var in variables_mixtes]
	#
	# 		system += t_der_cons
	# 		variables += f_der_mixed
	# 		variables = list(set(variables))
	# 		der_vars = [ode.getFinalMathFormula() for ode in self.ODE_der_vars]
	# 		dae_vars = [ode for ode in self.fastLaws_vars]
	#
	# 		# print system
	# 		# print variables
	# 		# (system, f_vars) = self.loadKnownInitialValues(system, variables, exclude_list=(der_vars+dae_vars))
	# 		# print system
	# 		# print variables
	#
	# 		fixed_fast_systen = False
	#
	# 		if len(system) > 0:
	# 			solved_variables = self.solveSystem(system, variables)
	#
	# 			# print solved_variables
	# 			der_vars = [ode.getFinalMathFormula() for ode in self.ODE_der_vars]
	# 			der_mixtes = [diff(var, MathFormula.t) for var in variables_mixtes]
	#
	# 			subs = {}
	# 			for i, var in enumerate(self.ODEs):
	# 				# if self.ODE_der_vars[i].getFinalMathFormula() not in der_mixtes:
	# 					subs.update({self.ODE_der_vars[i].getFinalMathFormula():var.getFinalMathFormula()})
	#
	# 			# print subs
	#
	# 			for variable, formula in solved_variables.items():
	#
	# 				t_formula = MathFormula(self)
	# 				t_formula.setFinalMathFormula(simplify(formula.subs(subs)))
	#
	# 				t_variable = MathFormula(self)
	# 				t_variable.setFinalMathFormula(variable)
	#
	# 				if variable in der_vars:
	# 					t_index = der_vars.index(variable)
	# 					t_var = self.listOfVariables[str(self.ODE_vars[t_index].getInternalMathFormula())]
	#
	# 					if not (t_var.isSpecies() and t_var.boundaryCondition):
	# 						self.ODEs[t_index] = t_formula
	#
	# 		# else:
	# 		#     fixed_fast_systen = True
	# 		#     solved_variables = {}
	# 		#     for var in unknowns:
	# 		#         solved_variables.update({var: SympyInteger(0)})
	#

	#
	# def loadKnownInitialValues(self, f_system, f_vars, exclude_list=[], force=False):
	#
	# 	valued_system = f_system
	# 	remaining_vars = f_vars
	#
	# 	# Substituing known values
	# 	# We should probably rewrite that and make one big subs call
	# 	for i_variable, variable in enumerate(self.listOfVariables.values()):
	#
	# 		t_symbol = variable.symbol.getFinalMathFormula()
	# 		t_symbol_derivative = diff(t_symbol, MathFormula.t)
	# 		t_symbol_meanwhile = SympySymbol("_etpendantcetempsla_")
	# 		t_value = None
	#
	# 		if not variable.isReaction() and variable.hasInitialAssignment():
	# 			t_value = variable.hasInitialAssignmentBy().getDefinition().getFinalMathFormula()
	#
	# 		elif not variable.isReaction() and variable.isAssignmentRuled():
	# 			t_value = variable.isRuledBy().getDefinition().getFinalMathFormula()
	#
	# 		elif not variable.isReaction() and variable.isInitialized and t_symbol not in exclude_list:
	# 			t_value = variable.value.getFinalMathFormula()
	#
	# 		elif force and t_symbol not in exclude_list:
	# 			t_value = SympyInteger(1)
	#
	#
	# 		if t_value is not None:
	#
	# 			t_valued_system = []
	# 			for equ in valued_system:
	#
	# 				if not isinstance(equ, bool):
	# 					t_equ = equ.subs({t_symbol_derivative: t_symbol_meanwhile, t_symbol: t_value, t_symbol_meanwhile: t_symbol_derivative})
	#
	# 					if t_equ != True:
	# 						t_valued_system.append(t_equ)
	#
	# 				else:
	# 					t_valued_system.append(equ)
	#
	# 			valued_system = t_valued_system
	#
	# 			if remaining_vars != [] and t_symbol in remaining_vars:
	# 				remaining_vars.remove(t_symbol)
	#
	# 	return (valued_system, remaining_vars)
	#
	#
	# def saveFoundInitialValues(self, solved_initial_conditions):
	#
	# 	for var, value in solved_initial_conditions.items():
	# 		# print var
	# 		for variable in self.listOfVariables.values():
	# 			# print "-" + str(variable.symbol.getFinalMathFormula())
	# 			if var == variable.symbol.getFinalMathFormula():
	# 				# print "initialization = %g" % value
	# 				variable.value.setFinalMathFormula(value)
	# 				variable.isInitialized = True
	#
	# 			elif var == variable.symbol.getInternalMathFormulaDerivative():
	# 				variable.derivative_value.setFinalMathFormula(value)
	# 				variable.isDerivativeInitialized = True
	#
	#
	# def solveSystem(self, system, variables):
	#
	# 	if Settings.verbose >= 1:
	#
	# 		print "\n\n> Calling solver with DAEs only : "
	# 		print ">> System : "
	# 		for equ in system:
	# 			print ">>> " + str(equ)
	#
	# 		print ">> Solve for : " + str(variables)
	#
	#
	# 	res = solve(system,variables)
	#
	# 	if Settings.verbose >= 1:
	# 		print ">> Result : %s\n\n" % str(res)
	#
	# 	solved_initial_conditions = {}
	#
	#
	# 	if res is not True and len(res) > 0:
	# 		if isinstance(res, dict):
	# 			for var, value in res.items():
	# 				solved_initial_conditions.update({var:value})
	#
	# 		elif isinstance(res[0], dict):
	# 			for var, value in res[0].items():
	# 				solved_initial_conditions.update({var:value})
	#
	# 		else:
	# 			for i_var, var in enumerate(variables):
	# 				value = res[0][i_var]
	# 				solved_initial_conditions.update({var:value})
	#
	# 	return solved_initial_conditions
	#
	#
	# def checkInitialValues(self):
	#
	#
	# 	t_daes = [SympyEqual(dae.getFinalMathFormula(), SympyInteger(0)) for dae in self.DAEs]
	# 	f_system = t_daes
	# 	f_vars = [t_symbol.getFinalMathFormula() for t_symbol in self.DAE_symbols]
	# 	f_vars = list(set(f_vars))
	# 	# print self.DAE_symbols
	# 	# print f_system
	# 	# print f_vars
	#
	# 	(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, force=True)
	#
	# 	# print f_system
	# 	# print f_vars
	#
	# 	if False in f_system:
	# 		f_system = t_daes
	# 		f_vars = [t_symbol.getFinalMathFormula() for t_symbol in self.DAE_symbols]
	# 		f_vars = list(set(f_vars))
	#
	# 		# print f_system
	# 		# print f_vars
	# 		dae_vars = [var.symbol.getInternalMathFormula() for var in self.listOfVariables.values() if var.isAlgebraic()]
	# 		# print dae_vars
	# 		(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, dae_vars)
	#
	# 		# print f_system
	# 		# print f_vars
	# 		solved_initial_conditions = self.solveSystem(f_system, f_vars)
	# 		self.saveFoundInitialValues(solved_initial_conditions)

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
