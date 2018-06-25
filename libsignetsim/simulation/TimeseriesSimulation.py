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
from __future__ import division

from libsignetsim.simulation.Simulation import Simulation
from libsignetsim.figure.SigNetSimFigure import SigNetSimFigure
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from libsignetsim.settings.Settings import Settings
from matplotlib.pyplot import show
from numpy import amin, amax, linspace, logspace
from os.path import join, isfile
from threading import Thread


class TimeseriesSimulation(Simulation):

	DEFAULT_NB_SAMPLES = 500

	def __init__ (self, list_of_models=[],
					experiment=None,
					time_min=Settings.simulationTimeMin,
					time_max=Settings.simulationTimeMax,
					abs_tol=Settings.defaultAbsTol,
					rel_tol=Settings.defaultRelTol,
					log_scale=Settings.simulationLogScale,
					time_ech=Settings.simulationTimeEch,
					nb_samples=Settings.simulationNbSamples,
					list_samples=None,
					keep_files=Settings.simulationKeepFiles):

		self.listOfSamples = list_samples
		if self.listOfSamples is None:
			self.buildListSamples(time_min, time_max, log_scale, time_ech, nb_samples)

		Simulation.__init__(self,
							list_of_models=list_of_models,
							time_min=Settings.simulationTimeMin,
							list_samples=self.listOfSamples,
							experiment=experiment,
							abs_tol=abs_tol,
							rel_tol=rel_tol,
							keep_files=keep_files)

		self.keepFiles = keep_files

	def buildListSamples(self, time_min, time_max, log_scale, time_ech, nb_samples):

		if time_ech is not None:
			nb_samples = int(round((time_max-time_min) / time_ech))+1

		if log_scale:
			self.listOfSamples = [float(value) for value in logspace(time_min, time_max, nb_samples)]
		else:
			self.listOfSamples = [float(value) for value in linspace(time_min, time_max, nb_samples)]

	def run(self, timeout=None):

		self.writeSimulationFiles()
		self.runSimulation(timeout=timeout)
		self.loadSimulationResults()

		if not self.keepFiles:
			self.cleanTempDirectory()

	def run_inside_thread(self, success, failure, timeout=None):
		try:
			self.run(timeout=timeout)
			success()
		except Exception as e:
			failure(e)


	def run_async(self, success, failure, timeout=None):

		t = Thread(group=None, target=self.run_inside_thread, args=(success, failure, timeout))
		t.setDaemon(True)
		t.start()

	def loadSimulationResults(self):
		self.rawData = []
		t_filename = self.getTempDirectory() + Settings.C_simulationResultsDirectory + "results_0"
		ind = 0
		while(isfile(t_filename + ("_%d" % ind))):
			(t, y) = self.readResultFile(t_filename + ("_%d" % ind))
			self.rawData.append((t, y))
			ind += 1


	def readResultFile(self, filename):

		resultsFile = open(filename, 'r')

		t = []
		trajs = {}

		variables = resultsFile.readline().strip().split(',')
		variables = [variable.strip() for variable in variables]

		for variable in variables:
			if variable != 'time':
				trajs.update({variable: []})

		for line in resultsFile.readlines():

			data = line.split()
			t.append(float(data[0]))

			for i_variable, variable in enumerate(variables):
				if variable != 'time':
					trajs[variable].append(float(data[i_variable]))

		resultsFile.close()

		# The simulations only deals with amounts, but some species are
		# Concentrations. So we need to transform them back

		for variable in self.listOfModels[0].listOfVariables:
			# print "%s : %s" % (variable.getSbmlId(), variable.symbol.getSymbol())
			if variable.isConcentration():
				t_traj = trajs[variable.getSymbolStr()]

				t_comp_traj = trajs[variable.getCompartment().getSymbolStr()]
				res_traj = []

				for i, point in enumerate(t_traj):

					if i == 0 or (i > 0 and t[i] > t[i-1]):
						if abs(t_comp_traj[i]) < self.absTol[0]:
							res_traj.append(0.0)
						else:
							res_traj.append(point / t_comp_traj[i])

				trajs.update({variable.getSymbolStr(): res_traj})
			else:
				res_traj = []

				for i, point in enumerate(trajs[variable.getSymbolStr()]):
					if i == 0 or (i > 0 and t[i] > t[i - 1]):
						res_traj.append(point)

				trajs.update({variable.getSymbolStr(): res_traj})

		t_t = []
		for i, point in enumerate(t):

			if i == 0 or (i > 0 and t[i] > t[i - 1]):
				t_t.append(point)

		t = t_t

		return (t, trajs)

	def plot(self, figure=None, plot=None, variables=[], suffix=""):


		if plot is None and figure is None:
			if self.listOfModels[0].timeUnits is not None and self.listOfModels[0].extentUnits is not None:
				figure = SigNetSimFigure(
						x_unit=self.listOfModels[0].timeUnits.getNameOrSbmlId(),
						y_unit=self.listOfModels[0].extentUnits.getNameOrSbmlId())
			else:
				figure = SigNetSimFigure()

		if plot is None and figure is not None:
			plot = figure.add_subplot(1, 1, 1)

		t, trajs = self.getRawData()[0]

		t_trajs = {}
		x_min = amin(t)
		x_max = amax(t)
		y_min = 0
		y_max = 0
		for t_id in list(trajs.keys()):

			if len(variables) == 0 or self.listOfModels[0].listOfVariables.getBySymbolStr(t_id).getSbmlId() in variables:

				y_min = min(y_min, amin(trajs[str(t_id)]))
				y_max = max(y_max, amax(trajs[str(t_id)]))
				t_trajs.update({t_id: trajs[str(t_id)]})

		for i_species, name in enumerate(t_trajs.keys()):

				t_var = self.listOfModels[0].listOfVariables.getBySymbol(SympySymbol(name))
				if not t_var.isConstant():
					figure.plot(plot, i_species, t, t_trajs[name], y_name=t_var.getNameOrSbmlId()+suffix)
					plot.legend(loc='upper right')

		plot.set_xlim([x_min, x_max])
		plot.set_ylim([y_min, y_max*1.1])
		show()

		return figure