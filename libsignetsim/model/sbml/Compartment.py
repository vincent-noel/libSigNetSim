#!/usr/bin/env python
""" Compartment.py


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
from libsignetsim.settings.Settings import Settings

class Compartment(Variable, SbmlObject, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable, HasUnits):
	""" Compartment definition """


	def __init__ (self, model, obj_id):


		self.model = model
		self.objId = obj_id

		SbmlObject.__init__(self, model)
		Variable.__init__(self, model, Variable.COMPARTMENT)
		InitiallyAssignedVariable.__init__(self, model)
		RuledVariable.__init__(self, model)
		EventAssignedVariable.__init__(self, model)
		HasUnits.__init__(self, model)

		self.spatialDimensions = None


	def new(self, name=None, sbml_id=None, size=1, constant=True, unit=None):
		""" Creates new compartment with default options """

		if sbml_id is None:
			sbml_id = name
		Variable.new(self, sbml_id, Variable.COMPARTMENT)
		SbmlObject.new(self, name)
		HasUnits.new(self, unit)

		self.setValue(size)
		self.constant = constant


	def copy(self, compartment, prefix="", shift=0, subs={}, deletions=[], replacements={}):

		SbmlObject.copy(self, compartment, prefix, shift)
		InitiallyAssignedVariable.copy(self, compartment, prefix, shift)
		EventAssignedVariable.copy(self, compartment, prefix, shift)
		RuledVariable.copy(self, compartment, prefix, shift)
		HasUnits.copy(self, compartment, prefix, shift)
		Variable.copy(self, compartment, prefix, shift, subs, deletions, replacements)

		self.spatialDimensions = compartment.spatialDimensions




	def readSbml(self, sbml_compartment,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		""" Reads compartment from a sbml file """

		SbmlObject.readSbml(self, sbml_compartment, sbml_level, sbml_version)
		Variable.readSbml(self, sbml_compartment, sbml_level, sbml_version)
		HasUnits.readSbml(self, sbml_compartment, sbml_level, sbml_version)


		# spatialDimensions
		if sbml_level >= 2:
			if sbml_compartment.isSetSpatialDimensions():
				self.spatialDimensions = sbml_compartment.getSpatialDimensions()
			elif sbml_level in [1, 2]:
				self.spatialDimensions = 3

			if self.spatialDimensions == 0:
				self.setValue(1)



	def readSbmlVariable(self, sbml_compartment,
							sbml_level=Settings.defaultSbmlLevel,
							sbml_version=Settings.defaultSbmlVersion):

		""" Reads the variable information from a sbml file """
		""" I'm doubting the purpose of isInitialized here... """

		# variable id
		self.symbol.readSbml(sbml_compartment.getId(), sbml_level, sbml_version)

		# Size/Volume
		if sbml_level >= 2:
			if sbml_compartment.isSetSize():
				self.isInitialized = True
				self.value.readSbml(sbml_compartment.getSize(),
										sbml_level, sbml_version)

		else:
			if sbml_compartment.isSetVolume():
				self.isInitialized = True
				self.value.readSbml(sbml_compartment.getVolume(),
									sbml_level, sbml_version)


		# constant
		if sbml_compartment.isSetConstant():
			self.constant = sbml_compartment.getConstant()
		elif sbml_level == 2:
			self.constant = True
		elif sbml_level == 1:
			self.constant = False



	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		""" Writes compartment to a sbml file """

		sbml_compartment = sbml_model.createCompartment()

		SbmlObject.writeSbml(self, sbml_compartment, sbml_level, sbml_version)
		Variable.writeSbml(self, sbml_compartment, sbml_level, sbml_version)
		HasUnits.writeSbml(self, sbml_compartment, sbml_level, sbml_version)

		# SpatialDimensions
		if sbml_level >= 2:
			if self.spatialDimensions is not None:
				if sbml_level == 2 and self.spatialDimensions == 3:
					pass
				else:
					sbml_compartment.setSpatialDimensions(self.spatialDimensions)



	def writeSbmlVariable(self, sbml_compartment,
							sbml_level=Settings.defaultSbmlLevel,
							sbml_version=Settings.defaultSbmlVersion):

		""" Writes the variable information to a sbml file """

		if self.constant is not None:
			if not (sbml_level == 2 and self.constant is True
				or sbml_level == 1 and self.constant is False):
				sbml_compartment.setConstant(self.constant)

		# Size/Volume
		if self.isInitialized and self.spatialDimensions != 0:
			t_value = self.getSbmlValue(sbml_level, sbml_version).getValue()
			if sbml_level >= 2:
				sbml_compartment.setSize(t_value)
			else:
				sbml_compartment.setVolume(t_value)



	def getSize(self):
		return self.value.getPrettyPrintMathFormula()


	def getSizeMath(self):
		return self.value


	def setSize(self , value):

		if self.value is None:
			self.value = MathFormula(self.model)

		self.value.setPrettyPrintMathFormula(value)

	# def setSbmlId(self, sbml_id):
	#     # for species in self.model.listOfSpecies.values():
	#     #     if species.getCompartment() == self:
	#     #         species.renameSbmlId(self.getSbmlId(), sbml_id)
	#     #
	#     # for reaction in self.model.listOfReactions.values():
	#     #     reaction.renameSbmlId(self.getSbmlId(), sbml_id)
	#
	#
	#     Variable.setSbmlId(self, sbml_id)

	def getSpecies(self):

		all_species = []
		for species in self.model.listOfSpecies.values():
			if species.getCompartment() == self:
				all_species.append(species)

		return all_species


	def getNbSpecies(self):

		count = 0
		for species in self.model.listOfSpecies.values():
			if species.getCompartment() == self:
				count += 1
		return count
