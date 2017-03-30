#!/usr/bin/env python
""" SteadyState.py


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

from libsignetsim.simulation.SteadyStatesSimulation import SteadyStatesSimulation

from libsignetsim.settings.Settings import Settings


class SteadyState(Simulation):

	def __init__(self, document):

		Simulation.__init__(self, document)

		self.__document = document

	def readSedml(self, simulation, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Simulation.readSedml(self, simulation, level, version)

	def writeSedml(self, simulation, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		Simulation.writeSedml(self, simulation, level,version)

	def build(self, sbml_model):

		return SteadyStatesSimulation(
			list_of_models=[sbml_model],
		)

	def getSimulationObject(self):
		return self.__simulationObject
