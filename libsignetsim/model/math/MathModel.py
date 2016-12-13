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


from libsignetsim.cwriter.CModelWriter import CModelWriter
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathEquation import MathEquation
from libsignetsim.model.math.MathODEs import MathODEs
from libsignetsim.model.math.sympy_shortcuts import  (
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
from libsignetsim.model.math.MathCFEs import MathCFEs
from libsignetsim.model.math.MathDAEs import MathDAEs

from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.MathConservationLaws import MathConservationLaws
from libsignetsim.model.math.MathJacobianMatrix import MathJacobianMatrix
from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.model.Variable import Variable
from sympy import simplify, diff, solve, zeros
from time import time

class MathModel(CModelWriter, MathODEs, MathCFEs, MathDAEs,
					MathConservationLaws, MathJacobianMatrix,
					MathStoichiometryMatrix):
	""" Sbml model class """

	def __init__ (self, obj_id=0):
		""" Constructor of model class """

		CModelWriter.__init__(self, obj_id)
		MathODEs.__init__(self)
		MathCFEs.__init__(self)
		MathDAEs.__init__(self)
		MathConservationLaws.__init__(self)
		MathJacobianMatrix.__init__(self)
		MathStoichiometryMatrix.__init__(self)

		self.listOfFinalVariables = ListOfVariables(self)

		self.nbOdes = None
		self.nbAssignments = None
		self.nbConstants = None
		self.nbAlgebraics = None

		self.variablesOdes = None
		self.variablesAssignment = None
		self.variablesConstant = None
		self.variablesAlgebraic = None
		self.__upToDate = False

		self.stoichiometryMatrix = None


	def isUpToDate(self):
		return self.__upToDate

	def setUpToDate(self, value):
		self.__upToDate = value

	def buildModel(self, vars_to_keep=[], dont_reduce=False):

		t0 = time()
		self.buildCFE()
		self.buildODEs()
		if self.listOfRules.hasAlgebraicRule():

			self.hasDAEs = True
			self.buildDAEs()
			self.checkInitialValues()
			# print "Initial values checked"



		# print self.listOfSpecies.hasBoundaryConditions()
		# print dont_reduce

		if self.listOfReactions.hasFastReaction():
			self.buildSlowSubstem()

		elif (len(self.listOfEvents) == 0 and len(self.listOfReactions) > 0
			and not self.listOfSpecies.hasBoundaryConditions()
			and not dont_reduce):

			t1 = time()

			self.buildStoichiometryMatrix()

			t1a = time()
			if Settings.verbose:
				print "> Stoichiometry matrix built (%.2gs)" % (t1a-t1)

			self.findConservationLaws()

			t2 = time()
			if Settings.verbose:
				print "> Conservation laws found (%.2gs)" % (t2-t1a)


			# print vars_to_keep
			self.buildReducedSystem(vars_to_keep=vars_to_keep)
			self.developODEs()
			if Settings.verbose:
				print "> Model reduced (%.2gs)" % (time()-t2)

#        self.buildJacobianMatrix()
		# self.printSystem()
		t1 = time()
		if Settings.verbose:
			print "> Model built (%.2gs)" % (t1-t0)

	def printSystem(self):

		print "\n> Full system : "

		self.printCFEs()
		self.printODEs()
		self.printDAEs()
		self.printConservationLaws()

		print "-----------------------------"

	def buildSlowSubstem(self):

		self.fastLaws = []
		self.fastLaws_vars = []
		self.fastStoichiometryMatrix = None
		self.fastConservationLaws = []


		for reaction in self.listOfReactions.values():
			if reaction.fast:
				self.fastLaws.append(reaction.kineticLaw.getFinalMathFormula())

				for reactant in reaction.listOfReactants.values():
					self.fastLaws_vars.append(reactant.getSpecies().symbol.getFinalMathFormula())

				for product in reaction.listOfProducts.values():
					self.fastLaws_vars.append(product.getSpecies().symbol.getFinalMathFormula())

				t_sto_matrix = reaction.getStoichiometryMatrix_v2()

				for t_stoi_reaction in t_sto_matrix:
					t_reaction = zeros(1,len(self.listOfSpecies))
					for j, t_formula in enumerate(t_stoi_reaction):

						t_reaction[j] = t_formula.getDeveloppedInternalMathFormula()

					if self.fastStoichiometryMatrix is None:
						self.fastStoichiometryMatrix = t_reaction
					else:
						self.fastStoichiometryMatrix = self.fastStoichiometryMatrix.col_join(t_reaction)



		if len(self.fastLaws) > 0:

			for i, t_res in enumerate(self.fastStoichiometryMatrix.nullspace()):

				t_law = MathFormula.ZERO
				t_value = MathFormula.ZERO
				t_vars = []

				for ii, tt_res in enumerate(t_res):

					t_species = self.listOfSpecies.values()[ii]

					# Getting symbol
					tt_symbol = t_species.symbol.getFinalMathFormula()
					if t_species.isConcentration():
						tt_symbol /= t_species.getCompartment().symbol.getFinalMathFormula()


					# Getting value
					if t_species.hasInitialAssignment():
						tt_value = t_species.hasInitialAssignmentBy().getExpressionMath().getFinalMathFormula()

						for tt_species in self.listOfSpecies.values():
							ttt_symbol = tt_species.symbol.getFinalMathFormula()
							ttt_value = tt_species.value.getFinalMathFormula()
							if ttt_symbol in tt_value.atoms(SympySymbol) and ttt_value is not None:
								tt_value = tt_value.subs(ttt_symbol, ttt_value)

						if t_species.isConcentration():
							tt_value /= t_species.getCompartment().symbol.getFinalMathFormula()

						if SympySymbol("_time_") in tt_value.atoms():
							tt_value = tt_value.subs(SympySymbol("_time_"), 0)

					elif t_species.value.getFinalMathFormula() is not None:
						tt_value =  t_species.getMathValue().getFinalMathFormula()
						if t_species.isConcentration():
							tt_value /= t_species.getCompartment().symbol.getFinalMathFormula()


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
					# print "New fast conservation law : %s" % str(SympyEqual(t_law, t_value))
					self.fastConservationLaws.append(SympyEqual(t_law, t_value))


			self.buildODEs(including_fast_reactions=False)

			t_ode_vars = [ode_var.getFinalMathFormula() for ode_var in self.ODE_vars]
			# print t_ode_vars
			# print self.fastLaws_vars
			variables_fast_only = list(set(self.fastLaws_vars) - set(t_ode_vars))
			variables_mixtes = list(set(self.fastLaws_vars).intersection(set(t_ode_vars)))

			# print "Mixed variables : %s" % str(variables_mixtes)
			# print "Fast variables : %s" % str(variables_fast_only)

			for fast_law in self.fastLaws:
				t_dae = MathFormula(self)
				t_dae.setFinalMathFormula(fast_law)
				self.DAEs.append(t_dae)

			for dae_var in variables_fast_only:
				t_dae_var = MathFormula(self, MathFormula.MATH_VARIABLE)
				t_dae_var.setFinalMathFormula(dae_var)
				self.DAE_vars.append(t_dae_var)
				self.DAE_symbols.append(t_dae_var)

				t_var = self.listOfVariables[str(t_dae_var.getInternalMathFormula())]
				self.listOfVariables.changeVariableType(t_var, MathVariable.VAR_DAE)

			self.DAE_vars = list(set(self.DAE_vars))
			self.DAE_symbols = list(set(self.DAE_symbols))

			t_fast_cons_laws = [law for law in self.fastConservationLaws]
			t_fast_vars = [var for var in self.fastLaws_vars]
			# print "Fast conservation law, checking initial conditions"
			# print t_fast_cons_laws
			# print t_fast_vars
			# (ss,vv)= self.loadKnownInitialValues(t_fast_cons_laws, t_fast_vars, force=True)
			# if len(ss) > 0:

			containsBoundaryConditions = False
			for var in variables_mixtes:
				t_var = self.listOfVariables[str(var.func)]
				# print "mixed : " + t_var.getSbmlId()
				if t_var.isSpecies() and t_var.boundaryCondition:
					containsBoundaryConditions = True
					break

			# print containsBoundaryConditions
			if not containsBoundaryConditions:

				f_vars = [dae for dae in self.fastLaws_vars]
				f_system = [SympyEqual(dae.getFinalMathFormula(), MathFormula.ZERO) for i, dae in enumerate(self.DAEs)]
				f_system += self.fastConservationLaws


				if len(f_system) > 0:
					(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, exclude_list=f_vars, force=True)
					solved_variables = self.solveSystem(f_system, f_vars)

					self.saveFoundInitialValues(solved_variables)

			else:
				f_vars = [dae for dae in self.fastLaws_vars]
				f_system = [SympyEqual(dae.getFinalMathFormula(), MathFormula.ZERO) for i, dae in enumerate(self.DAEs)]
				# f_system += self.fastConservationLaws


				if len(f_system) > 0:
					(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, exclude_list=variables_fast_only, force=True)
					solved_variables = self.solveSystem(f_system, variables_fast_only)

					self.saveFoundInitialValues(solved_variables)



			print "\n> Fist we solve the value of the mixed variables in the fast system"

			system = [SympyEqual(diff(law,MathFormula.t), SympyInteger(0)) for law in self.fastLaws]
			variables = [diff(var,MathFormula.t) for var in self.fastLaws_vars]
			# unknowns = [diff(var, MathFormula.t) for var in variables_fast_only]



			# Then we remove the fast variables from the conservation laws
			t_der_cons = []
			t_der_cons_vars = []
			for i, law in enumerate(self.LHSs_v2):

				containsFastSubsystem = True

				for var in self.DAE_vars:
					if not (var.getFinalMathFormula() in law.getFinalMathFormula().atoms(SympyFunction)):
						containsFastSubsystem = False

				if containsFastSubsystem:

					t_der_cons_law = SympyEqual(
						diff(law.getFinalMathFormula(), MathFormula.t),
						MathFormula.ZERO)

					t_der_cons.append(t_der_cons_law)


			f_der_mixed = [diff(var, MathFormula.t) for var in variables_mixtes]

			system += t_der_cons
			variables += f_der_mixed
			variables = list(set(variables))
			der_vars = [ode.getFinalMathFormula() for ode in self.ODE_der_vars]
			dae_vars = [ode for ode in self.fastLaws_vars]

			# print system
			# print variables
			# (system, f_vars) = self.loadKnownInitialValues(system, variables, exclude_list=(der_vars+dae_vars))
			# print system
			# print variables

			fixed_fast_systen = False

			if len(system) > 0:
				solved_variables = self.solveSystem(system, variables)

				# print solved_variables
				der_vars = [ode.getFinalMathFormula() for ode in self.ODE_der_vars]
				der_mixtes = [diff(var, MathFormula.t) for var in variables_mixtes]

				subs = {}
				for i, var in enumerate(self.ODEs):
					# if self.ODE_der_vars[i].getFinalMathFormula() not in der_mixtes:
						subs.update({self.ODE_der_vars[i].getFinalMathFormula():var.getFinalMathFormula()})

				# print subs

				for variable, formula in solved_variables.items():

					t_formula = MathFormula(self)
					t_formula.setFinalMathFormula(simplify(formula.subs(subs)))

					t_variable = MathFormula(self)
					t_variable.setFinalMathFormula(variable)

					if variable in der_vars:
						t_index = der_vars.index(variable)
						t_var = self.listOfVariables[str(self.ODE_vars[t_index].getInternalMathFormula())]

						if not (t_var.isSpecies() and t_var.boundaryCondition):
							self.ODEs[t_index] = t_formula

			# else:
			#     fixed_fast_systen = True
			#     solved_variables = {}
			#     for var in unknowns:
			#         solved_variables.update({var: SympyInteger(0)})



	def loadKnownInitialValues(self, f_system, f_vars, exclude_list=[], force=False):

		valued_system = f_system
		remaining_vars = f_vars

		# Substituing known values
		# We should probably rewrite that and make one big subs call
		for i_variable, variable in enumerate(self.listOfVariables.values()):

			t_symbol = variable.symbol.getFinalMathFormula()
			t_symbol_derivative = diff(t_symbol, MathFormula.t)
			t_symbol_meanwhile = SympySymbol("_etpendantcetempsla_")
			t_value = None

			if not variable.isReaction() and variable.hasInitialAssignment():
				t_value = variable.hasInitialAssignmentBy().definition.getFinalMathFormula()

			elif not variable.isReaction() and variable.isAssignmentRuled():
				t_value = variable.isRuledBy().definition.getFinalMathFormula()

			elif not variable.isReaction() and variable.isInitialized and t_symbol not in exclude_list:
				t_value = variable.value.getFinalMathFormula()

			elif force and t_symbol not in exclude_list:
				t_value = SympyInteger(1)


			if t_value is not None:

				t_valued_system = []
				for equ in valued_system:

					if not isinstance(equ, bool):
						t_equ = equ.subs({t_symbol_derivative: t_symbol_meanwhile, t_symbol: t_value, t_symbol_meanwhile: t_symbol_derivative})

						if t_equ != True:
							t_valued_system.append(t_equ)

					else:
						t_valued_system.append(equ)

				valued_system = t_valued_system

				if remaining_vars != [] and t_symbol in remaining_vars:
					remaining_vars.remove(t_symbol)

		return (valued_system, remaining_vars)


	def saveFoundInitialValues(self, solved_initial_conditions):

		for var, value in solved_initial_conditions.items():
			# print var
			for variable in self.listOfVariables.values():
				# print "-" + str(variable.symbol.getFinalMathFormula())
				if var == variable.symbol.getFinalMathFormula():
					# print "initialization = %g" % value
					variable.value.setFinalMathFormula(value)
					variable.isInitialized = True

				elif var == variable.symbol.getInternalMathFormulaDerivative():
					variable.derivative_value.setFinalMathFormula(value)
					variable.isDerivativeInitialized = True


	def solveSystem(self, system, variables):

		print "\n\n> Calling solver with DAEs only : "
		print ">> System : "
		for equ in system:
			print ">>> " + str(equ)

		print ">> Solve for : " + str(variables)


		res = solve(system,variables)
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


	def checkInitialValues(self):


		t_daes = [SympyEqual(dae.getFinalMathFormula(), SympyInteger(0)) for dae in self.DAEs]
		f_system = t_daes
		f_vars = [t_symbol.getFinalMathFormula() for t_symbol in self.DAE_symbols]
		f_vars = list(set(f_vars))

		(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, force=True)

		if False in f_system:
			f_system = t_daes
			f_vars = [t_symbol.getFinalMathFormula() for t_symbol in self.DAE_symbols]
			f_vars = list(set(f_vars))

			(f_system, f_vars) = self.loadKnownInitialValues(f_system, f_vars, self.DAE_vars)
			solved_initial_conditions = self.solveSystem(f_system, f_vars)
			self.saveFoundInitialValues(solved_initial_conditions)


	def buildReducedSystem(self, vars_to_keep=[]):

		reduced_odes = []
		reduced_odes_vars = []
		reduced_odes_der_vars = []
		reduced_odes_symbols = []

		self.findReducibleVariables(vars_to_keep=vars_to_keep)

		# print self.reducibleVariables
		t_reducible_vars = [var for var in self.reducibleVariables.keys()]
		t_reducible_values = [var for var in self.reducibleVariables.values()]

		if len(self.reducibleVariables) > 0:

			for i, ode_var in enumerate(self.ODE_vars):
				if ode_var.getInternalMathFormula() in t_reducible_vars:

					t_cfe = t_reducible_values[t_reducible_vars.index(ode_var.getInternalMathFormula())]
					t_formula = MathFormula(self)
					t_formula.setInternalMathFormula(t_cfe)
					self.CFEs.append(t_formula)

					self.CFE_vars.append(ode_var)
					self.CFE_types.append(MathCFEs.SOLVED)

					#Now changing the variable type
					t_var = self.listOfVariables[str(ode_var.getInternalMathFormula())]
					self.listOfVariables.changeVariableType(t_var, Variable.VAR_ASS)

				else:
					reduced_odes.append(self.ODEs[i])
					reduced_odes_vars.append(ode_var)
					reduced_odes_der_vars.append(self.ODE_der_vars[i])
					reduced_odes_symbols.append(self.ODE_symbols[i])

			self.ODEs = reduced_odes
			self.ODE_vars = reduced_odes_vars
			self.ODE_der_vars = reduced_odes_der_vars
			self.ODE_symbols = reduced_odes_symbols

			self.developCFEs()
