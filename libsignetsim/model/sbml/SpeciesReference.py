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

from libsignetsim.model.sbml.EventAssignedVariable import EventAssignedVariable
from libsignetsim.model.sbml.InitiallyAssignedVariable import InitiallyAssignedVariable
from libsignetsim.model.sbml.RuledVariable import RuledVariable
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.Variable import Variable
from libsignetsim.model.math.sympy_shortcuts import *
from libsignetsim.settings.Settings import Settings

from libsbml import AST_REAL, AST_INTEGER, AST_RATIONAL, formulaToString
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
from sympy import Symbol, sympify, srepr, simplify, expand, factor, nsimplify, Integer

class SpeciesReference(SbmlObject, Variable, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable):

	def __init__ (self, model, objId, is_modifier=False):

		SbmlObject.__init__(self, model)
		self.__model = model
		self.objId = objId
		self.__isModifier = is_modifier
		self.__species = None
		self.stoichiometry = MathFormula(model)
		self.constant = True # True by default sounds fair
		self.__hasId = False


	def load(self, species, stoichiometry=None):

		self.__species = species.getSbmlId()

		if stoichiometry is None:
			self.stoichiometry.setValueMathFormula(1)

		else:
			self.stoichiometry.setValueMathFormula(stoichiometry)


	def copy(self, obj, sids_subs={}, symbols_subs={}):

		SbmlObject.copy(self, obj)
		if obj.hasId():

			Variable.__init__(self, self.__model, Variable.STOICHIOMERY)
			InitiallyAssignedVariable.__init__(self, self.__model)
			RuledVariable.__init__(self, self.__model)
			EventAssignedVariable.__init__(self, self.__model)

			Variable.copy(self, obj, sids_subs=sids_subs, symbols_subs=symbols_subs)
			self.constant = obj.constant

		t_stoichiometry = unevaluatedSubs(obj.stoichiometry.getInternalMathFormula(), symbols_subs)
		self.stoichiometry.setInternalMathFormula(t_stoichiometry)

		if obj.getSpecies().getSbmlId() in list(sids_subs.keys()):
			self.__species = sids_subs[obj.getSpecies().getSbmlId()]
		else:
			self.__species = obj.getSpecies().getSbmlId()

		self.__isModifier = obj.isModifier()


	def readSbml(self, sbmlSpeciesReference, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads a species reference from a sbml file """

		SbmlObject.readSbml(self, sbmlSpeciesReference, sbml_level, sbml_version)
		if sbml_level >= 3 and sbmlSpeciesReference.isSetId():
			Variable.__init__(self, self.__model, Variable.STOICHIOMERY)
			InitiallyAssignedVariable.__init__(self, self.__model)
			RuledVariable.__init__(self, self.__model)
			EventAssignedVariable.__init__(self, self.__model)
			Variable.readSbml(self, sbmlSpeciesReference, sbml_level, sbml_version)
			self.stoichiometry = self.symbol
			self.__hasId = True
			self.__isModifier = sbmlSpeciesReference.isModifier()
		else:


			if sbmlSpeciesReference.isModifier():
				self.__isModifier = True
				self.stoichiometry.setValueMathFormula(1)

			else:
				if sbmlSpeciesReference.isSetStoichiometry():

					if sbml_level == 1:
						self.stoichiometry.setInternalMathFormula(
							SympyMul(
								SympyFloat(float(sbmlSpeciesReference.getStoichiometry())),
								SympyPow(SympyFloat(float(sbmlSpeciesReference.getDenominator())),
											SympyInteger(-1))))

					else:
						self.stoichiometry.readSbml(
							sbmlSpeciesReference.getStoichiometry())

				elif sbmlSpeciesReference.isSetStoichiometryMath():
					self.stoichiometry.readSbml(
						sbmlSpeciesReference.getStoichiometryMath().getMath(),
						sbml_level, sbml_version)


				else:
					self.stoichiometry.setValueMathFormula(1)


		if sbml_level >= 2:
			self.__species = sbmlSpeciesReference.getSpecies()
		else:
			self.__species = sbmlSpeciesReference.getSpecies()


	def readSbmlVariable(self, sbml_species_reference, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		self.symbol.readSbml(sbml_species_reference.getId(), sbml_level, sbml_version)
		if sbml_level == 3 and not sbml_species_reference.isModifier():
			self.constant = sbml_species_reference.getConstant()
		else:
			self.constant = True

		if not sbml_species_reference.isModifier() and sbml_species_reference.isSetStoichiometry():
			self.isInitialized = True
			self.value.readSbml(sbml_species_reference.getStoichiometry(), sbml_level, sbml_version)
		else:
			self.isInitialized = True
			self.value.setInternalMathFormula(Integer(1))

	def writeSbml(self, sbml_speciesReference, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes a species reference to  a sbml file """

		sbml_speciesReference.setSpecies(self.__species)
		SbmlObject.writeSbml(self, sbml_speciesReference, sbml_level, sbml_version)

		if sbml_level == 3 and self.__hasId:
			Variable.writeSbml(self, sbml_speciesReference, sbml_level, sbml_version)


		elif not sbml_speciesReference.isModifier():
			if sbml_level == 1:
				t_stoichiometry = nsimplify(self.stoichiometry.getInternalMathFormula())
				if t_stoichiometry.is_Rational and t_stoichiometry.q != 1:

					sbml_speciesReference.setStoichiometry(int(t_stoichiometry.p))
					sbml_speciesReference.setDenominator(int(t_stoichiometry.q))

				elif t_stoichiometry != MathFormula.ONE:
					# print srepr(t_stoichiometry)
					# t_stoichiometry = self.stoichiometry.getSbmlMathFormula(sbml_level, sbml_version)
					sbml_speciesReference.setStoichiometry(int(t_stoichiometry))

			else:

				t_stoichiometry = self.stoichiometry.getSbmlMathFormula(sbml_level, sbml_version)

				if t_stoichiometry.getType() == AST_REAL:
					if t_stoichiometry.getReal() != 1.0 or sbml_level == 3:
						sbml_speciesReference.setStoichiometry(t_stoichiometry.getReal())

				elif t_stoichiometry.getType() == AST_INTEGER:
					if t_stoichiometry.getInteger() != 1 or sbml_level == 3:
						sbml_speciesReference.setStoichiometry(t_stoichiometry.getInteger())

				elif t_stoichiometry.getType() == AST_RATIONAL:
					sbml_speciesReference.setStoichiometry(t_stoichiometry.getNumerator())
					sbml_speciesReference.setDenominator(t_stoichiometry.getDenominator())

				else:
					if sbml_level == 3:
						if self.__model.listOfVariables.containsSymbol(self.stoichiometry.getInternalMathFormula()):
							sbml_speciesReference.setId(t_stoichiometry.getName())

						else:
							sbml_speciesReference.setStoichiometry(t_stoichiometry)
					else:
						sbml_stoichiometry_math = sbml_speciesReference.createStoichiometryMath()
						sbml_stoichiometry_math.setMath(t_stoichiometry)

			if sbml_level >= 3:
				sbml_speciesReference.setConstant(self.constant)

	def writeSbmlVariable(self, sbml_species_reference, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if not self.isModifier():

			sbml_species_reference.setConstant(self.constant)

			if self.isInitialized:
				sbml_species_reference.setStoichiometry(self.getValue())


	def setSpecies(self, species):
		self.__species = species.getSbmlId()

	def getSpecies(self):
		if self.__species is not None:
			return self.__model.listOfSpecies.getBySbmlId(self.__species)


	def hasId(self):
		return self.__hasId

	def isModifier(self):
		return self.__isModifier

	def setStoichiometry(self, stoichiometry):

		if isinstance(stoichiometry, int) or isinstance(stoichiometry, float):
			self.stoichiometry.setValueMathFormula(stoichiometry)

		# elif isinstance(stoichiometry, float):
		# 	self.stoichiometry = setPrettyPrintMathFormula(stoichiometry)

	def getStoichiometry(self):
		return self.stoichiometry.getPrettyPrintMathFormula()

	def getStoichiometryMath(self):
		return self.stoichiometry

	def isVariableStoichiometry(self):

		if self.__hasId and not self.constant:
			return True
		elif self.stoichiometry.getInternalMathFormula().func == SympySymbol:
			t_var = self.__model.listOfVariables.getBySymbol(self.stoichiometry.getInternalMathFormula())
			return t_var is not None and not t_var.isConstant()
		else:
			return False
		
	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		if self.__species == old_sbml_id:
			self.__species = new_sbml_id