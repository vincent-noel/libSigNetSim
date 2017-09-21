#!/usr/bin/env python
""" MathSubmodel.py


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

from libsignetsim.model.math.container.ListOfODEs import ListOfODEs
from libsignetsim.model.math.container.ListOfCFEs import ListOfCFEs
from libsignetsim.model.math.container.ListOfDAEs import ListOfDAEs
from libsignetsim.model.ListOfVariables import ListOfVariables
from libsignetsim.model.sbml.container.ListOfEvents import ListOfEvents
from libsignetsim.model.math.MathFormula import MathFormula


class MathSubmodel(object):
	""" Sbml model class """

	def __init__(self, parent_model=None):
		""" Constructor of model class """

		self.parentModel = parent_model
		self.sbmlLevel = self.parentModel.sbmlLevel
		self.sbmlVersion = self.parentModel.sbmlVersion

		self.listOfODEs = ListOfODEs(self)
		self.listOfCFEs = ListOfCFEs(self)
		self.listOfDAEs = ListOfDAEs(self)
		self.listOfVariables = ListOfVariables(self)
		# self.listOfEvents = ListOfEvents(self)
		self.solvedInitialConditions = {}

		self.nbOdes = None
		self.nbAssignments = None
		self.nbConstants = None
		self.nbAlgebraics = None

		self.variablesOdes = None
		self.variablesAssignment = None
		self.variablesConstant = None
		self.variablesAlgebraic = None

		self.__upToDate = False


	def isUpToDate(self):
		return self.__upToDate

	def setUpToDate(self, value):
		self.__upToDate = value

	def copyVariables(self):
		""" Copies the listOfVariables and the solvedInitialConditions """

		self.listOfVariables.copySubmodel(self.parentModel)

		for variable, value in self.parentModel.solvedInitialConditions.items():
			t_value = MathFormula(self)
			t_value.setInternalMathFormula(value.getInternalMathFormula())
			self.solvedInitialConditions.update({variable: t_value})

		# self.listOfEvents.copySubmodel(self.parentModel.listOfEvents)


	def prettyPrint(self):

		print "\n> Full system : "
		print self.listOfCFEs
		print self.listOfDAEs
		print self.listOfODEs
		print "-----------------------------"
