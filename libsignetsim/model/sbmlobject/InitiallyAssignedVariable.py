#!/usr/bin/env python
""" InitiallyAssignedVariable.py


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


class InitiallyAssignedVariable(object):

    def __init__(self, model):

        self.__model = model

        self.__hasInitialAssignment = False
        self.__hasInitialAssignmentBy = None


    # Modifiers
    def setInitialAssignmentBy(self, initial_assignment, shift=0):
        self.__hasInitialAssignment = True
        self.__hasInitialAssignmentBy = initial_assignment.objId + shift


    def unsetInitialAssignmentBy(self):
        self.__hasInitialAssignment = False
        self.__hasInitialAssignmentBy = None


    # Queries
    def hasInitialAssignment(self):
        return self.__hasInitialAssignment

    def hasInitialAssignmentBy(self):
        if self.hasInitialAssignment():
            return self.__model.listOfInitialAssignments[self.__hasInitialAssignmentBy]
        else:
            return None


    # Copy
    def copy(self, obj, prefix="", shift=0):
        if obj.hasInitialAssignment():
            self.setInitialAssignmentBy(obj.hasInitialAssignmentBy(), shift)