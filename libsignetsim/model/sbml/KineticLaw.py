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

from libsignetsim.model.math.MathFormula import MathFormula
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
from libsignetsim.model.sbml.KineticLawIdentifier import KineticLawIdentifier
from libsignetsim.settings.Settings import Settings

from sympy import simplify, srepr, diff, zeros, pretty
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

class KineticLaw(KineticLawIdentifier):

	def __init__(self, model, isFromReaction):

		self.__model = model
		self.__definition = MathFormula(model, MathFormula.MATH_KINETICLAW, isFromReaction)
		KineticLawIdentifier.__init__(self, model, isFromReaction)

	def copy(self, obj, symbols_subs={}, conversion_factors={}, extent_conversion=None, time_conversion=None):

		t_convs = {}
		for var, conversion in list(conversion_factors.items()):
			t_convs.update({var: var/conversion})

		t_formula = unevaluatedSubs(obj.kineticLaw.getDefinition().getInternalMathFormula(), symbols_subs)
		t_formula = unevaluatedSubs(t_formula, t_convs)

		if extent_conversion is not None:
			t_formula *= extent_conversion.getInternalMathFormula()

		if time_conversion is not None:
			t_formula /= time_conversion.getInternalMathFormula()

		self.__definition.setInternalMathFormula(t_formula)

	def readSbml(self, sbml_math,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		self.__definition.readSbml(sbml_math, sbml_level, sbml_version)
		self.__definition.setInternalMathFormula(self.__definition.ensureFloat(self.__definition.getInternalMathFormula()))
		# And the we should look for the Kinetic law Here
		# But since it may take time, we will do it on demand
		# KineticLawIdentifier.findKineticLaw(self)

	def getRawDefinition(self, rawFormula=False):

		formula = self.__definition.getInternalMathFormula()

		if formula is not None:
			if (not rawFormula and len(self.reaction.listOfReactants) > 0
				and self.reaction.listOfReactants[0].getSpecies().isConcentration()):
				comp = self.reaction.listOfReactants[0].getSpecies().getCompartment()

				formula = SympyMul(
					formula,
					SympyPow(
						comp.symbol.getInternalMathFormula(),
						SympyInteger(-1),
						evaluate=False
					),
					evaluate=False
				)

			if not rawFormula:
				subs = {}
				for species in self.__model.listOfSpecies:
					if species.isConcentration():
						subs.update({species.symbol.getInternalMathFormula(rawFormula=True): species.symbol.getInternalMathFormula()})
				formula = unevaluatedSubs(formula, subs)
		return simplify(formula)


	def getDefinition(self, rawFormula=False):
		""" Getting the kinetic's law definition. It follows the sbml specification's type of kinetic law, 
			aka in substance units. rawFormula = True will return that (all rowFormula will work on substances"
			So it rawFormula is false, we must divide by the compartment. We must also switch all concentration 
			symbols with simple species symbols
		"""

		math_formula = MathFormula(self.__model, MathFormula.MATH_KINETICLAW)
		math_formula.setInternalMathFormula(self.getRawDefinition(rawFormula=rawFormula))
		return math_formula

	def setPrettyPrintMathFormula(self, definition, forcedConcentration=False):

		if (forcedConcentration and len(self.reaction.listOfReactants) > 0
			and self.reaction.listOfReactants[0].getSpecies().isConcentration()):
			t_comp = self.reaction.listOfReactants[0].getSpecies().getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_KINETICLAW)
			t_math_formula.setPrettyPrintMathFormula(definition, forcedConcentration)
			self.__definition.setInternalMathFormula(t_math_formula.getInternalMathFormula()*t_comp.symbol.getInternalMathFormula())

		else:
			self.__definition.setPrettyPrintMathFormula(definition, forcedConcentration)

		if self.reaction.value is None:
			self.reaction.value = MathFormula(self.__model)
		self.reaction.value.setInternalMathFormula(self.__definition.getInternalMathFormula())


	def getPrettyPrintMathFormula(self):

		if len(self.reaction.listOfReactants) > 0:
			first_reactant = self.reaction.listOfReactants[0].getSpecies()
			if first_reactant.isConcentration():
				t_comp = first_reactant.getCompartment()
				t_math_formula = MathFormula(self.__model, MathFormula.MATH_KINETICLAW)
				t_math_formula.setInternalMathFormula(
					self.__definition.getInternalMathFormula() / t_comp.symbol.getInternalMathFormula()
				)
				t_math_formula = t_math_formula.getPrettyPrintMathFormula()
			else:
				t_math_formula = self.__definition.getPrettyPrintMathFormula()
		else:
			t_math_formula = self.__definition.getPrettyPrintMathFormula()

		if len(self.reaction.listOfLocalParameters) > 0:
			t_math_formula = t_math_formula.replace("_local_%d_" % (self.reaction.objId), "")

		for species in self.__model.listOfSpecies:
			if species.isConcentration():
				t_math_formula = t_math_formula.replace(("_speciesForcedConcentration_%s_" % (species.symbol.getInternalMathFormula())), species.getSbmlId())

		return t_math_formula


	def getReactantsFormula(self):

		t_reactants = 1
		for reactant in self.reaction.listOfReactants:

			t_reactants *= reactant.getSpecies().symbol.getInternalMathFormula(rawFormula=True)

			if not reactant.stoichiometry.isOne():
				t_reactants *= reactant.stoichiometry.getInternalMathFormula(rawFormula=True)

		return t_reactants


	def getModifiersFormula(self):

		t_modifiers = 1
		for modifier in self.reaction.listOfModifiers:
			t_modifiers *= modifier.getSpecies().symbol.getInternalMathFormula(rawFormula=True)

			if not modifier.stoichiometry.isOne():
				t_modifiers *= modifier.stoichiometry.getInternalMathFormula(rawFormula=True)

		return t_modifiers


	def getProductsFormula(self):

		t_products = 1
		for product in self.reaction.listOfProducts:
			t_products *= product.getSpecies().symbol.getInternalMathFormula(rawFormula=True)

			if not product.stoichiometry.isOne():
				t_products *= product.stoichiometry.getInternalMathFormula(rawFormula=True)

		return t_products


	def setMassAction(self, parameters, reversible):

		t_reactants = self.getReactantsFormula()
		t_modifiers = self.getModifiersFormula()

		t_formula = t_reactants*t_modifiers
		t_formula *= parameters[0].symbol.getInternalMathFormula()

		if reversible:
			t_products = self.getProductsFormula()
			t_formula_back = t_modifiers*t_products
			t_formula_back *= parameters[1].symbol.getInternalMathFormula()

			t_formula -= t_formula_back

		if len(self.reaction.listOfReactants) > 0:
			first_reactant = self.reaction.listOfReactants[0].getSpecies()
			if not first_reactant.hasOnlySubstanceUnits:
				t_formula *= first_reactant.getCompartment().symbol.getInternalMathFormula()

		elif len(self.reaction.listOfModifiers) > 0:
			first_modifier = self.reaction.listOfModifiers[0].getSpecies()
			if not first_modifier.hasOnlySubstanceUnits:
				t_formula *= first_modifier.getCompartment().symbol.getInternalMathFormula()

		self.__definition.setInternalMathFormula(simplify(t_formula))


	def setMichaelis(self, parameters):

		t_reactants = self.getReactantsFormula()
		t_modifiers = self.getModifiersFormula()

		t_kcat = parameters[0].symbol.getInternalMathFormula()
		t_km = parameters[1].symbol.getInternalMathFormula()

		t_formula = t_kcat*t_reactants*t_modifiers/(t_reactants + t_km)

		if len(self.reaction.listOfReactants) > 0:
			first_reactant = self.reaction.listOfReactants[0].getSpecies()
			if not first_reactant.hasOnlySubstanceUnits:
				t_formula *= first_reactant.getCompartment().symbol.getInternalMathFormula()

		elif len(self.reaction.listOfModifiers) > 0:
			first_modifier = self.reaction.listOfModifiers[0].getSpecies()
			if not first_modifier.hasOnlySubstanceUnits:
				t_formula *= first_modifier.getCompartment().symbol.getInternalMathFormula()

		self.__definition.setInternalMathFormula(simplify(t_formula))



	def setHill(self, parameters):

		t_reactants = self.getReactantsFormula()
		t_modifiers = self.getModifiersFormula()

		t_kcat = parameters[0].symbol.getInternalMathFormula()
		t_kd = parameters[1].symbol.getInternalMathFormula()
		t_n = parameters[2].symbol.getInternalMathFormula()

		t_r_pow = t_reactants**t_n
		t_formula = t_kcat*t_modifiers*t_r_pow/(t_r_pow + t_kd)

		if len(self.reaction.listOfReactants) > 0:
			first_reactant = self.reaction.listOfReactants[0].getSpecies()
			if not first_reactant.hasOnlySubstanceUnits:
				t_formula *= first_reactant.getCompartment().symbol.getInternalMathFormula()

		elif len(self.reaction.listOfModifiers) > 0:
			first_modifier = self.reaction.listOfModifiers[0].getSpecies()
			if not first_modifier.hasOnlySubstanceUnits:
				t_formula *= first_modifier.getCompartment().symbol.getInternalMathFormula()

		self.__definition.setInternalMathFormula(simplify(t_formula))

	def getRawVelocities(self, subs={}, include_fast_reaction=True, include_slow_reaction=True):

		definition = self.__definition.getDeveloppedInternalMathFormula()
		if not KineticLawIdentifier.isReversible(self, definition):
			res = zeros(1)
			if (self.reaction.fast and include_fast_reaction) or (not self.reaction.fast and include_slow_reaction):
				res[0] += unevaluatedSubs(definition, subs)
			return res

		else:
			res_front = zeros(1)
			res_backward = zeros(1)
			if (self.reaction.fast and include_fast_reaction) or (not self.reaction.fast and include_slow_reaction):
				(definition_front, definition_back) = KineticLawIdentifier.getReversibleRates(self, definition)
				res_front[0] += unevaluatedSubs(definition_front, subs)
				res_backward[0] += unevaluatedSubs(definition_back, subs)

			return res_front.col_join(res_backward)

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		self.__definition.renameSbmlId(
			"_local_%d_%s" % (self.reaction.objId, old_sbml_id),
			"_local_%d_%s" % (self.reaction.objId, new_sbml_id)
		)
		self.__definition.renameSbmlId(old_sbml_id, new_sbml_id)
