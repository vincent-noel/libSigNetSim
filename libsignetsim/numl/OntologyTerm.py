#!/usr/bin/env python
""" OntologyTerm.py


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

class OntologyTerm (object):

	def __init__(self, document):

		self.__document = document
		self.__id = None
		self.__term = None
		self.__sourceTermId = None
		self.__ontologyURI = None

	def readNuML(self, ontology_term, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		self.__id = ontology_term.getId()
		self.__term = ontology_term.getTerm()
		self.__sourceTermId = ontology_term.getSourceTermId()
		self.__ontologyURI = ontology_term.getOntologyURI()

	def writeNuML(self, ontology_term, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		ontology_term.setId(self.__id)
		ontology_term.setTerm(self.__term)
		ontology_term.setSourceTermId(self.__sourceTermId)
		ontology_term.setOntologyURI(self.__ontologyURI)

	def getTerm(self):
		return self.__term

	def getId(self):
		return self.__id

	def setId(self, ontology_term_id):
		self.__id = ontology_term_id

	def defineAsTime(self):
		self.__term = "time"
		self.__sourceTermId = "SBO:0000345"
		self.__ontologyURI = "http://www.ebi.ac.uk/sbo/"

	def defineAsConcentration(self):
		self.__term = "concentration"
		self.__sourceTermId = "SBO:0000196"
		self.__ontologyURI = "http://www.ebi.ac.uk/sbo/"
