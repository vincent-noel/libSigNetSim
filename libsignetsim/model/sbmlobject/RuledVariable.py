#!/usr/bin/env python
""" RuledVariable.py


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


class RuledVariable(object):


    def __init__(self, model):

        self.__model = model
        self.__isRuled = False
        self.__isRuledBy = None


    def setRuledBy(self, rule, shift=0):

        self.__isRuled = True
        self.__isRuledBy = rule.objId + shift

    def unsetRuledBy(self):

        self.__isRuled = False
        self.__isRuledById = None


    def isRuled(self):
        return self.__isRuled


    def isRuledBy(self):
        if self.isRuled():
            return self.__model.listOfRules[self.__isRuledBy]
        else:
            return None


    def isRateRuled(self):
        """ Tests is the compartment size is computed with a rate rule """
        return self.isRuled() and self.__model.listOfRules[self.__isRuledBy].isRate()


    def isAssignmentRuled(self):
        """ Tests is the compartment size is computed with a rate rule """
        return self.isRuled() and self.__model.listOfRules[self.__isRuledBy].isAssignment()


    def copy(self, obj, prefix="", shift=0):
        if obj.isRuled():
            self.setRuledBy(obj.isRuledBy(), shift)