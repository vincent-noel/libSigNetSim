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



from libsignetsim.model.math.sympy_shortcuts import (
	SympySymbol, SympyInteger, SympyFloat, SympyPi, SympyMul, SympyPow, SympyRateOf, SympyUndefinedFunction,
	SympyTrue, SympyFalse, SympyExprCondPair, SympyITE, SympyLambda, SympyTuple, SympyAvogadro)
from re import match
from sympy import srepr


def unevaluatedSubs(expr, substitutions, *args, **kwargs):
	"""Crawl the expression tree, and apply func to every node."""
	if len(substitutions) == 0:
		return expr

	val = simpleSubs(expr, substitutions, *args, **kwargs)
	if val is not None:
		return val
	new_args = (unevaluatedSubs(arg, substitutions, *args, **kwargs) for arg in expr.args)

	if expr.func in [SympyExprCondPair, SympyITE]:
		return expr.func(*new_args)
	else:
		return expr.func(*new_args, evaluate=False)

def simpleSubs(expr, substitutions, *args, **kwarg):
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

		elif str(variable).startswith("_functionDefinition_"):
			res_match = match(r"_functionDefinition_(\d+)_", str(variable))
			t_id = int(res_match.groups()[0])
			t_definition = self.__model.listOfFunctionDefinitions[t_id].getDefinition().getInternalMathFormula()

			return self.translateForDeveloppedInternal(t_definition)

		else:

			return variable


	def translateForDeveloppedInternal(self, tree):

		if tree is None:
			return None

		if tree in [True, False]:
			return tree

		if tree in [SympyTrue, SympyFalse, SympyPi] or tree.func in [SympyInteger, SympyFloat]:
			return tree


		if tree.func == SympyRateOf:

			if str(tree.args[0]).startswith("_speciesForcedConcentration_"):
				res_match = match(r"_speciesForcedConcentration_(.*)_", str(tree.args[0]))

				t_sbml_id = str(res_match.groups()[0])
				t_variable = self.__model.listOfVariables.getBySymbol(SympySymbol(t_sbml_id))

				if t_variable.isSpecies() and not t_variable.hasOnlySubstanceUnits:# and not t_variable.isRateRuled():
					t_ode = t_variable.getODE().getDeveloppedInternalMathFormula()
					if t_ode is not None:
						if not t_variable.isRateRuled():
							t_ode /= t_variable.getCompartment().symbol.getDeveloppedInternalMathFormula()
						elif t_variable.getCompartment().isRateRuled():
							t_amount_species = t_variable.symbol.getInternalMathFormula()
							t_comp_rate = t_variable.getCompartment().isRuledBy().getDefinition().getInternalMathFormula()
							t_comp = t_variable.getCompartment().symbol.getInternalMathFormula()
							t_ode = t_ode - t_amount_species * t_comp_rate / t_comp

				else:
					t_ode = t_variable.getODE().getDeveloppedInternalMathFormula()

			else:
				t_variable = self.__model.listOfVariables.getBySymbol(tree.args[0])
				t_ode = t_variable.getODE().getDeveloppedInternalMathFormula()

			if t_ode is None:
				return SympyInteger(0)

			return t_ode

		if isinstance(tree.func, SympyUndefinedFunction) and "_functionDefinition_" in str(tree.func):
			res_match = match(r"_functionDefinition_(\d+)_", str(tree.func))
			t_id = int(res_match.groups()[0])
			t_definition = self.translateForDeveloppedInternal(self.__model.listOfFunctionDefinitions[t_id].getDefinition().getInternalMathFormula().args[1])
			t_arguments = list(self.__model.listOfFunctionDefinitions[t_id].getDefinition().getInternalMathFormula().args[0])

			subs = {}
			for child in range(0, len(tree.args)):
				subs.update({t_arguments[child]: self.translateForDeveloppedInternal(tree.args[child])})

			return unevaluatedSubs(t_definition, subs)

		elif isinstance(tree, SympyUndefinedFunction):
			res_match = match(r"_functionDefinition_(\d+)_", str(tree))
			t_id = int(res_match.groups()[0])
			t_definition = self.__model.listOfFunctionDefinitions[t_id].getDefinition().getInternalMathFormula()

			return self.translateForDeveloppedInternal(t_definition)

		elif tree.func == SympySymbol:
			return self.translateVariableForDeveloppedInternal(tree)

		elif tree.func == SympyLambda and len(tree.args) > 0 and tree.args[0] == SympyTuple():
			return self.translateForDeveloppedInternal(tree.args[1])

		else:
			if len(tree.args) > 0:
				t_children = []
				for child in range(0, len(tree.args)):
					t_children.append(self.translateForDeveloppedInternal(tree.args[child]))

				# Seems like not evaluating is not an option for these ones...
				if tree.func in [SympyExprCondPair, SympyITE]:
					return tree.func(*tuple(t_children))

				return tree.func(*tuple(t_children), evaluate=False)

			else:
				return tree

