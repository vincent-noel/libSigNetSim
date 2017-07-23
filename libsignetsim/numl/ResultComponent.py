#!/usr/bin/env python
""" ResultComponent.py


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
from libsignetsim.settings.Settings import Settings
from libsignetsim.numl.NMBase import NMBase
from libsignetsim.numl.CompositeDescription import CompositeDescription
from libsignetsim.numl.AtomicDescription import AtomicDescription
from libsignetsim.numl.TupleDescription import TupleDescription
from libsignetsim.numl.CompositeValue import CompositeValue
from libsignetsim.numl.TupleValue import TupleValue
from libsignetsim.numl.AtomicValue import AtomicValue
from re import sub

class ResultComponent (NMBase):

	def __init__(self, document, name=None):

		NMBase.__init__(self, document)
		self.__document = document
		self.__id = None
		self.__dimensionDescriptions = []
		self.__dimensions = []
		self.__name = name

	def createCompositeDescription(self, name=None, index_type="string"):

		dimension_description = CompositeDescription(self.__document, name, index_type)
		dimension_description.setId("%s_header_%d" % (self.__id, len(self.__dimensionDescriptions)))
		self.__dimensionDescriptions.append(dimension_description)
		return dimension_description

	def createCompositeValue(self, description, index_value="string"):

		dimension_value = CompositeValue(self.__document, self, description, index_value)
		self.__dimensions.append(dimension_value)
		return dimension_value

	def readNuML(self, result_component, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		NMBase.readNuML(self, result_component, level, version)
		self.__id = result_component.getId()

		# Always one element ??!!
		for dimension_description in result_component.getDimensionDescription():

			t_dimension_description = None
			if dimension_description.isContentCompositeDescription():
				t_dimension_description = CompositeDescription(self.__document)

			elif dimension_description.isContentTupleDescription():
				t_dimension_description = TupleDescription(self.__document)

			elif dimension_description.isContentAtomicDescription():
				t_dimension_description = AtomicDescription(self.__document)

			if t_dimension_description is not None:
				t_dimension_description.readNuML(dimension_description, level, version)
				self.__dimensionDescriptions.append(t_dimension_description)

		for dimension in result_component.getDimension():

			t_dimension = None
			if dimension.isContentCompositeValue():
				t_dimension = CompositeValue(self.__document, self, self.__dimensionDescriptions[0])

			elif dimension.isContentTupleValue():
				t_dimension = TupleValue(self.__document, self.__dimensionDescriptions[0])

			elif dimension.isContentAtomicValue():
				t_dimension = AtomicValue(self.__document, self.__dimensionDescriptions[0])

			if t_dimension is not None:
				t_dimension.readNuML(dimension, level, version)
				self.__dimensions.append(t_dimension)

	def writeNuML(self, result_component, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		NMBase.writeNuML(self, result_component, level, version)

		if self.__name is not None:
			result_component.setId(sub(r"[^A-Za-z0-9_]+", "", self.__name.replace(" ", "_")))
		else:
			result_component.setId(self.__id)

		for dimension_description in self.__dimensionDescriptions:
			dimension_description.writeNuML(result_component, level, version)

		for dimension in self.__dimensions:
			dimension.writeNuML(result_component, level, version)


	def setId(self, result_component_id):
		self.__id = result_component_id

	def getDimensionsDescriptions(self):
		return self.__dimensionDescriptions

	def getDimensions(self):
		return self.__dimensions