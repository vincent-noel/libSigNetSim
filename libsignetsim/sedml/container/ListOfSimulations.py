#!/usr/bin/env python
""" ListOfSimulations.py


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

from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.UniformTimeCourse import UniformTimeCourse
from libsignetsim.settings.Settings import Settings
# import libsbml

from libsedml import SEDML_SIMULATION_UNIFORMTIMECOURSE, SEDML_SIMULATION_ONESTEP, SEDML_SIMULATION_STEADYSTATE
# reload(libsbml)

class ListOfSimulations(SedBase):

	def __init__(self, document):

		SedBase.__init__(self, document)
		self.__document = document
		self.listOfSimulations = []

	def readSedml(self, list_of_simulations, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, list_of_simulations, level, version)

		for t_simulation in list_of_simulations:

			if t_simulation.getTypeCode() == SEDML_SIMULATION_UNIFORMTIMECOURSE:
				simulation = UniformTimeCourse(self.__document)
				simulation.readSedml(t_simulation, level, version)
				self.listOfSimulations.append(simulation)

	def writeSedml(self, list_of_simulations, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, list_of_simulations, level, version)

		for t_simulation in self.listOfSimulations:

			if isinstance(t_simulation, UniformTimeCourse):
				simulation = list_of_simulations.createUniformTimeCourse()
				t_simulation.writeSedml(simulation, level, version)


	def buildSimulation(self, simulation_reference, model):

		for t_simulation in self.listOfSimulations:
			if t_simulation.getId() == simulation_reference:
				return t_simulation.buildSimulation(model)