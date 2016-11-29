#!/usr/bin/env python
""" HasIds.py


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


class HasIds(object):
    """ Parent class for all the ListOf_ containers in a sbml model """

    def __init__ (self, model=None):

        self.__model = model




    def sbmlIds(self):
        """ Return a set of import ids of the sbml objects """
        return [obj.getSbmlId() for obj in self.values()]

    def getBySbmlId(self, sbml_id, pos=0):
        """ Find sbml objects by their import Id """

        res = []
        for obj in self.values():
            if obj.getSbmlId() == sbml_id:
                res.append(obj)

        if len(res) > 0:
            return res[pos]
        else:
            return None


    def containsSbmlId(self, sbml_id):
        """ Test if an sbml id is in the list """

        res = False
        for obj in self.values():
            if sbml_id == obj.getSbmlId():
                res = True

        return res



    def names(self):
        """ Return set of names of the sbml objects """
        return [obj.getName() for obj in self.values()]

    def getByName(self, name, pos=0):
        """ Find sbml objects by their name """

        res = []
        for obj in self.values():
            if obj.getName() == name:
                res.append(obj)

        if len(res) > 0:
            return res[pos]
        else:
            return non


    def containsName(self, name):
        """ Test if a name is in the list """

        res = False
        for obj in self.values():
            if name == obj.getName():
                res = True

        return res