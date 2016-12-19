#!/usr/bin/env python
""" Reaction.py


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


from libsignetsim.model.container.ListOfParameters import ListOfParameters
from libsignetsim.model.container.ListOfSpeciesReference import ListOfSpeciesReference

# from libsignetsim.model.math.MathKineticLaw import MathKineticLaw
from libsignetsim.model.sbmlobject.KineticLaw import KineticLaw
from libsignetsim.model.math.MathFormula import MathFormula

# from libsignetsim.model.sbmlobject.HasId import HasId
from libsignetsim.model.sbmlobject.HasUnits import HasUnits
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject
from libsignetsim.model.Variable import Variable
from libsignetsim.settings.Settings import Settings
from sympy import zeros
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

class Reaction(Variable, SbmlObject, HasUnits):
	""" Parent class for Sbml reaction """


	def __init__ (self, model, obj_id, name=None, reaction_type=KineticLaw.UNDEFINED):

		self.model = model
		self.objId = obj_id

		HasUnits.__init__(self, model)
		Variable.__init__(self, model, Variable.REACTION)
		SbmlObject.__init__(self, model)

		self.reversible = True
		self.fast = False
		self.reactionType = reaction_type

		self.kineticLaw = None

		self.listOfReactants = ListOfSpeciesReference(model)
		self.listOfModifiers = ListOfSpeciesReference(model)
		self.listOfProducts = ListOfSpeciesReference(model)
		self.listOfLocalParameters = ListOfParameters(model, are_local_parameters=True, reaction=self)


	def new(self, name=None):
		# self.setName(name)
		# print "Name is none : %s" % str(name == None)
		Variable.new(self, name, Variable.REACTION)
		self.kineticLaw = KineticLaw(self.model, self)

	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[],
				replacements={}, conversions={},
				extent_conversion=None, time_conversion=None):

		HasUnits.copy(self, obj, prefix, shift)
		SbmlObject.copy(self, obj, prefix, shift)
		Variable.copy(self, obj, prefix, shift, subs)

		if obj.listOfReactants not in deletions and len(obj.listOfReactants) > 0:
			self.listOfReactants.copy(obj.listOfReactants, prefix, shift, subs, deletions, replacements)
		if obj.listOfModifiers not in deletions and len(obj.listOfModifiers) > 0:
			self.listOfModifiers.copy(obj.listOfModifiers, prefix, shift, subs, deletions, replacements)
		if obj.listOfProducts not in deletions and len(obj.listOfProducts) > 0:
			self.listOfProducts.copy(obj.listOfProducts, prefix, shift, subs, deletions, replacements)

		if obj.listOfLocalParameters not in deletions and len(obj.listOfLocalParameters) > 0:
			self.listOfLocalParameters.copy(obj.listOfLocalParameters, prefix, shift, subs, deletions, replacements)

		if obj.kineticLaw is not None:
			self.kineticLaw = KineticLaw(self.model, self)
			self.kineticLaw.copy(obj, prefix, shift, subs, deletions, replacements, conversions, extent_conversion, time_conversion)

			self.value = MathFormula(self.model)
			t_formula = self.kineticLaw.definition.getInternalMathFormula()

			self.value.setInternalMathFormula(t_formula)
			self.constant = obj.constant

		self.reversible = obj.reversible
		self.fast = obj.fast

	def readSbml(self, reaction, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads an sbml reaction from sbml model """

		if sbml_level < 3:
			self.setUnits(self.model.substanceUnits)
		else:
			self.setUnits(self.model.extentUnits)


		SbmlObject.readSbml(self, reaction, sbml_level, sbml_version)

		if reaction.getListOfReactants():
			self.listOfReactants.readSbml(reaction.getListOfReactants(), sbml_level, sbml_version)

		if reaction.getListOfProducts():
			self.listOfProducts.readSbml(reaction.getListOfProducts(), sbml_level, sbml_version)

		if reaction.getListOfModifiers():
			self.listOfModifiers.readSbml(reaction.getListOfModifiers(), sbml_level, sbml_version)

		if reaction.isSetReversible():
			self.reversible = reaction.getReversible()

		if reaction.isSetFast():
			self.fast = reaction.getFast()

		if reaction.getKineticLaw() is not None:

			t_params = reaction.getKineticLaw().getListOfParameters()
			self.listOfLocalParameters.readSbml(t_params,
												sbml_level, sbml_version)
			self.kineticLaw = KineticLaw(self.model, self)
			self.kineticLaw.readSbml(reaction.getKineticLaw().getMath(),
										sbml_level, sbml_version)

		Variable.readSbml(self, reaction, sbml_level, sbml_version)


	def readSbmlVariable(self, variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		# variable id
		self.symbol.readSbml(variable.getId(), sbml_level, sbml_version)

		# self.isInitialized = True
		if self.kineticLaw is not None:
			self.value = self.kineticLaw.definition
			self.constant = False
		else:
			self.constant = True


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an sbml reaction to a sbml model """

		sbml_reaction = sbml_model.createReaction()

		Variable.writeSbml(self, sbml_reaction, sbml_level, sbml_version)
		SbmlObject.writeSbml(self, sbml_reaction, sbml_level, sbml_version)

		if (sbml_level < 3 and self.reversible == False) or sbml_level == 3:
			sbml_reaction.setReversible(self.reversible)

		if (sbml_level < 3 and self.fast == True) or sbml_level == 3:
			sbml_reaction.setFast(self.fast)

		if self.listOfModifiers:
			for modifier in self.listOfModifiers.keys():
				sbml_modifier = sbml_reaction.createModifier()
				self.listOfModifiers[modifier].writeSbml(sbml_modifier, sbml_level, sbml_version)

		if self.listOfReactants:
			for reactant in self.listOfReactants.keys():
				sbml_reactant = sbml_reaction.createReactant()
				self.listOfReactants[reactant].writeSbml(sbml_reactant, sbml_level, sbml_version)

		if self.listOfProducts:
			for product in self.listOfProducts.keys():
				sbml_product = sbml_reaction.createProduct()
				self.listOfProducts[product].writeSbml(sbml_product, sbml_level, sbml_version)

		if self.kineticLaw is not None:
			kinetic_law = sbml_reaction.createKineticLaw()
			kinetic_law.setMath(self.kineticLaw.definition.getSbmlMathFormula(sbml_level, sbml_version))
			self.listOfLocalParameters.writeSbml(kinetic_law, sbml_level, sbml_version)


	def writeSbmlVariable(self, variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an sbml reaction to a sbml model """

		pass


	def setKineticLaw(self, reaction_type, reversible, parameters=None, math=None):

		self.reversible = reversible

		if reaction_type == KineticLaw.UNDEFINED and math is not None:
			self.kineticLaw = KineticLaw(self.model, self)
			self.kineticLaw.definition.setPrettyPrintMathFormula(math)

		elif parameters is not None:
			if reaction_type == KineticLaw.MASS_ACTION:
				self.kineticLaw = KineticLaw(self.model, self)
				self.kineticLaw.setMassAction(parameters, reversible)

			elif reaction_type == KineticLaw.MICHAELIS:
				self.kineticLaw = KineticLaw(self.model, self)
				self.kineticLaw.setMichaelis(parameters)

			elif reaction_type == KineticLaw.HILL:
				self.kineticLaw = KineticLaw(self.model, self)
				self.kineticLaw.setHill(parameters)

		self.value = self.kineticLaw.definition
		self.constant = False

	def updateKineticLaw(self, kinetic_law):
		""" Update the kinetic law of the reaction """
		self.kineticLaw.definition.setMathFormula(kinetic_law)


	def getKineticLaw(self, math_type=MathFormula.MATH_DEVINTERNAL, forcedConcentration=False):
		""" Returns the kinetic law in the specified format """
		return self.kineticLaw.getMathFormula(math_type, forcedConcentration)


	def getKineticLawDerivative(self, variable, math_type):
		""" Returns the kinetic law's derivative in the specified format """
		return self.kineticLaw.definition.getMathFormulaDerivative(variable, math_type)


	def getReactionDescription(self):
		""" Returns the reaction description """
		lhs = ""
		if len(self.listOfReactants) + len(self.listOfModifiers) > 0:

			for i_reactant, reactant in enumerate(self.listOfReactants.values()):
				if i_reactant > 0:
					lhs += " + "

				if not reactant.stoichiometry.isOne():
					lhs += "%g " % reactant.stoichiometry.getValueMathFormula()

				lhs += reactant.getSpecies().getNameOrSbmlId()

			if len(self.listOfModifiers) > 0:
				for i_modifier, modifier in enumerate(self.listOfModifiers.values()):
					if i_modifier + len(self.listOfReactants) > 0:
						lhs += " + "

					if not modifier.stoichiometry.isOne():
						lhs += "%g " % modifier.stoichiometry.getValueMathFormula()

					lhs += modifier.getSpecies().getNameOrSbmlId()

		rhs = ""
		if len(self.listOfProducts) + len(self.listOfModifiers) > 0:

			for i_product, product in enumerate(self.listOfProducts.values()):
				if i_product > 0:
					rhs += " + "

				if not product.stoichiometry.isOne():
					lhs += "%g " % product.stoichiometry.getValueMathFormula()

				rhs += product.getSpecies().getNameOrSbmlId()

			if len(self.listOfModifiers) > 0:
				for i_modifier, modifier in enumerate(self.listOfModifiers.values()):
					if i_modifier + len(self.listOfProducts) > 0:
						rhs += " + "

					if not modifier.stoichiometry.isOne():
						lhs += "%g " % modifier.stoichiometry.getValueMathFormula()

					rhs += modifier.getSpecies().getNameOrSbmlId()

		if self.reversible == True:
			arrow = " <-> "
		else:
			arrow = " -> "

		return lhs + arrow + rhs

	def getReactionKineticLaw(self):

		if self.kineticLaw is not None:
			if self.kineticLaw.reactionType is None:
				self.kineticLaw.findKineticLaw()

			return self.kineticLaw.reactionTypes[self.kineticLaw.reactionType]


	def getReactionParameters(self):

		if self.kineticLaw is not None:
			if self.kineticLaw.reactionType is None:
				self.kineticLaw.findKineticLaw()
			return self.kineticLaw.getParameters()


	def getReactionType(self):
		""" Returns the reaction type """
		if self.kineticLaw is not None:
			if self.kineticLaw.reactionType is None:
				self.kineticLaw.findKineticLaw()
			return self.kineticLaw.reactionType

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		print "renaming %s in %s in reaction %d" % (old_sbml_id, new_sbml_id, self.objId)
		if self.kineticLaw is not None:
			self.kineticLaw.renameSbmlId(old_sbml_id, new_sbml_id)

		for reactant in self.listOfReactants.values():
			reactant.renameSbmlId(old_sbml_id, new_sbml_id)

		for modifier in self.listOfModifiers.values():
			modifier.renameSbmlId(old_sbml_id, new_sbml_id)

		for product in self.listOfProducts.values():
			product.renameSbmlId(old_sbml_id, new_sbml_id)

	def getODE(self, species, math_type=MathFormula.MATH_INTERNAL, forcedConcentration=False, symbols=False):

		ode = MathFormula.ZERO

		if self.listOfReactants:
			for reactant in self.listOfReactants.values():

				t_ode = MathFormula.ZERO

				if reactant.getSpecies() == species:


					if not symbols:
						t_ode -= self.getKineticLaw(math_type, forcedConcentration)
					else:
						t_ode -= self.symbol.getMathFormula(math_type)

					if not reactant.stoichiometry.isOne():
						t_ode *= reactant.stoichiometry.getMathFormula(math_type)

				ode += t_ode


		if self.listOfProducts:
			for product in self.listOfProducts.values():
				t_ode = MathFormula.ZERO

				if product.getSpecies() == species:

					if not symbols:
						t_ode += self.getKineticLaw(math_type, forcedConcentration)
					else:
						t_ode += self.symbol.getMathFormula(math_type)

					if not product.stoichiometry.isOne():
						t_ode *= product.stoichiometry.getMathFormula(math_type)

				ode += t_ode

		return ode


	# def getODEDerivative(self, species):
	#
	#     ode_der = MathFormula.ZERO
	#
	#     if self.listOfReactants:
	#         for reactant in self.listOfReactants.values():
	#             if reactant.getSpecies() == species:
	#                 ode_der -= self.getKineticLawDerivative(variable)*reactant.stoichiometry.getMathFormulaDerivative(variable)
	#
	#
	#     if self.listOfProducts:
	#         for product in self.listOfProducts.values():
	#             if product.getSpecies() == species:
	#                 ode_der += self.getKineticLawDerivative(variable)*product.stoichiometry.getMathFormulaDerivative(variable)
	#
	#     return ode_der
	#


	def getStoichiometryMatrix(self):

		front = zeros(len(self.model.listOfSpecies),1)

		if self.listOfReactants:
			for reactant in self.listOfReactants.values():
				if not reactant.getSpecies().boundaryCondition:
					front[self.model.listOfSpecies.values().index(reactant.getSpecies())] = -reactant.stoichiometry.getDeveloppedInternalMathFormula()


		if self.listOfProducts:
			for product in self.listOfProducts.values():
				if not product.getSpecies().boundaryCondition:
					front[self.model.listOfSpecies.values().index(product.getSpecies())] = product.stoichiometry.getDeveloppedInternalMathFormula()

		if not self.reversible:
			return front

		else:
			back = zeros(len(self.model.listOfSpecies),1)

			if self.listOfReactants:
				for reactant in self.listOfReactants.values():
					if not reactant.getSpecies().boundaryCondition:
						back[self.model.listOfSpecies.values().index(reactant.getSpecies())] = reactant.stoichiometry.getDeveloppedInternalMathFormula()


			if self.listOfProducts:
				for product in self.listOfProducts.values():
					if not product.getSpecies().boundaryCondition:
						back[self.model.listOfSpecies.values().index(product.getSpecies())] = -product.stoichiometry.getDeveloppedInternalMathFormula()

			return front.col_insert(1,back)



	def getStoichiometryMatrix_v2(self):

		front = [MathFormula(self.model, MathFormula.MATH_ZERO) for _ in self.model.listOfSpecies.keys()]

		if self.listOfReactants:
			for reactant in self.listOfReactants.values():
				if not reactant.getSpecies().boundaryCondition:
					t_formula = MathFormula(self.model)
					t_index = self.model.listOfSpecies.values().index(reactant.getSpecies())
					t_formula.setInternalMathFormula(
							(-reactant.stoichiometry.getDeveloppedInternalMathFormula()
							 + front[t_index].getDeveloppedInternalMathFormula()))

					front[t_index] = t_formula


		if self.listOfProducts:
			for product in self.listOfProducts.values():
				if not product.getSpecies().boundaryCondition:
					t_formula = MathFormula(self.model)
					t_index = self.model.listOfSpecies.values().index(product.getSpecies())
					t_formula.setInternalMathFormula(
							(product.stoichiometry.getDeveloppedInternalMathFormula()
							 + front[t_index].getDeveloppedInternalMathFormula()))
					front[t_index] = t_formula

		if not self.reversible:
			return [front]

		else:
			back = [MathFormula(self.model, MathFormula.MATH_ZERO) for _ in self.model.listOfSpecies.keys()]

			if self.listOfReactants:
				for reactant in self.listOfReactants.values():
					if not reactant.getSpecies().boundaryCondition:
						t_formula = MathFormula(self.model)
						t_index = self.model.listOfSpecies.values().index(reactant.getSpecies())
						t_formula.setInternalMathFormula(
							(reactant.stoichiometry.getDeveloppedInternalMathFormula()
							 + back[t_index].getDeveloppedInternalMathFormula()))

						back[t_index] = t_formula


			if self.listOfProducts:
				for product in self.listOfProducts.values():
					if not product.getSpecies().boundaryCondition:
						t_formula = MathFormula(self.model)
						t_index = self.model.listOfSpecies.values().index(product.getSpecies())
						t_formula.setInternalMathFormula(
							(-product.stoichiometry.getDeveloppedInternalMathFormula()
							 + back[t_index].getDeveloppedInternalMathFormula()))
						back[t_index] = t_formula

			return [front, back]


	def getValueMathFormula(self, math_type=MathFormula.MATH_INTERNAL, forcedConcentration=False):

		if self.kineticLaw is not None:
			return self.kineticLaw.getMathFormula(math_type, forcedConcentration)
