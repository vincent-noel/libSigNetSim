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

from libsignetsim.numl.DimensionDescription import DimensionDescription
from libsignetsim.numl.TupleDescription import TupleDescription
from libsignetsim.numl.AtomicDescription import AtomicDescription
from libsignetsim.settings.Settings import Settings

class CompositeDescription (DimensionDescription):

	def __init__(self, document, name=None, index_type="string"):
		DimensionDescription.__init__(self, document, name)
		self.__document = document
		self.__content = None
		self.__indexType = index_type
		self.__ontologyTerm = None

	def createCompositeDescription(self, name=None, index_type="string"):

		from libsignetsim.numl.CompositeDescription import CompositeDescription
		self.__content = CompositeDescription(self.__document, name, index_type)
		self.__content.setId("%s_0" % self.getId())
		return self.__content

	def createTupleDescription(self, name=None):
		self.__content = TupleDescription(self.__document, name)
		self.__content.setId("%s_0" % self.getId())
		return self.__content

	def createAtomicDescription(self, name=None, value_type="double"):
		self.__content = AtomicDescription(self.__document, name, value_type)
		self.__content.setId("%s_0" % self.getId())
		return self.__content

	def readNuML(self, composite_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		DimensionDescription.readNuML(self, composite_description)

		if composite_description.isContentCompositeDescription():
			from libsignetsim.numl.CompositeDescription import CompositeDescription
			self.__content = CompositeDescription(self.__document)
			self.__content.readNuML(composite_description[0], level, version)

		elif composite_description.isContentTupleDescription():
			self.__content = TupleDescription(self.__document)
			self.__content.readNuML(composite_description[0], level, version)

		elif composite_description.isContentAtomicDescription():
			self.__content = AtomicDescription(self.__document)
			self.__content.readNuML(composite_description[0], level, version)

		self.__indexType = composite_description.getIndexType()
		self.__ontologyTerm = self.__document.listOfOntologyTerms.getByOntologyTerm(composite_description.getOntologyTerm())

	def writeNuML(self, composite_description, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		DimensionDescription.writeNuML(self, composite_description)

		if self.__indexType is not None:
			composite_description.setIndexType(self.__indexType)

		if self.__ontologyTerm is not None:
			composite_description.setOntologyTerm(self.__ontologyTerm.getId())

		if self.__content is not None:
			t_content = None
			from libsignetsim.numl.CompositeDescription import CompositeDescription
			if isinstance(self.__content, CompositeDescription):
				t_content = composite_description.createCompositeDescription()

			elif isinstance(self.__content, TupleDescription):
				t_content = composite_description.createTupleDescription()

			elif isinstance(self.__content, AtomicDescription):
				t_content = composite_description.createAtomicDescription()

			if t_content is not None:
				self.__content.writeNuML(t_content, level, version)

	def getContent(self):
		return self.__content