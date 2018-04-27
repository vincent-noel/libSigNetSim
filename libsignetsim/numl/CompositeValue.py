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

from libsignetsim.numl.Dimension import Dimension
from libsignetsim.numl.TupleValue import TupleValue
from libsignetsim.numl.AtomicValue import AtomicValue
from libsignetsim.settings.Settings import Settings

class CompositeValue (Dimension):

	def __init__(self, document, result_component, description=None, index_value=""):

		Dimension.__init__(self, document, result_component, description)
		self.__document = document
		self.__contents = []
		self.__indexValue = index_value

	def createCompositeValue(self, description=None, index_value=""):

		from libsignetsim.numl.CompositeValue import CompositeValue
		composite_value = CompositeValue(self.__document, self.getResultComponent(), description, index_value)
		self.__contents.append(composite_value)
		return composite_value

	def createTupleValue(self, description=None):

		tuple_value = TupleValue(self.__document, self.getResultComponent(), description)
		self.__contents.append(tuple_value)
		return tuple_value


	def createAtomicValue(self, description=None, value=None):

		atomic_value = AtomicValue(self.__document, self.getResultComponent(), description, value)
		self.__contents.append(atomic_value)
		return atomic_value

	def readNuML(self, composite_value, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		Dimension.readNuML(self, composite_value)

		for composite_value_element in composite_value:
			if composite_value.isContentCompositeValue():
				from libsignetsim.numl.CompositeValue import CompositeValue
				t_content = CompositeValue(self.__document, self.getResultComponent(), self.getDescription().getContent())
				t_content.readNuML(composite_value_element, level, version)
				self.__contents.append(t_content)

			elif composite_value.isContentTuple():
				t_content = TupleValue(self.__document, self.getResultComponent(), self.getDescription().getContent())
				t_content.readNuML(composite_value_element, level, version)
				self.__contents.append(t_content)

			elif composite_value.isContentAtomicValue():
				t_content = AtomicValue(self.__document, self.getResultComponent(), self.getDescription().getContent())
				t_content.readNuML(composite_value_element, level, version)
				self.__contents.append(t_content)

		self.__indexValue = composite_value.getIndexValue()

	def writeNuML(self, dimension, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		Dimension.writeNuML(self, dimension)
		if self.getDescription() is not None:
			dimension.setDescription(self.getDescription().getId())

		for content in self.__contents:
			t_dimension = None

			from libsignetsim.numl.CompositeValue import CompositeValue
			if isinstance(content, CompositeValue):
				t_dimension = dimension.createCompositeValue()

			elif isinstance(content, TupleValue):
				t_dimension = dimension.createTuple()

			elif isinstance(content, AtomicValue):
				t_dimension = dimension.createAtomicValue()

			if t_dimension is not None:
				content.writeNuML(t_dimension, level, version)

		dimension.setIndexValue(str(self.__indexValue))

	def getContents(self):
		return self.__contents

	def getIndexValue(self):
		return self.__indexValue