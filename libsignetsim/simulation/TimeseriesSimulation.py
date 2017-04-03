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
from time import time

class TimeseriesSimulation(Simulation):

	DEFAULT_NB_SAMPLES = 500
	# color_scheme = ['#009ece', '#ff9e00', '#9ccf31', '#f7d708', '#ce0000']
	color_scheme = (["#FFB300",   "#803E75",   "#FF6800",   "#A6BDD7"]
					+ ["#C10020",   "#CEA262",   "#817066",   "#007D34"]
					+ ["#F6768E",   "#00538A",   "#FF7A5C",   "#53377A"]
					+ ["#FF8E00",   "#B32851",   "#F4C800",  "#7F180D"]
					+ ["#93AA00",   "#593315",   "#F13A13",   "#232C16"])

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

	def loadSimulationResults_v2(self):

		t_filename = join(self.getTempDirectory(),
									Settings.C_simulationDirectory,
									Settings.C_simulationResultsDirectory,
									"results_0")
		t_filename_2 = t_filename + "_0"

		t_model = self.listOfModels[0]


		if isfile(t_filename):
			(t, traj_vars) = self.readResultFile_v2(t_filename)
			self.listOfData_v2 = (t, traj_vars)

		elif isfile(t_filename_2):

			ind = 0
			self.listOfData_v2 = []
			while(isfile(t_filename + ("_%d" % ind))):
				(t, y) = self.readResultFile_v2(t_filename + ("_%d" % ind))
				self.listOfData_v2.append((t, y))
				ind += 1


	def readResultFile_v2(self, filename):

		resultsFile = open(filename, 'r')

		t = []
		traj_vars = {}
		for var in self.listOfModels[0].listOfVariables.keys():
			traj_vars.update({var:[]})

		for line in resultsFile:
			data = line.split()
			t.append(float(data[0]))

			for sbmlId, variable in self.listOfModels[0].listOfVariables.items():
				traj_vars[sbmlId].append(float(data[1+variable.getPos()]))

		resultsFile.close()

		return (t,traj_vars)



	def run(self):

		start = time()
		self.writeSimulationFiles()
		# mid = time()

		# if Settings.verbose >= 1:
		# 	print "> Files written in %.2fs" % (mid-start)
		res = self.runSimulation()
		if res == self.SIM_SUCCESS:
			self.loadSimulationResults()
			if not self.keepFiles:
				self.cleanTempDirectory()

		# stop = time()
		#
		# if Settings.verbose:
		# 	print "> Simulation executed in %.2fs" % (stop-start)

		return res

	def plot(self):

		if (self.listOfModels[0].timeUnits is not None and self.listOfModels[0].extentUnits is not None):
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
					color=self.color_scheme[i_species % len(self.color_scheme)],
					linewidth=int(5 * figure.w),
					label=str(t_var.getNameOrSbmlId()))

				ax.legend(loc='upper right', fontsize=int(15 * figure.w))

		ax.set_xlim([x_min, x_max])
		ax.set_ylim([y_min, y_max*1.1])
		show()
