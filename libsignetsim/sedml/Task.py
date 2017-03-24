#!/usr/bin/env python
""" Task.py


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
from libsignetsim.sedml.AbstractTask import AbstractTask
from libsignetsim.settings.Settings import Settings

class Task(AbstractTask):

    def __init__(self, document):

        AbstractTask.__init__(self, document)

        self.__document = document
        self.__modelReference = None
        self.__simulationReference = None

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

    def setModelReference(self, model_reference):
        self.__modelReference = model_reference

    def setSimulationReference(self, simulation_reference):
        self.__simulationReference = simulation_reference