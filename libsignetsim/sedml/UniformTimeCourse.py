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

from libsignetsim.sedml.Simulation import Simulation

from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation

from libsignetsim.settings.Settings import Settings
from numpy import linspace

class UniformTimeCourse(Simulation):

	def __init__(self, document):

		Simulation.__init__(self, document)

		self.__document = document
		self.__initialTime = None
		self.__outputStartTime = None
		self.__outputEndTime = None
		self.__numberOfPoints = None

	def readSedml(self, simulation, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Simulation.readSedml(self, simulation, level, version)

		if simulation.isSetInitialTime():
			self.__initialTime = simulation.getInitialTime()

		if simulation.isSetOutputStartTime():
			self.__outputStartTime = simulation.getOutputStartTime()

		if simulation.isSetOutputEndTime():
			self.__outputEndTime = simulation.getOutputEndTime()

		if simulation.isSetNumberOfPoints():
			self.__numberOfPoints = simulation.getNumberOfPoints()

	def writeSedml(self, simulation, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Simulation.writeSedml(self, simulation, level,version)

		if self.__initialTime is not None:
			simulation.setInitialTime(self.__initialTime)

		if self.__outputStartTime is not None:
			simulation.setOutputStartTime(self.__outputStartTime)

		if self.__outputEndTime is not None:
			simulation.setOutputEndTime(self.__outputEndTime)

		if self.__numberOfPoints is not None:
			simulation.setNumberOfPoints(self.__numberOfPoints)


	def getInitialTime(self):
		return self.__initialTime

	def getOutputStartTime(self):
		return self.__outputStartTime

	def getOutputEndTime(self):
		return self.__outputEndTime

	def getNumberOfPoints(self):
		return self.__numberOfPoints

	def run(self, sbmlModel, timeout=None):
		samples = [float(value) for value in linspace(self.__outputStartTime, self.__outputEndTime, self.__numberOfPoints+1)]

		t_simulation = TimeseriesSimulation(
			list_of_models=[sbmlModel],
			time_min=self.__initialTime,
			list_samples=samples,
			abs_tol=Simulation.getAlgorithm(self).getAbsTol(),
			rel_tol=Simulation.getAlgorithm(self).getRelTol(),
		)
		t_simulation.run(timeout=timeout)
		return t_simulation

	def getSimulationObject(self):
		return self.__simulationObject

	def setInitialTime(self, initial_time):
		self.__initialTime = initial_time

	def setOutputStartTime(self, output_start_time):
		self.__outputStartTime = output_start_time

	def setOutputEndTime(self, output_end_time):
		self.__outputEndTime = output_end_time

	def setNumberOfPoints(self, number_of_points):
		self.__numberOfPoints = number_of_points
