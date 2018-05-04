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
from .PyDSToolModel import PyDSToolModel

class EquilibriumPointCurve(object):

	NOT_STARTED = 10
	STARTED 	= 11
	SUCCESS		= 12
	FAILED		= 13

	MAIN_CURVE = 'EQ1'
	LIMIT_CYCLE_CURVE = 'LC1'

	def __init__ (self, model):

		self.model = model
		self.system = PyDSToolModel(model)
		self.continuation = None
		self.parameter = None
		self.continuationParameters = None
		self.fromValue = None
		self.toValue = None
		self.ds = 0.1
		self.maxSteps = 1000
		self.verbosity = 0
		self.status = self.NOT_STARTED

	def setParameter(self, parameter):
		self.parameter = parameter

	def setRange(self, from_value, to_value):
		self.fromValue = from_value
		self.toValue = to_value

	def setDs(self, ds):
		self.ds = ds

	def setMaxSteps(self, max_steps):
		self.maxSteps = max_steps

	def setVerbosity(self, verbosity):
		self.verbosity = verbosity

	def build(self):

		self.system.build(
			self.parameter,
			self.fromValue, vars_to_keep=[self.parameter.getSymbolStr()]
		)

		self.buildCont()

	def run_async(self, callback_function_success, callback_function_error):
		self.executeContThread(callback_function_success, callback_function_error)

	def run(self):
		self.executeCont()

	def buildCont(self):

		self.continuation = ContClass(self.system.getSystem())

		self.continuationParameters = args(name=self.MAIN_CURVE, type='EP-C')
		self.continuationParameters.freepars = [self.parameter.getSymbolStr()]
		self.continuationParameters.StepSize = abs(self.ds)
		self.continuationParameters.MaxNumPoints = self.maxSteps
		self.continuationParameters.MaxStepSize = self.ds*100
		self.continuationParameters.MinStepSize = self.ds/100
		self.continuationParameters.LocBifPoints = 'All'
		self.continuationParameters.verbosity = self.verbosity
		self.continuationParameters.SaveEigen = True

		self.continuation.newCurve(self.continuationParameters)

	def executeCont(self, callback_function_success=None, callback_function_error=None):

		if callback_function_success is not None:
			print("> Starting thread")

		self.status = self.STARTED
		try:
			t0 = time()
			if self.ds > 0:
				self.continuation[self.MAIN_CURVE].forward()
			else:
				self.continuation[self.MAIN_CURVE].backward()

			if self.hasHopfBifurcations():
				self.findLimitCycleCurves()

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

	def getCurve(self, variable):

		if self.status == self.SUCCESS:
			x, ys = self.getCurves()
			return x, ys[variable.getSymbolStr()]

	def getCurves(self):

		if self.status == self.SUCCESS:

			len_curve = len(self.continuation[self.MAIN_CURVE].curve[:, 1]) - 1
			nb_variables = len(self.continuation[self.MAIN_CURVE].varslist)
			x = self.continuation[self.MAIN_CURVE].curve[0:len_curve, nb_variables]
			x = [x_i for x_i in x if self.fromValue <= x_i <= self.toValue]
			ys = {}
			for i, var in enumerate(self.continuation[self.MAIN_CURVE].varslist):

				y = self.continuation[self.MAIN_CURVE].curve[0:len_curve, i]
				y = [y_i for x_i, y_i in zip(x, y) if self.fromValue <= x_i <= self.toValue]
				ys.update({var: y})

			return x, ys

	def getStability(self, x):

		if self.status == self.SUCCESS:

			stability = []
			for i in range(len(self.continuation[self.MAIN_CURVE].sol.labels)):
				label = self.continuation[self.MAIN_CURVE].sol.labels[i]
				if 'EP' in list(label.keys()) and i < len(x) and self.fromValue <= x[i] <= self.toValue:
						stability.append(label['EP']['stab'])

			return stability


	def getStabilitySlicedCurves(self):

		if self.status == self.SUCCESS:

			x, ys = self.getCurves()
			stability = self.getStability(x)

			split = []
			t_res = []
			for i, x_i in enumerate(stability):
				if i == 0:
					t_res.append(i)
				else:
					if x_i == stability[i - 1]:
						t_res.append(i)
					else:
						split.append(t_res)
						t_res = [i]

			split.append(t_res)

			split_stability = []
			split_x = []
			split_ys = {var: [] for var in list(ys.keys())}

			for inds in split:
				split_stability.append(stability[inds[0]])
				split_x.append([x[i] for i in inds])

				for var, y in list(ys.items()):
					split_ys[var].append([y[i] for i in inds])

			return split_x, split_ys, split_stability


	def getLimitCycleCurves(self):

		x = []
		curves = {}

		if self.status == self.SUCCESS and self.LIMIT_CYCLE_CURVE in list(self.continuation.curves.keys()):

			len_curve = len(self.continuation[self.LIMIT_CYCLE_CURVE].curve[:, 1]) - 1
			nb_variables = len(self.continuation[self.LIMIT_CYCLE_CURVE].varslist)
			x = self.continuation[self.LIMIT_CYCLE_CURVE].curve[0:len_curve - 1, nb_variables * 2]
			x = [x_i for x_i in x if self.fromValue <= x_i <= self.toValue]

			for i, var in enumerate(self.continuation[self.LIMIT_CYCLE_CURVE].varslist):
				t_ys = {}
				y_min = self.continuation[self.LIMIT_CYCLE_CURVE].curve[0:len_curve - 1, i]
				y_max = self.continuation[self.LIMIT_CYCLE_CURVE].curve[0:len_curve - 1, i + nb_variables]
				y_min = [y_i for x_i, y_i in zip(x, y_min) if self.fromValue <= x_i <= self.toValue]
				y_max = [y_i for x_i, y_i in zip(x, y_max) if self.fromValue <= x_i <= self.toValue]
				t_ys.update({'min': y_min})
				t_ys.update({'max': y_max})

				curves.update({var: t_ys})

		return x, curves

	def getPoints(self):

		if self.status == self.SUCCESS:

			t_points = {}
			for var in self.continuation[self.MAIN_CURVE].varslist:
				t_points.update({var: []})

			for points_type, points in list(self.continuation[self.MAIN_CURVE].BifPoints.items()):
				for point in points.found:
					if self.fromValue <= point.X[self.parameter.getSymbolStr()] <= self.toValue:
						points_x = point.X[self.parameter.getSymbolStr()]
						for var in self.continuation[self.MAIN_CURVE].varslist:
							t_points[var].append((points_type, points_x, point.X[var]))

			return t_points

	def hasHopfBifurcations(self):
		return len(self.continuation[self.MAIN_CURVE].BifPoints['H'].found) > 0

	def findLimitCycleCurves(self, point='H1'):

		if self.hasHopfBifurcations():

			limit_cycle_args = args(name=self.LIMIT_CYCLE_CURVE, type='LC-C')
			limit_cycle_args.initpoint = self.MAIN_CURVE + ':' + point
			limit_cycle_args.freepars = [self.parameter.getSymbolStr()]
			limit_cycle_args.MaxNumPoints = self.maxSteps
			limit_cycle_args.setSize = self.ds
			limit_cycle_args.MinStepSize = self.ds/100
			limit_cycle_args.MaxStepSize = self.ds*100
			limit_cycle_args.LocBifPoints = 'all'
			limit_cycle_args.SaveEigen = True
			limit_cycle_args.verbosity = self.verbosity
			self.continuation.newCurve(limit_cycle_args)

			self.continuation[self.LIMIT_CYCLE_CURVE].forward()

	def plotCurve(self, plot, variable):

		x, ys, stab = self.getStabilitySlicedCurves()
		points = self.getPoints()

		for i, (slice_x, slice_y) in enumerate(zip(x, ys[variable.getSymbolStr()])):

			if stab[i] == 'S':
				color = "b-"
			elif stab[i] == 'N':
				color = 'r--'
			elif stab[i] == 'U':
				color = 'b--'
			else:
				color = 'r-'

			plot.plot(slice_x, slice_y, color)

		points_var = points[variable.getSymbolStr()]
		x = [x_i for _, x_i, _ in points_var]
		y = [y_i for _, _, y_i in points_var]
		plot.plot(x, y, 'ro')
		plot.set_xlim(self.fromValue, self.toValue)

	def plotLimitCycles(self, plot, variable):

		if self.hasHopfBifurcations():
			self.findLimitCycleCurves()
			x, ys = self.getLimitCycleCurves()
			plot.plot(x, ys[variable.getSymbolStr()]['min'], 'b-')
			plot.plot(x, ys[variable.getSymbolStr()]['max'], 'b-')