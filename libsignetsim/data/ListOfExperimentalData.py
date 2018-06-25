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

from numpy import amin, amax, linspace, interp
from libsignetsim.data.ExperimentalData import ExperimentalData

class ListOfExperimentalData(dict):

	def __init__(self):

		self.currentId = 0


	def add(self, experimental_data):
		self.update({self.currentId: experimental_data})
		self.currentId += 1

	def readNuML(self, list_of_data):

		for data in list_of_data.getContents():
			exp_data = ExperimentalData()
			exp_data.readNuML(data)
			self.add(exp_data)

	def writeNuML(self, composite_value):

		for data in list(self.values()):
			data.writeNuML(composite_value)

	def getMaxTime(self):

		max_time = 0
		for data in list(self.values()):
			if data.t > max_time:
				max_time = data.t
		return max_time

	def getSpecies(self):
		""" Returns an array of sbml ids"""
		species = []
		for data in list(self.values()):
			species.append(data.name)
		return list(set(species))

	def getTimes(self):

		times = []
		for data in list(self.values()):
			times.append(data.t)

		return times


	def getByVariable(self):
		result = {}
		for species in self.getSpecies():
			result.update({species: []})
		for data in list(self.values()):
			result[data.name].append(data)

		return result


	def getValuesOfSpecies(self):

		values = {}
		for data in list(self.values()):
			if data.name not in list(values.keys()):
				values.update({data.name: []})

			values[data.name].append(data.value)
		return values

	def getTimesOfSpecies(self):

		times = {}
		for data in list(self.values()):
			if data.name not in list(times.keys()):
				times.update({data.name: []})

			times[data.name].append(data.t)

		return times

	def getValues(self):

		values = {}
		for data in list(self.values()):
			if data.name not in list(values.keys()):
				values.update({data.name: []})

			values[data.name].append((data.t, data.value))

		return values

	def interpolate(self, size=101):

		new_experimental_data = {}
		new_currentId = 0

		list_species = list(set([data.name for data in list(self.values())]))

		for species in list_species:
			times = []
			values = []
			for data in list(self.values()):
				if data.name == species:
					times.append(data.t)
					values.append(data.value)

			if amin(times) != amax(times):
				times_interpolation = linspace(amin(times), amax(times), size)
				values_interpolation = interp(times_interpolation, times, values)

				for i_data, data in enumerate(values_interpolation):
					t_data = ExperimentalData()
					t_data.readDB(species, times_interpolation[i_data], data)
					new_experimental_data.update({new_currentId: t_data})
					new_currentId += 1
			else:
				t_data = ExperimentalData()
				t_data.readDB(species, times[0], values[0])
				new_experimental_data.update({new_currentId: t_data})
				new_currentId += 1

		dict.clear(self)
		dict.update(self, new_experimental_data)
		self.currentId = new_currentId

	def getVariables(self):

		variables = []
		for data in list(self.values()):
			variables.append(data.name)

		return list(set(variables))
