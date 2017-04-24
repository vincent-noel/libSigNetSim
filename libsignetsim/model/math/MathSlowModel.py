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

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula
from sympy import solve, zeros, srepr
from libsignetsim.model.math.sympy_shortcuts import (
	SympyInteger, SympyAdd, SympyEqual, SympySymbol, SympyRational,
	SympyStrictGreaterThan)
from libsignetsim.model.math.container.ListOfODEs import ListOfODEs
from libsignetsim.model.math.container.ListOfCFEs import ListOfCFEs
from libsignetsim.model.math.container.ListOfDAEs import ListOfDAEs
from libsignetsim.model.math.DAE import DAE
from libsignetsim.model.math.CFE import CFE
from libsignetsim.model.math.ODE import ODE
from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from libsignetsim.model.math.container.ListOfConservationLaws import ListOfConservationLaws
class MathSlowModel(object):
	""" Sbml model class """

	def __init__ (self, parent_model=None, reduced_model=None):
		""" Constructor of model class """

		# MathModel.__init__(self)
		self.parentModel = parent_model
		self.listOfODEs = ListOfODEs(self)
		self.listOfCFEs = ListOfCFEs(self)
		self.listOfDAEs = ListOfDAEs(self)
		self.listOfVariables = ListOfVariables(self)

		self.sbmlLevel = self.parentModel.sbmlLevel
		self.sbmlVersion = self.parentModel.sbmlVersion
		self.solvedInitialConditions = {}

		self.nbOdes = None
		self.nbAssignments = None
		self.nbConstants = None
		self.nbAlgebraics = None

		self.variablesOdes = None
		self.variablesAssignment = None
		self.variablesConstant = None
		self.variablesAlgebraic = None

		self.fastLaws = []
		self.fastLaws_vars = []
		self.fastStoichiometryMatrix = MathStoichiometryMatrix(self.parentModel)
		self.fastConservationLaws = []
		self.fastConservationLaws_v2 = ListOfConservationLaws(self)
		self.hasDAEs = self.parentModel.hasDAEs

		self.slow_variables = []
		self.fast_variables = []
		self.mixed_variables = []


	def copyVariables(self):
		""" Copies the listOfVariables and the solvedInitialConditions """

		# First we copy the variables list
		for variable in self.parentModel.listOfVariables.values():
			new_var = MathVariable(self)
			new_var.copy(variable)
			new_var_id = new_var.symbol.getPrettyPrintMathFormula()
			self.listOfVariables.update({new_var_id:new_var})

		# Then we copy the solved initial conditions
		for variable, value in self.parentModel.solvedInitialConditions.items():
			self.solvedInitialConditions.update({variable: value})


		self.nbOdes = self.parentModel.nbOdes
		self.nbAssignments = self.parentModel.nbAssignments
		self.nbConstants = self.parentModel.nbConstants
		self.nbAlgebraics = self.parentModel.nbAlgebraics

		self.variablesOdes = []
		for i, var_ode in enumerate(self.parentModel.variablesOdes):
			t_var = self.listOfVariables.getBySymbol(var_ode.symbol.getSymbol())
			self.variablesOdes.append(t_var)

		self.variablesAssignment = []
		for var_ass in self.parentModel.variablesAssignment:
			t_var = self.listOfVariables.getBySymbol(var_ass.symbol.getSymbol())
			self.variablesAssignment.append(t_var)

		self.variablesConstant = []
		for var_cst in self.parentModel.variablesConstant:
			t_var = self.listOfVariables.getBySymbol(var_cst.symbol.getSymbol())
			self.variablesConstant.append(t_var)

		self.variablesAlgebraic = []
		for var_alg in self.parentModel.variablesAlgebraic:
			t_var = self.listOfVariables.getBySymbol(var_alg.symbol.getSymbol())
			self.variablesAlgebraic.append(t_var)

		for cfe in self.parentModel.listOfCFEs:
			t_var = self.listOfVariables.getBySymbol(cfe.getVariable().symbol.getSymbol())
			t_cfe = CFE(self)
			t_cfe.new(t_var, cfe.getDefinition())
			self.listOfCFEs.append(t_cfe)

	def findFastReactions(self):
		""" Finds the fast reactions and build the fast stoichiometry matrix """

		for reaction in self.parentModel.listOfReactions.values():
			if reaction.fast:
				self.fastLaws.append(reaction.kineticLaw.getDefinition().getDeveloppedInternalMathFormula())

				for reactant in reaction.listOfReactants.values():
					self.fastLaws_vars.append(reactant.getSpecies().symbol.getDeveloppedInternalMathFormula())

				for product in reaction.listOfProducts.values():
					self.fastLaws_vars.append(product.getSpecies().symbol.getDeveloppedInternalMathFormula())



	def findFastConservationLaws(self):
		""" Finds the conservation laws from the fast reactions """

		for i, t_res in enumerate(self.fastStoichiometryMatrix.getSimpleStoichiometryMatrix().nullspace()):

			# print "Finding conservation law #%d\n" % i
			# print t_res
			t_law = MathFormula.ZERO
			t_value = MathFormula.ZERO
			t_vars = []

			for ii, tt_res in enumerate(t_res):

				t_species = self.parentModel.listOfSpecies.values()[ii]

				# Getting symbol
				tt_symbol = t_species.symbol.getInternalMathFormula()
				if t_species.isConcentration():
					tt_symbol /= t_species.getCompartment().symbol.getInternalMathFormula()


				# Getting value
				if t_species.hasInitialAssignment():
					tt_value = t_species.hasInitialAssignmentBy().getExpressionMath().getInternalMathFormula()

					for tt_species in self.parentModel.listOfSpecies.values():
						ttt_symbol = tt_species.symbol.getInternalMathFormula()
						ttt_value = tt_species.value.getInternalMathFormula()
						if ttt_symbol in tt_value.atoms(SympySymbol) and ttt_value is not None:
							tt_value = tt_value.subs(ttt_symbol, ttt_value)

					if t_species.isConcentration():
						tt_value /= t_species.getCompartment().symbol.getInternalMathFormula()

					if SympySymbol("_time_") in tt_value.atoms():
						tt_value = tt_value.subs(SympySymbol("_time_"), 0)

				elif t_species.value.getInternalMathFormula() is not None:
					tt_value =  t_species.getMathValue().getInternalMathFormula()
					if t_species.isConcentration():
						tt_value /= t_species.getCompartment().symbol.getInternalMathFormula()


				# Building law and total value
				if tt_res == SympyInteger(1):
					t_law += tt_symbol
					t_value += tt_value

				elif tt_res == SympyInteger(-1):
					t_law -= tt_symbol
					t_value -= tt_value

				else:
					t_law += tt_res * tt_symbol
					t_value += tt_res * tt_value

			if t_law.func == SympyAdd:
				print " >> New fast conservation law : %s" % str(SympyEqual(t_law, t_value))
				self.fastConservationLaws.append(SympyEqual(t_law, t_value))


	def fixInitialConditions(self):

		""" The fast reactions might introduce new initial values. checking,
			and fixing them if needed """

		t_fast_cons_laws = [law for law in self.fastConservationLaws]
		t_fast_vars = [var for var in self.fastLaws_vars]

		containsBoundaryConditions = False
		for var in self.mixed_variables:
			t_var = self.listOfVariables[str(var)]
			if t_var.boundaryCondition:
				containsBoundaryConditions = True
				# print "> Some mixed variables have boundaryCondition !"
				break

		subs = {}
		for var, value in self.solvedInitialConditions.items():
			# if len(value.getInternalMathFormula().atoms(SympySymbol)) > 0:

			subs.update({var: value.getInternalMathFormula()})

		if not containsBoundaryConditions:

			f_vars = [dae for dae in self.fastLaws_vars]
			f_system = [SympyEqual(law, MathFormula.ZERO) for law in self.fastLaws]
			f_system += self.fastConservationLaws

			if len(f_system) > 0:
				# print f_system

				(f_system_subs, f_vars_subs) = self.loadKnownInitialValues_v2(f_system, f_vars)

				all_true = True
				for equ in f_system_subs:
					if equ != True:
						all_true = False

				if not all_true:

					(f_system, f_vars) = self.loadKnownInitialValues_v2(f_system, f_vars, exclude_list=f_vars)

					# print f_system

					solved_variables = self.solveSystem(f_system, f_vars)

					# print "Solved initial conditions : %s" % str(solved_variables)

					for solved_variable, solved_value in solved_variables.items():
						t_var = self.listOfVariables[str(solved_variable)]
						t_value = MathFormula(self)
						t_value.setInternalMathFormula(solved_value.subs(subs))

						self.solvedInitialConditions.update({solved_variable:t_value})
				# else:
				# 	print "All true !"
		else:
			f_vars = [dae for dae in self.fastLaws_vars]
			f_system = [SympyEqual(law, MathFormula.ZERO) for law in self.fastLaws]

			if len(f_system) > 0:

				(f_system_subs, f_vars_subs) = self.loadKnownInitialValues_v2(f_system, f_vars)

				all_true = True
				for equ in f_system_subs:
					if equ != True:
						all_true = False

				if not all_true:

					(f_system, f_vars) = self.loadKnownInitialValues_v2(f_system, f_vars, exclude_list=f_vars)

					solved_variables = self.solveSystem(f_system, self.fast_variables)

					for solved_variable, solved_value in solved_variables.items():
						t_var = self.listOfVariables[str(solved_variable)]
						t_value = MathFormula(self)
						t_value.setInternalMathFormula(solved_value.subs(subs))

						self.solvedInitialConditions.update({t_var:t_value})


	def build(self):

		self.copyVariables()
		self.fastStoichiometryMatrix.build(including_slow_reactions=False)
		# print self.fastStoichiometryMatrix.getSimpleStoichiometryMatrix()
		self.fastConservationLaws_v2.build(self.fastStoichiometryMatrix)
		print self.fastConservationLaws_v2
		self.findFastReactions()

		if len(self.fastLaws) > 0:
			self.findFastConservationLaws()
			# self.listOfODEs.buildFromModel(model=self.parentModel,
			# 								including_fast_reactions=False)

			self.slow_variables = []
			for variable in self.parentModel.listOfVariables.values():
				if variable.isDerivative():

					# First we found the corresponding variable in the new list
					t_var = self.parentModel.listOfVariables[str(variable.symbol.getInternalMathFormula())]
					t_definition = variable.getODE(including_fast_reactions=False)

					if t_definition is not None:
						self.slow_variables.append(t_var.symbol.getSymbol())


			self.fast_variables = list(set(self.fastLaws_vars) - set(self.slow_variables))
			self.mixed_variables = list(set(self.fastLaws_vars).intersection(set(self.slow_variables)))

			print "\n > Slow variables : %s" % str(self.mixed_variables)
			print " > Mixed variables : %s" % str(self.mixed_variables)
			print " > Fast variables : %s" % str(self.fast_variables)

			self.fixInitialConditions()

			t_odes = zeros(1,len(self.parentModel.listOfODEs))
			t_odes_vars = zeros(1,len(self.parentModel.listOfODEs))
			for i, ode in enumerate(self.parentModel.listOfODEs):

				t_odes[i] = ode.getDefinition().getDeveloppedInternalMathFormula()
				if ode.getVariable().symbol.getInternalMathFormula() in self.fast_variables:

					t_odes_vars[i] = MathFormula.ZERO
				else:
					t_odes_vars[i] = ode.getVariable().symbol.getInternalMathFormula()


			matrix_species = zeros(1,self.parentModel.nbOdes)
			list_species = []
			for i, var in enumerate(self.parentModel.variablesOdes):
				if var.isDerivative():
					matrix_species[i] = var.symbol.getInternalMathFormula()
					list_species.append(var.symbol.getInternalMathFormula())
			# print " > matrix species :"
			# print matrix_species
			nullspace_normalized = []
			nullspace = self.fastStoichiometryMatrix.getSimpleStoichiometryMatrix().nullspace()
			# print "> stoichiometry :"
			# print self.fastStoichiometryMatrix

			# print "> nullspace :"
			# print nullspace
			for t_cons_law in nullspace:
				t_sum = SympyInteger(0)
				for element in t_cons_law:
					t_sum += element

				if SympyStrictGreaterThan(t_sum, SympyInteger(1)):
					# print t_cons_law
					t_system = [SympyEqual((matrix_species*t_cons_law)[0,0], SympyInteger(1))]
					t_system += self.fastLaws
					t_vars = self.fast_variables + self.mixed_variables
					# print '-'*25
					# print t_system
					# print t_vars

					(t_system, t_vars) = self.loadKnownInitialValues_v2(t_system, t_vars, exclude_list=t_vars)
					# print '-'*25
					# print t_system
					# print t_vars

					res = solve(t_system,t_vars)
					t_cons_law_normalized = t_cons_law
					# print "RES"
					# print res
					# print t_cons_law_normalized
					for var, value in res.items():
						# print "index of %s : %d" % (var, list_species.index(var))
						t_cons_law_normalized[list_species.index(var)] = value
					# print t_cons_law_normalized
					nullspace_normalized.append(t_cons_law_normalized)
				else:
					nullspace_normalized.append(t_cons_law)


			nullspace = nullspace_normalized



			# print nullspace
			# print "\n > Slow+Fast ODES"
			# for t_ode in t_odes:
			#  	print t_ode

			pseudo_odes = {}
			for i, pseudo_var in enumerate(nullspace):
				t_pseudo_ode = (t_odes*pseudo_var)[0,0]
				t_pseudo_variable = (t_odes_vars*pseudo_var)[0,0].atoms(SympySymbol)
				if len(t_pseudo_variable) == 1:
					pseudo_odes.update({list(t_pseudo_variable)[0]: t_pseudo_ode })

			# print "\n > Slow ODES"
			# for t_ode in pseudo_odes.values():
			#  	print t_ode


			# system = [law for law in self.fastLaws]
			# variables = [var for var in self.fast_variables]
			#
			# new_cfes = self.solveSystem(system, variables)
			#
			for pseudo_var, pseudo_ode in pseudo_odes.items():

				t_var = self.listOfVariables[str(pseudo_var)]
				t_definition = MathFormula(self)
				t_definition.setInternalMathFormula(pseudo_ode)
				t_ode = ODE(self)
				t_ode.new(t_var, t_definition)
				self.listOfODEs.append(t_ode)
			#
			#
			# for cfe_var, cfe_def in new_cfes.items():
			# 	t_var = self.listOfVariables[str(cfe_var)]
			# 	t_def = MathFormula(self)
			# 	t_def.setInternalMathFormula(cfe_def)
			# 	t_cfe = CFE(self)
			# 	t_cfe.new(t_var, t_def)
			# 	self.listOfCFEs.append(t_cfe)


			# system = [law for law in self.fastLaws]
			# variables = [var for var in self.fast_variables]
			#
			# new_cfes = self.solveSystem(system, variables)

			for law in self.fastLaws:

				# t_var = self.listOfVariables[str(pseudo_var)]
				t_definition = MathFormula(self)
				t_definition.setInternalMathFormula(law)
				t_dae = DAE(self)
				t_dae.new(t_definition)
				self.listOfDAEs.append(t_dae)

			self.hasDAEs = True
			for fast_var in self.fast_variables:
				t_var = self.listOfVariables[str(fast_var)]
				self.listOfVariables.changeVariableType(t_var, MathVariable.VAR_DAE)

			if Settings.verbose >= 2:
				self.listOfODEs.prettyPrint()

	def loadKnownInitialValues_v2(self, f_system, f_vars, exclude_list=[]):

		valued_system = f_system
		remaining_vars = f_vars

		# Substituing known values
		# We should probably rewrite that and make one big subs call
		subs = {}
		for i_variable, t_symbol in enumerate(self.solvedInitialConditions.keys()):


			# t_symbol = variable.symbol.getInternalMathFormula()

			if t_symbol not in exclude_list:
				subs.update({t_symbol: self.solvedInitialConditions[t_symbol].getInternalMathFormula()})
			# print subs
			# print "subs :"
			# print subs
			res_system = []
			for equ in f_system:
				# print "equ"
				# print equ
				# print equ.subs(subs, evaluate=False)
				res_system.append(equ.subs(subs))

		return (res_system, f_vars)


	def solveSystem(self, system, variables):

		if Settings.verbose >= 2:

			print "\n\n> Calling solver : "
			print ">> System : "
			for equ in system:
				print ">>> " + str(equ)

			print ">> Solve for : " + str(variables)


		res = solve(system,variables)

		if Settings.verbose >= 2:
			print ">> Result : %s\n\n" % str(res)

		solved_initial_conditions = {}


		if res is not True and len(res) > 0:
			if isinstance(res, dict):
				for var, value in res.items():
					solved_initial_conditions.update({var:value})

			elif isinstance(res[0], dict):
				for var, value in res[0].items():
					solved_initial_conditions.update({var:value})

			else:
				for i_var, var in enumerate(variables):
					value = res[0][i_var]
					solved_initial_conditions.update({var:value})

		return solved_initial_conditions
