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

from libsignetsim.sedml.container.ListOf import ListOf
from libsignetsim.sedml.UniformTimeCourse import UniformTimeCourse
from libsignetsim.sedml.SteadyState import SteadyState
from libsignetsim.sedml.OneStep import OneStep

from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_SIMULATION_UNIFORMTIMECOURSE, SEDML_SIMULATION_ONESTEP, SEDML_SIMULATION_STEADYSTATE
from six.moves import reload_module
reload_module(libsbml)

class ListOfSimulations(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)
		self.__document = document
		self.__simulationCounter = 0

	def new(self, simulation_type, simulation_id=None):

		t_simulation_id = simulation_id
		if t_simulation_id is None:
			t_simulation_id = "simulation_%d" % self.__simulationCounter

		if simulation_type == SEDML_SIMULATION_UNIFORMTIMECOURSE:
			simulation = UniformTimeCourse(self.__document)
			simulation.setId(t_simulation_id)
			ListOf.append(self, simulation)
			self.__simulationCounter += 1
			return simulation

		elif simulation_type == SEDML_SIMULATION_STEADYSTATE:
			simulation = SteadyState(self.__document)
			simulation.setId(t_simulation_id)
			ListOf.append(self, simulation)
			self.__simulationCounter += 1
			return simulation

		elif simulation_type == SEDML_SIMULATION_ONESTEP:
			simulation = OneStep(self.__document)
			simulation.setId(t_simulation_id)
			ListOf.append(self, simulation)
			self.__simulationCounter += 1
			return simulation

	def createUniformTimeCourse(self, simulation_id=None):
		return self.new(SEDML_SIMULATION_UNIFORMTIMECOURSE, simulation_id)

	def createSteadyState(self, simulation_id=None):
		return self.new(SEDML_SIMULATION_STEADYSTATE, simulation_id)

	def createOneStep(self, simulation_id=None):
		return self.new(SEDML_SIMULATION_ONESTEP, simulation_id)

	def readSedml(self, list_of_simulations, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_simulations, level, version)

		for t_simulation in list_of_simulations:

			if t_simulation.getTypeCode() == SEDML_SIMULATION_UNIFORMTIMECOURSE:
				simulation = UniformTimeCourse(self.__document)
				simulation.readSedml(t_simulation, level, version)
				ListOf.append(self, simulation)
				self.__simulationCounter += 1

			elif t_simulation.getTypeCode() == SEDML_SIMULATION_STEADYSTATE:
				simulation = SteadyState(self.__document)
				simulation.readSedml(t_simulation, level, version)
				ListOf.append(self, simulation)
				self.__simulationCounter += 1

			elif t_simulation.getTypeCode() == SEDML_SIMULATION_ONESTEP:
				simulation = OneStep(self.__document)
				simulation.readSedml(t_simulation, level, version)
				ListOf.append(self, simulation)
				self.__simulationCounter += 1

	def writeSedml(self, list_of_simulations, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_simulations, level, version)

		for t_simulation in self:

			if isinstance(t_simulation, UniformTimeCourse):
				simulation = list_of_simulations.createUniformTimeCourse()
				t_simulation.writeSedml(simulation, level, version)
				self.__simulationCounter += 1

			elif isinstance(t_simulation, SteadyState):
				simulation = list_of_simulations.createSteadyState()
				t_simulation.writeSedml(simulation, level, version)
				self.__simulationCounter += 1

			elif isinstance(t_simulation, OneStep):
				simulation = list_of_simulations.createOneStep()
				t_simulation.writeSedml(simulation, level, version)
				self.__simulationCounter += 1

	def getSimulation(self, simulation_reference):

		for simulation in self:
			if simulation.getId() == simulation_reference:
				return simulation
	#
	# def buildSimulation(self, simulation_reference, model):
	#
	# 	return self.getSimulation(simulation_reference).build(model)
	#
	# def runSimulation(self, simulation_reference):
	#
	# 	return self.getSimulation(simulation_reference).run()
