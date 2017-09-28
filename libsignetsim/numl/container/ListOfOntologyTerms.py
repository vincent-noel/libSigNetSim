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

from libsignetsim.numl.container.ListOf import ListOf
from libsignetsim.numl.OntologyTerm import OntologyTerm
from libsignetsim.settings.Settings import Settings

class ListOfOntologyTerms(ListOf, list):

	def __init__(self, document):

		ListOf.__init__(self, document)
		self.__document = document
		self.__termCounter = 0

	def createOntologyTerm(self):
		ontology_term = OntologyTerm(self.__document)
		ontology_term.setId("term_%d" % self.__termCounter)
		ListOf.append(self, ontology_term)
		self.__termCounter += 1
		return ontology_term

	def readNuML(self, list_of_ontology_terms, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		ListOf.readNuML(self, list_of_ontology_terms, level, version)
		for ontology_term in list_of_ontology_terms:
			t_ontology_term = OntologyTerm(self.__document)
			t_ontology_term.readNuML(ontology_term, level, version)
			ListOf.append(self, t_ontology_term)

	def writeNuML(self, numl_document, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):
		# ListOf.writeNuML(self, numl_document., level, version)

		for ontology_term in self:
			t_ontology_term = numl_document.createOntologyTerm()
			ontology_term.writeNuML(t_ontology_term, level, version)

	def getByOntologyTerm(self, lookup_term):
		for ontology_term in self:
			if ontology_term.getId() == lookup_term:
				return ontology_term