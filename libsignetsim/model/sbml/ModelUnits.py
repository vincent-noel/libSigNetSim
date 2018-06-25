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


from libsignetsim.model.sbml.container.ListOfSpecies import ListOfSpecies
from libsignetsim.model.sbml.container.ListOfParameters import ListOfParameters
from libsignetsim.model.sbml.container.ListOfReactions import ListOfReactions
from libsignetsim.model.sbml.container.ListOfCompartments import ListOfCompartments
from libsignetsim.model.sbml.container.ListOfFunctionDefinitions import ListOfFunctionDefinitions
from libsignetsim.model.sbml.container.ListOfUnitDefinitions import ListOfUnitDefinitions
from libsignetsim.model.sbml.container.ListOfRules import ListOfRules
from libsignetsim.model.sbml.container.ListOfEvents import ListOfEvents
from libsignetsim.model.sbml.container.ListOfConstraints import ListOfConstraints
from libsignetsim.model.sbml.container.ListOfInitialAssignments import ListOfInitialAssignments
from libsignetsim.model.sbml.container.ListOfSbmlObjects import ListOfSbmlObjects
from libsignetsim.model.sbml.container.ListOfSubmodels import ListOfSubmodels
from libsignetsim.model.sbml.container.ListOfPorts import ListOfPorts

from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.SbmlModelAnnotation import SbmlModelAnnotation
from libsignetsim.model.sbml.HasId import HasId

from os.path import isfile
from libsbml import SBMLReader, SBMLDocument, formulaToString,\
					formulaToL3String, writeSBMLToFile,\
					XMLFileUnreadable, XMLFileOperationError, \
					LIBSBML_CAT_UNITS_CONSISTENCY, LIBSBML_SEV_INFO, \
					LIBSBML_SEV_WARNING, SBMLExtensionRegistry

from time import time

class ModelUnits(object):
	""" Sbml model units class """


	def __init__ (self):
		""" Constructor of model class """


		self.timeUnits = None
		self.substanceUnits = None
		self.concentrationUnits = None
		self.compartmentUnits = None
		self.extentUnits = None


	def setDefaultUnits(self):

		self.substanceUnits = self.listOfUnitDefinitions.new()
		self.substanceUnits.defaultAmountUnit()

		self.extentUnits = self.substanceUnits

		self.timeUnits = self.listOfUnitDefinitions.new()
		self.timeUnits.defaultTimeUnits()

		self.concentrationUnits = self.listOfUnitDefinitions.new()
		self.concentrationUnits.defaultConcentrationUnit()

		self.compartmentUnits = self.listOfUnitDefinitions.new()
		self.compartmentUnits.defaultCompartmentUnits()

		# self.defaultCompartment.setUnits(self.compartmentUnits)

	def readSbml(self, sbmlModel,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion, parent_doc=None):

		# We need to load the units before reading the model's default units
		if self.sbmlLevel >= 3:
			if sbmlModel.isSetTimeUnits():
				self.timeUnits = self.listOfUnitDefinitions.getBySbmlId(
												sbmlModel.getTimeUnits())

			if sbmlModel.isSetSubstanceUnits():
				self.substanceUnits = self.listOfUnitDefinitions.getBySbmlId(
												sbmlModel.getSubstanceUnits())


			if sbmlModel.isSetExtentUnits():
				self.extentUnits = self.listOfUnitDefinitions.getBySbmlId(
												sbmlModel.getExtentUnits())

		else:
			if self.listOfUnitDefinitions.containsSbmlId("time"):
				self.timeUnits = self.listOfUnitDefinitions.getBySbmlId("time")

			if self.listOfUnitDefinitions.containsSbmlId("substance"):
				self.substanceUnits = self.listOfUnitDefinitions.getBySbmlId("substance")



	def writeSbml(self, sbmlModel,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):


		if self.sbmlLevel >= 3:
			if self.timeUnits is not None:
				sbmlModel.setTimeUnits(self.timeUnits.getSbmlId())
			if self.substanceUnits is not None:
				sbmlModel.setSubstanceUnits(self.substanceUnits.getSbmlId())
			if self.extentUnits is not None:
				sbmlModel.setExtentUnits(self.extentUnits.getSbmlId())


	def getTimeUnits(self):
		return self.timeUnits

	def setTimeUnits(self, unit_sbml_id):

		if unit_sbml_id is None:
			self.timeUnits = None

		elif self.sbmlLevel == 3:
			self.timeUnits = self.listOfUnitDefinitions.getBySbmlId(unit_sbml_id)

		elif self.sbmlLevel == 2:

			# First we remove the old one if it exists
			if self.listOfUnitDefinitions.containsSbmlId("time"):

				t_unit_def = self.listOfUnitDefinitions.getBySbmlId("time")
				i=0
				while self.listOfUnitDefinitions.containsSbmlId("time_%d" % i):
					i += 1

				t_unit_def.sbmlId = "time_%d" % i

			t_unit_def = self.listOfUnitDefinitions.getBySbmlId(unit_sbml_id)
			t_unit_def.sbmlId = "time"
			self.timeUnits = t_unit_def


	def getSubstanceUnits(self):
		return self.substanceUnits

	def setSubstanceUnits(self, unit_sbml_id):

		if unit_sbml_id is None:
			self.substanceUnits = None

		elif self.sbmlLevel == 3:
			self.substanceUnits = self.listOfUnitDefinitions.getBySbmlId(unit_sbml_id)

		elif self.sbmlLevel == 2:

			# First we remove the old one if it exists
			if self.listOfUnitDefinitions.containsSbmlId("substance"):

				t_unit_def = self.listOfUnitDefinitions.getBySbmlId("substance")
				i=0
				while self.listOfUnitDefinitions.containsSbmlId("substance_%d" % i):
					i += 1

				t_unit_def.sbmlId = "substance_%d" % i

			t_unit_def = self.listOfUnitDefinitions.getBySbmlId(unit_sbml_id)
			t_unit_def.sbmlId = "substance"
			self.substanceUnits = t_unit_def

	def getExtentUnits(self):
		return self.extentUnits

	def setExtentUnits(self, unit_sbml_id):
		if unit_sbml_id is None:
			self.extentUnits = None

		else:
			self.extentUnits = self.listOfUnitDefinitions.getBySbmlId(unit_sbml_id)


	def getCompartmentUnits(self):
		return self.compartmentUnits