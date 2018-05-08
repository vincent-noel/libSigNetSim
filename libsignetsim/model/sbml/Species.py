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
from __future__ import division

from libsignetsim.model.sbml.EventAssignedVariable import EventAssignedVariable
from libsignetsim.model.sbml.InitiallyAssignedVariable import InitiallyAssignedVariable
from libsignetsim.model.sbml.RuledVariable import RuledVariable
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasUnits import HasUnits
from libsignetsim.model.sbml.HasConversionFactor import HasConversionFactor
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import SympyFloat
from libsignetsim.model.ModelException import InvalidXPath


class Species(SbmlObject, Variable, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable, HasUnits, HasConversionFactor, HasParentObj):

	def __init__(self, model, parent_obj, objId):

		self.__model = model
		self.objId = objId

		HasParentObj.__init__(self, parent_obj)
		Variable.__init__(self, model, Variable.SPECIES)
		SbmlObject.__init__(self, model)
		InitiallyAssignedVariable.__init__(self, model)
		RuledVariable.__init__(self, model)
		EventAssignedVariable.__init__(self, model)
		HasUnits.__init__(self, model)
		HasConversionFactor.__init__(self, model)

		self.__compartment = None
		self.boundaryCondition = False
		self.hasOnlySubstanceUnits = False
		self.isDeclaredConcentration = True
		self.concentrationUnit = None

	def new(self, name=None, compartment=None, value=0, unit=None,
			 constant=False, boundaryCondition=False, hasOnlySubstanceUnits=False):


		if compartment != None:
			self.__compartment = compartment.getSbmlId()

		else:
			if len(self.__model.listOfCompartments) == 0:
				self.__model.listOfCompartments.new("cell")

			self.__compartment = self.__model.listOfCompartments[0].getSbmlId()

		SbmlObject.new(self)
		Variable.new(self, name, Variable.SPECIES)
		HasUnits.new(self, unit)

		self.setValue(value)

		self.constant = constant
		self.boundaryCondition = boundaryCondition
		self.hasOnlySubstanceUnits = hasOnlySubstanceUnits
		self.setUnits(self.__model.getSubstanceUnits())

	def copy(self, obj, sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factor=None):

		self.setCompartment(obj.getCompartment(), sids_subs=sids_subs)

		Variable.copy(self, obj, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factor=conversion_factor)
		SbmlObject.copy(self, obj)
		HasUnits.copy(self, obj, usids_subs=usids_subs)
		HasConversionFactor.copy(self, obj)

		self.constant = obj.constant
		self.boundaryCondition = obj.boundaryCondition
		self.hasOnlySubstanceUnits = obj.hasOnlySubstanceUnits
		self.isDeclaredConcentration = obj.isDeclaredConcentration

	def readSbml(self, sbml_species, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if sbml_level >= 2:
			self.__compartment = sbml_species.getCompartment()
		else:
			self.__compartment = sbml_species.getCompartment()

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

		if sbml_species.isSetBoundaryCondition():
			self.boundaryCondition = sbml_species.getBoundaryCondition()

		elif sbml_level in [1,2]:
			self.boundaryCondition = False

		if sbml_species.isSetConstant():
			self.constant = sbml_species.getConstant()

		elif sbml_level in [1,2]:
			self.constant = False

		if sbml_level >= 3 and sbml_species.isSetConversionFactor():
			HasConversionFactor.readSbml(self, sbml_species.getConversionFactor(), sbml_level, sbml_version)

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
				t_formula.setInternalMathFormula(
					self.value.getInternalMathFormula()/self.getCompartment().symbol.getInternalMathFormula()
				)
				sbml_sp.setInitialConcentration(t_formula.getValueMathFormula())

		if self.boundaryCondition is not None and (sbml_level >= 3 or self.boundaryCondition is not False):
			sbml_sp.setBoundaryCondition(self.boundaryCondition)

		if ((sbml_level == 2 and self.hasOnlySubstanceUnits)
			or sbml_level == 3):
			sbml_sp.setHasOnlySubstanceUnits(self.hasOnlySubstanceUnits)

		if self.constant is not None and (sbml_level == 3 or (sbml_level == 2 and self.constant)):
			sbml_sp.setConstant(self.constant)


		if sbml_level >= 3 and self.isSetConversionFactor():
			HasConversionFactor.writeSbml(self, sbml_sp, sbml_level, sbml_version)

	def isInReactions(self, including_fast_reactions=False, including_modifiers=False):
		""" The purpose of this function is to test is the species's amount
			is actually modified by a reaction. Thus not checking the Modifiers
			makes sense.
		"""

		for i_reaction, reaction in enumerate(self.__model.listOfReactions):
			# print "\n> reaction #%d" % i_reaction
			if not reaction.fast or including_fast_reactions:
				# print "well, first, it's not fast"
				if reaction.listOfReactants:
					for i, reactant in enumerate(reaction.listOfReactants):
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
					for i, product in enumerate(reaction.listOfProducts):
						# print ">>> product #%d : %s" % (i, product.getSpecies().getSbmlId())
						if product.getSpecies() == self:
							return True
				if including_modifiers and reaction.listOfModifiers:
					for i, modifier in enumerate(reaction.listOfModifiers):
						# print ">>> product #%d : %s" % (i, product.getSpecies().getSbmlId())
						if modifier.getSpecies() == self:
							return True
		return False

	def isInFastReactions(self):
		""" The purpose of this function is to test is the species's amount
			is actually modified by a reaction. Thus not checking the Modifiers
			makes sense.
		"""

		for reaction in self.__model.listOfReactions:
				if reaction.listOfReactants:
					for reactant in reaction.listOfReactants:
						if reactant.getSpecies() == self:
							if reaction.fast:
								return True
							else:
								return False

				if reaction.listOfProducts:
					for product in reaction.listOfProducts:
						if product.getSpecies() == self:
							if reaction.fast:
								return True
							else:
								return False

		return False

	def isOnlyInFastReactions(self):
		""" The purpose of this function is to test is the species's amount
			is actually modified by a reaction. Thus not checking the Modifiers
			makes sense.
		"""

		for reaction in self.__model.listOfReactions:
				if reaction.listOfReactants:
					for reactant in reaction.listOfReactants:
						if reactant.getSpecies() == self:
							if not reaction.fast:
								return False

				if reaction.listOfProducts:
					for product in reaction.listOfProducts:
						if product.getSpecies() == self:
							if not reaction.fast:
								return False

		return True

	def getODE(self, including_fast_reactions=True, rawFormula=False, symbols=False):

		t_formula = MathFormula(self.__model)

		if self.constant == True:
			t_formula.setInternalMathFormula(MathFormula.ZERO)
			return t_formula

		elif self.isRateRuled():
			t_rule = self.isRuledBy().getDefinition(rawFormula=rawFormula).getInternalMathFormula()

			if t_rule is None:
				t_rule = MathFormula.ZERO

			if self.hasOnlySubstanceUnits:
				t_formula.setInternalMathFormula(t_rule)

			elif self.getCompartment().isRateRuled() and not t_rule == MathFormula.ZERO:
				""" Then things get complicated. We need to add a term :
					 amount_species * rate_comp / comp
				"""
				t_amount_species = self.symbol.getInternalMathFormula()
				t_comp_rate = self.getCompartment().isRuledBy().getDefinition(rawFormula=rawFormula).getInternalMathFormula()
				t_comp = self.getCompartment().symbol.getInternalMathFormula()

				t_formula.setInternalMathFormula(t_rule + t_amount_species*t_comp_rate/t_comp)
			else:
				t_formula.setInternalMathFormula(t_rule)
			return t_formula

		elif self.isInReactions(including_fast_reactions):

			ode = MathFormula.ZERO

			if not self.boundaryCondition:
				for reaction in self.__model.listOfReactions:
					if not reaction.fast or including_fast_reactions:
						ode += reaction.getODE(self, symbols=symbols, rawFormula=rawFormula).getInternalMathFormula()

			if self.isSetConversionFactor():
				ode *= self.getSymbolConversionFactor()

			elif self.__model.isSetConversionFactor():
				ode *= self.__model.getSymbolConversionFactor()

			t_formula.setInternalMathFormula(ode)
			return t_formula



	def getMathValue(self, rawFormula=False):

		if rawFormula and (self.isDeclaredConcentration or not self.hasOnlySubstanceUnits):
			t_formula = MathFormula(self.__model)
			t_formula.setInternalMathFormula(
				self.value.getInternalMathFormula()/self.getCompartment().symbol.getInternalMathFormula()
			)
			return t_formula
		else:
			return self.value


	def getValue(self):

		if self.isInitialized:
			if self.isDeclaredConcentration:
				return float(self.value.getInternalMathFormula()/self.getCompartment().symbol.getInternalMathFormula())
			else:
				return Variable.getValue(self)


	def setValue(self, value):

		if value is None:
			self.isInitialized = False
			self.value.setInternalMathFormula(None)

		else:
			self.isInitialized = True
			if self.isDeclaredConcentration:

				self.value.setInternalMathFormula(SympyFloat(value)*self.getCompartment().symbol.getInternalMathFormula())
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
			return HasUnits.getUnits(self)
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
			return self.__model.listOfCompartments.getBySbmlId(self.__compartment)

	def setCompartment(self, compartment, sids_subs={}):

		if compartment.getSbmlId() in list(sids_subs.keys()):
			self.__compartment = sids_subs[compartment.getSbmlId()]
		else:
			self.__compartment = compartment.getSbmlId()

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		if self.__compartment == old_sbml_id:
			self.__compartment = new_sbml_id


	def getByXPath(self, xpath):

		if len(xpath) == 0:
			return self

		if len(xpath) > 1:
			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@value":
			return self.getValue()

		elif xpath[0] == "@name":
			return self.getName()

		elif xpath[0] == "@id":
			return self.getSbmlId()


	def setByXPath(self, xpath, object):

		# In this case, we assume it points to the value
		if len(xpath) == 0:
			return self.setValue(object)

		if len(xpath) > 1:
			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@value":
			return self.setValue(object)

		elif xpath[0] == "@name":
			return self.setName(object)

		elif xpath[0] == "@id":
			return self.setSbmlId(object)

		else:
			return InvalidXPath("/".join(xpath))

	def getXPath(self, attribute=None):

		xpath = "sbml:species"
		if self.__model.sbmlLevel == 1:
			xpath += "[@name='%s']" % self.getSbmlId()
		else:
			xpath += "[@id='%s']" % self.getSbmlId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])