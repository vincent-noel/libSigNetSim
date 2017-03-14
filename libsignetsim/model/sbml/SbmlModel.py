#!/usr/bin/env python
""" SbmlModel.py


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

# from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasId import HasId

from os.path import isfile
from libsbml import SBMLReader, SBMLDocument, formulaToString,\
					formulaToL3String, writeSBMLToFile,\
					XMLFileUnreadable, XMLFileOperationError, \
					LIBSBML_CAT_UNITS_CONSISTENCY, LIBSBML_SEV_INFO, \
					LIBSBML_SEV_WARNING, SBMLExtensionRegistry

from time import time

class SbmlModel(HasId, SbmlObject):
	""" Sbml model class """


	def __init__ (self, parent_document, obj_id=0):
		""" Constructor of model class """

		self.objId = obj_id
		self.parentDoc = parent_document

		HasId.__init__(self, self)
		self.listOfSbmlObjects = ListOfSbmlObjects(self)
		SbmlObject.__init__(self, self)

		self.listOfSpecies = ListOfSpecies(self)
		self.listOfParameters = ListOfParameters(self)
		self.listOfReactions = ListOfReactions(self)
		self.listOfCompartments = ListOfCompartments(self)
		self.listOfFunctionDefinitions = ListOfFunctionDefinitions(self)
		self.listOfUnitDefinitions = ListOfUnitDefinitions(self)
		self.listOfRules = ListOfRules(self)
		self.listOfEvents = ListOfEvents(self)
		self.listOfConstraints = ListOfConstraints(self)
		self.listOfInitialAssignments = ListOfInitialAssignments(self)

		self.listOfSubmodels = ListOfSubmodels(self)
		self.listOfPorts = ListOfPorts(self)

		self.conversionFactor = None
		self.defaultCompartment = None

		self.timeUnits = None
		self.substanceUnits = None
		self.concentrationUnits = None
		self.compartmentUnits = None
		self.extentUnits = None

		self.sbmlLevel = Settings.defaultSbmlLevel
		self.sbmlVersion = Settings.defaultSbmlVersion

	def newModel(self, name):

		self.setName(name)
		self.setSbmlId("model_%d" % self.objId)

		self.defaultCompartment = self.listOfCompartments.new("cell")
		self.setDefaultUnits()

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

		self.defaultCompartment.setUnits(self.compartmentUnits)

	def readSbml(self, sbmlModel,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion, parent_doc=None):

		t0 = time()

		HasId.readSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)
		SbmlObject.readSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)

		self.sbmlLevel = sbml_level
		self.sbmlVersion = sbml_version

		self.listOfFunctionDefinitions.readSbml(sbmlModel.getListOfFunctionDefinitions(), self.sbmlLevel, self.sbmlVersion)
		self.listOfUnitDefinitions.readSbml(sbmlModel.getListOfUnitDefinitions(), self.sbmlLevel, self.sbmlVersion)

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


		self.listOfCompartments.readSbml(sbmlModel.getListOfCompartments(), self.sbmlLevel, self.sbmlVersion)
		self.listOfParameters.readSbml(sbmlModel.getListOfParameters(), self.sbmlLevel, self.sbmlVersion)

		# We need to load the parameters before reading the conversion factor
		if self.sbmlLevel >= 3:
			if sbmlModel.isSetConversionFactor():
				self.conversionFactor = MathFormula(self)
				self.conversionFactor.readSbml(sbmlModel.getConversionFactor(), self.sbmlLevel, self.sbmlVersion)

		self.listOfSpecies.readSbml(sbmlModel.getListOfSpecies(), self.sbmlLevel, self.sbmlVersion)
		self.listOfReactions.readSbml(sbmlModel.getListOfReactions(), self.sbmlLevel, self.sbmlVersion)
		self.listOfInitialAssignments.readSbml(sbmlModel.getListOfInitialAssignments(), self.sbmlLevel, self.sbmlVersion)
		self.listOfRules.readSbml(sbmlModel.getListOfRules(), self.sbmlLevel, self.sbmlVersion)
		self.listOfConstraints.readSbml(sbmlModel.getListOfConstraints(), self.sbmlLevel, self.sbmlVersion)
		self.listOfEvents.readSbml(sbmlModel.getListOfEvents(), self.sbmlLevel, self.sbmlVersion)

		if self.sbmlLevel == 3 and self.parentDoc.isCompEnabled():
			self.listOfSubmodels.readSbml(sbmlModel.getPlugin("comp").getListOfSubmodels(), self.sbmlLevel, self.sbmlVersion)
			self.listOfPorts.readSbml(sbmlModel.getPlugin("comp").getListOfPorts(), self.sbmlLevel, self.sbmlVersion)

		if Settings.verbose >= 1:
			print "> SBML Model %s read in %.2gs" % (self.getSbmlId(), time()-t0)


	def writeSbml(self, sbmlModel,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		t0 = time()

		if self.sbmlLevel == 3 and self.parentDoc.isCompEnabled():
			sbmlModel.enablePackage("http://www.sbml.org/sbml/level3/version1/comp/version1", "comp", True)

		SbmlObject.writeSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)
		HasId.writeSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)

		self.listOfUnitDefinitions.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfFunctionDefinitions.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfCompartments.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfSpecies.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfParameters.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfInitialAssignments.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfRules.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfConstraints.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfReactions.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		self.listOfEvents.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)
		if self.sbmlLevel >= 3:
			if self.timeUnits is not None:
				sbmlModel.setTimeUnits(self.timeUnits.getSbmlId())
			if self.substanceUnits is not None:
				sbmlModel.setSubstanceUnits(self.substanceUnits.getSbmlId())
			if self.extentUnits is not None:
				sbmlModel.setExtentUnits(self.extentUnits.getSbmlId())

			if self.conversionFactor is not None:
				sbmlModel.setConversionFactor(formulaToL3String(self.conversionFactor.writeSbml(self.sbmlLevel, self.sbmlVersion)))


		if self.sbmlLevel == 3 and self.parentDoc.isCompEnabled():
			self.listOfSubmodels.writeSbml(sbmlModel.getPlugin("comp"), self.sbmlLevel, self.sbmlVersion)
			self.listOfPorts.writeSbml(sbmlModel.getPlugin("comp"), self.sbmlLevel, self.sbmlVersion)

		if Settings.verbose >= 1:
			print "> SBML Model %s written in %.2gs" % (self.getSbmlId(), time()-t0)


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


	def getConversionFactor(self):
		if self.conversionFactor is not None:
			t_sbml_id = str(self.conversionFactor.getInternalMathFormula())
			return self.listOfVariables.getBySbmlId(t_sbml_id)


	def setConversionFactor(self, sbml_id):

		if sbml_id is None:
			self.conversionFactor = None

		elif sbml_id in self.listOfVariables.keys():
			if self.conversionFactor is None:
				self.conversionFactor = MathFormula(self)
			self.conversionFactor.setInternalMathFormula(self.listOfVariables[sbml_id].symbol.getInternalMathFormula())




	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		""" Here we rename the variable in all the math """
		#TODO
		# self.listOfFunctionDefinitions.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfSpecies.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfInitialAssignments.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfRules.renameSbmlId(old_sbml_id, new_sbml_id)
		# self.listOfConstraints.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfReactions.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfEvents.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfVariables.renameSbmlId(old_sbml_id, new_sbml_id)


	def getLevels(self):
		return [1,2,3]

	def getVersions(self):
		if self.sbmlLevel == 1:
			return [2]
		elif self.sbmlLevel == 2:
			return [1,2,3,4,5]
		elif self.sbmlLevel == 3:
			return [1]
		else:
			return []


	def setSbmlLevel(self, level):

		self.sbmlLevel = level

		if level == 1:
			self.sbmlVersion = 2
		elif level == 2:
			self.sbmlVersion = 5
		elif level == 3:
			self.sbmlVersion = 1
