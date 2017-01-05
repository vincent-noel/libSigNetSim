#!/usr/bin/env python
""" Species.py


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

from libsignetsim.model.sbml.EventAssignedVariable import EventAssignedVariable
from libsignetsim.model.sbml.InitiallyAssignedVariable import InitiallyAssignedVariable
from libsignetsim.model.sbml.RuledVariable import RuledVariable
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasUnits import HasUnits
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathSymbol import MathSymbol
from libsignetsim.model.math.sympy_shortcuts import *
from libsignetsim.settings.Settings import Settings

from libsbml import formulaToL3String
from sympy import Symbol

class Species(SbmlObject, Variable, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable, HasUnits):

	def __init__ (self, model, objId):

		self.__model = model
		self.objId = objId

		Variable.__init__(self, model, Variable.SPECIES)
		SbmlObject.__init__(self, model)
		InitiallyAssignedVariable.__init__(self, model)
		RuledVariable.__init__(self, model)
		EventAssignedVariable.__init__(self, model)
		HasUnits.__init__(self, model)

		self.__compartment = None
		# self.boundaryCondition = False
		self.hasOnlySubstanceUnits = False
		self.isDeclaredConcentration = True
		self.concentrationUnit = None
		self.conversionFactor = None



	def new(self, name=None, compartment=None, init_value=0, unit=None,
			 constant=False, boundaryCondition=False, hasOnlySubstanceUnits=False):


		if compartment != None:
			self.__compartment = compartment.objId

		else:
			if len(self.__model.listOfCompartments) == 0:
				self.__model.listOfCompartments.new("cell")

			self.__compartment = self.__model.listOfCompartments.values()[0].objId

		SbmlObject.new(self)
		Variable.new(self, name, Variable.SPECIES)
		HasUnits.new(self, unit)


		self.setValue(init_value)

		self.constant = constant
		self.boundaryCondition = boundaryCondition
		self.hasOnlySubstanceUnits = hasOnlySubstanceUnits
		self.setUnits(self.__model.substanceUnits)



	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[], replacements={}):

		self.setCompartment(obj.getCompartment(), prefix, shift, subs, deletions, replacements)

		Variable.copy(self, obj, prefix, shift, subs, deletions, replacements)
		SbmlObject.copy(self, obj, prefix, shift)
		InitiallyAssignedVariable.copy(self, obj, prefix, shift)
		RuledVariable.copy(self, obj, prefix, shift)
		EventAssignedVariable.copy(self, obj, prefix, shift)
		HasUnits.copy(self, obj, prefix, shift)

		self.constant = obj.constant
		self.boundaryCondition = obj.boundaryCondition
		self.hasOnlySubstanceUnits = obj.hasOnlySubstanceUnits
		self.isDeclaredConcentration = obj.isDeclaredConcentration
		if obj.conversionFactor is not None:
			self.conversionFactor = MathFormula(self.__model)
			self.conversionFactor.setInternalMathFormula(obj.conversionFactor.getInternalMathFormula())




	def readSbml(self, sbml_species, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if sbml_level >= 2:
			self.__compartment = self.__model.listOfCompartments.getBySbmlId(sbml_species.getCompartment()).objId
		else:
			self.__compartment = self.__model.listOfCompartments.getByName(sbml_species.getCompartment()).objId

		Variable.readSbml(self, sbml_species, sbml_level, sbml_version)
		SbmlObject.readSbml(self, sbml_species, sbml_level, sbml_version)
		HasUnits.readSbml(self, sbml_species, sbml_level, sbml_version)

		if HasUnits.getUnits(self) is None and self.__model.substanceUnits is not None:
			HasUnits.setUnits(self, self.__model.substanceUnits)


	def readSbmlVariable(self, sbml_species, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		self.symbol.readSbml(sbml_species.getId(), sbml_level, sbml_version)

		if sbml_species.isSetHasOnlySubstanceUnits():
			self.hasOnlySubstanceUnits = sbml_species.getHasOnlySubstanceUnits()

		elif sbml_level in [1,2]:
			self.hasOnlySubstanceUnits = False

		if sbml_species.isSetInitialAmount():
			self.isInitialized = True
			self.isDeclaredConcentration = False
			self.value.readSbml(sbml_species.getInitialAmount(), sbml_level, sbml_version)

		elif sbml_species.isSetInitialConcentration():
			self.isInitialized = True
			self.isDeclaredConcentration = True
			self.value.readSbml(sbml_species.getInitialConcentration(), sbml_level, sbml_version)
			self.value.setInternalMathFormula(self.value.getInternalMathFormula()*self.getCompartment().symbol.getInternalMathFormula())
			# print self.value.getInternalMathFormula()

		if sbml_species.isSetBoundaryCondition():
			self.boundaryCondition = sbml_species.getBoundaryCondition()

		elif sbml_level in [1,2]:
			self.boundaryCondition = False


		if sbml_species.isSetConstant():
			self.constant = sbml_species.getConstant()

		elif sbml_level in [1,2]:
			self.constant = False

		if sbml_level >= 3 and sbml_species.isSetConversionFactor():
			self.conversionFactor = MathFormula(self.__model)
			self.conversionFactor.readSbml(sbml_species.getConversionFactor(), sbml_level, sbml_version)


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		sbml_sp = sbml_model.createSpecies()

		Variable.writeSbml(self, sbml_sp, sbml_level, sbml_version)
		SbmlObject.writeSbml(self, sbml_sp, sbml_level, sbml_version)
		HasUnits.writeSbml(self, sbml_sp, sbml_level, sbml_version)

		sbml_sp.setCompartment(self.getCompartment().getSbmlId())


	def writeSbmlVariable(self, sbml_sp, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if self.isInitialized:
			t_value = self.value.getSbmlMathFormula(sbml_level, sbml_version)
			if not self.isDeclaredConcentration:
				sbml_sp.setInitialAmount(t_value.getValue())
			else:
				t_formula = MathFormula(self.__model)
				t_formula.setInternalMathFormula(self.value.getInternalMathFormula()/self.getCompartment().symbol.getInternalMathFormula())
				sbml_sp.setInitialConcentration(t_formula.getValueMathFormula())

		if self.boundaryCondition is not None and (sbml_level >= 3 or self.boundaryCondition is not False):
			sbml_sp.setBoundaryCondition(self.boundaryCondition)

		if ((sbml_level == 2 and self.hasOnlySubstanceUnits)
			or sbml_level == 3):
			sbml_sp.setHasOnlySubstanceUnits(self.hasOnlySubstanceUnits)

		if self.constant is not None and (sbml_level == 3 or (sbml_level == 2 and self.constant)):
			sbml_sp.setConstant(self.constant)


		if sbml_level >= 3 and self.conversionFactor is not None:
			sbml_sp.setConversionFactor(formulaToL3String(
				self.conversionFactor.writeSbml(sbml_level, sbml_version)))



	def isInReactions(self, including_fast_reactions=False):
		""" The purpose of this function is to test is the species's amount
			is actually modified by a reaction. Thus not checking the Modifiers
			makes sense.
		"""

		# print "> Entering isInReactions : %s" % self.getSbmlId()

		for i_reaction, reaction in enumerate(self.__model.listOfReactions.values()):
			# print "\n> reaction #%d" % i_reaction
			if not reaction.fast or including_fast_reactions:
				# print "well, first, it's not fast"
				if reaction.listOfReactants:
					for i, reactant in enumerate(reaction.listOfReactants.values()):
						# print ">>> reactant #%d : %s" % (i, reactant.getSpecies().getSbmlId())
						if reactant.getSpecies() == self:
							return True

				# # TODO
				# # This might break some stuff, needs to pass the sbml test suite
				# if reaction.listOfModifiers:
				#     for modifier in reaction.listOfModifiers.values():
				#         if modifier.getSpecies() == self:
				#             return True

				if reaction.listOfProducts:
					for i, product in enumerate(reaction.listOfProducts.values()):
						# print ">>> product #%d : %s" % (i, product.getSpecies().getSbmlId())
						if product.getSpecies() == self:
							return True

		return False


	def isInFastReactions(self):
		""" The purpose of this function is to test is the species's amount
			is actually modified by a reaction. Thus not checking the Modifiers
			makes sense.
		"""

		for reaction in self.__model.listOfReactions.values():
				if reaction.listOfReactants:
					for reactant in reaction.listOfReactants.values():
						if reactant.getSpecies() == self:
							if reaction.fast:
								return True
							else:
								return False

				if reaction.listOfProducts:
					for product in reaction.listOfProducts.values():
						if product.getSpecies() == self:
							if reaction.fast:
								return True
							else:
								return False

		return False


	def getODE(self, including_fast_reactions=True, forcedConcentration=False, symbols=False):

		t_formula = MathFormula(self.__model)

		if self.constant == True:
			t_formula.setInternalMathFormula(MathFormula.ZERO)
			return t_formula

		elif self.isRateRuled():
			t_rule = self.isRuledBy().getDefinition(forcedConcentration).getInternalMathFormula()

			if self.getCompartment().isRateRuled() and not t_rule == MathFormula.ZERO:
				""" Then things get complicated. We need to add a term :
					 amount_species * rate_comp / comp
				"""
				t_formula_corrector = MathFormula(self.__model)
				t_amount_species = self.symbol.getInternalMathFormula()
				t_comp_rate = self.getCompartment().isRuledBy().getDefinition(forcedConcentration).getInternalMathFormula()
				t_comp = self.getCompartment().symbol.getInternalMathFormula()

				t_formula.setInternalMathFormula(t_rule + t_amount_species*t_comp_rate/t_comp)
			else:
				t_formula.setInternalMathFormula(t_rule)
			return t_formula

		elif self.isInReactions(including_fast_reactions):

			ode = MathFormula.ZERO

			if not self.boundaryCondition:
				for reaction in self.__model.listOfReactions.values():
					if not reaction.fast or including_fast_reactions:
						ode += reaction.getODE(self, forcedConcentration, symbols).getInternalMathFormula()

			if self.conversionFactor is not None:
				ode *= self.conversionFactor.getInternalMathFormula()

			elif self.__model.conversionFactor is not None:
				ode *= self.__model.conversionFactor.getInternalMathFormula()

			t_formula.setInternalMathFormula(ode)
			return t_formula



	def getMathValue(self, forcedConcentration=False):

		if forcedConcentration and (self.isDeclaredConcentration or not self.hasOnlySubstanceUnits):
			t_formula = MathFormula(self.__model)
			t_formula.setInternalMathFormula(self.value.getInternalMathFormula()/self.getCompartment().symbol.getInternalMathFormula())
			return t_formula
		else:
			return self.value


	def getValue(self):

		if self.isDeclaredConcentration:
			return float(self.value.getInternalMathFormula()/self.getCompartment().symbol.getInternalMathFormula())
		else:
			return Variable.getValue(self)


	def setValue(self, value):
		self.isInitialized = True

		if self.isDeclaredConcentration:
			self.value.setInternalMathFormula(value*self.getCompartment().symbol.getInternalMathFormula())
		else:
			Variable.setValue(self, value)


	def hasUnits(self):

		if self.hasOnlySubstanceUnits:
			return HasUnits.hasUnits(self)
		else:
			return HasUnits.hasUnits(self) and self.getCompartment().hasUnits()



	def setUnits(self, unit, prefix=""):

		if unit is not None:
			if self.hasOnlySubstanceUnits:
				HasUnits.setUnits(self, unit, prefix)
			else:
				if unit is not None and self.getCompartment().getUnits() is not None:
					HasUnits.setUnits(self, self.__model.listOfUnitDefinitions.getAmountUnit(unit,
														self.getCompartment().getUnits()), prefix)

	def getUnits(self):

		if self.hasOnlySubstanceUnits:
			return self.unit
		else:
			if self.concentrationUnit is None:
				if HasUnits.getUnits(self) is not None and self.getCompartment().getUnits() is not None:
					self.concentrationUnit = self.__model.listOfUnitDefinitions.getConcentrationUnit(HasUnits.getUnits(self),
															self.getCompartment().getUnits())
					return self.concentrationUnit
			else:
				return self.concentrationUnit


	def getCompartment(self):
		if self.__compartment is not None:
			return self.__model.listOfCompartments[self.__compartment]

	def setCompartment(self, compartment, prefix="", shift=0, subs={}, deletions=[], replacements={}):

		t_symbol = Symbol(compartment.getSbmlId())
		if t_symbol in subs.keys():
			t_sbml_id = str(subs[t_symbol])
			tt_symbol = Symbol(t_sbml_id)
			if tt_symbol in replacements.keys():
				t_sbml_id = str(replacements[tt_symbol])
		else:
			t_sbml_id = prefix+compartment.getSbmlId()

		self.__compartment = self.__model.listOfCompartments.getBySbmlId(t_sbml_id).objId
