#!/usr/bin/env python
""" EquilibriumPointCurve.py


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

from PyDSTool import args, ContClass, PyDSTool_ExistError

import threading
from time import time
from PyDSToolModel import PyDSToolModel

class EquilibriumPointCurve(object):

	def __init__ (self, model):

		self.model = model
		self.system = PyDSToolModel(model)
		self.continuation = None
		self.parameter = None
		self.variable = None
		self.continuationParameters = None
		self.fromValue = None
		self.toValue = None
		

	def setParameter(self, parameter):

		if parameter.localParameter:
			self.parameter = "local_%d_%s" % (parameter.reaction.objId, parameter.getSbmlId())
		else:
			self.parameter = parameter.getSbmlId()


	def setVariable(self, sbml_id):
		self.variable = sbml_id

	def setRange(self, from_value, to_value):
		self.fromValue = from_value
		self.toValue = to_value

	def build(self):

		self.system.build(self.parameter, self.toValue, vars_to_keep=[self.parameter, self.variable])
		self.buildCont()

	def run(self, callback_function_success, callback_function_error):
		self.executeContThread(callback_function_success, callback_function_error)


	def buildCont(self):

		self.continuation = ContClass(self.system.getSystem())

		self.continuationParameters = args(name='EQ1', type='EP-C')
		self.continuationParameters.freepars = [self.parameter]
		self.continuationParameters.StepSize = 0.001
		self.continuationParameters.MaxNumPoints = 1500
		self.continuationParameters.MaxStepSize = 1
		self.continuationParameters.MinStepSize = 0.00001
		self.continuationParameters.LocBifPoints = 'All'
		self.continuationParameters.verbosity = 0
		self.continuationParameters.SaveEigen = True

		self.continuation.newCurve(self.continuationParameters)



	def executeCont(self, callback_function_success, callback_function_error):

		try:
			print "> Starting thread"
			t0 = time()
			self.continuation['EQ1'].forward()
			callback_function_success(self)

			print "> Exiting thread (executed in %.3gs)" % (time()-t0)
		except RuntimeError:
			callback_function_error()
		except PyDSTool_ExistError:
			callback_function_error()

	def executeContThread(self, callback_function_success, callback_function_error):


		t = threading.Thread(group=None, target=self.executeCont, args=(callback_function_success, callback_function_error))
		t.setDaemon(True)
		t.start()
