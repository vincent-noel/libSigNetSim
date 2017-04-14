#!/usr/bin/env python
""" MathDevelopper.py


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


from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyFloat, SympyPi, SympyMul, SympyPow, SympyUndefinedFunction,
	SympyTrue, SympyFalse, SympyExprCondPair, SympyITE)
from re import match


def unevaluatedSubs(expr, substitutions, *args, **kwargs):
	"""Crawl the expression tree, and apply func to every node."""
	val = simpleSubs(expr, substitutions, *args, **kwargs)
	if val is not None:
		return val
	new_args = (unevaluatedSubs(arg, substitutions, *args, **kwargs) for arg in expr.args)

	if expr.func in [SympyExprCondPair, SympyITE]:
		return expr.func(*new_args)
	else:
		return expr.func(*new_args, evaluate=False)

def simpleSubs(expr, substitutions, *args, **kwargs):
	"""Perform expression substitution, ignoring derivatives."""
	if expr in substitutions:
		return substitutions[expr]
	elif not expr.args:
		return expr


class MathDevelopper(object):
	""" Class for handling math formulaes """

	def __init__(self, model):
		""" Constructor """

		self.__model = model

	def translateVariableForDeveloppedInternal(self, variable):

		if str(variable).startswith("_speciesForcedConcentration_"):
			res_match = match(r"_speciesForcedConcentration_(.*)_", str(variable))

			t_sbml_id = str(res_match.groups()[0])
			t_species = self.__model.listOfVariables.getBySymbol(SympySymbol(t_sbml_id))
			t_compartment = t_species.getCompartment()

			return SympyMul(t_species.symbol.getInternalMathFormula(),
							SympyPow(t_compartment.symbol.getInternalMathFormula(),
										SympyInteger(-1)))

		else:
			return variable


	def translateForDeveloppedInternal(self, tree):

		if tree is None:
			return None

		if tree in [True, False]:
			return tree

		if tree in [SympyTrue, SympyFalse, SympyPi] or tree.func in [SympyInteger, SympyFloat]:
			return tree

		if isinstance(tree.func, SympyUndefinedFunction) and "_functionDefinition_" in str(tree.func):

			res_match = match(r"_functionDefinition_(\d+)_", str(tree.func))
			t_id = int(res_match.groups()[0])
			t_definition = self.__model.listOfFunctionDefinitions[t_id].getDefinition().getInternalMathFormula().args[1]
			t_arguments = list(self.__model.listOfFunctionDefinitions[t_id].getDefinition().getInternalMathFormula().args[0])

			for child in range(0, len(tree.args)):
				t_definition = t_definition.subs(t_arguments[child], self.translateForDeveloppedInternal(tree.args[child]))

			return t_definition


		elif tree.func == SympySymbol:
			return self.translateVariableForDeveloppedInternal(tree)

		else:
			if len(tree.args) >= 1:
				t_children = []
				for child in range(0, len(tree.args)):
					t_children.append(self.translateForDeveloppedInternal(tree.args[child]))

				# Seems like not evaluating is not an option for these ones...
				if tree.func in [SympyExprCondPair, SympyITE]:
					return tree.func(*tuple(t_children))

				return tree.func(*tuple(t_children), evaluate=False)

			else:
				return tree


	def translateForFinalInternal(self, formula, forcedConcentration=False):

		if self.__model.isUpToDate():
			return formula.subs(self.__model.listOfVariables.getInternalToFinal(forcedConcentration))

	def translateFinalForInternal(self, formula, forcedConcentration=False):

		if self.__model.isUpToDate():
			return formula.subs(self.__model.listOfVariables.getFinalToInternal(forcedConcentration))
