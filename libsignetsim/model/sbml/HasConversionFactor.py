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


from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.ModelException import UnknownSIdRefException


class HasConversionFactor(object):
	""" HasConversionFactor property class """


	def __init__ (self, model):
		""" Constructor of class """

		self.__model = model
		self.__conversionFactor = None

	def copy(self, obj):
		self.__conversionFactor = obj.getRawConversionFactor()

	def readSbml(self, conversion_factor,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		self.__conversionFactor = conversion_factor

	def writeSbml(self, object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		if self.__conversionFactor is not None:
			object.setConversionFactor(self.__conversionFactor)

	def isSetConversionFactor(self):
		return self.__conversionFactor is not None

	def getRawConversionFactor(self):
		return self.__conversionFactor

	def getConversionFactor(self):
		if self.__conversionFactor is not None:
			formula = MathFormula(self.__model)
			variable = self.__model.listOfVariables.getBySbmlId(self.__conversionFactor)
			formula.setInternalMathFormula(variable.symbol.getInternalMathFormula())
			return formula

	def getVariableConversionFactor(self):
		if self.__conversionFactor is not None:
			return self.__model.listOfVariables.getBySbmlId(self.__conversionFactor)

	def getSymbolConversionFactor(self):
		if self.__conversionFactor is not None:
			variable = self.__model.listOfVariables.getBySbmlId(self.__conversionFactor)
			return variable.symbol.getInternalMathFormula()

	def setConversionFactor(self, sbml_id):
		if sbml_id is not None and not self.__model.listOfVariables.containsSbmlId(sbml_id):
			raise UnknownSIdRefException("Variable reference %s is unknown" % sbml_id)

		self.__conversionFactor = sbml_id

