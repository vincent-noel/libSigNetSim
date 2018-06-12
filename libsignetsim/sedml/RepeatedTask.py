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

from libsignetsim.sedml.AbstractTask import AbstractTask
from libsignetsim.sedml.container.ListOfSetValueChanges import ListOfSetValueChanges
from libsignetsim.sedml.container.ListOfRanges import ListOfRanges
from libsignetsim.sedml.container.ListOfSubTasks import ListOfSubTasks
from libsignetsim.sedml.SedmlException import SedmlMixedSubtasks, SedmlMultipleModels
from libsignetsim.simulation.SteadyStatesSimulation import SteadyStatesSimulation
from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation
from libsignetsim.settings.Settings import Settings

class RepeatedTask(AbstractTask):

	def __init__(self, document):

		AbstractTask.__init__(self, document)

		self.__document = document
		self.__range = None
		self.__resetModel = None
		self.listOfSetValueChanges = ListOfSetValueChanges(self.__document, self)
		self.listOfRanges = ListOfRanges(self.__document, self)
		self.listOfSubTasks = ListOfSubTasks(self.__document)

		self.__simulationObject = None
		self.__times = None
		self.__results = None

	def readSedml(self, task, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		AbstractTask.readSedml(self, task, level, version)

		if task.isSetRangeId():
			self.__range = task.getRangeId()

		if task.isSetResetModel():
			self.__resetModel = task.getResetModel()

		self.listOfSetValueChanges.readSedml(task.getListOfTaskChanges(), level, version)
		self.listOfRanges.readSedml(task.getListOfRanges(), level, version)
		self.listOfSubTasks.readSedml(task.getListOfSubTasks(), level, version)

	def writeSedml(self, task, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		AbstractTask.writeSedml(self, task, level, version)

		if self.__range is not None:
			task.setRangeId(self.__range)

		if self.__resetModel is not None:
			task.setResetModel(self.__resetModel)

		self.listOfSetValueChanges.writeSedml(task.getListOfTaskChanges(), level, version)
		self.listOfRanges.writeSedml(task.getListOfRanges(), level, version)
		self.listOfSubTasks.writeSedml(task.getListOfSubTasks(), level, version)

	def setRangeReference(self, range_reference):
		self.__range = range_reference

	def setRange(self, range_obj):
		self.__range = range_obj.getId()

	def setResetModel(self, reset_model):
		self.__resetModel = reset_model


	def getModel(self):
		models = self.listOfSubTasks.getModels()
		if len(models) == 1:
			return models[0]
		else:
			raise SedmlMultipleModels("Multiple models are not implemented")

	def run(self, timeout=None):

		if not self.listOfSubTasks.hasSingleTypeOfTask():
			raise SedmlMixedSubtasks("Mixed subtasks are not implemented")

		if self.listOfSubTasks.hasOneSteps():
			models = self.listOfSubTasks.getModels()
			abs_tol = self.listOfSubTasks.getAbsTols()[0]
			rel_tol = self.listOfSubTasks.getRelTols()[0]
			range = self.listOfRanges.getByRangeId(self.__range)
			timepoints = range.getValuesArray()

			self.__simulationObject = TimeseriesSimulation(
				list_of_models=models,
				list_samples=timepoints,
				abs_tol=abs_tol,
				rel_tol=rel_tol,
				keep_files=True
			)
			self.__simulationObject.run(timeout=timeout)

			self.__times = self.__simulationObject.getRawData()[0][0]
			self.__results = self.__simulationObject.getRawData()[0][1]

		elif self.listOfSubTasks.hasSteadyStates():
			models = self.listOfSubTasks.getModels()
			value_changes = self.listOfSetValueChanges.getValueChanges()

			self.__simulationObject = SteadyStatesSimulation(
				list_of_models=models,
				species_input=list(value_changes.keys())[0],
				list_of_initial_values=list(value_changes.values())[0]
			)
			self.__simulationObject.run(timeout=timeout)
			self.__results = self.__simulationObject.getRawData()

		elif self.listOfSubTasks.hasUniformTimeCourses():
			pass


	def getResultsByVariable(self, variable_sbmlid):
		return self.__results[variable_sbmlid]

	def getTimes(self):
		return self.__times

	def getDuration(self):
		return self.__simulationObject.getSimulationDuration()