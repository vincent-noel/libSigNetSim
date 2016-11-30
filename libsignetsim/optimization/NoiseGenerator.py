#!/usr/bin/env python
""" NoiseGenerator.py


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


from math import exp
from numpy.random import normal

class NoiseGenerator(object):

	def __init__ (self, list_of_experimental_data={}, noise=0, sampling=None):

		self.listOfExperimentalData = list_of_experimental_data

		self.noise = noise
		self.sampling = sampling


	def applyNoiseToData(self):

		for i, experimental_data in enumerate(self.listOfExperimentalData.keys()):

			t_experimental_data = self.listOfExperimentalData[experimental_data]

			t_filtered_t = []
			t_filtered_values = []

			# Filter some time points to impose a sampling
			if self.sampling is not None:
				for j,t_time in enumerate(t_experimental_data.t):

					if not (abs((float(t_time)/self.sampling - round(float(t_time)/self.sampling,0))) > 1e-12 and float(t_time) > 0):
						t_filtered_t.append(float(t_time))
						t_filtered_values.append(float(t_experimental_data.values[j]))

			else:
				t_filtered_t = t_experimental_data.t
				t_filtered_values = t_experimental_data.values

			# Add noise to all variables
			if self.noise > 0:
				for j,value in enumerate(t_filtered_values):
					noise = math.exp(normal(0,self.noise))
					t_filtered_values[j] = t_filtered_values[j] * noise

			self.listOfExperimentalData[experimental_data].size = len(t_filtered_t)
			self.listOfExperimentalData[experimental_data].t = t_filtered_t
			self.listOfExperimentalData[experimental_data].values = t_filtered_values
