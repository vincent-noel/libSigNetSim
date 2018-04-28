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

	Initialization of the module URIs

"""


from libsignetsim.uris.NCBITaxonomyResolver import NCBITaxonomyResolver
from libsignetsim.uris.SBOResolver import SBOResolver
from libsignetsim.uris.GoResolver import GoResolver
from libsignetsim.uris.PubmedResolver import PubmedResolver
class URI(object):

	GO = 0
	TAXONOMY = 1
	BIOMODELS = 2
	PUBMED = 3
	SBO = 4
	GO_bis = 5

	IDENTIFIERS = {
		GO: 'http://identifiers.org/go/',
		GO_bis: 'http://identifiers.org/obo.go/',
		TAXONOMY: 'http://identifiers.org/taxonomy/',
		BIOMODELS: 'http://identifiers.org/biomodels.db/',
		PUBMED: 'http://identifiers.org/pubmed/',
		SBO: 'http://biomodels.net/SBO/'
	}

	def __init__(self):
		self.__rawURI = None
		self.__identifier = None
		self.__id = None

	def readURI(self, uri):

		self.__rawURI = uri
		tokens = self.__rawURI.split("/")
		self.__id = tokens[-1]
		start_token = self.__rawURI.replace(self.__id, "")

		for identifier, string in list(self.IDENTIFIERS.items()):
			if start_token.startswith(string):
				self.__identifier = identifier

		if self.__identifier is None:
			self.__id = None

	def writeURI(self):
		if self.__id is None and self.__identifier is None:
			return self.__rawURI
		else:
			return self.IDENTIFIERS[self.__identifier] + self.__id

	def __str__(self):

		if self.__rawURI is not None:
			return self.__rawURI
		else:
			return ""

	def __eq__(self, uri):

		if self.__id is not None and self.__identifier is not None:
			return self.__identifier == uri.getIdentifier() and self.__id == uri.getId()
		else:
			return self.__rawURI == uri.getRawURI()

	def getId(self):
		return self.__id
	def getIdentifier(self):
		return self.__identifier
	def getRawURI(self):
		return self.__rawURI

	def setGO(self, go_id):
		self.__identifier = self.GO
		self.__id = go_id

	def isGO(self):
		return self.__identifier == self.GO or self.__identifier == self.GO_bis


	def setBiomodels(self, biomodels_id):
		self.__identifier = self.BIOMODELS
		self.__id = biomodels_id

	def isBiomodels(self):
		return self.__identifier == self.BIOMODELS


	def setTaxonomy(self, taxonomy_id):
		self.__identifier = self.TAXONOMY
		self.__id = taxonomy_id

	def isTaxonomy(self):
		return self.__identifier == self.TAXONOMY


	def setPubmed(self, pubmed_id):
		self.__identifier = self.PUBMED
		self.__id = pubmed_id

	def isPubmed(self):
		return self.__identifier == self.PUBMED

	def setSBO(self, sbo_id):
		self.__identifier = self.SBO
		self.__id = "SBO_%.7d" % sbo_id

	def isSBO(self):
		return self.__identifier == self.SBO

	def getName(self):

		resolver = None

		if self.isTaxonomy():
			resolver = NCBITaxonomyResolver(self.__id)
		elif self.isGO():
			resolver = GoResolver(self.__id)
		elif self.isSBO():
			resolver = SBOResolver(self.__id)
		elif self.isPubmed():
			resolver = PubmedResolver(self.__id)

		try:
			resolver.lookup()
		except:
			return ""
		return resolver.getName()
