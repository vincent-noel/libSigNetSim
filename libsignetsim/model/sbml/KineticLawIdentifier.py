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


from sympy import simplify, expand, srepr
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from libsignetsim.model.math.sympy_shortcuts import (
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


class KineticLawIdentifier(object):
	""" Class for handling math formulaes """

	MASS_ACTION = 0
	MICHAELIS = 1
	UNDEFINED = 2
	HILL = 3

	reactionTypes = {MASS_ACTION: "Mass Action reaction",
					MICHAELIS: "Enzymatic reaction",
					UNDEFINED: "User defined reaction",
					HILL: "Hill kinetics reaction"}

	#parametersList = {(MASS_ACTION, False): ["Forward kinetic parameter"],
	#                  (MASS_ACTION, True): ["Forward kinetic parameter", "Backward kinetic parameter"],
	#                  (MICHAELIS, False): ["Catalytic constant", "Michaelis constant"],
	#                  }

	allowReversibleList = {

		MASS_ACTION: True,
		MICHAELIS: False,
		UNDEFINED: True,
		HILL: False,
	}

	parametersList = {

		MASS_ACTION: {
			False: ["Kinetic parameter"],
			True: ["Forward kinetic parameter", "Backward kinetic parameter"],
		},

		MICHAELIS: {
			False: ["Catalytic sconstant", "Michaelis constant"],
		},

		UNDEFINED: {
			True: [],
			False: [],
		},

		HILL: {
			False: ["kcat", "Kd", "n"],
		},
	}


	T_PARAM = SympySymbol("_parameter_")
	T_SPECIES = SympySymbol("_species_")
	T_COMPARTMENT = SympySymbol("_compartment_")
	T_REACTANT = SympySymbol("_reactant_")
	T_MODIFIER = SympySymbol("_modifier_")
	T_PRODUCT = SympySymbol("_product_")

	T_MM_1 = SympyMul(SympyMul(SympySymbol("_parameter_"), SympySymbol("_species_")),
						SympyPow(SympyAdd(SympySymbol("_parameter_"), SympySymbol("_species_")),
									SympyInteger(-1)))
	T_MM_2 = SympyMul(SympyMul(SympySymbol("_parameter_"), SympyPow(SympySymbol("_species_"), SympyInteger(2))),
						SympyPow(SympyAdd(SympySymbol("_parameter_"), SympySymbol("_species_")),
									SympyInteger(-1)))


	T_MA_IR = SympyMul(SympySymbol("_parameter_"), SympySymbol("_reactant_"))
	T_MA_R = SympyMul(SympySymbol("_parameter_"), SympySymbol("_reactant_")) - SympyMul(SympySymbol("_parameter_"), SympySymbol("_product_"))


	T_MM_WITHOUT_ENZYME = SympyMul(SympyMul(SympySymbol("_parameter_"), SympySymbol("_reactant_")),
						SympyPow(SympyAdd(SympySymbol("_parameter_"), SympySymbol("_reactant_")),
									SympyInteger(-1)))

	T_MM_WITH_ENZYME = SympyMul(SympyMul(SympySymbol("_parameter_"), SympySymbol("_reactant_"), SympySymbol("_modifier_")),
						SympyPow(SympyAdd(SympySymbol("_parameter_"), SympySymbol("_reactant_")),
									SympyInteger(-1)))

	ZERO = SympyInteger(0)

	def __init__(self, model, reaction):
		""" Constructor """

		self.model = model
		self.reaction = reaction

		self.reactionType = None

		self.reversible = None
		self.forwardMathFormula = None
		self.reactionTypeForward = None
		self.backwardMathFormula = None
		self.reactionTypeBackward = None

		self.mathRate = None
		self.typeRate = None

	def removeCompartmentsFromRate(self, formula=None):

		if formula is None:
			t_rate = self.getDefinition().getDeveloppedInternalMathFormula()
		else:
			t_rate = formula

		t_replaces = {}

		for compartment in self.model.listOfCompartments:
			t_replaces.update({compartment.symbol.getInternalMathFormula(): SympyInteger(1)})

		return unevaluatedSubs(t_rate, t_replaces)


	def removeSpeciesAndCompartmentsFromRate(self, formula=None):

		if formula is None:
			t_rate = self.getDefinition().getDeveloppedInternalMathFormula()
		else:
			t_rate = formula

		t_replaces = {}

		for compartment in self.model.listOfCompartments:
			t_replaces.update({compartment.symbol.getInternalMathFormula(): SympyInteger(1)})

		for species in self.model.listOfSpecies:
			t_replaces.update({species.symbol.getInternalMathFormula(): SympyInteger(1)})

		return expand(simplify(unevaluatedSubs(t_rate, t_replaces)))


	def simplifyRate(self, formula=None):

		if formula is None:
			t_rate = self.removeCompartmentsFromRate()
		else:
			t_rate = formula

		t_replaces = {}

		for var in self.model.listOfVariables:
			if var.isParameter():
				t_replaces.update({var.symbol.getInternalMathFormula(): self.T_PARAM})
			elif var.isCompartment():
				t_replaces.update({var.symbol.getInternalMathFormula(): SympyInteger(1)})

		for i, reactant in enumerate(self.reaction.listOfReactants):
			if i == 0:
				t_replaces.update({reactant.getSpecies().symbol.getInternalMathFormula(): self.T_REACTANT})
			else:
				t_replaces.update({reactant.getSpecies().symbol.getInternalMathFormula(): SympyInteger(1)})

		for i, modifier in enumerate(self.reaction.listOfModifiers):
			if i == 0:
				t_replaces.update({modifier.getSpecies().symbol.getInternalMathFormula(): self.T_MODIFIER})
			else:
				t_replaces.update({modifier.getSpecies().symbol.getInternalMathFormula(): SympyInteger(1)})

		for i, product in enumerate(self.reaction.listOfProducts):
			if i == 0:
				t_replaces.update({product.getSpecies().symbol.getInternalMathFormula(): self.T_PRODUCT})
			else:
				t_replaces.update({product.getSpecies().symbol.getInternalMathFormula(): SympyInteger(1)})

		return simplify(unevaluatedSubs(t_rate, t_replaces))

	def isReversible(self, formula=None):

		if formula is None:
			formula = self.simplifyRate()

		formula = expand(simplify(formula))
		# If we had an addition
		if formula.func == SympyAdd:

			# And one of the terms
			for arg in formula.args:

				# is *(-1)
				if (arg.func == SympyMul
					and (arg.args[0] == SympyInteger(-1)
						or arg.args[1] == SympyInteger(-1))):

					return True

		return False

	def getReversibleRates(self, formula):

		t_backward = None
		formula = expand(simplify(formula))
		# If we had an addition
		if formula.func == SympyAdd:
			# And one of the terms
			for arg in formula.args:
				# is *(-1)
				if arg.func == SympyMul:
					if (arg.args[0] == SympyInteger(-1)
						or arg.args[1] == SympyInteger(-1)):
						t_backward = arg*SympyInteger(-1)
		else:
			return (formula,SympyInteger(0))

		t_forward = SympyAdd(formula, t_backward)

		return (t_forward, t_backward)


	def findKineticLaw(self):

		# print "> Looking for the kinetic law"

		self.reactionType = self.UNDEFINED

		self.mathRate = self.removeCompartmentsFromRate()
		self.typeRate = self.simplifyRate()
		self.reversible = False

		t_formula = expand(simplify(self.typeRate))

		if simplify(self.typeRate - self.T_MA_IR) == 0 or simplify(self.typeRate - self.T_MA_R) == 0:
			self.reactionType = self.MASS_ACTION

			if self.isReversible(t_formula):
				self.reversible = True
				self.reaction.reversible = True
				self.getReversibleFormulas()
		elif (
			simplify(self.typeRate - self.T_MM_WITH_ENZYME) == 0
			or simplify(self.typeRate - self.T_MM_WITHOUT_ENZYME) == 0
		):
			self.reactionType = self.MICHAELIS

		else:
			self.reactionType = self.UNDEFINED

	def getReversibleFormulas(self):

		t_formula = self.getDefinition().getDeveloppedInternalMathFormula()
		for compartment in self.model.listOfCompartments:
			t_formula = t_formula.subs(compartment.symbol.getInternalMathFormula(), SympyInteger(1))

		t_formula = expand(simplify(t_formula))
		found = False

		if t_formula.func == SympyAdd:

			if t_formula.args[0].func == SympyMul:
				if (t_formula.args[0].args[0] == SympyInteger(-1)
					or t_formula.args[0].args[1] == SympyInteger(-1)):

					self.forwardMathFormula = t_formula.args[1]
					self.backwardMathFormula = t_formula.args[0]*SympyInteger(-1)
					found = True

			if t_formula.args[1].func == SympyMul and not found:
				if (t_formula.args[1].args[0] == SympyInteger(-1)
					or t_formula.args[1].args[1] == SympyInteger(-1)):

					self.forwardMathFormula = t_formula.args[0]
					self.backwardMathFormula = t_formula.args[1]*SympyInteger(-1)

	def getParameters(self):

		if self.reactionType == self.MASS_ACTION and not self.reversible:
			return self.findMassActionParameters()

		elif self.reactionType == self.MASS_ACTION and self.reversible:
			return self.findReversibleMassActionParameters()

		elif self.reactionType == self.MICHAELIS:
			return self.findMichaelisMentenParameters()

	def findMichaelisMentenParameters(self):

		param_catalytic = None
		param_michaelis = None

		t_formula = self.removeSpeciesAndCompartmentsFromRate()

		if t_formula.func == SympyMul:
			if t_formula.args[0].func == SympyPow:

				param_catalytic = t_formula.args[1]

				if t_formula.args[0].args[0].func == SympyAdd:
					if t_formula.args[0].args[0].args[1] == SympyInteger(1):
						param_michaelis = t_formula.args[0].args[0].args[0]
					elif t_formula.args[0].args[0].args[0] == SympyInteger(1):
						param_michaelis = t_formula.args[0].args[0].args[1]

				elif t_formula.args[0].args[1].func == SympyAdd:
					if t_formula.args[0].args[1].args[1] == SympyInteger(1):
						param_michaelis = t_formula.args[0].args[1].args[1]
					elif t_formula.args[0].args[1].args[0] == SympyInteger(1):
						param_michaelis = t_formula.args[0].args[1].args[0]

			elif t_formula.args[1].func == SympyPow:

				param_catalytic = t_formula.args[0]

				if t_formula.args[1].args[0].func == SympyAdd:
					if t_formula.args[1].args[0].args[1] == SympyInteger(1):
						param_michaelis = t_formula.args[1].args[0].args[0]
					elif t_formula.args[1].args[0].args[0] == SympyInteger(1):
						param_michaelis = t_formula.args[1].args[0].args[1]

				elif t_formula.args[1].args[1].func == SympyAdd:
					if t_formula.args[1].args[1].args[0] == SympyInteger(1):
						param_michaelis = t_formula.args[1].args[1].args[1]
					elif t_formula.args[1].args[1].args[1] == SympyInteger(1):
						param_michaelis = t_formula.args[1].args[1].args[0]

		param_catalytic = self.model.listOfVariables.getBySymbol(param_catalytic)
		param_michaelis = self.model.listOfVariables.getBySymbol(param_michaelis)

		return [param_catalytic, param_michaelis]

	def findMassActionParameters(self):

		param = self.removeSpeciesAndCompartmentsFromRate()
		return [self.model.listOfVariables.getBySymbol(param)]

	def findReversibleMassActionParameters(self):

		self.getReversibleFormulas()

		front_param = self.removeSpeciesAndCompartmentsFromRate(self.forwardMathFormula)
		front_param = self.model.listOfVariables.getBySymbol(front_param)

		back_param = self.removeSpeciesAndCompartmentsFromRate(self.backwardMathFormula)
		back_param = self.model.listOfVariables.getBySymbol(back_param)

		return [front_param, back_param]
