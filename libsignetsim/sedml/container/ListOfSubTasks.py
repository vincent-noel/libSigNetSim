#!/usr/bin/env python
""" ListOfSubTasks.py


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
from libsignetsim.sedml.container.ListOf import ListOf
from libsignetsim.sedml.SubTask import SubTask

from libsignetsim.settings.Settings import Settings


class ListOfSubTasks(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)
		self.__document = document
		self.__subTaskCounter = 0

	def new(self):

		sub_task = SubTask(self.__document)
		ListOf.append(self, sub_task)
		self.__subTaskCounter += 1
		return sub_task

	def createSubTask(self):
		return self.new()

	def readSedml(self, list_of_sub_tasks, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_sub_tasks, level, version)

		for sub_task in list_of_sub_tasks:
			t_sub_task = SubTask(self.__document)
			t_sub_task.readSedml(sub_task, level, version)
			ListOf.append(self, t_sub_task)
			self.__subTaskCounter += 1

	def writeSedml(self, list_of_sub_tasks, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_sub_tasks, level, version)

		for sub_task in self:
			t_sub_task = list_of_sub_tasks.createSubTask()
			sub_task.writeSedml(t_sub_task, level, version)


