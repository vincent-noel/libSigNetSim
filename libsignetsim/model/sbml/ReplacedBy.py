#!/usr/bin/env python
""" ReplacedBy.py




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


from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.HasRef import HasRef

class ReplacedBy(HasRef):

	def __init__(self, model, parent_obj):

		self.__model = model
		self.__parentObj = parent_obj
		HasRef.__init__(self, model)
		self.__submodelRef = None



	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasRef.readSbml(self, sbml_object, sbml_level, sbml_version)
		if sbml_object.isSetSubmodelRef():
			self.__submodelRef = sbml_object.getSubmodelRef()


	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		sbml_rb = sbml_object.createReplacedBy()
		HasRef.writeSbml(self, sbml_rb, sbml_level, sbml_version)
		if self.__submodelRef is not None:
			sbml_rb.setSubmodelRef(self.__submodelRef)

	def setSubmodelRef(self, submodel_ref):
		self.__submodelRef = submodel_ref


	def getSubmodelRef(self):
		return self.__submodelRef

	def hasModelRef(self):
		return self.__submodelRef is not None


	def getReplacingElementMetaId(self):

		# Now choosing the right model
		if self.hasModelRef():

			if self.getSubmodelRef() == self.__model.getSbmlId():
				tt_model = t_model

			else:
				tt_model = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef()).getModelObject()

			if self.hasIdRef():


				if self.hasSBaseRef():
					ttt_model = tt_model.listOfSubmodels.getBySbmlIdRef(self.getIdRef()).getModelObject()
					refs = self.getSBaseRef().getRef(ttt_model)

					t_ref = self.getIdRef()
					while len(refs) > 1:
						t_ref = "%s__%s" % (t_ref, refs[0])
						ttt_model = ttt_model.listOfSubmodels.getBySbmlIdRef(refs[0]).getModelObject()
						refs = refs[-1:]

					t_object = ttt_model.listOfSbmlObjects[refs[0]]

					return "%s__%s" % (t_ref, t_object.getMetaId())
				else:
					t_object = tt_model.listOfVariables.getBySbmlId(self.getIdRef())


			elif self.hasPortRef():
				t_object = tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

			elif self.hasMetaId():
				t_object = tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

			return t_object.getMetaId()


	# 
	# def getReplacingElementSubmodelAndObject(self):
	# 
	# 	submodels = []
	# 	res = None
	# 	# Now choosing the right model
	# 	if self.hasModelRef():
	# 
	# 		if self.getSubmodelRef() == self.__model.getSbmlId():
	# 			tt_model = t_model
	# 
	# 		else:
	# 			tt_model = self.__model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef()).getModelObject()
	# 
	# 		submodels.append(self.getSubmodelRef())
	# 
	# 		if self.hasIdRef():
	# 
	# 
	# 			if self.hasSBaseRef():
	# 				ttt_model = tt_model.listOfSubmodels.getBySbmlIdRef(self.getIdRef()).getModelObject()
	# 				refs = self.getSBaseRef().getRef(ttt_model)
	# 
	# 				# t_ref = self.getIdRef()
	# 				submodels.append(self.getIdRef())
	# 				while len(refs) > 1:
	# 					# t_ref = "%s__%s" % (t_ref, refs[0])
	# 					submodels.append(refs[0])
	# 					ttt_model = ttt_model.listOfSubmodels.getBySbmlIdRef(refs[0]).getModelObject()
	# 					refs = refs[-1:]
	# 
	# 				res = ttt_model.listOfSbmlObjects[refs[0]]
	# 
	# 				# return "%s__%s" % (t_ref, t_object.getMetaId())
	# 			else:
	# 				res = tt_model.listOfVariables.getBySbmlId(self.getIdRef())
	# 
	# 
	# 		elif self.hasPortRef():
	# 			res = tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()
	# 
	# 		elif self.hasMetaId():
	# 			res = tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())
	# 
	# 		return (submodels, res)

	def getReplacingElement(self):

		# Going back to the top level model
		if self.__model.isMainModel:
			t_model = self.__model
		else:
			self.__model.parentDoc.model


		# Now choosing the right model
		if self.hasModelRef():

			if self.getSubmodelRef() == t_model.getSbmlId():
				tt_model = t_model

			else:
				tt_model = t_model.listOfSubmodels.getBySbmlIdRef(self.getSubmodelRef()).getModelObject()


			if self.hasIdRef():
				t_object = tt_model.listOfVariables.getBySbmlId(self.getIdRef())
			elif self.hasPortRef():
				t_object = tt_model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

			elif self.hasMetaId():
				t_object = tt_model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

			return t_object


	def copy(self, obj, prefix="", shift=0):
		HasRef.copy(self, obj, prefix, shift)
		self.setSubmodelRef(obj.getSubmodelRef())

	def getParentObject(self):
		return self.__parentObj