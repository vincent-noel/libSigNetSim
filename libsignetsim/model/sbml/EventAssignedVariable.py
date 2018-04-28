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


class EventAssignedVariable(object):

	def __init__(self, model):

		self.__model = model

		self.__hasEventAssignment = False
		self.__hasEventAssignmentBy = []

	# we need both add and remove implemented for shifts,
	# since we might have to delete some of them after having created them
	def addEventAssignmentBy(self, event, shift=0):
		self.__hasEventAssignmentBy.append((event.objId + shift))
		self.__hasEventAssignment = True

	def removeEventAssignmentBy(self, event, shift=0):
		self.__hasEventAssignmentBy.remove((event.objId + shift))
		self.__hasEventAssignment = (len(self.__hasEventAssignmentBy) > 0)

	def hasEventAssignment(self):
		return self.__hasEventAssignment

	def hasEventAssignmentBy(self):
		return [self.__model.listOfEvents[event] for event in self.__hasEventAssignmentBy]
