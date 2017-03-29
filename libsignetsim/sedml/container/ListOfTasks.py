#!/usr/bin/env python
""" ListOfTasks.py


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
from libsignetsim.sedml.Task import Task
from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_TASK
reload(libsbml)

class ListOfTasks(SedBase):

	def __init__(self, document):

		SedBase.__init__(self, document)

		self.__document = document
		self.listOfTasks = []

	def readSedml(self, list_of_tasks, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, list_of_tasks, level, version)

		for t_task in list_of_tasks:
			task = None

			if t_task.getTypeCode() == SEDML_TASK:
				task = Task(self.__document)

			if task is not None:
				task.readSedml(t_task, level, version)
				self.listOfTasks.append(task)

	def writeSedml(self, list_of_tasks, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, list_of_tasks, level, version)

		for t_task in self.listOfTasks:

			if isinstance(t_task, Task):
				task = list_of_tasks.createTask()
				t_task.writeSedml(task, level, version)

	def getTask(self, task_reference):

		for task in self.listOfTasks:
			if task.getId() == task_reference:
				return task

	def buildTasks(self):

		for task in self.listOfTasks:
			task.build()

	def runTasks(self):

		for task in self.listOfTasks:
			task.run()
