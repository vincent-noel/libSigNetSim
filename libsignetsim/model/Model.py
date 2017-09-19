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


from libsignetsim.model.sbml.SbmlModel import SbmlModel
from libsignetsim.model.math.MathModel import MathModel
from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.settings.Settings import Settings
from time import time

class Model(SbmlModel, MathModel):
	""" Sbml model class """

	def __init__(self, obj_id=0, parent_doc=None, parent_obj=None):

		""" Constructor of model class """

		self.objId = obj_id

		SbmlModel.__init__(self, parent_doc, parent_obj, obj_id)
		MathModel.__init__(self, obj_id)
		self.listOfVariables = ListOfVariables(self)

	def build(self, vars_to_keep=[], dont_reduce=False, tmin=0):

		t0 = time()
		self.listOfVariables.classifyVariables()
		MathModel.buildModel(self, vars_to_keep=vars_to_keep, dont_reduce=dont_reduce, tmin=tmin)

		if Settings.verboseTiming >= 1:
			print ">> Model built in %.2gs" % (time()-t0)

	def cleanBeforePickle(self):
		# self.listOfVariables.cleanFinal()
		pass