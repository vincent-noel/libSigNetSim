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
from libsignetsim.sedml.Task import Task
from libsignetsim.sedml.RepeatedTask import RepeatedTask
from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_TASK, SEDML_TASK_REPEATEDTASK
from six.moves import reload_module
reload_module(libsbml)


class ListOfTasks(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)

		self.__document = document
		self.__taskCounter = 0

	def new(self, task_type, task_id=None):

		t_task_id = task_id
		if t_task_id is None:
			t_task_id = "task_%d" % self.__taskCounter

		if task_type == SEDML_TASK:
			task = Task(self.__document)
			task.setId(t_task_id)
			ListOf.append(self, task)
			self.__taskCounter += 1
			return task

		elif task_type == SEDML_TASK_REPEATEDTASK:
			task = RepeatedTask(self.__document)
			task.setId(t_task_id)
			ListOf.append(self, task)
			self.__taskCounter += 1
			return task

	def createTask(self, task_id=None):
		return self.new(SEDML_TASK, task_id)

	def createRepeatedTask(self, task_id=None):
		return self.new(SEDML_TASK_REPEATEDTASK, task_id)

	def readSedml(self, list_of_tasks, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_tasks, level, version)

		for t_task in list_of_tasks:

			if t_task.getTypeCode() == SEDML_TASK:
				task = Task(self.__document)
				task.readSedml(t_task, level, version)
				ListOf.append(self, task)
				self.__taskCounter += 1

			elif t_task.getTypeCode() == SEDML_TASK_REPEATEDTASK:
				task = RepeatedTask(self.__document)
				task.readSedml(t_task, level, version)
				ListOf.append(self, task)
				self.__taskCounter += 1

	def writeSedml(self, list_of_tasks, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_tasks, level, version)

		for t_task in self:

			if isinstance(t_task, Task):
				task = list_of_tasks.createTask()
				t_task.writeSedml(task, level, version)

			elif isinstance(t_task, RepeatedTask):
				task = list_of_tasks.createRepeatedTask()
				t_task.writeSedml(task, level, version)

	def getTask(self, task_reference):

		for task in self:
			if task.getId() == task_reference:
				return task

	def buildTasks(self):

		for task in self:
			task.build()

	def runTasks(self):

		for task in self:
			task.run()
