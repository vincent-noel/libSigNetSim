#!/usr/bin/env python
""" SbmlDocument.py


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



from libsignetsim.model.Model import Model

from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.container.ListOfModelDefinitions import ListOfModelDefinitions
from libsignetsim.model.sbml.container.ListOfExternalModelDefinitions import ListOfExternalModelDefinitions
from libsignetsim.model.ModelInstance import ModelInstance
from libsignetsim.model.ModelException import (FileException, SbmlException,
														MissingModelException,
													  MissingSubmodelException)
from libsignetsim.settings.Settings import Settings

from os.path import isfile, isabs, dirname, join, basename
from libsbml import SBMLReader, SBMLDocument, writeSBMLToFile,\
					XMLFileUnreadable, XMLFileOperationError, \
					LIBSBML_CAT_UNITS_CONSISTENCY, LIBSBML_SEV_INFO, \
					LIBSBML_SEV_WARNING, \
					SBMLExtensionRegistry, readSBMLFromString
from time import time

class SbmlDocument(object):
	""" Sbml model class """


	def __init__ (self, model=None, path=None):
		""" Constructor of model class """

		self.useCompPackage = False
		self.modelInstance = None
		self.sbmlLevel = Settings.defaultSbmlLevel
		self.sbmlVersion = Settings.defaultSbmlVersion

		self.documentPath = None
		self.documentFilename = None
		self.documentDependenciesPaths = None
		self.documentDependencies = None

		self.isCompatible = None

		if model is None:
			self.model = Model(parent_doc=self, is_main_model=True)

		else:
			self.model = model
			self.sbmlLevel = model.sbmlLevel
			self.sbmlVersion = model.sbmlVersion

		self.listOfModelDefinitions = ListOfModelDefinitions(self.model)
		self.listOfExternalModelDefinitions = ListOfExternalModelDefinitions(self.model)


	def getSubmodel(self, submodel_id):
		if submodel_id in self.listOfModelDefinitions.sbmlIds():
			return self.listOfModelDefinitions.getBySbmlId(submodel_id)
		elif submodel_id in self.listOfExternalModelDefinitions.sbmlIds():
			return self.listOfExternalModelDefinitions.getBySbmlId(submodel_id)


	def enableComp(self):
		self.useCompPackage = True

	def isCompEnabled(self):
		return self.useCompPackage

	def checkCompatible(self, doc):
		""" This function checks if the documents
		needs a non-implemented package """

		for i in range(doc.getNumPlugins()):
			if doc.getPlugin(i).getPackageName() != "comp":
				return False
			else:
				return True


	def readSbml(self, sbmlDoc):

		if sbmlDoc.getNumErrors() > 0:
			if sbmlDoc.getError(0).getErrorId() == XMLFileUnreadable:
				raise FileException("Unreadable SBML file !")

			elif sbmlDoc.getError(0).getErrorId() == XMLFileOperationError:
				raise FileException("Error opening SBML file !")

			else:
				# Handle other error cases here.
				if Settings.showSbmlErrors:# and Settings.verbose:
					for error in range(0, sbmlDoc.getNumErrors()):
						print ">>> SBML Error %d : %s" % (error, sbmlDoc.getError(error).getMessage())


		self.sbmlLevel = sbmlDoc.getLevel()
		self.sbmlVersion = sbmlDoc.getVersion()

		if self.sbmlLevel == 3 and sbmlDoc.isSetPackageRequired("comp"):
			self.useCompPackage = True

		self.model.readSbml(sbmlDoc.getModel(), self.sbmlLevel, self.sbmlVersion)

		if self.useCompPackage:

			sbmlCompPlugin = sbmlDoc.getPlugin("comp")

			try:
				self.loadExternalDocumentDependencies(sbmlDoc)
				self.listOfModelDefinitions.readSbml(sbmlCompPlugin.getListOfModelDefinitions(), self.sbmlLevel, self.sbmlVersion)
				self.listOfExternalModelDefinitions.readSbml(sbmlCompPlugin.getListOfExternalModelDefinitions(), self.sbmlLevel, self.sbmlVersion)

			except MissingModelException as e:
				raise MissingSubmodelException(e.filename)


	def readSbmlFromFile(self, sbml_filename):
		# print "> Opening SBML file : %s" % sbml_filename
		t0 = time()

		if self.documentPath is None and dirname(sbml_filename) != "":
			self.documentPath = dirname(sbml_filename)

		self.documentFilename = basename(sbml_filename)

		t_filename = sbml_filename
		if dirname(sbml_filename) == "" and self.documentPath is not None:
			t_filename = join(self.documentPath, sbml_filename)

		if not isfile(t_filename):
			raise MissingModelException(t_filename)

		if Settings.verbose >= 2:
			print "> Opening SBML file : %s" % t_filename

		sbmlReader = SBMLReader()
		if sbmlReader == None:
			raise SbmlException("Error instanciating the SBMLReader !")

		sbmlDoc = sbmlReader.readSBML(t_filename)

		self.readSbml(sbmlDoc)


	def readSbmlFromString(self, string):


		sbmlReader = SBMLReader()
		if sbmlReader == None:
			raise SbmlException("Error instanciating the SBMLReader !")

		sbmlDoc = sbmlReader.readSBMLFromString(string)
		self.readSbml(sbmlDoc)


	def writeSbml(self):

		t0 = time()

		sbmlDoc = SBMLDocument(self.sbmlLevel,self.sbmlVersion)

		# Adding xhtml namespace to write notes
		# sbmlDoc.getNamespaces().add("http://www.w3.org/1999/xhtml", "xhtml")
		sbmlDoc.setLevelAndVersion(self.sbmlLevel, self.sbmlVersion)
		sbmlDoc.setConsistencyChecks(LIBSBML_CAT_UNITS_CONSISTENCY, False)


		if self.sbmlLevel == 3 and self.useCompPackage:
			sbmlDoc.enablePackage("http://www.sbml.org/sbml/level3/version1/comp/version1", "comp", True)
			sbmlDoc.setPackageRequired("comp", True)

		sbmlModel = sbmlDoc.createModel()
		self.model.writeSbml(sbmlModel, self.sbmlLevel, self.sbmlVersion)

		if self.sbmlLevel == 3 and self.useCompPackage:
			self.saveExternalDocumentDependencies(self.documentPath)
			self.listOfModelDefinitions.writeSbml(sbmlDoc.getPlugin("comp"), self.sbmlLevel, self.sbmlVersion)
			self.listOfExternalModelDefinitions.writeSbml(sbmlDoc.getPlugin("comp"), self.sbmlLevel, self.sbmlVersion)



		if Settings.showSbmlErrors:
			sbmlDoc.validateSBML()
			for error in range(0, sbmlDoc.getNumErrors()):

				if sbmlDoc.getError(error).getSeverity() not in [LIBSBML_SEV_INFO, LIBSBML_SEV_WARNING]:
					print ">>> SBML Error %d : %s" % (error, sbmlDoc.getError(error).getMessage())

				else:
					print ">>> SBML Warning %d : %s" % (error, sbmlDoc.getError(error).getMessage())

		return sbmlDoc


	def writeSbmlToFile(self, sbml_filename=None, path=None):

		t0 = time()

		# print sbml_filename

		if sbml_filename is not None:
			# if isabs(sbml_filename):
			self.documentPath = dirname(sbml_filename)

			self.documentFilename = basename(sbml_filename)

		if path is not None:
			self.documentPath = path

		# print self.documentPath
		# print self.documentFilename

		sbmlDoc = self.writeSbml()

		# Writing the final file

		result = writeSBMLToFile(sbmlDoc, join(self.documentPath, self.documentFilename))
		if result == 1:
			return True
		else:
			raise FileException("Failed to write %s" % join(self.documentPath, self.documentFilename))

			return False

		# if Settings.verboseTiming >= 1:
		# 	print "Writing document %s into directory %s in %.2gs" % (self.documentFilename, self.documentPath, time()-t0)


	def getModelInstance(self):
		if self.useCompPackage:
			t0 = time()
			t_instance = ModelInstance(self.model, self)
			t1 = time()

			if Settings.verboseTiming >= 1:
				print "> Instance produced in %.2gs" % (t1-t0)

			return t_instance
		else:
			return self.model

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

	def getExternalDocumentDependencies(self, sbml_doc=None):

		if self.useCompPackage:

			self.documentDependenciesPaths = []

			if sbml_doc is None:
				for external_doc in self.listOfExternalModelDefinitions.values():
					self.documentDependenciesPaths.append(external_doc.getSource())
			else:
				for external_doc in sbml_doc.getPlugin("comp").getListOfExternalModelDefinitions():
					if external_doc.isSetSource():
						self.documentDependenciesPaths.append(external_doc.getSource())

			self.documentDependenciesPaths = list(set(self.documentDependenciesPaths))


	def loadExternalDocumentDependencies(self, sbml_doc=None):

		if self.useCompPackage:
			if self.documentDependenciesPaths is None:
				self.getExternalDocumentDependencies(sbml_doc)

			self.documentDependencies = []
			# print self.documentDependenciesPaths
			# print self.documentPath
			for path in self.documentDependenciesPaths:
				t_document = SbmlDocument()
				t_document.readSbmlFromFile(join(self.documentPath, path))
				self.documentDependencies.append(t_document)


	def saveExternalDocumentDependencies(self, path=None):

		if self.useCompPackage:
			for document in self.documentDependencies:
				if path is None:
					document.writeSbmlToFile()
				else:
					document.writeSbmlToFile(path=path)
