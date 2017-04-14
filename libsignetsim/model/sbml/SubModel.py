#!/usr/bin/env python
""" SubModel.py




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


from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.sbml.container.ListOfDeletions import ListOfDeletions

class SubModel(HasId):#, SbmlObject):

	def __init__(self, model, obj_id):

		self.__model = model
		self.objId = obj_id

		HasId.__init__(self, model)
		# SbmlObject.__init__(self, model)

		self.__modelRef = None
		self.__timeConversionFactor = None
		self.__extentConversionFactor = None
		self.listOfDeletions = ListOfDeletions(model, self)

	def readSbml(self, sbml_submodel,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasId.readSbml(self, sbml_submodel, sbml_level, sbml_version)

		if sbml_submodel.isSetModelRef():
			self.__modelRef = sbml_submodel.getModelRef()

		if sbml_submodel.isSetTimeConversionFactor():
			self.__timeConversionFactor = MathFormula(self.__model)
			self.__timeConversionFactor.readSbml(
					sbml_submodel.getTimeConversionFactor(),
					sbml_level, sbml_version)

		if sbml_submodel.isSetExtentConversionFactor():
			self.__extentConversionFactor = MathFormula(self.__model)
			self.__extentConversionFactor.readSbml(
					sbml_submodel.getExtentConversionFactor(),
					sbml_level, sbml_version)

		self.listOfDeletions.readSbml(sbml_submodel.getListOfDeletions(),
									sbml_level, sbml_version)

		# SbmlObject.readSbml(self, sbml_submodel, sbml_level, sbml_version)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		sbml_submodel = sbml_model.createSubmodel()

		HasId.writeSbml(self, sbml_submodel, sbml_level, sbml_version)
		if self.__modelRef is not None:
			sbml_submodel.setModelRef(self.__modelRef)

		if self.__timeConversionFactor is not None:
			sbml_submodel.setTimeConversionFactor(self.__timeConversionFactor.getSbmlMathFormula().getName())

		if self.__extentConversionFactor is not None:
			sbml_submodel.setExtentConversionFactor(self.__extentConversionFactor.getSbmlMathFormula().getName())

		self.listOfDeletions.writeSbml(sbml_submodel, sbml_level, sbml_version)
		# SbmlObject.writeSbml(self, sbml_submodel, sbml_level, sbml_version)

	def hasExtentConversionFactor(self):
		return self.__extentConversionFactor is not None

	def getExtentConversionFactor(self):
		return self.__extentConversionFactor

	def setExtentConversionFactor(self, conv_factor):
		if self.__extentConversionFactor is None:
			self.__extentConversionFactor = MathFormula(self.__model)
		self.__extentConversionFactor.setPrettyPrintMathFormula(conv_factor)

	def unsetExtentConversionFactor(self):
		self.__extentConversionFactor = None

	def hasTimeConversionFactor(self):
		return self.__timeConversionFactor is not None

	def getTimeConversionFactor(self):
		return self.__timeConversionFactor

	def setTimeConversionFactor(self, conv_factor):
		if self.__timeConversionFactor is None:
			self.__timeConversionFactor = MathFormula(self.__model)
		self.__timeConversionFactor.setPrettyPrintMathFormula(conv_factor)

	def unsetTimeConversionFactor(self):
		self.__timeConversionFactor = None

	def setModelRef(self, model_ref):
		self.__modelRef = model_ref


	def getModelRef(self):
		return self.__modelRef

	def getModelObject(self):

		if self.__modelRef == self.__model.getSbmlId():
			return self.__model
		else:
			t_doc = self.__model.parentDoc
			if self.__modelRef in t_doc.listOfModelDefinitions.sbmlIds():
				return t_doc.listOfModelDefinitions.getBySbmlId(self.__modelRef).modelDefinition
			elif self.__modelRef in t_doc.listOfExternalModelDefinitions.sbmlIds():
				return t_doc.listOfExternalModelDefinitions.getBySbmlId(self.__modelRef).modelDefinition


	def getDeletionsMetaIds(self):

		deletions = []

		for deletion in self.listOfDeletions.values():
			if deletion.hasIdRef():
				if deletion.hasSBaseRef():
					ttt_model = self.getModelObject().listOfSubmodels.getBySbmlIdRef(deletion.getIdRef()).getModelObject()
					refs = deletion.getSBaseRef().getRef(ttt_model)

					t_ref = deletion.getIdRef()
					while len(refs) > 1:
						t_ref = "%s__%s" % (t_ref, refs[0])
						ttt_model = ttt_model.listOfSubmodels.getBySbmlIdRef(refs[0]).getModelObject()
						refs = refs[-1:]

					t_object = ttt_model.listOfSbmlObjects[refs[0]]
					deletions.append("%s__%s" % (t_ref, t_object.getMetaId()))

				else:
					if deletion.getIdRef() in self.getModelObject().listOfVariables.keys():
						deletions.append(self.getModelObject().listOfVariables.getBySbmlId(deletion.getIdRef()).getMetaId())
					elif self.getModelObject().listOfEvents.containsSbmlId(deletion.getIdRef()):
						deletions.append(self.getModelObject().listOfEvents.getBySbmlId(deletion.getIdRef()).getMetaId())

			elif deletion.hasPortRef():
				deletions.append(self.getModelObject().listOfPorts.getBySbmlId(deletion.getPortRef()).getRefObject().getMetaId())

			elif deletion.hasMetaIdRef():
				deletions.append(deletion.getMetaIdRef())

		return deletions

	def getModelInstance(self):
		from libsignetsim.model.ModelInstance import ModelInstance

		return ModelInstance(self.getModelObject(), self.__model.parentDoc)
