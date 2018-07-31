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
# from __future__ import print_function

from libsignetsim.settings.Settings import Settings
from libsignetsim.optimization.OptimizationException import OptimizationCompilationException, OptimizationExecutionException
from time import time, sleep
from os.path import join, getsize, isfile
from os import getcwd, setpgrp, mkdir
from subprocess import call
from math import log10
from threading import Thread


class OptimizationExecution(object):


	OPTIM_FAILURE       =	-1
	OPTIM_SUCCESS       =	0
	OPTIM_RUNNING		=	1
	OPTIM_INTERRUPTED	= 	2
	OPTIM_INITIALIZED 	= 	3


	def __init__ (self):

		self.startTime = None
		self.stopTime = None
		self.elapsedTime = None
		self.monitor = False
		self.optimizationId = int(time()*1000)
		self.directory = None
		self.finalScore = None
		self.status = self.OPTIM_INITIALIZED
		# mkdir(self.getTempDirectory())


	def getTempDirectory(self):

		if self.directory is None:
			return join(Settings.tempDirectory,	"optimization_%s/" % str(self.optimizationId))

		else:
			return join(self.directory, "optimization_%s/" % str(self.optimizationId))

	def setTempDirectory(self, directory):

		self.directory = directory



	def compile(self, nb_procs):

		mkdir(join(self.getTempDirectory(), "logs"))
		mkdir(join(self.getTempDirectory(), "logs", "score"))
		mkdir(join(self.getTempDirectory(), "logs", "res"))

		if nb_procs > 1:
			target = "lsa.mpi"

		else:
			target = "lsa"

		cmd_comp = "make -f %sMakefile -C %s %s 1>/dev/null" % (
								self.getTempDirectory(),
								self.getTempDirectory(),
								target)

		with open(join(self.getTempDirectory(), "out_optim_comp"), "w") as stdout,  open(join(self.getTempDirectory(), "err_optim_comp"), "w") as stderr:
			res_comp = call(cmd_comp, stdout=stdout, stderr=stderr, shell=True, preexec_fn=setpgrp, close_fds=True)

		timeout = 3
		i = 0
		while not isfile(join(self.getTempDirectory(), "err_optim_comp")) or i == timeout:
			sleep(1)
			i += 1

		if res_comp != 0 or getsize(join(self.getTempDirectory(), "err_optim_comp")) > 0:
			self.status = self.OPTIM_FAILURE
			if Settings.verbose >= 1:
				print("-"*40 + "\n")
				print("> Error during optimization compilation :")
				with open(join(self.getTempDirectory(), "err_optim_comp"), 'r') as f_err_comp:
					for line in f_err_comp:
						print(line)

				print("-"*40 + "\n")
			raise OptimizationCompilationException("Error during optimization compilation")
		else:
			self.status = self.OPTIM_SUCCESS
			return self.OPTIM_SUCCESS


	def run(self, nb_procs, timeout, maxiter):

		t_timeout = ""
		if timeout is not None and timeout > 0:
			t_timeout = "-d %d " % timeout

		s_maxiter = ""
		if maxiter is not None and maxiter > 0:
			s_maxiter = "-m %d " % maxiter

		present_dir = getcwd()

		if nb_procs > 1:
			target = "cd %s; mpirun -np %d ./lsa.mpi; cd %s" % (self.getTempDirectory(), nb_procs, present_dir)

		else:
			target = "cd %s; ./lsa; cd %s" % (self.getTempDirectory(), present_dir)

		t_command_line = "%s" % target

		self.status = self.OPTIM_RUNNING
		with open(join(self.getTempDirectory(), "out_optim"), "w") as stdout, open(join(self.getTempDirectory(), "err_optim"), "w") as stderr:
			res_optim = call(t_command_line,
					stdout=stdout, stderr=stderr,
					shell=True, preexec_fn=setpgrp, close_fds=True)

		if res_optim != 0 and res_optim != 124:

			self.stopTime = int(time())
			self.elapsedTime = self.stopTime - self.startTime
			self.status = self.OPTIM_FAILURE
			raise OptimizationExecutionException("Optim execution returned %s" % res_optim)

		timeout = 3
		i = 0
		while not isfile(join(self.getTempDirectory(), "err_optim")) or i == timeout:
			sleep(1)
			i += 1

		if getsize(join(self.getTempDirectory(), "err_optim")) > 0:

			# There is some weird error here, apparently caused by docker filesystem.
			# ** apparently ** we can ignore it
			non_docker_err = False
			with open(self.getTempDirectory() + "err_optim", 'r') as f_err_optim:
				for line in f_err_optim:
					if not line.startswith("Unexpected end of /proc/mounts"):
						non_docker_err = True


			if non_docker_err:
				if Settings.verbose >= 1:
					print("-" * 40 + "\n")
					print("> Error during optimization execution :")
					with open(join(self.getTempDirectory(), "err_optim"), 'r') as f_err:
						for line in f_err:
							print(line)

					print("-" * 40 + "\n")

				err = open(join(self.getTempDirectory(), "err_optim"))

				if err.readline() != "mpirun: killing job...\n":
					err.close()
					self.stopTime = int(time())
					self.elapsedTime = self.stopTime - self.startTime
					self.status = self.OPTIM_FAILURE
					raise OptimizationExecutionException("Error during optimization execution")

				err.close()

		if isfile(join(self.getTempDirectory(), "pid")):
			self.status = self.OPTIM_INTERRUPTED
		else:
			self.status = self.OPTIM_SUCCESS

		return self.OPTIM_SUCCESS


	def run_inside_thread(self, success, failure, nb_procs=2, timeout=None, maxiter=None):

		try:
			res = self.runOptimization(nb_procs=nb_procs, timeout=timeout, maxiter=maxiter)

			if res != self.OPTIM_FAILURE:
				if success is not None:
					success(self)
			else:
				if failure is not None:
					failure(self)

		except Exception as e:
			if failure is not None:
				failure(self, e)


	def run_async(self, success, failure, nb_procs=2, timeout=None, maxiter=None):

		t = Thread(group=None, target=self.run_inside_thread, args=(success, failure, nb_procs, timeout, maxiter))
		t.setDaemon(True)
		t.start()
		return t

	def restart_inside_thread(self, success, failure, nb_procs=2, timeout=None, maxiter=None):

		try:
			res = self.restartOptimization(nb_procs=nb_procs, timeout=timeout, maxiter=maxiter)

			if res != self.OPTIM_FAILURE:
				if success is not None:
					success(self)
			else:
				if failure is not None:
					failure(self)

		except Exception as e:
			if failure is not None:
				failure(self, e)


	def restart_async(self, success, failure, nb_procs=2, timeout=None, maxiter=None):

		t = Thread(group=None, target=self.restart_inside_thread, args=(success, failure, nb_procs, timeout, maxiter))
		t.setDaemon(True)
		t.start()
		return t

	def readFinalScore(self):

		file_final_score = open(join(self.getTempDirectory(), "logs", "score", "score"))
		final_score = float(file_final_score.readline())

		final_score = max(round(final_score, int(-log10(Settings.defaultPlsaCriterion))),
							Settings.defaultPlsaCriterion)

		file_final_score.close()


		if Settings.verbose >= 1:
			print("> Optimization executed. Final score : %.5g" % final_score)
		return final_score

	def restartOptimization(self, nb_procs=2, timeout=None, maxiter=None):

		self.startTime = int(time())

		res_2 = self.run(nb_procs, timeout, maxiter)
		if res_2 == self.OPTIM_SUCCESS:

			self.stopTime = int(time())
			self.elapsedTime = self.stopTime - self.startTime
			self.finalScore = self.readFinalScore()
			return self.finalScore
		elif Settings.verbose >= 1:
			print("> Execution failed !")

		self.stopTime = int(time())
		self.elapsedTime = self.stopTime - self.startTime

		return self.OPTIM_FAILURE


	def runOptimization(self, nb_procs, timeout=None, maxiter=None):

		# if self.monitor:
		# t = OptimizationMonitor(self)  #threading.Thread(target=self.monitorOptimization)
		# t.start()

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
				print("> Execution failed !")
		elif Settings.verbose >= 1:
			print("> Compilation failed !")

		self.stopTime = int(time())
		self.elapsedTime = self.stopTime - self.startTime

		return self.OPTIM_FAILURE

	def isInterrupted(self):
		return self.status == self.OPTIM_INTERRUPTED
	def hasSucceeded(self):
		return self.status == self.OPTIM_SUCCESS
	def hasFailed(self):
		return self.status == self.OPTIM_FAILURE
	def hasStarted(self):
		return self.status != self.OPTIM_INITIALIZED