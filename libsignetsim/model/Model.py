#!/usr/bin/env python
""" Model.py


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


from libsignetsim.model.sbmlobject.SbmlModel import SbmlModel
from libsignetsim.model.math.MathModel import MathModel
from libsignetsim.model.ListOfVariables import ListOfVariables


class Model(SbmlModel, MathModel):
	""" Sbml model class """


	def __init__ (self, obj_id=0, parent_doc=None, is_main_model=False, is_model_instance=False):
		""" Constructor of model class """

		self.objId = obj_id
		self.isMainModel = is_main_model
		self.isModelInstance = is_model_instance

		SbmlModel.__init__(self, parent_doc, obj_id)
		MathModel.__init__(self, obj_id)
		self.listOfVariables = ListOfVariables(self)
		self.listOfInstanceVariables = ListOfVariables(self)

	def build(self, vars_to_keep=[], dont_reduce=False):

		self.listOfInstanceVariables.buildInstance()
		self.listOfVariables.classifyVariables()
		MathModel.buildModel(self, vars_to_keep=vars_to_keep, dont_reduce=dont_reduce)

	def cleanBeforePickle(self):
		self.listOfVariables.cleanFinal()
