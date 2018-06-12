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
from libsignetsim.sedml.OneStep import OneStep
from libsignetsim.sedml.SedmlException import SedmlOneStepTaskException
from libsignetsim.settings.Settings import Settings

class Task(AbstractTask):

	def __init__(self, document):

		AbstractTask.__init__(self, document)

		self.__document = document
		self.__modelReference = None
		self.__simulationReference = None

		self.__simulationObject = None
		self.__results = None

	def readSedml(self, task, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		AbstractTask.readSedml(self, task, level, version)

		if task.isSetModelReference():
			self.__modelReference = task.getModelReference()

		if task.isSetSimulationReference():
			self.__simulationReference = task.getSimulationReference()

	def writeSedml(self, task, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		AbstractTask.writeSedml(self, task, level, version)

		if self.__modelReference is not None:
			task.setModelReference(self.__modelReference)

		if self.__simulationReference is not None:
			task.setSimulationReference(self.__simulationReference)

	def getModelReference(self):
		return self.__modelReference

	def getSimulationReference(self):
		return self.__simulationReference

	def getModel(self):
		return self.__document.listOfModels.getSbmlModelByReference(self.__modelReference)

	def getSimulation(self):
		return self.__document.listOfSimulations.getSimulation(self.__simulationReference)

	def setModelReference(self, model_reference):
		self.__modelReference = model_reference

	def setSimulationReference(self, simulation_reference):
		self.__simulationReference = simulation_reference

	def setModel(self, model):
		self.__modelReference = model.getId()

	def setSimulation(self, simulation):
		self.__simulationReference = simulation.getId()

	def run(self, timeout=None):

		# One step simulations cannot be executed as a single task, they must be part of a repeated task
		# At least, that's what I understand
		if isinstance(self.__document.listOfSimulations.getSimulation(self.__simulationReference), OneStep):
			raise SedmlOneStepTaskException("One step simulations cannot be executed as a single task")

		model = self.__document.listOfModels.getSbmlModelByReference(self.__modelReference)
		simulation = self.__document.listOfSimulations.getSimulation(self.__simulationReference)
		self.__simulationObject = simulation.run(model, timeout=timeout)
		self.__results = self.__simulationObject.getRawData()[0]

	def getSimulationObject(self):
		return self.__simulationObject

	def getResults(self):
		return self.__results

	def getResultsByVariable(self, variable_sbmlid):
		return self.__results[1][variable_sbmlid]

	def getTimes(self):
		return self.__results[0]

	def getDuration(self):
		return self.__simulationObject.getSimulationDuration()