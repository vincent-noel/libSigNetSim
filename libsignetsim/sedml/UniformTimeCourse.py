#!/usr/bin/env python
""" UniformTimeCourse.py


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

from libsignetsim.sedml.Simulation import Simulation
from libsignetsim.sedml.Algorithm import Algorithm
from libsignetsim.settings.Settings import Settings


class UniformTimeCourse(Simulation):

	def __init__(self, document):

		Simulation.__init__(self, document)

		self.__document = document
		self.__initialTime = None
		self.__outputStartTime = None
		self.__outputEndTime = None
		self.__numberOfPoints = None
		self.__algorithm = None


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

		if simulation.isSetAlgorithm():
			self.__algorithm = Algorithm(self.__document)
			self.__algorithm.readSedml(simulation.getAlgorithm(), level, version)

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

		if self.__algorithm is not None:
			self.__algorithm.writeSedml(simulation.createAlgorithm(), level, version)


	def getInitialTime(self):
		return self.__initialTime

	def getOutputStartTime(self):
		return self.__outputStartTime

	def getOutputEndTime(self):
		return self.__outputEndTime

	def getNumberOfPoints(self):
		return self.__numberOfPoints

	def getAlgorithm(self):
		return self.__algorithm