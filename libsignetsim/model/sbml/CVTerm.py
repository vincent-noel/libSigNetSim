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



from libsignetsim.uris.URI import URI
from libsignetsim.settings.Settings import Settings
from libsbml import (
	MODEL_QUALIFIER, BIOLOGICAL_QUALIFIER, BQB_ENCODES, BQB_HAS_PART, BQB_HAS_PROPERTY, BQB_HAS_TAXON, BQB_HAS_VERSION,
	BQB_IS, BQB_IS_DESCRIBED_BY, BQB_IS_ENCODED_BY, BQB_IS_HOMOLOG_TO, BQB_IS_PART_OF, BQB_IS_PROPERTY_OF,
	BQB_IS_VERSION_OF, BQB_OCCURS_IN, BQB_UNKNOWN, BQM_HAS_INSTANCE, BQM_IS, BQM_IS_DERIVED_FROM, BQM_IS_DESCRIBED_BY,
	BQM_IS_INSTANCE_OF, BQM_UNKNOWN
)

class CVTerm(object):

	biological_qualifiers = {
		BQB_ENCODES: "encodes",
		BQB_HAS_PART: "hasPart",
		BQB_HAS_PROPERTY: "hasProperty",
		BQB_HAS_TAXON: "hasTaxon",
		BQB_HAS_VERSION: "hasVersion",
		BQB_IS: "is",
		BQB_IS_DESCRIBED_BY: "isDescribedBy",
		BQB_IS_ENCODED_BY: "isEncodedBy",
		BQB_IS_HOMOLOG_TO: "isHomologTo",
		BQB_IS_PART_OF: "isPartOf",
		BQB_IS_PROPERTY_OF: "isPropertyOf",
		BQB_IS_VERSION_OF: "isVersionOf",
		BQB_OCCURS_IN: "occursIn",
		BQB_UNKNOWN: "unknown",
	}
	model_qualifiers = {
		BQM_HAS_INSTANCE: "hasInstance",
		BQM_IS: "is",
		BQM_IS_DERIVED_FROM: "isDerivedFrom",
		BQM_IS_DESCRIBED_BY: "isDescribedBy",
		BQM_IS_INSTANCE_OF: "isInstanceOf",
		BQM_UNKNOWN: "unknown"
	}

	def __init__(self, model):

		self.__model = model
		self.__qualifierType = None
		self.__qualifier = None
		self.__resources = []


	def readSbml(self, cv_term,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		self.__qualifierType = cv_term.getQualifierType()

		if self.__qualifierType == MODEL_QUALIFIER:
			self.__qualifier = cv_term.getModelQualifierType()
		elif self.__qualifierType == BIOLOGICAL_QUALIFIER:
			self.__qualifier = cv_term.getBiologicalQualifierType()

		for i_res in range(cv_term.getResources().getNumAttributes()):
			t_uri = URI()
			t_uri.readURI(cv_term.getResourceURI(i_res))
			self.__resources.append(t_uri)

	def writeSbml(self, cv_term,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):


		if self.__qualifierType == MODEL_QUALIFIER:

			cv_term.setQualifierType(self.__qualifierType)
			cv_term.setModelQualifierType(self.__qualifier)
			for uri in self.__resources:
				cv_term.addResource(uri.writeURI())

		elif self.__qualifierType == BIOLOGICAL_QUALIFIER:
			cv_term.setQualifierType(self.__qualifierType)
			cv_term.setBiologicalQualifierType(self.__qualifier)
			for uri in self.__resources:
				cv_term.addResource(str(uri.writeURI()))

	def __str__(self):

		res = ""
		if self.__qualifierType == MODEL_QUALIFIER:
			res += ">> Model qualifier\n"
			for uri in self.__resources:
				res += ">>> %s : %s\n" % (self.model_qualifiers[self.__qualifier], self(uri))

		elif self.__qualifierType == BIOLOGICAL_QUALIFIER:
			res += ">> Biological\n"
			for uri in self.__resources:
				res += ">>> %s : %s\n" % (self.biological_qualifiers[self.__qualifier], self(uri))

		return res

	def getURIs(self):
		return self.__resources

	def addURI(self, uri):
		self.__resources.append(uri)

	def isHasPart(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_HAS_PART

	def isHasProperty(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_HAS_PROPERTY

	def isHasTaxon(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_HAS_TAXON

	def isHasVersion(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_HAS_VERSION

	def isIs(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_IS

	def isIsDescribedBy(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_IS_DESCRIBED_BY

	def setIsDescribedBy(self):

		self.__qualifierType = BIOLOGICAL_QUALIFIER
		self.__qualifier = BQB_IS_DESCRIBED_BY

	def isIsEncodedBy(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_IS_ENCODED_BY

	def isIsHomologTo(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_IS_HOMOLOG_TO

	def isIsPartOf(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_IS_PART_OF

	def isIsPropertyOf(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_IS_PROPERTY_OF

	def isIsVersionOf(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_IS_VERSION_OF

	def isOccursIn(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_OCCURS_IN

	def isUnknown(self):
		return self.__qualifierType == BIOLOGICAL_QUALIFIER and list(self.biological_qualifiers.keys())[self.__qualifier] == BQB_UNKNOWN

	def isModelHasInstance(self):
		return self.__qualifierType == MODEL_QUALIFIER and list(self.model_qualifiers.keys())[self.__qualifier] == BQM_HAS_INSTANCE

	def isModelIs(self):
		return self.__qualifierType == MODEL_QUALIFIER and list(self.model_qualifiers.keys())[self.__qualifier] == BQM_IS

	def isModelIsDerivedFrom(self):
		return self.__qualifierType == MODEL_QUALIFIER and list(self.model_qualifiers.keys())[self.__qualifier] == BQM_IS_DERIVED_FROM

	def isModelIsDescribedBy(self):
		return self.__qualifierType == MODEL_QUALIFIER and list(self.model_qualifiers.keys())[self.__qualifier] == BQM_IS_DESCRIBED_BY

	def isModelIsInstanceOf(self):
		return self.__qualifierType == MODEL_QUALIFIER and list(self.model_qualifiers.keys())[self.__qualifier] == BQM_IS_INSTANCE_OF

	def isModelUnknown(self):
		return self.__qualifierType == MODEL_QUALIFIER and list(self.model_qualifiers.keys())[self.__qualifier] == BQM_UNKNOWN