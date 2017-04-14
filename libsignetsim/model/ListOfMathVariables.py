#!/usr/bin/env python
""" ListOfMathVariables.py


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


# from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathVariable import MathVariable
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

class ListOfMathVariables(object):

	def __init__ (self, model):


		self.__model = model

		self.amountsToConcentrations = None
		self.concentrationsToAmounts = None

		self.internalToFinal = None
		self.finalToInternal = None

		self.internalToFinalWithConcentrations = None
		self.finalWithConcentrationsToInternal = None

	def isUpToDate(self):
		return self.__upToDate


	def removeMathVariable(self, variable):

		if variable.isDerivative():
			self.__model.variablesOdes.remove(variable)
			self.__model.nbOdes -= 1

		elif variable.isAssignment():
			self.__model.variablesAssignment.remove(variable)
			self.__model.nbAssignments -= 1

		elif variable.isConstant():
			self.__model.variablesConstant.remove(variable)
			self.__model.nbConstants -= 1

		elif variable.isAlgebraic():
			self.__model.variablesAlgebraic.remove(variable)
			self.__model.nbAlgebraics -= 1


	def classifyVariables(self):

		# print ">> Starting to classify variables"
		i_variables_constant = 0
		i_variables_assignment = 0
		i_variables_odes = 0
		i_variables_algebraics = 0

		variables_odes = []
		variables_assignment = []
		variables_constant = []
		variables_algebraic = []

		for variable in self.values():

			if variable.isReaction() or variable.isAssignmentRuled():
				# print "Assignment variable detected : %s" % variable.getSbmlId()
				variable.type = MathVariable.VAR_ASS
				variable.ind = i_variables_assignment
				variables_assignment.append(variable)
				i_variables_assignment+=1


			elif (variable.constant
					or (variable.isSpecies() and not variable.isRuled() and not variable.isInAlgebraicRules() and not variable.isInReactions(including_fast_reactions=True))
					or ((variable.isParameter() or variable.isCompartment() or variable.isStoichiometry()) and not variable.isRuled() and not variable.isInAlgebraicRules())
					or (self.__model.sbmlLevel == 1 and variable.isCompartment() and not variable.isRuled() and not variable.isInAlgebraicRules())
					or (self.__model.sbmlLevel == 1 and variable.isParameter() and not variable.isRuled() and not variable.isInAlgebraicRules())
				):
				# print "Constant variable detected : %s (%d)" % (variable.getSbmlId(), i_variables_constant)
				variable.type = MathVariable.VAR_CST
				variable.ind = i_variables_constant
				variables_constant.append(variable)
				i_variables_constant += 1


			elif not (variable.isRuled() or (variable.isSpecies() and variable.isInReactions())) and variable.isInAlgebraicRules():
				# print "Algebraic variable detected : %s" % variable.getSbmlId()
				variable.type = MathVariable.VAR_DAE
				variable.ind = i_variables_algebraics
				variables_algebraic.append(variable)
				i_variables_algebraics += 1

			else:
				# print "Derivative variable detected : %s" % variable.getSbmlId()
				variable.type = MathVariable.VAR_ODE
				variable.ind = i_variables_odes
				variables_odes.append(variable)
				i_variables_odes += 1


		self.__model.nbOdes = i_variables_odes
		self.__model.nbAssignments = i_variables_assignment
		self.__model.nbConstants = i_variables_constant
		self.__model.nbAlgebraics = i_variables_algebraics

		self.__model.variablesOdes = variables_odes
		self.__model.variablesAssignment = variables_assignment
		self.__model.variablesConstant = variables_constant
		self.__model.variablesAlgebraic = variables_algebraic

		self.__model.setUpToDate(True)
		# print ">> Done classifying variables"

	def changeVariableType(self, variable, new_type):

		# print "Changing variable %s to type %d" % (str(variable.symbol.getInternalMathFormula), new_type)

		if variable.isDerivative():
			self.__model.variablesOdes.remove(variable)
			self.__model.nbOdes -= 1

		elif variable.isAssignment():
			self.__model.variablesAssignment.remove(variable)
			self.__model.nbAssignments -= 1

		elif variable.isConstant():
			self.__model.variablesConstant.remove(variable)
			self.__model.nbConstants -= 1

		elif variable.isAlgebraic():
			self.__model.variablesAlgebraic.remove(variable)
			self.__model.nbAlgebraics -= 1


		if new_type == MathVariable.VAR_ODE:
			self.__model.variablesOdes.append(variable)
			self.__model.nbOdes += 1

		elif new_type == MathVariable.VAR_ASS:
			self.__model.variablesAssignment.append(variable)
			self.__model.nbAssignments += 1

		elif new_type == MathVariable.VAR_CST:
			self.__model.variablesConstant.append(variable)
			self.__model.nbConstants += 1

		elif new_type == MathVariable.VAR_DAE:
			self.__model.variablesAlgebraic.append(variable)
			self.__model.nbAlgebraics += 1

		variable.type = new_type

		for i, var in enumerate(self.__model.variablesOdes):
			var.ind = i
		for i, var in enumerate(self.__model.variablesConstant):
			var.ind = i
		for i, var in enumerate(self.__model.variablesAssignment):
			var.ind = i
		for i, var in enumerate(self.__model.variablesAlgebraic):
			var.ind = i



	def getInternalToFinal(self, forcedConcentration=False):
		"""
			Here is's kinda weird. We still cannot pickle Sympy functions
			so we can't save one within the model object.
			So this function will only be called on a "as needed" basis

		"""


		if forcedConcentration:

			if self.internalToFinalWithConcentrations is None:
				self.internalToFinalWithConcentrations = {}
				for var in self.values():
					if var.isDerivative() or var.isAssignment():
						t_symbol = var.symbol.getInternalMathFormula()
						# if var.isConcentration():
						#     t_function = SympyFunction("[%s]" % str(t_symbol))(MathFormula.t)
						# else:
						t_function = SympyFunction(str(t_symbol))(MathFormula.t)

						self.internalToFinalWithConcentrations.update({t_symbol: t_function})

			return self.internalToFinalWithConcentrations

		elif self.internalToFinal is None:

			self.internalToFinal = {}
			for var in self.values():
				if var.isDerivative() or var.isAssignment():
					t_symbol = var.symbol.getInternalMathFormula()
					t_function = SympyFunction(str(t_symbol))(MathFormula.t)
					self.internalToFinal.update({t_symbol: t_function})

		return self.internalToFinal

	def getFinalToInternal(self, forcedConcentration=False):
		"""
			Here is's kinda weird. We still cannot pickle Sympy functions
			so we can't save one within the model object.
			So this function will only be called on a "as needed" basis

		"""

		if forcedConcentration:
			if self.finalWithConcentrationsToInternal is None:

				self.finalWithConcentrationsToInternal = {}
				for var in self.values():
					if var.isDerivative() or var.isAssignment():
						t_symbol = var.symbol.getInternalMathFormula()
						# if var.isConcentration():
						#     t_function = SympyFunction("[%s]" % str(t_symbol))(MathFormula.t)
						# else:
						t_function = SympyFunction(str(t_symbol))(MathFormula.t)

						self.finalWithConcentrationsToInternal.update({t_function: t_symbol})

			return self.finalWithConcentrationsToInternal


		elif self.finalToInternal is None:

			self.finalToInternal = {}
			for var in self.values():
				if var.isDerivative() or var.isAssignment():
					t_symbol = var.symbol.getInternalMathFormula()
					t_function = SympyFunction(str(t_symbol))(MathFormula.t)
					self.finalToInternal.update({t_function: t_symbol})

		return self.finalToInternal

	def cleanFinal(self):

		self.finalToInternal = None
		self.internalToFinal = None
		self.finalWithConcentrationsToInternal = None
		self.internalToFinalWithConcentrations = None


	def getAmountsToConcentrations(self):

		if self.amountsToConcentrations is None:
			self.buildAmountsConcentrationsSubs()

		return self.amountsToConcentrations


	def getConcentrationsToAmounts(self):

		"""
			Building the dict for concentrations to amounts substitutions

			Basically just having key:value = species/compartment:species

		"""
		if self.concentrationsToAmounts is None:
			self.buildAmountsConcentrationsSubs()

		return self.concentrationsToAmounts


	def buildAmountsConcentrationsSubs(self):

		self.amountsToConcentrations = {}
		self.concentrationsToAmounts = {}
		for var in self.values():
			if var.isSpecies() and not var.hasOnlySubstanceUnits:
				t_symbol_concentration = var.symbol.getInternalMathFormula()
				t_symbol_amount = var.symbol.getInternalMathFormula(forcedConcentration=True)

				self.amountsToConcentrations.update({t_symbol_amount: t_symbol_concentration})
				self.concentrationsToAmounts.update({t_symbol_concentration: t_symbol_amount})
