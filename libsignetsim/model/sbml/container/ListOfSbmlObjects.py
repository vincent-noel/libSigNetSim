#!/usr/bin/env python
""" ListOfSbmlObjects.py


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


from libsignetsim.model.sbml.container.ListOf_v2 import ListOf_v2
from libsignetsim.model.sbml.container.ListOfReplacedElements import ListOfReplacedElements


class ListOfSbmlObjects(ListOf_v2):
	""" Class for the listOfModelDefinition in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		ListOf_v2.__init__(self, model)
		self.isListOfSbmlObjects = True
		self.currentObjId = -1

	def nextMetaId(self):
		self.currentObjId += 1
		return "_meta_id_%d_" % self.currentObjId

	def addSbmlObject(self, sbml_object, prefix=""):

		if sbml_object.getMetaId() is None:
			sbml_object.setMetaId(self.nextMetaId())

		if self.containsMetaId(sbml_object.getMetaId()):

			t_meta_id = sbml_object.getMetaId()
			while self.containsMetaId(t_meta_id):
				t_meta_id = self.nextMetaId()

			sbml_object.rawSetMetaId(t_meta_id)

		self.append(sbml_object)

		return sbml_object


	def listReplacedElements(self):

		res = []
		for obj in ListOf_v2.values(self):
			if not isinstance(obj, ListOfReplacedElements) and obj.hasReplacedElements():
				for replaced_element in obj.getReplacedElements():
					res.append(replaced_element)
		return res


	def getListOfSubstitutions(self):

		res = []
		for obj in ListOf_v2.values(self):
			if obj.hasReplacedElements():
				res += obj.getReplacedElements()

			if obj.isReplaced():
				res.append(obj.getReplacedBy())

		return res

	def getListOfSubstitutions_old(self):

		res = []
		type_substitutions = []
		for obj in ListOf_v2.values(self):
			if obj.hasReplacedElements():
				for replaced_element in obj.getReplacedElements():

					model_object = obj
					submodels, submodel_object = replaced_element.getReplacedElementSubmodelAndObject()
					res.append((0, model_object, submodels, submodel_object))
			if obj.isReplaced():
				t_rp = obj.getReplacedBy()
				model_object = obj
				submodels, submodel_object = t_rp.getReplacingElementSubmodelAndObject()
				res.append((1, model_object, submodels, submodel_object))
		return res

	def getListOfElementsToBeReplaced(self):

		res = []
		for obj in ListOf_v2.values(self):
			if not isinstance(obj, ListOfReplacedElements) and obj.hasReplacedElements():
				for replaced_element in obj.getReplacedElements():
					if replaced_element.getSubmodelRef() == self.__model.getSbmlId():
						t_object = self.__model.listOfVariables.getBySbmlId(replaced_element.getIdRef())
						res.append(t_object)

					else:
						t_model = self.__model.listOfSubmodels.getBySbmlId(replaced_element.getSubmodelRef()).getModelObject()
						t_object = t_model.listOfVariables.getBySbmlId(replaced_element.getIdRef())
						res.append(t_object)

		return res


	def hasToBeReplaced(self, ask_object):

		for obj in ListOf_v2.values(self):
			if not isinstance(obj, ListOfReplacedElements) and obj.hasReplacedElements():
				for replaced_element in obj.getReplacedElements():
					if replaced_element.getSubmodelRef() == self.__model.getSbmlId():
						t_object = self.__model.listOfVariables.getBySbmlId(replaced_element.getIdRef())
						if t_object == ask_object:
							return True

					else:
						t_model = self.__model.listOfSubmodels.getBySbmlId(replaced_element.getSubmodelRef()).getModelObject()
						t_object = t_model.listOfVariables.getBySbmlId(replaced_element.getIdRef())
						if t_object == ask_object:
							return True
		return False


	def getReplacedBy(self, ask_object):

		for obj in ListOf_v2.values(self):
			if not isinstance(obj, ListOfReplacedElements) and not isinstance(obj, Model) and obj.hasReplacedElements():
				for replaced_element in obj.getReplacedElements():
					if replaced_element.getSubmodelRef() == self.__model.getSbmlId():
						t_object = self.__model.listOfVariables.getBySbmlId(replaced_element.getIdRef())
						if t_object == ask_object:
							return obj

					else:
						t_model = self.__model.listOfSubmodels.getBySbmlId(replaced_element.getSubmodelRef()).getModelObject()
						t_object = t_model.listOfVariables.getBySbmlId(replaced_element.getIdRef())
						if t_object == ask_object:
							return obj



	def metaIds(self):
		""" Return set of names of the sbml objects """
		return [obj.getMetaId() for obj in self.values()]

	def getByMetaId(self, meta_id, pos=0):
		""" Find sbml objects by their name """

		res = []
		for obj in self.values():
			if obj.getMetaId() == meta_id:
				res.append(obj)

		if len(res) > 0:
			return res[pos]
		else:
			return None


	def containsMetaId(self, meta_id):
		""" Test if a name is in the list """

		res = False
		for obj in self.values():
			if meta_id == obj.getMetaId():
				res = True

		return res

