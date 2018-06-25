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
from __future__ import print_function

from libsignetsim.cwriter.CModelWriter import CModelWriter
from libsignetsim.model.math.container.ListOfConservationLaws import ListOfConservationLaws
from libsignetsim.model.math.container.ListOfODEs import ListOfODEs
from libsignetsim.model.math.container.ListOfCFEs import ListOfCFEs
from libsignetsim.model.math.container.ListOfDAEs import ListOfDAEs
from libsignetsim.model.math.container.ListOfInitialConditions import ListOfInitialConditions

from libsignetsim.model.math.MathStoichiometryMatrix import MathStoichiometryMatrix
from libsignetsim.model.math.MathConservationMatrix import MathConservationMatrix
from libsignetsim.model.math.MathSlowModel import MathSlowModel
from libsignetsim.model.math.MathAsymmetricModel import MathAsymmetricModel

from libsignetsim.settings.Settings import Settings

from time import time


class MathModel(CModelWriter):
	""" Sbml model class """

	def __init__(self, obj_id=0):
		""" Constructor of model class """

		CModelWriter.__init__(self, obj_id)

		self.listOfODEs = ListOfODEs(self)
		self.listOfCFEs = ListOfCFEs(self)
		self.listOfDAEs = ListOfDAEs(self)

		self.listOfInitialConditions = ListOfInitialConditions(self)

		self.slowModel = None
		self.asymetricModel = MathAsymmetricModel(self)
		self.stoichiometryMatrix = MathStoichiometryMatrix(self)
		self.conservationMatrix = MathConservationMatrix(self)
		self.listOfConservationLaws = ListOfConservationLaws(self)
		self.slowModel = MathSlowModel(self, self.asymetricModel)

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

	def setUpToDate(self, value=True):
		self.__upToDate = value

	def getMathModel(self):

		if self.slowModel.isUpToDate():
			return self.slowModel

		elif self.asymetricModel.isUpToDate():
			return self.asymetricModel
		else:
			return self

	def buildModel(self, vars_to_keep=[], reduce=Settings.reduceByDefault, tmin=0):

		if not reduce:
			self.slowModel.setUpToDate(False)
			self.asymetricModel.setUpToDate(False)

		self.listOfCFEs.build()
		self.listOfODEs.build()
		self.listOfDAEs.build()

		t0 = time()

		self.listOfInitialConditions.solve(tmin)

		if Settings.verboseTiming >= 1:
			print("> Initial condition solved in %.2gs" % (time()-t0))

		if len(self.listOfDAEs) > 0:
			self.listOfDAEs.solveInitialConditions(tmin)
			self.listOfDAEs.solveDAEs()

		if reduce:
			self.buildReducedModel(vars_to_keep=vars_to_keep)

		if len(self.listOfEvents) == 0 and self.listOfReactions.hasFastReaction():
			self.buildSlowModel()

		self.setUpToDate()

	def buildConservationLaws(self):

		t0 = time()
		self.stoichiometryMatrix.build()
		if Settings.verboseTiming >= 2:
			print("> stoichiometry matrix built in %.2gs" % (time() -t0))

		t0 = time()
		self.listOfConservationLaws.build()
		if Settings.verboseTiming >= 2:
			print("> conservation laws built in %.2gs" % (time() - t0))

	def buildReducedModel(self, vars_to_keep=[]):

		t0 = time()
		self.stoichiometryMatrix.build()
		self.listOfConservationLaws.build()
		self.asymetricModel.build(treated_variables=vars_to_keep)
		if Settings.verboseTiming >= 1:
			print("> model reduced in %.2gs" % (time() - t0))

	def buildSlowModel(self):

		vars_to_keep = (
			[var.getSymbolStr() for var in self.listOfVariables.getFastVariables()]
			+ [var.getSymbolStr() for var in self.listOfVariables.getSlowVariables()]
		)

		self.buildReducedModel(vars_to_keep=vars_to_keep)
		self.slowModel.build()

	def prettyPrint(self):

		print("\n> Full system : ")

		print(self.listOfCFEs)
		print(self.listOfDAEs)
		print(self.listOfODEs)
		print(self.listOfConservationLaws)

		print("-----------------------------")

	def pprint(self):
		self.listOfCFEs.pprint()
		self.listOfDAEs.pprint()
		self.listOfODEs.pprint()
		self.listOfInitialConditions.pprint()
