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
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasUnits import HasUnits
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.settings.Settings import Settings


class Compartment(Variable, SbmlObject, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable, HasUnits, HasParentObj):
	""" Compartment definition """


	def __init__ (self, model, parent_obj, obj_id):


		self.__model = model
		self.objId = obj_id

		SbmlObject.__init__(self, model)
		Variable.__init__(self, model, Variable.COMPARTMENT)
		InitiallyAssignedVariable.__init__(self, model)
		RuledVariable.__init__(self, model)
		EventAssignedVariable.__init__(self, model)
		HasUnits.__init__(self, model)
		HasParentObj.__init__(self, parent_obj)
		self.spatialDimensions = None


	def new(self, name=None, sbml_id=None, value=1, constant=True, unit=None):
		""" Creates new compartment with default options """

		if sbml_id is None:
			sbml_id = name
		Variable.new(self, sbml_id, Variable.COMPARTMENT)
		SbmlObject.new(self, name)
		HasUnits.new(self, unit)

		self.setValue(value)
		self.constant = constant
		self.setUnits(self.__model.getCompartmentUnits())


	def copy(self, compartment, sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factors=None):

		SbmlObject.copy(self, compartment)
		HasUnits.copy(self, compartment, usids_subs=usids_subs)
		Variable.copy(self, compartment, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factor=conversion_factors)

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
				if sbml_level == 2:
					self.spatialDimensions = sbml_compartment.getSpatialDimensions()
				else:
					self.spatialDimensions = sbml_compartment.getSpatialDimensionsAsDouble()
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
			self.value = MathFormula(self.__model)

		self.value.setPrettyPrintMathFormula(value)


	def getXPath(self, attribute=None):

		xpath = "sbml:species"
		if self.__model.sbmlLevel == 1:
			xpath += "[@name='%s']" % self.getSbmlId()
		else:
			xpath += "[@id='%s']" % self.getSbmlId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])

	def getSpecies(self):

		all_species = []
		for species in self.__model.listOfSpecies:
			if species.getCompartment() == self:
				all_species.append(species)

		return all_species


	def getNbSpecies(self):

		count = 0
		for species in self.__model.listOfSpecies:
			if species.getCompartment() == self:
				count += 1
		return count

	def getByXPath(self, xpath):

		if len(xpath) == 0:
			return self

		if len(xpath) > 1:
			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@size":
			return self.getValue()

		elif xpath[0] == "@name":
			return self.getName()

		elif xpath[0] == "@id":
			return self.getSbmlId()

	def setByXPath(self, xpath, object):

		if len(xpath) == 0:
			return InvalidXPath("/".join(xpath))

		if len(xpath) > 1:
			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@size":
			return self.setValue(object)

		elif xpath[0] == "@name":
			return self.setName(object)

		elif xpath[0] == "@id":
			return self.setSbmlId(object)

	def getXPath(self, attribute=None):

		xpath = "sbml:compartment"
		if self.__model.sbmlLevel == 1:
			xpath += "[@name='%s']" % self.getSbmlId()
		else:
			xpath += "[@id='%s']" % self.getSbmlId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])