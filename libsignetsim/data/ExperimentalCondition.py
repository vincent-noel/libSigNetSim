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

from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.ExperimentalData import ExperimentalData
from libsignetsim.figure.SigNetSimFigure import SigNetSimFigure
from matplotlib.pyplot import show


class ExperimentalCondition(object):

	def __init__(self, name=""):

		self.listOfInitialConditions = ListOfExperimentalData()
		self.listOfExperimentalData = ListOfExperimentalData()
		self.name = name
		self.notes = ""


	def addInitialCondition(self, t=0, name="", value=0, value_dev=None, name_attribute="name", quantification_ratio=1):

		initial_condition = ExperimentalData(t, name, value, value_dev, name_attribute, quantification_ratio)
		self.listOfInitialConditions.add(initial_condition)


	def addObservation(self, t=0, name="", value=0, value_dev=0, name_attribute="name", quantification_ratio=1):

		observation = ExperimentalData(t, name, value, value_dev, name_attribute, quantification_ratio)
		self.listOfExperimentalData.add(observation)

	def read(self, list_of_initial_values, list_of_observed_values, name=""):

		self.listOfInitialConditions = list_of_initial_values
		self.listOfExperimentalData = list_of_observed_values
		self.name = name

	def readNuML(self, condition):

		self.name = condition.getIndexValue()
		self.notes = condition.getNotes()

		for data_type in condition.getContents():

			if data_type.getIndexValue() == "initial_values":
				self.listOfInitialConditions.readNuML(data_type)
			elif data_type.getIndexValue() == "observations":
				self.listOfExperimentalData.readNuML(data_type)


	def writeNuML(self, condition):

		if self.notes is not None and len(self.notes) > 0:
			condition.setNotes(self.notes)

		list_of_initial_values = condition.createCompositeValue(condition.getDescription().getContent(), "initial_values")
		self.listOfInitialConditions.writeNuML(list_of_initial_values)

		list_of_observations = condition.createCompositeValue(condition.getDescription().getContent(), "observations")
		self.listOfExperimentalData.writeNuML(list_of_observations)

	def getMaxTime(self):
		return self.listOfExperimentalData.getMaxTime()

	def getTimes(self):
		return self.listOfExperimentalData.getTimes() + self.listOfInitialConditions.getTimes()

	def getTreatedVariables(self):
		return self.listOfInitialConditions.getVariables()

	def getVariables(self):
		return self.listOfInitialConditions.getVariables() + self.listOfExperimentalData.getVariables()

	def plot(self, figure=None, plot=None, suffix="", marker="-"):

		if plot is None:

			if figure is None:
				figure = SigNetSimFigure()
			plot = figure.add_subplot(1, 1, 1)

		for i, (var, values) in enumerate(self.listOfExperimentalData.getValues().items()):
			x = [x_i for x_i, _ in values]
			y = [y_i for _, y_i in values]
			figure.plot(plot, i, x, y, y_name=var+suffix, marker=marker)

		plot.legend(loc='upper right')
		show()

		return plot
