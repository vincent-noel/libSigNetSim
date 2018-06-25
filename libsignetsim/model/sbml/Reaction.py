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

from libsignetsim.model.sbml.container.ListOfParameters import ListOfParameters
from libsignetsim.model.sbml.container.ListOfSpeciesReference import ListOfSpeciesReference

from libsignetsim.model.sbml.KineticLaw import KineticLaw
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from libsignetsim.model.sbml.HasUnits import HasUnits
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.settings.Settings import Settings
from sympy import zeros
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from libsignetsim.model.ModelException import InvalidXPath


class Reaction(Variable, SbmlObject, HasUnits, HasParentObj):
	""" Parent class for Sbml reaction """


	def __init__ (self, model, parent_obj, obj_id, name=None, reaction_type=KineticLaw.UNDEFINED):

		self.__model = model
		self.objId = obj_id

		HasUnits.__init__(self, model)
		Variable.__init__(self, model, Variable.REACTION)
		SbmlObject.__init__(self, model)
		HasParentObj.__init__(self, parent_obj)

		self.reversible = True
		self.fast = False
		self.reactionType = reaction_type

		self.kineticLaw = None

		self.listOfReactants = ListOfSpeciesReference(model)
		self.listOfModifiers = ListOfSpeciesReference(model)
		self.listOfProducts = ListOfSpeciesReference(model)
		self.listOfLocalParameters = ListOfParameters(model, self, are_local_parameters=True, reaction=self)


	def new(self, name=None):

		Variable.new(self, name, Variable.REACTION)
		self.kineticLaw = KineticLaw(self.__model, self)
		SbmlObject.new(self)

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs=[], usids_subs={}, conversion_factors={},
			extent_conversion=None, time_conversion=None):

		HasUnits.copy(self, obj, usids_subs=usids_subs)
		SbmlObject.copy(self, obj)
		Variable.copy(self, obj, sids_subs=sids_subs, symbols_subs=symbols_subs)

		if obj.listOfReactants not in deletions and len(obj.listOfReactants) > 0:
			self.listOfReactants.copy(
				obj.listOfReactants,
				deletions=deletions,
				sids_subs=sids_subs,
				symbols_subs=symbols_subs
			)
		if obj.listOfModifiers not in deletions and len(obj.listOfModifiers) > 0:
			self.listOfModifiers.copy(
				obj.listOfModifiers,
				deletions=deletions,
				sids_subs=sids_subs,
				symbols_subs=symbols_subs
			)
		if obj.listOfProducts not in deletions and len(obj.listOfProducts) > 0:
			self.listOfProducts.copy(
				obj.listOfProducts,
				deletions=deletions,
				sids_subs=sids_subs,
				symbols_subs=symbols_subs
			)

		if obj.listOfLocalParameters not in deletions and len(obj.listOfLocalParameters) > 0:
			self.listOfLocalParameters.copy(
				obj.listOfLocalParameters,
				deletions=deletions,
				sids_subs=sids_subs,
				symbols_subs=symbols_subs,
				usids_subs=usids_subs
			)

		# Here we need to add the deleted local parameters to the symbols subs, because they were promoted
		for local_param in obj.listOfLocalParameters:
			if local_param in deletions and local_param.symbol.getSymbol() not in symbols_subs:
				new_symbol = symbols_subs[SympySymbol(local_param.getSbmlId())]
				symbols_subs.update({local_param.symbol.getSymbol(): new_symbol})

		if obj.kineticLaw is not None:
			self.kineticLaw = KineticLaw(self.__model, self)
			self.kineticLaw.copy(
				obj,
				symbols_subs=symbols_subs,
				conversion_factors=conversion_factors,
				extent_conversion=extent_conversion,
				time_conversion=time_conversion)

			self.value = MathFormula(self.__model)
			t_formula = self.kineticLaw.getDefinition(rawFormula=True).getInternalMathFormula()

			if extent_conversion is not None:
				t_formula /= extent_conversion.getInternalMathFormula()

			if time_conversion is not None:
				t_formula *= time_conversion.getInternalMathFormula()

			self.value.setInternalMathFormula(t_formula)
			self.constant = obj.constant

		self.reversible = obj.reversible
		self.fast = obj.fast

	def readSbml(self, reaction, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads an sbml reaction from sbml model """

		if sbml_level < 3:
			self.setUnits(self.__model.substanceUnits)
		else:
			self.setUnits(self.__model.extentUnits)

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
			self.kineticLaw = KineticLaw(self.__model, self)
			self.kineticLaw.readSbml(reaction.getKineticLaw().getMath(),
										sbml_level, sbml_version)

		Variable.readSbml(self, reaction, sbml_level, sbml_version)


	def readSbmlVariable(self, variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		# variable id
		self.symbol.readSbml(variable.getId(), sbml_level, sbml_version)

		# self.isInitialized = True
		if self.kineticLaw is not None:
			self.value = self.kineticLaw.getDefinition(rawFormula=True)
			self.constant = False
		else:
			self.constant = True


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an sbml reaction to a sbml model """

		sbml_reaction = sbml_model.createReaction()

		Variable.writeSbml(self, sbml_reaction, sbml_level, sbml_version)
		SbmlObject.writeSbml(self, sbml_reaction, sbml_level, sbml_version)

		if (sbml_level < 3 and not self.reversible) or sbml_level == 3:
			sbml_reaction.setReversible(self.reversible)

		if (sbml_level < 3 and self.fast) or (sbml_level == 3 and sbml_version == 1):
			sbml_reaction.setFast(self.fast)
		else:
			sbml_reaction.setFast(False)

		if self.listOfModifiers:
			for modifier in self.listOfModifiers:
				sbml_modifier = sbml_reaction.createModifier()
				modifier.writeSbml(sbml_modifier, sbml_level, sbml_version)

		if self.listOfReactants:
			for reactant in self.listOfReactants:
				sbml_reactant = sbml_reaction.createReactant()
				reactant.writeSbml(sbml_reactant, sbml_level, sbml_version)

		if self.listOfProducts:
			for product in self.listOfProducts:
				sbml_product = sbml_reaction.createProduct()
				product.writeSbml(sbml_product, sbml_level, sbml_version)

		if self.kineticLaw is not None:
			kinetic_law = sbml_reaction.createKineticLaw()
			kinetic_law.setMath(self.kineticLaw.getDefinition(rawFormula=True).getSbmlMathFormula(sbml_level, sbml_version))
			self.listOfLocalParameters.writeSbml(kinetic_law, sbml_level, sbml_version)


	def writeSbmlVariable(self, variable, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an sbml reaction to a sbml model """

		pass


	def __str__(self):

		return self.getReactionDescription() + " (" + str(self.kineticLaw.getDefinition().getInternalMathFormula() )+ ")"

	def setKineticLaw(self, reaction_type, reversible, parameters=None, math=None):

		self.reversible = reversible

		if reaction_type == KineticLaw.UNDEFINED and math is not None:
			self.kineticLaw = KineticLaw(self.__model, self)
			self.kineticLaw.setPrettyPrintMathFormula(math, forcedConcentration=True)

		elif parameters is not None:
			if reaction_type == KineticLaw.MASS_ACTION:
				self.kineticLaw = KineticLaw(self.__model, self)
				self.kineticLaw.setMassAction(parameters, reversible)

			elif reaction_type == KineticLaw.MICHAELIS:
				self.kineticLaw = KineticLaw(self.__model, self)
				self.kineticLaw.setMichaelis(parameters)

			elif reaction_type == KineticLaw.HILL:
				self.kineticLaw = KineticLaw(self.__model, self)
				self.kineticLaw.setHill(parameters)

		self.value = self.kineticLaw.getDefinition()
		self.constant = False

	def updateKineticLaw(self, kinetic_law):
		""" Update the kinetic law of the reaction """
		self.kineticLaw.getDefinition().setMathFormula(kinetic_law)


	def getKineticLaw(self, math_type=MathFormula.MATH_DEVINTERNAL, forcedConcentration=False):
		""" Returns the kinetic law in the specified format """
		return self.kineticLaw.getMathFormula(math_type, forcedConcentration)


	def getKineticLawDerivative(self, variable, math_type):
		""" Returns the kinetic law's derivative in the specified format """
		return self.kineticLaw.getDefinition().getMathFormulaDerivative(variable, math_type)


	def getReactionDescription(self):
		""" Returns the reaction description """
		lhs = ""
		if len(self.listOfReactants) + len(self.listOfModifiers) > 0:

			for i_reactant, reactant in enumerate(self.listOfReactants):
				if i_reactant > 0:
					lhs += " + "

				if not reactant.stoichiometry.isOne():
					lhs += "%g " % reactant.stoichiometry.getValueMathFormula()

				lhs += reactant.getSpecies().getNameOrSbmlId()

			if len(self.listOfModifiers) > 0:
				for i_modifier, modifier in enumerate(self.listOfModifiers):
					if i_modifier + len(self.listOfReactants) > 0:
						lhs += " + "

					if not modifier.stoichiometry.isOne():
						lhs += "%g " % modifier.stoichiometry.getValueMathFormula()

					lhs += modifier.getSpecies().getNameOrSbmlId()

		rhs = ""
		if len(self.listOfProducts) + len(self.listOfModifiers) > 0:

			for i_product, product in enumerate(self.listOfProducts):
				if i_product > 0:
					rhs += " + "

				if not product.stoichiometry.isOne():
					lhs += "%g " % product.stoichiometry.getValueMathFormula()

				rhs += product.getSpecies().getNameOrSbmlId()

			if len(self.listOfModifiers) > 0:
				for i_modifier, modifier in enumerate(self.listOfModifiers):
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

		if self.kineticLaw is not None:
			self.kineticLaw.renameSbmlId(old_sbml_id, new_sbml_id)

		# if the stoichiometry is a variable,then it's in the list of variables
		# if it isn't, then there shouldn't be anything to rename

		for reactant in self.listOfReactants:
			reactant.renameSbmlId(old_sbml_id, new_sbml_id)

		for modifier in self.listOfModifiers:
			modifier.renameSbmlId(old_sbml_id, new_sbml_id)

		for product in self.listOfProducts:
			product.renameSbmlId(old_sbml_id, new_sbml_id)


	def getODE(self, species, rawFormula=False, symbols=False):

		ode = MathFormula.ZERO

		if self.listOfReactants:

			for reactant in self.listOfReactants:

				t_ode = MathFormula.ZERO

				if reactant.getSpecies() == species:

					if not symbols:
						t_ode -= self.kineticLaw.getDefinition(rawFormula=rawFormula).getInternalMathFormula()
					else:
						t_ode -= self.symbol.getInternalMathFormula()

					if not reactant.stoichiometry.isOne():
						t_ode *= reactant.stoichiometry.getInternalMathFormula()

				ode += t_ode


		if self.listOfProducts:
			for product in self.listOfProducts:
				t_ode = MathFormula.ZERO

				if product.getSpecies() == species:

					if not symbols:
						t_ode += self.kineticLaw.getDefinition(rawFormula=rawFormula).getInternalMathFormula()
					else:
						t_ode += self.symbol.getInternalMathFormula()

					if not product.stoichiometry.isOne():
						t_ode *= product.stoichiometry.getInternalMathFormula()

				ode += t_ode

		t_formula = MathFormula(self.__model)
		t_formula.setInternalMathFormula(ode)

		return t_formula

	def getStoichiometryMatrix(self, subs={}, including_fast_reactions=True, including_slow_reactions=True, include_variable_stoichiometry=False):

		front = zeros(self.__model.nbOdes, 1)

		if (
			(not self.hasVariableStoichiometry() or include_variable_stoichiometry) and
			(
				(self.fast and including_fast_reactions)
				or (not self.fast and including_slow_reactions)
			)
		):
			if self.listOfReactants:
				for reactant in self.listOfReactants:
					if not reactant.getSpecies().boundaryCondition:
						index = reactant.getSpecies().ind
						stoichiometry = unevaluatedSubs(
							reactant.stoichiometry.getDeveloppedInternalMathFormula(),
							subs
						)
						front[index] = -stoichiometry + front[index]

			if self.listOfProducts:
				for product in self.listOfProducts:
					if not product.getSpecies().boundaryCondition:
						index = product.getSpecies().ind
						stoichiometry = unevaluatedSubs(
							product.stoichiometry.getDeveloppedInternalMathFormula(),
							subs
						)
						front[index] = stoichiometry + front[index]


		if not self.kineticLaw.isReversible(self.kineticLaw.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula()):
			return front

		else:
			back = zeros(self.__model.nbOdes, 1)
			if (
				(not self.hasVariableStoichiometry() or include_variable_stoichiometry) and
				(
					(self.fast and including_fast_reactions)
					or (not self.fast and including_slow_reactions)
				)
			):
				if self.listOfReactants:
					for reactant in self.listOfReactants:
						if not reactant.getSpecies().boundaryCondition:
							index = reactant.getSpecies().ind
							stoichiometry = unevaluatedSubs(
								reactant.stoichiometry.getDeveloppedInternalMathFormula(),
								subs
							)
							back[index] = stoichiometry + back[index]

				if self.listOfProducts:
					for product in self.listOfProducts:
						if not product.getSpecies().boundaryCondition:
							index = product.getSpecies().ind
							stoichiometry = unevaluatedSubs(
								product.stoichiometry.getDeveloppedInternalMathFormula(),
								subs
							)
							back[index] = -stoichiometry + back[index]

			return front.row_join(back)

	def hasVariableStoichiometry(self):
		return self.listOfReactants.hasVariableStoichiometry() or self.listOfProducts.hasVariableStoichiometry()

	def isReactant(self, species):

		for reactant in self.listOfReactants:
			if reactant.getSpecies() == species:
				return True

		return False

	def isProduct(self, species):

		for product in self.listOfProducts:
			if product.getSpecies() == species:
				return True

		return False

	def containsVariable(self, variable):

		return (
			variable.symbol.getInternalMathFormula() in self.kineticLaw.getDefinition(rawFormula=True).getDeveloppedInternalMathFormula().atoms()
		)

	def getByXPath(self, xpath):

		if len(xpath) == 0:
			return self

		if len(xpath) > 1:
			if xpath[0] in ["sbml:listOfParameters", "listOfParameters"]:
				return self.listOfLocalParameters.getByXPath(xpath[1:])

			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@value":
			return self.getValue()

		elif xpath[0] == "@name":
			return self.getName()

		elif xpath[0] == "@id":
			return self.getSbmlId()

	def getXPath(self, attribute=None):

		xpath = "sbml:reaction"
		if self.__model.sbmlLevel == 1:
			xpath += "[@name='%s']" % self.getSbmlId()
		else:
			xpath += "[@id='%s']" % self.getSbmlId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])

	def isValid(self):
		return self.kineticLaw.getDefinition() is not None

	def getCompartment(self):
		if len(self.listOfReactants) > 0:
			return self.listOfReactants[0].getSpecies().getCompartment()
		elif len(self.listOfProducts) > 0:
			return self.listOfProducts[0].getSpecies().getCompartment()
