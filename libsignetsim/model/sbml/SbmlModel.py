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
from __future__ import print_function

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

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.ModelUnits import ModelUnits
from libsignetsim.model.sbml.SbmlModelAnnotation import SbmlModelAnnotation
from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.HasConversionFactor import HasConversionFactor
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.ModelException import InvalidXPath

from time import time
from re import match


class SbmlModel(HasId, SbmlObject, ModelUnits, SbmlModelAnnotation, HasConversionFactor, HasParentObj):
	""" Sbml model class """


	def __init__ (self, parent_document, parent_obj, obj_id=0):
		""" Constructor of model class """

		self.objId = obj_id

		self.sbmlLevel = Settings.defaultSbmlLevel
		self.sbmlVersion = Settings.defaultSbmlVersion

		if parent_document is None:
			from libsignetsim.model.SbmlDocument import SbmlDocument
			self.parentDoc = SbmlDocument(self)
		else:
			self.parentDoc = parent_document

		if parent_obj is None:
			HasParentObj.__init__(self, self.parentDoc)
		else:
			HasParentObj.__init__(self, parent_obj)

		HasId.__init__(self, self)
		self.listOfSbmlObjects = ListOfSbmlObjects(self)
		SbmlObject.__init__(self, self)
		SbmlModelAnnotation.__init__(self)
		ModelUnits.__init__(self)
		HasConversionFactor.__init__(self, self)

		self.listOfSpecies = ListOfSpecies(self, self)
		self.listOfParameters = ListOfParameters(self, self)
		self.listOfReactions = ListOfReactions(self, self)
		self.listOfCompartments = ListOfCompartments(self, self)
		self.listOfFunctionDefinitions = ListOfFunctionDefinitions(self)
		self.listOfUnitDefinitions = ListOfUnitDefinitions(self)
		self.listOfRules = ListOfRules(self)
		self.listOfEvents = ListOfEvents(self, self)
		self.listOfConstraints = ListOfConstraints(self)
		self.listOfInitialAssignments = ListOfInitialAssignments(self, self)

		self.listOfSubmodels = ListOfSubmodels(self)
		self.listOfPorts = ListOfPorts(self)

		self.defaultCompartment = None

	def newModel(self, name):

		self.setName(name)
		self.setSbmlId("model_%d" % self.objId)

		ModelUnits.setDefaultUnits(self)
		self.defaultCompartment = self.listOfCompartments.new("cell")

	def readSbml(self, sbmlModel,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion, parent_doc=None):

		t0 = time()

		self.sbmlLevel = sbml_level
		self.sbmlVersion = sbml_version

		HasId.readSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)
		SbmlObject.readSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)
		SbmlModelAnnotation.readSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)

		self.listOfFunctionDefinitions.readSbml(sbmlModel.getListOfFunctionDefinitions(), self.sbmlLevel, self.sbmlVersion)
		self.listOfUnitDefinitions.readSbml(sbmlModel.getListOfUnitDefinitions(), self.sbmlLevel, self.sbmlVersion)
		ModelUnits.readSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)


		self.listOfCompartments.readSbml(sbmlModel.getListOfCompartments(), self.sbmlLevel, self.sbmlVersion)
		self.listOfParameters.readSbml(sbmlModel.getListOfParameters(), self.sbmlLevel, self.sbmlVersion)

		# We need to load the parameters before reading the conversion factor
		if self.sbmlLevel >= 3:
			if sbmlModel.isSetConversionFactor():
				HasConversionFactor.readSbml(self, sbmlModel.getConversionFactor(), self.sbmlLevel, self.sbmlVersion)

		self.listOfSpecies.readSbml(sbmlModel.getListOfSpecies(), self.sbmlLevel, self.sbmlVersion)
		self.listOfReactions.readSbml(sbmlModel.getListOfReactions(), self.sbmlLevel, self.sbmlVersion)
		self.listOfInitialAssignments.readSbml(sbmlModel.getListOfInitialAssignments(), self.sbmlLevel, self.sbmlVersion)
		self.listOfRules.readSbml(sbmlModel.getListOfRules(), self.sbmlLevel, self.sbmlVersion)
		self.listOfConstraints.readSbml(sbmlModel.getListOfConstraints(), self.sbmlLevel, self.sbmlVersion)
		self.listOfEvents.readSbml(sbmlModel.getListOfEvents(), self.sbmlLevel, self.sbmlVersion)

		if self.sbmlLevel == 3 and self.parentDoc.isCompEnabled():
			self.listOfSubmodels.readSbml(sbmlModel.getPlugin("comp").getListOfSubmodels(), self.sbmlLevel, self.sbmlVersion)
			self.listOfPorts.readSbml(sbmlModel.getPlugin("comp").getListOfPorts(), self.sbmlLevel, self.sbmlVersion)

		if Settings.verboseTiming >= 1:
			print(">> SBML Model %s read in %.2gs" % (self.getSbmlId(), time()-t0))


	def writeSbml(self, sbmlModel,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		t0 = time()

		if self.sbmlLevel == 3 and self.parentDoc.isCompEnabled():
			sbmlModel.enablePackage("http://www.sbml.org/sbml/level3/version1/comp/version1", "comp", True)

		SbmlObject.writeSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)
		HasId.writeSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)
		SbmlModelAnnotation.writeSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)

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
		ModelUnits.writeSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)

		if self.sbmlLevel >= 3:
			if self.isSetConversionFactor():
				HasConversionFactor.writeSbml(self, sbmlModel, self.sbmlLevel, self.sbmlVersion)

		if self.sbmlLevel == 3 and self.parentDoc.isCompEnabled():
			self.listOfSubmodels.writeSbml(sbmlModel.getPlugin("comp"), self.sbmlLevel, self.sbmlVersion)
			self.listOfPorts.writeSbml(sbmlModel.getPlugin("comp"), self.sbmlLevel, self.sbmlVersion)

		if Settings.verboseTiming >= 2:
			print("> SBML Model %s written in %.2gs" % (self.getSbmlId(), time()-t0))

	def renameSbmlId(self, old_sbml_id, new_sbml_id):
		""" Here we rename the variable in all the math """

		self.listOfSpecies.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfVariables.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfInitialAssignments.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfRules.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfReactions.renameSbmlId(old_sbml_id, new_sbml_id)
		self.listOfEvents.renameSbmlId(old_sbml_id, new_sbml_id)


	def getSbmlLevels(self):
		return [1,2,3]

	def getSbmlVersions(self):
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

	def resolveXPath(self, selector):

		if selector in ["sbml:listOfSpecies", "listOfSpecies"]:
			return self.listOfSpecies

		elif selector in ["sbml:listOfParameters", "listOfParameters"]:
			return self.listOfParameters

		elif selector in ["sbml:listOfCompartments", "listOfCompartments"]:
			return self.listOfCompartments

		elif selector in ["sbml:listOfReactions", "listOfReactions"]:
			return self.listOfReactions

		elif selector in ["sbml:listOfInitialAssignments", "listOfInitialAssignments"]:
			return self.listOfInitialAssignments

		elif selector in ["sbml:listOfEvents", "listOfEvents"]:
			return self.listOfEvents


		elif selector == "sbml:listOfSubmodels" and self.parentDoc.useCompPackage:
			return self.listOfSubmodels


		elif selector.startswith("descendant::"):
			res_match = match(r"descendant::\*\[@(.*)=\'(.*)\'\]", selector)
			if res_match is None:
				raise InvalidXPath(selector)

			res = res_match.groups()
			if res[0] == "id":
				return self.listOfVariables.getBySbmlId(res[1])

			elif res[0] == "name":
				return self.listOfVariables.getByName(res[1])

			elif res[0] == "metaid":
				return self.listOfSbmlObjects.getByMetaId(res[1])

		raise InvalidXPath(selector)

	def getByXPath(self, xpath):
		return self.resolveXPath(xpath[0]).getByXPath(xpath[1:])

	def setByXPath(self, xpath, object):
		self.resolveXPath(xpath[0]).setByXPath(xpath[1:], object)

	def getXPath(self):
		if self.getParentObj() is not None:
			return "/".join([self.getParentObj().getXPath(), "sbml:model"])
		else:
			return "sbml:model"