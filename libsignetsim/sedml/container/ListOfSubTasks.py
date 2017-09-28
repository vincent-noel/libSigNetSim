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
from libsignetsim.sedml.SubTask import SubTask
from libsignetsim.sedml.UniformTimeCourse import UniformTimeCourse
from libsignetsim.sedml.OneStep import OneStep
from libsignetsim.sedml.SteadyState import SteadyState
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

	def hasSingleTypeOfTask(self):
		""" Return true if all the subtasks are of the same type. Mixed subtasks are not implemented yet """

		types = []
		for sub_task in self:
			types.append(type(sub_task.getTask().getSimulation()))

		return len(set(types)) <= 1

	def hasSingleModel(self):

		models = []
		for sub_task in self:
			models.append(sub_task.getModel())

		return len(set(models)) <= 1

	def hasOneSteps(self):

		for sub_task in self:
			if not isinstance(sub_task.getTask().getSimulation(), OneStep):
				return False

		return True

	def hasSteadyStates(self):

		for sub_task in self:
			if not isinstance(sub_task.getTask().getSimulation(), SteadyState):
				return False

		return True

	def hasUniformTimeCourses(self):

		for sub_task in self:
			if not isinstance(sub_task.getTask().getSimulation(), UniformTimeCourse):
				return False

		return True

	def getModels(self):

		models = []
		for sub_task in self:
			models.append(sub_task.getTask().getModel())

		return list(set(models))

	def getAbsTols(self):
		abs_tols = []
		for sub_task in self:
			abs_tols.append(sub_task.getTask().getSimulation().getAlgorithm().getAbsTol())

		return abs_tols

	def getRelTols(self):
		rel_tols = []
		for sub_task in self:
			rel_tols.append(sub_task.getTask().getSimulation().getAlgorithm().getRelTol())

		return rel_tols