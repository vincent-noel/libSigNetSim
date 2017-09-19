#!/usr/bin/env python
""" HasMetaIds.py


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


class HasMetaIds(object):
	""" Parent class for all the ListOf_ containers in a sbml model """

	def __init__ (self, model=None):

		self.__model = model




	def metaIds(self):
		""" Return set of names of the sbml objects """
		return [obj.getMetaId() for obj in self.values()]

	def getByMetaId(self, meta_id, pos=0):
		""" Find sbml objects by their name """

		res = []
		for obj in self.values():
			if obj.getMetaId() == meta_id:
				res.append(obj)

		if len(res) > 0:
			return res[pos]
		else:
			return None


	def containsMetaId(self, meta_id):
		""" Test if a name is in the list """

		res = False
		for obj in self.values():
			if meta_id == obj.getMetaId():
				res = True

		return res
