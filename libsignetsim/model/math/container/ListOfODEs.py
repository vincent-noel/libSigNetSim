#!/usr/bin/env python
""" MathODEs.py


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

from libsignetsim.model.math.ODE import ODE

class ListOfODEs(list):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)


	def build(self, including_fast_reactions=True):

		for variable in self.__model.listOfVariables.values():
			if variable.isDerivative():
				# print "\n\n> New var: \n"
				t_ode = ODE(self.__model)
				t_raw_ode = variable.getODE(including_fast_reactions)
				t_ode.new(variable,
							t_raw_ode)

				list.append(self, t_ode)

				# print t_raw_ode.getDeveloppedInternalMathFormula()

		# self.prettyPrint()
	# def buildFromModel(self, model, including_fast_reactions=True):
	# 	for variable in model.listOfVariables.values():
	# 		if variable.isDerivative():
	#
	# 			# First we found the corresponding variable in the new list
	# 			t_var = self.__model.listOfVariables[str(variable.symbol.getInternalMathFormula())]
	# 			t_definition = variable.getODE(including_fast_reactions)
	#
	# 			if t_definition is not None:
	# 				t_ode = ODE(self.__model)
	# 				t_ode.new(t_var, variable.getODE(including_fast_reactions))
	# 				list.append(self, t_ode)
	#
	# def developODEs(self):
	#
	# 	# Here we just develop the expression,
	# 	# so that the whole system is here
	# 	# Just to be sure not to get any ordering constraints
	# 	# In two passes, not sure it's the right thing to do, but it works
	#
	# 	for i_ode, t_ode in enumerate(self.ODEs):
	# 		tt_ode = t_ode.getDeveloppedInternalMathFormula()
	# 		# print "> CFE #%d : %s" % (i_cfe, str(tt_cfe))
	# 		for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
	# 			if t_cfe_var.getInternalMathFormula() in tt_ode.atoms(SympySymbol) and i_cfe_var < i_ode:
	# 				tt_ode = tt_ode.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
	# 		self.ODEs[i_ode].setInternalMathFormula(tt_ode)
	#
	#
	# 	for i_ode, t_ode in enumerate(self.ODEs):
	#
	# 		tt_ode = t_ode.getDeveloppedInternalMathFormula()
	#
	# 		for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
	# 			if t_cfe_var.getInternalMathFormula() in tt_ode.atoms(SympySymbol):
	# 				tt_ode = tt_ode.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
	# 		self.ODEs[i_ode].setInternalMathFormula(tt_ode)
	# 		# self.ODEs[i_ode].setInternalMathFormula(simplify(tt_ode))

	def prettyPrint(self):

		print "-----------------------------"
		for t_ode in self:
			print ">> %s = %s" % (str(t_ode.getVariable().symbol.getDerivative().getDeveloppedInternalMathFormula()),
								str(t_ode.getDefinition().getDeveloppedInternalMathFormula()))
