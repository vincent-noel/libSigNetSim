#!/usr/bin/env python
""" RepeatedTask.py


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
from libsignetsim.sedml.container.ListOfSetValueChanges import ListOfSetValueChanges
from libsignetsim.sedml.container.ListOfRanges import ListOfRanges
from libsignetsim.sedml.container.ListOfSubTasks import ListOfSubTasks
from libsignetsim.settings.Settings import Settings

class RepeatedTask(AbstractTask):

	def __init__(self, document):

		AbstractTask.__init__(self, document)

		self.__document = document
		self.__range = None
		self.__resetModel = None
		self.listOfSetValueChanges = ListOfSetValueChanges(self)
		self.listOfRanges = ListOfRanges(self)
		self.listOfSubTasks = ListOfSubTasks(self)

	def readSedml(self, task, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		AbstractTask.readSedml(self, task, level, version)

		if task.isSetRangeId():
			self.__range = task.getRangeId()

		if task.isSetResetModel():
			self.__resetModel = task.getResetModel()

		self.listOfSetValueChanges.readSedml(task.getListOfTaskChanges(), level, version)
		self.listOfRanges.readSedml(task.getListOfRanges(), level, version)
		self.listOfSubTasks.readSedml(task.getListOfSubTasks(), level, version)

	def writeSedml(self, task, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		AbstractTask.writeSedml(self, task, level, version)

		if self.__range is not None:
			task.setRangeId(self.__range)

		if self.__resetModel is not None:
			task.setResetModel(self.__resetModel)

		self.listOfSetValueChanges.writeSedml(task.getListOfTaskChanges(), level, version)
		self.listOfRanges.writeSedml(task.getListOfRanges(), level, version)
		self.listOfSubTasks.writeSedml(task.getListOfSubTasks(), level, version)

	def setRangeReference(self, range_reference):
		self.__range = range_reference

	def setRange(self, range_obj):
		self.__range = range_obj.getId()

	def setResetModel(self, reset_model):
		self.__resetModel = reset_model
