#!/usr/bin/env python
""" MathKineticLaw.py


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
from libsignetsim.model.math.KineticLawIdentifier import KineticLawIdentifier
from libsignetsim.settings.Settings import Settings

from sympy import simplify, srepr


class MathKineticLaw(MathFormula, KineticLawIdentifier):

	def __init__(self, model, isFromReaction):

		self.__model = model
		MathFormula.__init__(self, model,
								MathFormula.MATH_KINETICLAW, isFromReaction)
		KineticLawIdentifier.__init__(self, model, isFromReaction)




	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[],
				replacements={}, conversions={},
				extent_conversion=None, time_conversion=None):

		t_convs = {}
		for var, conversion in conversions.items():
			t_convs.update({var:var/conversion})

		t_formula = obj.kineticLaw.getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs)

		if extent_conversion is not None:
			t_formula *= extent_conversion.getInternalMathFormula()

		if time_conversion is not None:
			t_formula /= time_conversion.getInternalMathFormula()

		MathFormula.setInternalMathFormula(self, t_formula)

	def readSbml(self, sbml_math,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		MathFormula.readSbml(self, sbml_math, sbml_level, sbml_version)
		# And the we should look for the Kinetic law Here
		# But since it may take time, we will do it on demand
		# KineticLawIdentifier.findKineticLaw(self)
		# print "reading kinetic law"
		# print MathFormula.getInternalMathFormula(self)

	def getMathFormula(self, math_type, forcedConcentration=False):

		t_formula = MathFormula(self.__model, MathFormula.MATH_KINETICLAW)

		if forcedConcentration and len(self.reaction.listOfReactants) > 0:
				first_reactant = self.reaction.listOfReactants[0].getSpecies()
				if first_reactant.isConcentration():
					t_comp = first_reactant.getCompartment()
					t_formula.setInternalMathFormula((
								MathFormula.getInternalMathFormula(self)
								/ t_comp.symbol.getInternalMathFormula()))

		else:
			t_formula.setInternalMathFormula(MathFormula.getInternalMathFormula(self))

		# print "\n getMathFormula from kinetic law : " + str(forcedConcentration)
		# print t_formula.getInternalMathFormula()

		if forcedConcentration:
			for species in self.__model.listOfSpecies.values():
				if species.isConcentration():
					t_internal = MathFormula.getInternalMathFormula(t_formula)
					t_fc = SympySymbol("_speciesForcedConcentration_%s_" % str(species.symbol.getInternalMathFormula()))
					t_species = SympySymbol(species.getSbmlId())
					t_internal = t_internal.subs({ t_fc : t_species })
					t_formula.setInternalMathFormula(t_internal)

		# print t_formula.getInternalMathFormula()

		return MathFormula.getMathFormula(t_formula, math_type)

	def setPrettyPrintMathFormula(self, definition):

		if len(self.reaction.listOfReactants) > 0:
			first_reactant = self.reaction.listOfReactants[0].getSpecies()
			if first_reactant.isConcentration():
				t_comp = first_reactant.getCompartment()
				t_math_formula = MathFormula(self.__model, MathFormula.MATH_KINETICLAW)
				t_math_formula.setPrettyPrintMathFormula(definition)
				MathFormula.setInternalMathFormula(self, t_math_formula.getInternalMathFormula()*t_comp.symbol.getInternalMathFormula())

			else:
				MathFormula.setPrettyPrintMathFormula(self, definition)

		else:
			MathFormula.setPrettyPrintMathFormula(self, definition)

		if self.reaction.value is None:
			self.reaction.value = MathFormula(self.__model)
		self.reaction.value.setInternalMathFormula(MathFormula.getInternalMathFormula(self))


	def getPrettyPrintMathFormula(self):

		if len(self.reaction.listOfReactants) > 0:
			first_reactant = self.reaction.listOfReactants[0].getSpecies()
			if first_reactant.isConcentration():
				t_comp = first_reactant.getCompartment()
				t_math_formula = MathFormula(self.__model, MathFormula.MATH_KINETICLAW)
				t_math_formula.setInternalMathFormula(MathFormula.getInternalMathFormula(self)/t_comp.symbol.getInternalMathFormula())
				t_math_formula = t_math_formula.getPrettyPrintMathFormula()
			else:
				t_math_formula = MathFormula.getPrettyPrintMathFormula(self)
		else:
			t_math_formula = MathFormula.getPrettyPrintMathFormula(self)

		if self.reaction.listOfLocalParameters > 0:
			t_math_formula = t_math_formula.replace("_local_%d_" % (self.reaction.objId), "")

		for species in self.__model.listOfSpecies.values():
			if species.isConcentration():
				t_math_formula = t_math_formula.replace(("_speciesForcedConcentration_%s_" % (species.symbol.getInternalMathFormula())), species.getSbmlId())

		return t_math_formula


	def getReactantsFormula(self):

		t_reactants = 1
		for reactant in self.reaction.listOfReactants.values():

			t_reactants *= reactant.getSpecies().symbol.getInternalMathFormula()

			if not reactant.stoichiometry.isOne():
				t_reactants *= reactant.stoichiometry.getInternalMathFormula()

		return t_reactants


	def getModifiersFormula(self):

		t_modifiers = 1
		for modifier in self.reaction.listOfModifiers.values():
			t_modifiers *= modifier.getSpecies().symbol.getInternalMathFormula()

			if not modifier.stoichiometry.isOne():
				t_modifiers *= modifier.stoichiometry.getInternalMathFormula()

		return t_modifiers


	def getProductsFormula(self):

		t_products = 1
		for product in self.reaction.listOfProducts.values():
			t_products *= product.getSpecies().symbol.getInternalMathFormula()

			if not product.stoichiometry.isOne():
				t_products *= product.stoichiometry.getInternalMathFormula()

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
				print "SbmlId : %s" % first_reactant.getCompartment().getSbmlId()

				t_formula *= first_reactant.getCompartment().symbol.getInternalMathFormula()

		elif len(self.reaction.listOfModifiers) > 0:
			first_modifier = self.reaction.listOfModifiers[0].getSpecies()
			if not first_modifier.hasOnlySubstanceUnits:
				print first_modifier.getCompartment().symbol.getInternalMathFormula()
				t_formula *= first_modifier.getCompartment().symbol.getInternalMathFormula()

		print "Kinetic law"
		print t_formula
		self.setInternalMathFormula(simplify(t_formula))


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

		self.setInternalMathFormula(simplify(t_formula))



	def setHill(self, parameters):

		t_reactants = self.getReactantsFormula()
		t_modifiers = self.getModifiersFormula()

		t_cat = parameters[0].symbol.getInternalMathFormula()
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

		self.setInternalMathFormula(simplify(t_formula))



	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		t_symbol = SympySymbol(old_sbml_id)
		t_local_symbol = SympySymbol("_local_%d_%s" % (self.reaction.objId, old_sbml_id))
		t_concentration_symbol = SympySymbol("_speciesForcedConcentration_%s_" % old_sbml_id)
		if t_symbol in self.getInternalMathFormula().atoms():
			MathFormula.renameSbmlId(self, old_sbml_id, new_sbml_id)
		elif t_local_symbol in self.getInternalMathFormula().atoms():
			self.setInternalMathFormula(
				MathFormula.getInternalMathFormula(self).subs(t_local_symbol,
					SympySymbol("_local_%d_%s" % (self.reaction.objId, new_sbml_id))))
		elif t_concentration_symbol in self.getInternalMathFormula().atoms():
			self.setInternalMathFormula(
				MathFormula.getInternalMathFormula(self).subs(
					t_concentration_symbol, SympySymbol("_speciesForcedConcentration_%s_" % new_sbml_id)))
