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

from libsignetsim.model.math.DAE import DAE
from libsignetsim.model.math.CFE import CFE
from libsignetsim.model.math.ODE import ODE
from libsignetsim.model.math.MathSubmodel import MathSubmodel
from libsignetsim.model.math.MathVariable import MathVariable
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from sympy import solve, simplify


class MathAsymmetricModel(MathSubmodel):
	""" Sbml model class """

	def __init__(self, parent_model=None):
		""" Constructor of model class """

		MathSubmodel.__init__(self, parent_model=parent_model)

	def copyEquations(self):
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

		self.listOfEvents.copySubmodel(self.parentModel.listOfEvents)

	def build(self, treated_variables=[]):

		forbidden_variables = []
		for species in self.parentModel.variablesOdes:
			if (str(species.symbol.getSymbol()) in treated_variables) or (species.hasEventAssignment()):
				forbidden_variables.append(species.symbol.getSymbol())

		if len(self.parentModel.listOfConservationLaws) > 0:

			nullspace = self.parentModel.stoichiometryMatrix.getSimpleNullspace()
			independent_species = []
			independent_species_formula = []
			solutions_subs = {}

			for i_cons, cons_law in enumerate(self.parentModel.listOfConservationLaws):

				can_reduce = True
				for var in forbidden_variables:
					if var in cons_law.getFormula().atoms(SympySymbol):
						can_reduce = False
						# print "Refused conservation law : %s" % cons_law

				if can_reduce:

					for i_ode, species in enumerate(self.parentModel.variablesOdes):

						if (
							nullspace[i_cons][i_ode] == 1
							and species.symbol.getSymbol() not in independent_species
							and cons_law.getNbVars() > 1
							and not species.hasEventAssignment()
						):
							solution = solve(
									unevaluatedSubs(cons_law.getFormula(), solutions_subs),
									species.symbol.getSymbol()
								)
							if len(solution) > 0:
								independent_species.append(species.symbol.getSymbol())
								independent_species_formula.append(solution[0])
								solutions_subs.update({species.symbol.getSymbol(): solution[0]})
								break


			if len(independent_species) > 0:

				self.copyVariables()
				self.copyEquations()

				for var in self.parentModel.variablesOdes:
					new_var = self.listOfVariables.getBySymbol(var.symbol.getSymbol())
					if var.symbol.getSymbol() in independent_species:

						t_formula = MathFormula(self)

						t_formula.setInternalMathFormula(
							independent_species_formula[independent_species.index(var.symbol.getSymbol())]
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

				self.setUpToDate(True)
				self.listOfCFEs.developCFEs()
