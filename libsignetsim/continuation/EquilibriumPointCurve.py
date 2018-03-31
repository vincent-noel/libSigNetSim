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

from PyDSTool import args, ContClass, PyDSTool_ExistError

import threading
from time import time
from PyDSToolModel import PyDSToolModel

class EquilibriumPointCurve(object):

	NOT_STARTED = 10
	STARTED 	= 11
	SUCCESS		= 12
	FAILED		= 13

	def __init__ (self, model):

		self.model = model
		self.system = PyDSToolModel(model)
		self.continuation = None
		self.parameter = None
		self.variable = None
		self.continuationParameters = None
		self.fromValue = None
		self.toValue = None
		self.ds = 0.1
		self.maxSteps = 1000
		self.status = self.NOT_STARTED

	def setParameter(self, parameter):
		self.parameter = parameter

	def setVariable(self, variable):
		self.variable = variable

	def setRange(self, from_value, to_value):
		self.fromValue = from_value
		self.toValue = to_value

	def setDs(self, ds):
		self.ds = ds

	def setMaxSteps(self, max_steps):
		self.maxSteps = max_steps

	def build(self):

		self.system.build(
			self.parameter.getSymbolStr(),
			self.fromValue, vars_to_keep=[self.parameter.getSymbolStr(), self.variable.getSymbolStr()]
		)
		self.buildCont()

	def run_async(self, callback_function_success, callback_function_error):
		self.executeContThread(callback_function_success, callback_function_error)

	def run(self):
		self.executeCont()

	def buildCont(self):

		self.continuation = ContClass(self.system.getSystem())

		self.continuationParameters = args(name='EQ1', type='EP-C')
		self.continuationParameters.freepars = [self.parameter.getSymbolStr()]
		self.continuationParameters.StepSize = self.ds
		self.continuationParameters.MaxNumPoints = self.maxSteps
		self.continuationParameters.MaxStepSize = self.ds*100
		self.continuationParameters.MinStepSize = self.ds/100
		self.continuationParameters.LocBifPoints = 'All'
		self.continuationParameters.verbosity = 0
		self.continuationParameters.SaveEigen = True

		self.continuation.newCurve(self.continuationParameters)

	def executeCont(self, callback_function_success=None, callback_function_error=None):

		if callback_function_success is not None:
			print("> Starting thread")

		self.status = self.STARTED
		try:
			t0 = time()
			if self.ds > 0:
				self.continuation['EQ1'].forward()
			else:
				self.continuation['EQ1'].backward()

			self.status = self.SUCCESS

			if callback_function_success is not None:
				print("> Exiting thread (executed in %.3gs)" % (time() - t0))
				callback_function_success(self)


		except RuntimeError:
			self.status = self.FAILED
			if callback_function_error is not None:
				callback_function_error()

		except PyDSTool_ExistError:
			self.status = self.FAILED
			if callback_function_error is not None:
				callback_function_error()

	def executeContThread(self, callback_function_success, callback_function_error):

		t = threading.Thread(group=None, target=self.executeCont, args=(callback_function_success, callback_function_error))
		t.setDaemon(True)
		t.start()

	def getCurves(self):

		curves = []

		if self.status == self.SUCCESS:

			for curve_id in self.continuation.curves.keys():
				t_curves = {}

				len_curve = len(self.continuation[curve_id].curve[:, 1]) - 1
				parameter_indice = len(self.continuation[curve_id].varslist)

				for i, var in enumerate(self.continuation[curve_id].varslist):

					x = self.continuation[curve_id].curve[0:len_curve - 1, parameter_indice]
					y = self.continuation[curve_id].curve[0:len_curve - 1, i]
					xy = [(x_i, y_i) for i, (x_i, y_i) in enumerate(zip(x, y)) if x_i < 500]
					t_curves.update({var: xy})

				curves.append(t_curves)

		return curves

	def getPoints(self):

		res_points = []

		if self.status == self.SUCCESS:

			for curve_id in self.continuation.curves.keys():
				t_points = {}
				for var in self.continuation[curve_id].varslist:
					t_points.update({var: []})


				for points_type, points in self.continuation[curve_id].BifPoints.items():

					for point in points.found:
						points_x = point.X[self.parameter.getSymbolStr()]
						for var in self.continuation[curve_id].varslist:
							t_points[var].append((points_type, points_x, point.X[var]))

				res_points.append(t_points)
		return res_points