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


from libsignetsim.settings.Settings import Settings


class SubTask(object):

	def __init__(self, document):

		self.__document = document
		self.__task = None
		self.__order = None

	def readSedml(self, subtask, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if subtask.isSetTask():
			self.__task = subtask.getTask()

		if subtask.isSetOrder():
			self.__order = subtask.getOrder()

	def writeSedml(self, subtask, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if self.__task is not None:
			subtask.setTask(self.__task)

		if self.__order is not None:
			subtask.setOrder(self.__order)

	def getTaskReference(self):
		return self.__task

	def getTask(self):
		return self.__document.listOfTasks.getTask(self.__task)

	def getOrder(self):
		return self.__order

	def setTaskReference(self, task_reference):
		self.__task = task_reference

	def setTask(self, task):
		self.__task = task.getId()

	def setOrder(self, order):
		self.__order = order

