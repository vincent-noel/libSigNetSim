#!/usr/bin/env python
""" TimeseriesSimulation.py


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

from libsignetsim.simulation.Simulation import Simulation
from libsignetsim.simulation.SigNetSimFigure import SigNetSimFigure
from libsignetsim.settings.Settings import Settings
from matplotlib.pyplot import show
from numpy import amin, amax, linspace, logspace
from os.path import join, isfile

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
			nb_samples = int(round((time_max-time_min)/time_ech))+1

		if log_scale:
			self.listOfSamples = logspace(time_min, time_max, nb_samples)
		else:
			self.listOfSamples = linspace(time_min, time_max, nb_samples)

	def run(self):

		self.writeSimulationFiles()
		self.runSimulation()
		self.loadSimulationResults()

		if not self.keepFiles:
			self.cleanTempDirectory()

	def loadSimulationResults(self):

		self.rawData = []
		t_filename = self.getTempDirectory() + Settings.C_simulationResultsDirectory + "results_0"
		t_filename_2 = t_filename + "_0"
		if isfile(t_filename):
			(t, y) = self.readResultFile(t_filename)
			self.rawData.append((t,y))

		elif isfile(t_filename_2):
			ind = 0
			while(isfile(t_filename + ("_%d" % ind))):
				(t, y) = self.readResultFile(t_filename + ("_%d" % ind))
				self.rawData.append((t,y))
				ind += 1

	def readResultFile(self, filename):

		resultsFile = open(filename, 'r')

		t = []
		trajs = {}

		variables = resultsFile.readline().strip().split(',')
		variables = [variable.strip() for variable in variables]

		for variable in variables:
			if variable != 'time':
				trajs.update({variable:[]})

		for line in resultsFile.readlines():

			data = line.split()
			t.append(float(data[0]))

			for i_variable, variable in enumerate(variables):
				if variable != 'time':
					trajs[variable].append(float(data[i_variable]))

		resultsFile.close()

		# The simulations only deals with amounts, but some species are
		# Concentrations. So we need to transform them back
		for key, variable in self.listOfModels[0].listOfVariables.iteritems():
			if variable.isConcentration():
				t_traj = trajs[key]

				t_comp_traj = trajs[variable.getCompartment().getSbmlId()]
				res_traj = []

				for i, point in enumerate(t_traj):
					res_traj.append(point/t_comp_traj[i])
				trajs.update({key:res_traj})

		return (t, trajs)

	def plot(self):

		if self.listOfModels[0].timeUnits is not None and self.listOfModels[0].extentUnits is not None:
			figure = SigNetSimFigure(
					x_unit=self.listOfModels[0].timeUnits.getNameOrSbmlId(),
					y_unit=self.listOfModels[0].extentUnits.getNameOrSbmlId())
		else:
			figure = SigNetSimFigure()
		ax = figure.add_subplot(1, 1, 1)
		t, trajs = self.getRawData()[0]

		t_trajs = []
		x_min = amin(t)
		x_max = amax(t)
		y_min = 0
		y_max = 0
		for t_id in trajs.keys():
			y_min = min(y_min, amin(trajs[str(t_id)]))
			y_max = max(y_max, amax(trajs[str(t_id)]))
			t_trajs.append(trajs[str(t_id)])

		for i_species, name in enumerate(trajs.keys()):

			t_var = self.listOfModels[0].listOfVariables[name]
			if not t_var.isConstant():
				ax.plot(t, t_trajs[i_species], '-',
					color=SigNetSimFigure.color_scheme[i_species % len(self.color_scheme)],
					linewidth=int(5 * figure.w),
					label=str(t_var.getNameOrSbmlId()))

				ax.legend(loc='upper right', fontsize=int(15 * figure.w))

		ax.set_xlim([x_min, x_max])
		ax.set_ylim([y_min, y_max*1.1])
		show()
