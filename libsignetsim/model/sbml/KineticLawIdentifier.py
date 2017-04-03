#!/usr/bin/env python
""" KineticLawIdentifier.py


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


from sympy import simplify
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

	T_MM_1 = SympyMul(SympyMul(SympySymbol("_parameter_"), SympySymbol("_species_")),
						SympyPow(SympyAdd(SympySymbol("_parameter_"), SympySymbol("_species_")),
									SympyInteger(-1)))
	T_MM_2 = SympyMul(SympyMul(SympySymbol("_parameter_"), SympyPow(SympySymbol("_species_"), SympyInteger(2))),
						SympyPow(SympyAdd(SympySymbol("_parameter_"), SympySymbol("_species_")),
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

		for compartment in self.model.listOfCompartments.values():
			t_replaces.update({compartment.symbol.getInternalMathFormula(): SympyInteger(1)})

		return t_rate.subs(t_replaces)


	def removeSpeciesAndCompartmentsFromRate(self, formula=None):

		if formula is None:
			t_rate = self.getDefinition().getDeveloppedInternalMathFormula()
		else:
			t_rate = formula

		t_replaces = {}

		for compartment in self.model.listOfCompartments.values():
			t_replaces.update({compartment.symbol.getInternalMathFormula(): SympyInteger(1)})

		for species in self.model.listOfSpecies.values():
			t_replaces.update({species.symbol.getInternalMathFormula(): SympyInteger(1)})

		return t_rate.subs(t_replaces)


	def simplifyRate(self, formula=None):

		if formula is None:
			t_rate = self.removeCompartmentsFromRate()
		else:
			t_rate = formula

		t_replaces = {}

		for var in self.model.listOfVariables.values():
			if var.isParameter():
				t_replaces.update({var.symbol.getInternalMathFormula(): self.T_PARAM})
			elif var.isSpecies():
				t_replaces.update({var.symbol.getInternalMathFormula(): self.T_SPECIES})
			elif var.isCompartment():
				t_replaces.update({var.symbol.getInternalMathFormula(): SympyInteger(1)})
		return t_rate.subs(t_replaces)

	def isFactor(self, formula, term):



		if formula == term:
			return True

		elif formula.func == SympyPow and formula.args[0] == term and formula.args[1].func == SympyInteger and int(formula.args[1]) > 0:
			# print "Fuck yeah pow"
			return True

		elif formula.func == SympyMul:
			for arg in formula.args:
				if self.isFactor(arg, term):
					return True

		return False



	def isMassAction(self, formula):

		# print formula
		# We look for parameter*(species^n)
		if formula.func == SympyMul:
			if self.isFactor(formula, self.T_PARAM):
				t_formula = formula/self.T_PARAM

				if t_formula == self.T_SPECIES:
					return True
				elif t_formula.func == SympyPow and t_formula.args[0] == self.T_SPECIES and t_formula.args[1].func == SympyInteger:
					return True
		elif formula == self.T_PARAM:
			return True
		return False

	def isMichaelisMentenWithoutEnzyme(self, formula):
		return formula == self.T_MM_1

	def isMichaelisMentenWithEnzyme(self, formula):
		return formula == self.T_MM_2


	def isReversible(self, formula):

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

		t_forward = None
		t_backward = None
		# If we had an addition
		if formula.func == SympyAdd:

			# And one of the terms
			for arg in formula.args:

				# is *(-1)
				if arg.func == SympyMul:
					if (arg.args[0] == SympyInteger(-1)
						or arg.args[1] == SympyInteger(-1)):
						t_backward = arg*SympyInteger(-1)

		t_forward = SympyAdd(formula, t_backward)

		return (t_forward, t_backward)



	def findKineticLaw(self):

		# print "> Looking for the kinetic law"

		self.reactionType = self.UNDEFINED

		self.mathRate = self.removeCompartmentsFromRate()
		self.typeRate = self.simplifyRate()

		self.reversible = False

		t_formula = self.typeRate

		if self.isMassAction(t_formula):
			self.reactionType = self.MASS_ACTION

		elif self.isMichaelisMentenWithoutEnzyme(t_formula):
			self.reactionType = self.MICHAELIS

		elif self.isMichaelisMentenWithEnzyme(t_formula):
			self.reactionType = self.MICHAELIS

		elif self.isReversible(t_formula):
			self.reversible = True
			self.reaction.reversible = True
			(forward, backward) = self.getReversibleRates(self.mathRate)

			if (self.isMassAction(self.simplifyRate(forward))
				and self.isMassAction(self.simplifyRate(backward))):

				self.reactionType = self.MASS_ACTION

		else:
			self.reactionType = self.UNDEFINED

		# print self.reactionTypes[self.reactionType]


	def getReversibleFormulas(self):

		t_formula = self.getDefinition().getDeveloppedInternalMathFormula()
		for compartment in self.model.listOfCompartments.values():
			t_formula = t_formula.subs(compartment.symbol.getInternalMathFormula(), SympyInteger(1))

		t_formula = simplify(t_formula)
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


		param_catalytic = self.model.listOfVariables[str(param_catalytic)]
		param_michaelis = self.model.listOfVariables[str(param_michaelis)]
		return [param_catalytic, param_michaelis]





	def findMassActionParameters(self):

		param = self.removeSpeciesAndCompartmentsFromRate()
		param = self.model.listOfVariables[str(param)]
		return [param]


	def findReversibleMassActionParameters(self):

		self.getReversibleFormulas()

		front_param = self.removeSpeciesAndCompartmentsFromRate(self.forwardMathFormula)
		front_param = self.model.listOfVariables[str(front_param)]

		back_param = self.removeSpeciesAndCompartmentsFromRate(self.backwardMathFormula)
		back_param = self.model.listOfVariables[str(back_param)]

		return [front_param, back_param]
