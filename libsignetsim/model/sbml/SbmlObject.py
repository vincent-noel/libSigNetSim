#!/usr/bin/env python
""" SbmlObject.py


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

from libsignetsim.model.sbml.SimpleSbmlObject import SimpleSbmlObject
from libsignetsim.model.sbml.HasReplacedElements import HasReplacedElements

from libsignetsim.settings.Settings import Settings
from libsbml import SyntaxChecker
from libsbml import XMLNode


class SbmlObject(SimpleSbmlObject, HasReplacedElements):

	def __init__(self, model):

		self.__model = model
		SimpleSbmlObject.__init__(self, model)
		HasReplacedElements.__init__(self, model)
		self.isMarkedToBeReplaced = False
		self.isMarkedToBeReplacedBy = None
		self.isMarkedToBeDeleted = False
		self.isMarkedToBeRenamed = False
		self.hasConversionFactor = None


	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasReplacedElements.readSbml(self, sbml_object, sbml_level, sbml_version)
		SimpleSbmlObject.readSbml(self, sbml_object, sbml_level, sbml_version)


	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		HasReplacedElements.writeSbml(self, sbml_object, sbml_level, sbml_version)
		SimpleSbmlObject.writeSbml(self, sbml_object, sbml_level, sbml_version)


	def instance(self):

		if self.__model.isMainModel:
			t_model = self.__model
		else:
			t_model = self.__model.parentDoc.model

		if t_model.listOfSbmlObjects.hasToBeReplaced(self):
			return t_model.listOfSbmlObjects.getReplacedBy(self)
		else:
			return self


	def needReplacement(self):
		return self.__model.listOfSbmlObjects.hasToBeReplaced(self)


	def copy(self, obj, prefix="", shift=0):
		SimpleSbmlObject.copy(self, obj, prefix, shift)
		HasReplacedElements.copy(self, obj, prefix, shift)

	def isInMainModel(self):
		return self.__model.isMainModel

	def getModel(self):
		return self.__model
