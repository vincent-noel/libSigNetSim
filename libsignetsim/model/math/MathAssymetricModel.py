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
# from libsignetsim.model.math.MathEquation import MathEquation
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

class MathAssymetricModel(MathModel):
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

	def printSystem(self):

		print "\n> Full system : "

		self.printCFEs()
		self.printODEs()
		self.printDAEs()
		self.printConservationLaws()

		print "-----------------------------"


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




	def findReducibleVariables(self, vars_to_keep=[]):

		odes_vars_in_laws = []
		for law in self.LHSs_v2:
			t_vars = []
			for var in law.getDeveloppedInternalMathFormula().atoms(SympySymbol):
				t_variable = self.listOfVariables[str(var)]
				if t_variable.isDerivative() and not t_variable.isCompartment():
					t_vars.append(var)
			odes_vars_in_laws.append(t_vars)


		system = []
		for i, law in enumerate(self.LHSs_v2):
			t_law = law.getDeveloppedInternalMathFormula()
			t_value = self.RHSs_v2[i].getDeveloppedInternalMathFormula()
			system.append(SympyEqual(t_law, t_value))


		vars_to_extract = []
		for i, ode_var in enumerate(odes_vars_in_laws):

			j=0
			while j < len(ode_var) and (
				(len(vars_to_extract) > 0 and ode_var[j] in vars_to_extract)
				or (len(vars_to_keep) > 0 and str(ode_var[j]) in vars_to_keep)):
				j += 1

			if j < len(ode_var):
				vars_to_extract.append(ode_var[j])

		# print [equ for equ in system]
		# print vars_to_extract[1]

		# print solve(system, vars_to_extract[1])
		solutions = solve(system, vars_to_extract)
		# print solutions
		if len(solutions) > 0:
			self.reducibleVariables = solutions
		else:
			self.reducibleVariables = {}
