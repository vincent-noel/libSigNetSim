#!/usr/bin/env python
""" Simulation.py


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

from libsignetsim.simulation.CWriterSimulation import CWriterSimulation
from libsignetsim.simulation.SimulationException import SimulationExecutionException, SimulationCompilationException, SimulationNoDataException
from libsignetsim.settings.Settings import Settings
from time import time, clock
from os import mkdir, setpgrp, getcwd
from os.path import join, isfile, exists, getsize
from subprocess import call
from shutil import rmtree
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

class Simulation(CWriterSimulation):

	SIM_DONE            =   10
	SIM_TODO            =   11


	def __init__ (self,
					list_of_models,
				  	time_min,
					list_samples,
					experiment=None,
					abs_tol=Settings.defaultAbsTol,
					rel_tol=Settings.defaultRelTol,
					keep_files=Settings.simulationKeepFiles):

		self.keepFiles = keep_files
		self.sessionId = None
		self.simulationId = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(12))

		CWriterSimulation.__init__(self,
						list_of_models=list_of_models,
						time_min=time_min,
						list_samples=list_samples,
						experiment=experiment,
						abs_tol=abs_tol,
						rel_tol=rel_tol)

		self.listOfModels = list_of_models

		self.__simulationDone = self.SIM_TODO
		self.rawData = None

		self.nbConditions = 0

		if experiment is not None:
			self.nbConditions = len(experiment.listOfConditions)


	def getTempDirectory(self):
		if self.sessionId is None:
			return join(Settings.tempDirectory,
								"simulation_%s/" % self.simulationId)
		else:
			return join(self.sessionId,
								("simulation_%s/" % self.simulationId))


	def isDone(self):
		return self.__simulationDone == self.SIM_DONE


	def cleanTempDirectory(self):
		rmtree(self.getTempDirectory())


	def writeSimulationFiles(self):

		mkdir(self.getTempDirectory())
		CWriterSimulation.writeSimulationFiles(self)

		res_path = join(self.getTempDirectory(),
								# Settings.C_simulationDirectory,
								Settings.C_simulationResultsDirectory)

		if not exists(res_path):
			mkdir(res_path)
	#
	# def writeModelsFile(self):
	# 	if len(self.listOfModels) > 1:
	# 		for i_model, model in enumerate(self.listOfModels):
	# 			model.writeSbmlToFile(join(self.getTempDirectory(),
	# 											"model_%d.sbml" % i_model))
	#
	# 	else:
	# 		self.listOfModels[0].writeSbmlToFile(join(self.getTempDirectory(),
	# 													"model.sbml"))
	#
	#

	def __compile__(self, nb_procs=4):


		if self.nbConditions == 0 or nb_procs <= 1:
			cmd_comp = "make -C %s sim-serial" % self.getTempDirectory()
		else:
			cmd_comp = "make -C %s sim-parallel" % self.getTempDirectory()

		res_comp = call(cmd_comp,
						stdout=open("%sout_comp" % self.getTempDirectory(),"w"),
						stderr=open("%serr_comp" % self.getTempDirectory(),"w"),
						shell=True,preexec_fn=setpgrp,close_fds=True)

		if (res_comp != 0
			or getsize(self.getTempDirectory() + "err_comp") > 0):


			if Settings.verbose >= 1:
				print "-"*40 + "\n"
				print "> Error during simulation compilation :"
				f_err_comp = open(self.getTempDirectory() + "err_comp", 'r')
				for line in f_err_comp:
					print line
				print "-"*40 + "\n"
				f_err_comp.close()

			raise SimulationCompilationException("Error during simulation compilation (%d)" % res_comp)

	def __execute__(self, nb_procs=Settings.defaultMaxProcNumbers, steady_states=False):

		present_dir = getcwd()

		flags = ""
		if steady_states:
			flags += "-s "

		cmd_sim = ""
		if self.nbConditions == 0 or nb_procs <= 1:
			cmd_sim = "cd %s; ./sim-serial %s; cd %s" % (
					self.getTempDirectory(),
					flags, present_dir)

		else:
			cmd_sim = "cd %s; mpirun -np %d ./sim-parallel %s; cd %s" % (
					self.getTempDirectory(),
					nb_procs, flags,
					present_dir)

		res_sim = call(cmd_sim,
					  stdout=open("%sout_sim" % self.getTempDirectory(),"w"),
					  stderr=open("%serr_sim" % self.getTempDirectory(),"w"),
					  shell=True,preexec_fn=setpgrp,close_fds=True)

		if res_sim != 0 or getsize(join(self.getTempDirectory(), "err_sim")) > 0:

			if Settings.verbose >= 1:
				print "-" * 40 + "\n"
				print "> Error during simulation execution :"
				f_err_sim = open(self.getTempDirectory() + "err_sim", 'r')
				for line in f_err_sim:
					print line
				print "-" * 40 + "\n"
				f_err_sim.close()

			raise SimulationExecutionException("Error during simulation execution (%d)" % res_sim)

		else:
			if Settings.verbose >= 2:
				print "-"*40 + "\n"
				print "> Execution returned : \n"
				f_out_sim = open(self.getTempDirectory() + "out_sim", 'r')
				for line in f_out_sim:
					print line
				print "-"*40 + "\n"
				f_out_sim.close()


	def runSimulation(self, progress_signal=None, steady_states=False, nb_procs=4):

		start = time()
		self.__compile__(nb_procs=nb_procs)

		mid = time()

		if Settings.verboseTiming >= 1:
			print ">> Compilation executed in %.2fs" % (mid-start)

		self.__execute__(nb_procs=nb_procs, steady_states=steady_states)
		end = time()

		if Settings.verboseTiming >= 1:
			print ">> Simulation executed in %.2fs" % (end-mid)

		self.__simulationDone = self.SIM_DONE


	def getRawData(self):
		if self.__simulationDone == self.SIM_DONE:
			return self.rawData
		else:
			raise SimulationNoDataException("No data : simulation hasn't been executed yet")

