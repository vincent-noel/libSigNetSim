#!/usr/bin/env python
""" ExperimentalCondition.py


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

from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData

class ExperimentalCondition(object):

	def __init__ (self):

		self.listOfInitialConditions = ListOfExperimentalData()
		self.listOfExperimentalData = ListOfExperimentalData()
		self.name = ""

	def read(self, list_of_initial_values, list_of_observed_values, name=""):

		self.listOfInitialConditions = list_of_initial_values
		self.listOfExperimentalData = list_of_observed_values
		self.name = name


	def getMaxTime(self):
		return self.listOfExperimentalData.getMaxTime()

	def getTimes(self):
		return self.listOfExperimentalData.getTimes() + self.listOfInitialConditions.getTimes()

	def getTreatedVariables(self):
		return self.listOfInitialConditions.getVariables()
