#!/usr/bin/env python
""" InitialAssignment.py


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


from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import  (
	SympySymbol, SympyInteger, SympyMul, SympyPow)


class InitialAssignment(SbmlObject):
	""" Initial assignment definition """

	def __init__ (self, model, obj_id):

		self.__model = model
		self.objId = obj_id

		SbmlObject.__init__(self, model)
		self.__definition = MathFormula(model, MathFormula.MATH_ASSIGNMENTRULE)
		self.__var = None


	def readSbml(self, initial_assignment, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads an initial assignment from a sbml file """

		SbmlObject.readSbml(self, initial_assignment, sbml_level, sbml_version)

		if self.__model.listOfVariables.containsSbmlId(initial_assignment.getSymbol()):
			self.__var = self.__model.listOfVariables.getBySbmlId(initial_assignment.getSymbol())
			self.__var.setInitialAssignmentBy(self)

		self.__definition.readSbml(initial_assignment.getMath(), sbml_level, sbml_version)

		if self.__var.isConcentration():
			self.__definition.setInternalMathFormula(
				SympyMul(self.__definition.getInternalMathFormula(),
						self.__var.getCompartment().symbol.getInternalMathFormula()))


	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes an initial assignment to a sbml file """

		sbml_initial_assignment = sbml_model.createInitialAssignment()

		SbmlObject.writeSbml(self, sbml_initial_assignment, sbml_level, sbml_version)

		t_definition = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
		t_definition.setInternalMathFormula(self.__definition.getInternalMathFormula())
		t_variable = self.__var.symbol.getSbmlMathFormula(sbml_level, sbml_version).getName()

		if self.__var.isConcentration():
			t_definition.setInternalMathFormula(
				SympyMul(self.__definition.getInternalMathFormula(),
						SympyPow(self.__var.getCompartment().symbol.getInternalMathFormula(),
									SympyInteger(-1))))

		sbml_initial_assignment.setSymbol(t_variable)
		sbml_initial_assignment.setMath(t_definition.getSbmlMathFormula(sbml_level, sbml_version))


	def copy(self, obj, prefix="", shift="", subs={}, deletions=[], replacements={}, conversions=[]):
		SbmlObject.copy(self, obj, prefix, shift)

		t_symbol = SympySymbol(obj.getVariable().getSbmlId())

		if t_symbol in subs.keys():
			t_sbml_id = str(subs[t_symbol])
			tt_symbol = SympySymbol(t_sbml_id)
			if tt_symbol in replacements.keys():
				t_sbml_id = str(replacements[tt_symbol])
		else:
			t_sbml_id = prefix+obj.getVariable().getSbmlId()

		self.__var = self.__model.listOfVariables.getBySbmlId(t_sbml_id)
		self.__var.setInitialAssignmentBy(self)

		t_convs = {}
		for var, conversion in conversions.items():
			t_convs.update({var:var/conversion})

		t_definition = obj.getDefinition().getInternalMathFormula().subs(subs).subs(replacements).subs(t_convs)

		t_var_symbol = obj.getVariable().symbol.getInternalMathFormula().subs(subs).subs(replacements)
		if t_var_symbol in conversions:
			t_definition *= conversions[t_var_symbol]

		self.__definition.setInternalMathFormula(t_definition)


	def getVariable(self):
		return self.__var


	def setVariable(self, variable):

		if self.__var is not None:
			self.__var.unsetInitialAssignmentBy()

		self.__var = variable
		self.__var.setInitialAssignmentBy(self)


	def getDefinition(self, forcedConcentration=False):

		if self.__var.isConcentration() and forcedConcentration:
			t_definition = MathFormula(self.__model, MathFormula.MATH_RATERULE)
			t_definition.setInternalMathFormula(
							self.__definition.getInternalMathFormula()
							/ self.__var.getCompartment().symbol.getInternalMathFormula())
			return t_definition
		else:
			return self.__definition



	def setDefinition(self, definition):

		if self.__var.isConcentration():
			t_comp = self.__var.getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_RATERULE)
			t_math_formula.setInternalMathFormula(
						definition.getInternalMathFormula()
						* t_comp.symbol.getInternalMathFormula()
			)

			self.__definition = t_math_formula

		else:
			self.__definition = definition


	def getRuleTypeDescription(self):
		return "Initial assignment"

	def setPrettyPrintDefinition(self, definition):

		if self.__var.isSpecies() and not self.__var.hasOnlySubstanceUnits:
			t_comp = self.__var.getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
			t_math_formula.setPrettyPrintMathFormula(definition)
			self.__definition.setInternalMathFormula(t_math_formula.getInternalMathFormula()*t_comp.symbol.getInternalMathFormula())

		else:
			self.__definition.setPrettyPrintMathFormula(definition)


	def getPrettyPrintDefinition(self):

		if self.__var.isSpecies() and not self.__var.hasOnlySubstanceUnits:
			t_comp = self.__var.getCompartment()
			t_math_formula = MathFormula(self.__model, MathFormula.MATH_ASSIGNMENTRULE)
			t_math_formula.setInternalMathFormula(self.__definition.getInternalMathFormula()/t_comp.symbol.getInternalMathFormula())
			return t_math_formula.getPrettyPrintMathFormula()

		else:
			return self.__definition.getPrettyPrintMathFormula()


	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		old_symbol = SympySymbol(old_sbml_id)

		if old_symbol in self.__definition.getInternalMathFormula().atoms():
			self.__definition.setInternalMathFormula(self.__definition.getInternalMathFormula.subs(old_symbol, SympySymbol(new_sbml_id)))


	def containsVariable(self, variable):
		return (variable.symbol.getInternalMathFormula() in self.__definition.getInternalMathFormula().atoms()
				or (variable.isSpecies() and SympySymbol("_speciesForcedConcentration_%s_" % str(variable.symbol.getInternalMathFormula())) in self.__definition.getInternalMathFormula().atoms())
				or variable.symbol.getInternalMathFormula() == self.__var.symbol.getInternalMathFormula())
