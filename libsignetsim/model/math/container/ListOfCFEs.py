#!/usr/bin/env python
""" ListOfCFEs.py


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

from libsignetsim.model.math.CFE import CFE

class ListOfCFEs(ListOf):
	""" Sbml model class """


	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)


	def build(self):

		if self.listOfRules.hasAssignmentRule():
			for rule in self.listOfRules.values():
				if rule.isAssignment():
					list.append(self, self.buildCFE(rule.getVariable(), rule.definition, CFE.ASSIGNMENT))
					#
					#
					# self.CFE_types.append(self.ASSIGNMENT)
					#
					# t_var = MathFormula(self, MathFormula.MATH_VARIABLE)
					# t_var.setInternalMathFormula(rule.variable.getInternalMathFormula())
					# self.CFE_vars.append(t_var)
					#
					# t_cfe = MathFormula(self)
					# t_cfe.setInternalMathFormula(rule.getInternalDefinition())
					# self.CFEs.append(t_cfe)


		for reaction in self.listOfReactions.values():
			# self.CFE_types.append(self.REACTION)
			#
			# t_var = MathFormula(self, MathFormula.MATH_VARIABLE)
			# t_var.setInternalMathFormula(reaction.symbol.getInternalMathFormula())
			# self.CFE_vars.append(t_var)
			#
			# t_cfe = MathFormula(self)
			# t_cfe.setInternalMathFormula(reaction.value.getInternalMathFormula())
			# self.CFEs.append(t_cfe)
			list.append(self,self.buildCFE(reaction, reaction.value, CFE.REACTION))

		# self.developCFEs()

	def buildCFE(self, variable, definition, cfe_type):

		t_cfe = CFE(self.__model, cfe_type)
		t_cfe.new(variable, definition)
		return t_cfe

	def developCFEs(self):

		# print "developping CFEs"
		# Here we just develop the expression,
		# so that no closed-form depends on another.
		# Just to be sure not to get any ordering constraints
		# In two passes, not sure it's the right thing to do, but it works

		if len(self.CFEs) > 0:
			for i_cfe, t_cfe in enumerate(self.CFEs):
				tt_cfe = t_cfe.getDeveloppedInternalMathFormula()
				for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
					if t_cfe_var.getInternalMathFormula() in tt_cfe.atoms(SympySymbol) and i_cfe_var < i_cfe:
						tt_cfe = tt_cfe.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
				self.CFEs[i_cfe].setInternalMathFormula(tt_cfe)


			for i_cfe, t_cfe in enumerate(self.CFEs):
				tt_cfe = t_cfe.getDeveloppedInternalMathFormula()
				for i_cfe_var, t_cfe_var in enumerate(self.CFE_vars):
					if t_cfe_var.getInternalMathFormula() in tt_cfe.atoms(SympySymbol):
						tt_cfe = tt_cfe.subs(t_cfe_var.getInternalMathFormula(), self.CFEs[i_cfe_var].getInternalMathFormula())
				self.CFEs[i_cfe].setInternalMathFormula(simplify(tt_cfe))


	def printCFEs(self):

		print "-----------------------------"
		for i_equ, equ in enumerate(self.CFEs):
			print ">> %s = %s" % (str(self.CFE_vars[i_equ].getDeveloppedInternalMathFormula()),
								str(equ.getDeveloppedInternalMathFormula()))
