#!/usr/bin/env python
""" CompositeValue.py


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
			# elif composite_description.isContentTupleDescription():
			# 	self.__content = TupleValue(self.__document)
			# 	self.__content.readNuML(composite_description[0], level, version)
			elif composite_value.isContentAtomicValue():
				t_content = AtomicValue(self.__document, self.getResultComponent(), self.getDescription().getContent())
				t_content.readNuML(composite_value_element, level, version)
				self.__contents.append(t_content)

		self.__indexValue = composite_value.getIndexValue()

	def writeNuML(self, dimension, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		composite_value = dimension.createCompositeValue()
		Dimension.writeNuML(self, composite_value)
		if self.getDescription() is not None:
			composite_value.setDescription(self.getDescription().getId())

		for content in self.__contents:
			content.writeNuML(composite_value, level, version)
		composite_value.setIndexValue(str(self.__indexValue))

	def getContents(self):
		return self.__contents

	def getIndexValue(self):
		return self.__indexValue