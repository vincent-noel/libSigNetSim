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
from __future__ import print_function
from __future__ import division


from past.utils import old_div
from libsignetsim.settings.Settings import Settings
from threading import Thread

from time import sleep, time
from os.path import isfile
from math import isnan
from re import split
from numpy import log10

class OptimizationMonitor(Thread):

	def __init__(self, parent_optimization): #, referenceModel=None, referenceData=None):

		Thread.__init__(self)
		self.daemon = True
		self.frequency = 6
		self.parentOptimization = parent_optimization


	def run(self):
		while not isfile(self.parentOptimization.getTempDirectory() + "final_score"):
			start_time = int(time())
			if isfile(self.parentOptimization.getTempDirectory() + "optim.log"):

				#Reading file
				f_optim = open(self.parentOptimization.getTempDirectory() + "optim.log","r");
				temps = []
				times = []
				for line in f_optim:
					data = split("\t", line.strip())
					temps.append(float(data[1]))
					times.append(int(data[9]))
				f_optim.close()

				#Filtering results
				#At first, the temperature will free fall and then stabilize to
				# decrease linearly.
				#We filter out the free fall part waiting for the following condition to become true :
				# derivative of the logs > -0.005
				f_temps = []
				f_times = []
				stabilized=False
				steps_ignored = old_div(Settings.defaultPlsaInitialMoves,Settings.defaultPlsaTau)-1
				for i, step in enumerate(temps):

					if i == 0:
						steps_ignored += 1

					#Here we wait for the end of the "freefall"
					elif not stabilized:
						steps_ignored += 1
						if (log10(temps[i]) - log10(temps[i-1])) > -0.001:
							stabilized = True
					else:
						#Here we also transform the standard deviation using :
						# new_temp = log10(old_temp) - log10(precision)
						#If everything is right, we can some quasi straight line until 0
						if not isnan(temps[i]):
							f_temps.append(log10(temps[i])-(log10(Settings.defaultPlsaCriterion)-1))
							f_times.append(times[i])

				#And now we compute the remaining times
				#We wait for 5 more steps, we want a smoothed average, and the first results are crap anyway
				steps_done = len(f_temps)
				if steps_done > 100:

					if isnan(f_temps[steps_done-1]) or  f_temps[steps_done-1] < 0:
						print("> Optimization %d : finishing..." % self.parentOptimization.optimizationId)
					else:
						#We compute the smoothed average
						window = steps_done - 75

						avg_der = 0
						avg_dur = 0
						for point in range(1, window):
							avg_dur += float(f_times[steps_done-point] - f_times[steps_done-point-1])
							avg_der += (f_temps[steps_done-point] - f_temps[steps_done-point-1])
						avg_dur /= float(window-1)
						avg_der /= float(window-1)

						#And the remaining steps and fime
						steps_remaining = old_div(-f_temps[steps_done-1],avg_der)
						time_remaining = steps_remaining*avg_dur

						steps_done = steps_done + steps_ignored
						ratio_done = old_div(steps_done,(steps_done + steps_remaining))

						if (not isfile(self.parentOptimization.getTempDirectory() + "final_score") and
							time_remaining > 0 and ratio_done > 0.1):
							print("> Optimization %d : %.0f minutes remaining (%d%% done, running for %.0f minutes, remaining %.0f minutes)" % (
									self.parentOptimization.optimizationId, old_div(time_remaining,60),
									int(ratio_done*100),
									old_div((times[len(times)-1]-self.parentOptimization.startTime),60),
									(((times[len(times)-1]-self.parentOptimization.startTime)*(steps_remaining))/(steps_done)/60)))


			elapsed_time = int(time()) - start_time
			sleep(max(0, (self.frequency - elapsed_time)))
