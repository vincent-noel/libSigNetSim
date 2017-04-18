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

from libsignetsim.model.math.container.ListOfODEs import ListOfODEs
from libsignetsim.model.math.container.ListOfCFEs import ListOfCFEs
from libsignetsim.model.math.container.ListOfDAEs import ListOfDAEs
from libsignetsim.model.math.DAE import DAE
from libsignetsim.model.math.CFE import CFE
from libsignetsim.model.math.ODE import ODE
from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from libsignetsim.model.math.container.ListOfConservationLaws import ListOfConservationLaws
from sympy import solve
class MathAsymmetricModel(object):
	""" Sbml model class """

	def __init__ (self, parent_model=None):
		""" Constructor of model class """

		# MathModel.__init__(self)
		self.parentModel = parent_model
		self.sbmlLevel = self.parentModel.sbmlLevel
		self.sbmlVersion = self.parentModel.sbmlVersion

		self.listOfODEs = ListOfODEs(self)
		self.listOfCFEs = ListOfCFEs(self)
		self.listOfDAEs = ListOfDAEs(self)
		self.listOfVariables = ListOfVariables(self)

		self.solvedInitialConditions = {}

		self.nbOdes = None
		self.nbAssignments = None
		self.nbConstants = None
		self.nbAlgebraics = None

		self.variablesOdes = None
		self.variablesAssignment = None
		self.variablesConstant = None
		self.variablesAlgebraic = None

		# self.hasDAEs = self.parentModel.hasDAEs
		self.__upToDate = False


	def isUpToDate(self):
		return self.__upToDate

	def setUpToDate(self, value):
		self.__upToDate = value

	def copyVariables(self):
		""" Copies the listOfVariables and the solvedInitialConditions """

		# First we copy the variables list
		for variable in self.parentModel.listOfVariables.values():
			new_var = MathVariable(self)
			new_var.copy(variable)
			new_var_id = new_var.symbol.getPrettyPrintMathFormula()
			self.listOfVariables.update({new_var_id:new_var})

		for variable, value in self.parentModel.solvedInitialConditions.items():
			t_value = MathFormula(self)
			t_value.setInternalMathFormula(value.getInternalMathFormula())
			self.solvedInitialConditions.update({variable: t_value})
			# print "old: %s : %s" % (variable, value.getInternalMathFormula())
			# print "new: %s : %s" % (variable, t_value.getInternalMathFormula())
		# print self.solvedInitialConditions.items()

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
			t_cfe_formula = MathFormula(self)
			t_cfe_formula.setInternalMathFormula(cfe.getDefinition().getDeveloppedInternalMathFormula())
			t_cfe = CFE(self)
			t_cfe.new(t_var, t_cfe_formula)
			self.listOfCFEs.append(t_cfe)

		for dae in self.parentModel.listOfDAEs:
			t_dae_formula = MathFormula(self)
			t_dae_formula.setInternalMathFormula(dae.getDefinition().getDeveloppedInternalMathFormula())
			t_dae = DAE(self)
			t_dae.new(t_dae_formula)
			self.listOfDAEs.append(t_dae)

	def build(self, treated_variables=[]):

		if self.parentModel.stoichiometryMatrix.hasNullSpace():
			nullspace = self.parentModel.stoichiometryMatrix.getSimpleNullspace()

			independent_species = []
			independent_species_formula = []
			for i_cons, cons in enumerate(nullspace):

				cons_law = self.parentModel.listOfConservationLaws[i_cons]

				can_reduce = True
				for var in treated_variables:
					if SympySymbol(var) in cons_law.getFormula().atoms(SympySymbol):
						can_reduce = False
						# print "Refused conservation law : %s" % cons_law

				if can_reduce:
					for i, species in enumerate(self.parentModel.variablesOdes):
						if (
							cons[i] == 1
							and species.symbol.getSymbol() not in independent_species
							and cons_law.getNbVars() > 1

						):
							independent_species.append(species.symbol.getSymbol())
							independent_species_formula.append(
								solve(
									cons_law.getFormula(),
									species.symbol.getSymbol()
								)
							)
							break

			self.copyVariables()

			for var in self.parentModel.variablesOdes:
				new_var = self.listOfVariables.getBySymbol(var.symbol.getSymbol())
				if var.symbol.getSymbol() in independent_species:

					t_formula = MathFormula(self)

					t_formula.setInternalMathFormula(
						independent_species_formula[independent_species.index(var.symbol.getSymbol())][0]
					)

					t_cfe = CFE(self)
					t_cfe.new(new_var, t_formula)
					self.listOfCFEs.append(t_cfe)
					self.listOfVariables.changeVariableType(new_var, MathVariable.VAR_ASS)

				else:

					t_formula = MathFormula(self)
					t_formula.setInternalMathFormula(
						self.parentModel.listOfODEs.getByVariable(var).getDefinition().getDeveloppedInternalMathFormula()
					)

					t_ode = ODE(self)
					t_ode.new(new_var, t_formula)
					self.listOfODEs.append(t_ode)

			self.__upToDate = True
			self.listOfCFEs.developCFEs()

	def prettyPrint(self):

		print "\n> Full system : "
		print self.listOfCFEs
		print self.listOfDAEs
		print self.listOfODEs
		print "-----------------------------"
