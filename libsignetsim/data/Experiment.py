#!/usr/bin/env python
""" Experiment.py


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

class Experiment(object):

    def __init__ (self):

        self.listOfConditions = {}
        self.currentId = 0
        self.name = ""

    def addCondition(self, condition):
        self.listOfConditions.update({self.currentId: condition})
        self.currentId += 1


    def getMaxTime(self):

        max_time = 0
        for condition in self.listOfConditions.values():
            if condition.getMaxTime() > max_time:
                max_time = condition.getMaxTime()

        return max_time


    def getTimes(self):
        times = []
        for condition in self.listOfConditions.values():
            times += condition.getTimes()
        return times

    def getTreatedVariables(self):
        species = []
        for condition in self.listOfConditions.values():
            species += condition.getTreatedVariables()
        print species

        if len(species) > 1:
            return list(set(species))
        else:
            return species
