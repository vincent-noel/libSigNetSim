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

from libsignetsim.numl.NMBase import NMBase
from libsignetsim.numl.container.ListOfOntologyTerms import ListOfOntologyTerms
from libsignetsim.numl.container.ListOfResultComponents import ListOfResultComponents
from libsignetsim.numl.NuMLException import NuMLFileNotFound
from libsignetsim.settings.Settings import Settings

import libsbml, libnuml
from libnuml import readNUMLFromFile, writeNUML, NUMLDocument
from six.moves import reload_module
reload_module(libsbml)
from os.path import exists, dirname, basename

class NuMLDocument (NMBase):

	def __init__(self):
		NMBase.__init__(self, self)

		self.path = None
		self.filename = None

		self.listOfOntologyTerms = ListOfOntologyTerms(self)
		self.listOfResultComponents = ListOfResultComponents(self)


	def readNuML(self, numl_document, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		reload_module(libnuml)
		NMBase.readNuML(self, numl_document, level, version)
		self.listOfOntologyTerms.readNuML(numl_document.getOntologyTerms(), level, version)
		self.listOfResultComponents.readNuML(numl_document.getResultComponents(), level, version)
		reload_module(libsbml)
	def writeNuML(self, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		reload_module(libnuml)
		document = NUMLDocument(level, version)

		NMBase.writeNuML(self, document, level, version)

		self.listOfOntologyTerms.writeNuML(document, level, version)
		self.listOfResultComponents.writeNuML(document, level, version)
		reload_module(libsbml)
		return document

	def readNuMLFromFile(self, filename):

		if not exists(filename):
			raise NuMLFileNotFound("NuML file %s not found" % filename)

		document = readNUMLFromFile(filename)
		self.path = dirname(filename)
		self.filename = basename(filename)
		self.readNuML(document)

	def writeNuMLToFile(self, filename):

		self.path = dirname(filename)
		self.filename = basename(filename)

		document = self.writeNuML()
		writeNUML(document, filename)
