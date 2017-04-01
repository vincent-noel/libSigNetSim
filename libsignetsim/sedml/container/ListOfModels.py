#!/usr/bin/env python
""" ListOfModels.py


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

from libsignetsim.sedml.container.ListOf import ListOf
from libsignetsim.sedml.Model import Model
from libsignetsim.settings.Settings import Settings


class ListOfModels(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)

		self.__document = document
		self.__modelCounter = 0

	def new(self, model_id=None):

		t_model_id = model_id
		if t_model_id is None:
			t_model_id = "model_%d" % self.__modelCounter

		model = Model(self.__document)
		model.setId(t_model_id)
		ListOf.append(self, model)
		self.__modelCounter += 1
		return model

	def createModel(self, model_id=None):
		return self.new(model_id)

	def readSedml(self, list_of_models, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_models, level, version)

		for t_model in list_of_models:
			model = Model(self.__document)
			model.readSedml(t_model, level, version)
			ListOf.append(self, model)
			self.__modelCounter += 1

	def writeSedml(self, list_of_models, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_models, level, version)

		for t_model in self:
			model = list_of_models.createModel()
			t_model.writeSedml(model, level, version)

	def getSbmlModels(self):

		models = []
		for model in self:
			models.append(model.getSbmlModel())

		return models

	def getByModelReference(self, model_reference):

		for model in self:
			if model.getId() == model_reference:
				return model.getSbmlModel()

	def writeSbmlModelsToPath(self, path):

		for model in self:
			model.writeSbmlModelToPath(path)
