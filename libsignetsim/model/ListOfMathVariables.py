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

	def __init__(self, model):


		self.__model = model

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

		for variable in self:

			if (variable.isReaction() or variable.isEvent()) or variable.isAssignmentRuled():
				# print "Assignment variable detected : %s" % variable.getSbmlId()
				variable.type = MathVariable.VAR_ASS
				variable.ind = i_variables_assignment
				variables_assignment.append(variable)
				i_variables_assignment+=1


			elif (variable.constant
					or (variable.isSpecies() and not variable.isRuled() and not variable.isInAlgebraicRules() and not variable.isInReactions(including_fast_reactions=True))
					or ((variable.isParameter() or variable.isCompartment() or variable.isStoichiometry() or variable.isConservedMoiety()) and not variable.isRuled() and not variable.isInAlgebraicRules())
					or (self.__model.sbmlLevel == 1 and variable.isCompartment() and not variable.isRuled() and not variable.isInAlgebraicRules())
					or (self.__model.sbmlLevel == 1 and variable.isParameter() and not variable.isRuled() and not variable.isInAlgebraicRules())
				):
				# print "Constant variable detected : %s (%d)" % (variable.getSbmlId(), i_variables_constant)
				variable.type = MathVariable.VAR_CST
				variable.ind = i_variables_constant
				variables_constant.append(variable)
				i_variables_constant += 1


			elif not (variable.isRuled() or (variable.isSpecies() and variable.isInReactions() or variable.hasEventAssignment())) and variable.isInAlgebraicRules():
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

	def changeVariableType(self, variable, new_type):

		if variable.isDerivative():
			if variable in self.__model.variablesOdes:
				self.__model.variablesOdes.remove(variable)
				self.__model.nbOdes -= 1

		elif variable.isAssignment():
			if variable in self.__model.variablesAssignment:
				self.__model.variablesAssignment.remove(variable)
				self.__model.nbAssignments -= 1

		elif variable.isConstant():
			if variable in self.__model.variablesConstant:
				self.__model.variablesConstant.remove(variable)
				self.__model.nbConstants -= 1

		elif variable.isAlgebraic():
			if variable in self.__model.variablesAlgebraic:
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

	def copyVariables(self, model):
		# First we copy the variables list
		self.clear()

		for variable in model.listOfVariables:
			new_var = MathVariable(self.__model)
			new_var.copy(variable, pure_math_variable=True)
			self.append(new_var)


	def copySubmodel(self, model):
		# # First we copy the variables list
		self.copyVariables(model)

		self.__model.nbOdes = model.nbOdes
		self.__model.nbAssignments = model.nbAssignments
		self.__model.nbConstants = model.nbConstants
		self.__model.nbAlgebraics = model.nbAlgebraics

		self.__model.variablesOdes = []
		for var_ode in model.variablesOdes:
			t_var = self.__model.listOfVariables.getBySymbol(var_ode.symbol.getSymbol())
			self.__model.variablesOdes.append(t_var)

		self.__model.variablesAssignment = []
		for var_ass in model.variablesAssignment:
			t_var = self.__model.listOfVariables.getBySymbol(var_ass.symbol.getSymbol())
			self.__model.variablesAssignment.append(t_var)

		self.__model.variablesConstant = []
		for var_cst in model.variablesConstant:
			t_var = self.__model.listOfVariables.getBySymbol(var_cst.symbol.getSymbol())
			self.__model.variablesConstant.append(t_var)

		self.__model.variablesAlgebraic = []
		for var_alg in model.variablesAlgebraic:
			t_var = self.__model.listOfVariables.getBySymbol(var_alg.symbol.getSymbol())
			self.__model.variablesAlgebraic.append(t_var)
