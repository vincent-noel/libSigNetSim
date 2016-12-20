#!/usr/bin/env python
""" ListOfDAEs.py


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


from libsignetsim.model.math.DAE import DAE

class ListOfDAEs(list):
	""" Sbml model class """

	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = model
		list.__init__(self)


	def build(self):

		for rule in self.listOfRules.values():
			if rule.isAlgebraic():
				t_dae = DAE(self.__model)
				t_dae.new(dae.getExpressionMath())
				list.append(self, t_dae)


	def buildDAE(self, dae):
