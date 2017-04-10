#!/usr/bin/env python
""" CVTerm.py


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

			if self.__qualifierType == MODEL_QUALIFIER:
				self.__resources.append(cv_term.getResourceURI(i_res))
			elif self.__qualifierType == BIOLOGICAL_QUALIFIER:
				self.__resources.append(cv_term.getResourceURI(i_res))

	def writeSbml(self, cv_term,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):


		if self.__qualifierType == MODEL_QUALIFIER:

			cv_term.setQualifierType(self.__qualifierType)
			cv_term.setModelQualifierType(self.__qualifier)
			for uri in self.__resources:
				cv_term.addResource(uri)

		elif self.__qualifierType == BIOLOGICAL_QUALIFIER:
			cv_term.setQualifierType(self.__qualifierType)
			cv_term.setBiologicalQualifierType(self.__qualifier)
			for uri in self.__resources:
					cv_term.addResource(uri)

	def __str__(self):

		res = ""
		if self.__qualifierType == MODEL_QUALIFIER:
			res += ">> Model qualifier\n"
			for uri in self.__resources:
				res += ">>> %s : %s\n" % (self.model_qualifiers[self.__qualifier], uri)

		elif self.__qualifierType == BIOLOGICAL_QUALIFIER:
			res += ">> Biological\n"
			for uri in self.__resources:
				res += ">>> %s : %s\n" % (self.biological_qualifiers[self.__qualifier], uri)

		return res