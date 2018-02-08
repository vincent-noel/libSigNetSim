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

from libsignetsim.settings.Settings import Settings

from time import time, sleep
from os.path import join, getsize, isfile
from os import getcwd, setpgrp, mkdir
from subprocess import call
from math import log10

class OptimizationExecution(object):

	OPTIM_FAILURE       =   -1
	OPTIM_SUCCESS       =   0

	def __init__ (self):

		self.startTime = None
		self.stopTime = None
		self.elapsedTime = None
		self.monitor = False
		self.optimizationId = int(time()*1000)
		self.directory = None
		self.finalScore = None
		# mkdir(self.getTempDirectory())


	def getTempDirectory(self):

		if self.directory is None:
			return join(Settings.tempDirectory,
								"optimization_%s/" % str(self.optimizationId))

		else:
			return join(self.directory,
								"optimization_%s/" % str(self.optimizationId))

	def setTempDirectory(self, directory):

		self.directory = directory



	def compile(self, nb_procs):

		if nb_procs > 1:
			target = "lsa.mpi"

		else:
			target = "lsa"

		cmd_comp = "make -f %sMakefile -C %s %s 1>/dev/null" % (
								self.getTempDirectory(),
								self.getTempDirectory(),
								target)

		res_comp = call(cmd_comp,
								stdout=open(join(self.getTempDirectory(), "sout_optim_comp"), "w"),
								stderr=open(join(self.getTempDirectory(), "err_optim_comp"), "w"),
								shell=True, preexec_fn=setpgrp, close_fds=True)

		timeout = 3
		i = 0
		while not isfile(join(self.getTempDirectory(), "err_optim_comp")) or i == timeout:
			sleep(1)
			i += 1

		if res_comp != 0 or getsize(join(self.getTempDirectory(), "err_optim_comp")) > 0:
			return self.OPTIM_FAILURE
		else:
			return self.OPTIM_SUCCESS


	def run(self, nb_procs, timeout, maxiter):

		t_timeout = ""
		if timeout is not None and timeout > 0:
			t_timeout = "-d %d " % timeout

		s_maxiter = ""
		if maxiter is not None and maxiter > 0:
			s_maxiter = "-m %d " % maxiter

		mkdir(join(self.getTempDirectory(), "logs"))
		mkdir(join(self.getTempDirectory(), "logs", "score"))
		mkdir(join(self.getTempDirectory(), "logs", "res"))

		present_dir = getcwd()

		if nb_procs > 1:
			target = "cd %s; mpirun -np %d ./lsa.mpi; cd %s" % (self.getTempDirectory(), nb_procs, present_dir)

		else:
			target = "cd %s; ./lsa; cd %s" % (self.getTempDirectory(), present_dir)

		t_command_line = "%s" % target

		res_optim = call(t_command_line,
				stdout=open(join(self.getTempDirectory(), "out_optim"), "w"),
				stderr=open(join(self.getTempDirectory(), "err_optim"), "w"),
				shell=True, preexec_fn=setpgrp, close_fds=True)

		if res_optim != 0 and res_optim != 124:
			self.stopTime = int(time())
			self.elapsedTime = self.stopTime - self.startTime
			return self.OPTIM_FAILURE

		timeout = 3
		i = 0
		while not isfile(join(self.getTempDirectory(), "err_optim")) or i == timeout:
			sleep(1)
			i += 1

		if (getsize(join(self.getTempDirectory(), "err_optim")) > 0 or
			not isfile(join(self.getTempDirectory(), "logs", "score", "score"))):

			err = open(join(self.getTempDirectory(), "err_optim"))

			if err.readline() != "mpirun: killing job...\n":
				err.close()
				self.stopTime = int(time())
				self.elapsedTime = self.stopTime - self.startTime
				return self.OPTIM_FAILURE

			err.close()

		return self.OPTIM_SUCCESS


	def readFinalScore(self):

		file_final_score = open(join(self.getTempDirectory(), "logs", "score", "score"))
		final_score = float(file_final_score.readline())

		final_score = max(round(final_score, int(-log10(Settings.defaultPlsaCriterion))),
							Settings.defaultPlsaCriterion)

		file_final_score.close()


		if Settings.verbose >= 1:
			print "> Optimization executed. Final score : %.5g" % final_score
		return final_score


	def runOptimization(self, nb_procs, timeout=None, maxiter=None):

		# if self.monitor:
		#     t = OptimizationMonitor(self)  #threading.Thread(target=self.monitorOptimization)
		#     t.start()
		self.startTime = int(time())

		res = self.compile(nb_procs)

		if res == self.OPTIM_SUCCESS:

			res_2 = self.run(nb_procs, timeout, maxiter)

			if res_2 == self.OPTIM_SUCCESS:

				self.stopTime = int(time())
				self.elapsedTime = self.stopTime - self.startTime
				self.finalScore = self.readFinalScore()
				return self.finalScore
			elif Settings.verbose >= 1:
				print "> Execution failed !"
		elif Settings.verbose >= 1:
			print "> Compilation failed !"

		self.stopTime = int(time())
		self.elapsedTime = self.stopTime - self.startTime

		return self.OPTIM_FAILURE
