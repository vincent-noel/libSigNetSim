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


import libsbml

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.CVTerm import CVTerm
from libsignetsim.uris.URI import URI
from libsbml import CVTerm as LibsbmlCVTerm
from libsbml import SBO


class SbmlAnnotation(object):


	def __init__(self, model):

		self.__model = model
		self.__cvTerms = []
		self.__sboTerm = None
		self.__sboURI = None

	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		if sbml_object.getCVTerms() is not None:

			for cvterm in sbml_object.getCVTerms():
				t_cvterm = CVTerm(self.__model)
				t_cvterm.readSbml(cvterm, sbml_level, sbml_version)
				self.__cvTerms.append(t_cvterm)

		if sbml_object.isSetSBOTerm():
			self.__sboTerm = int(sbml_object.getSBOTerm())
			self.__sboURI = URI()
			self.__sboURI.setSBO(self.__sboTerm)


	def writeSbml(self, sbml_object, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if self.__sboTerm is not None:
			sbml_object.setSBOTerm(str(self.__sboTerm))

		for cv_term in self.__cvTerms:
			t_cvterm = LibsbmlCVTerm()
			cv_term.writeSbml(t_cvterm, sbml_level, sbml_version)
			sbml_object.addCVTerm(t_cvterm)

	def getSBOTerm(self):
		return self.__sboTerm

	def getSBOTermDescription(self):
		if self.__sboURI is not None:
			return self.__sboURI.getName()
		elif self.__sboTerm is not None:
			self.__sboURI = URI()
			self.__sboURI.setSBO(self.__sboTerm)
			return self.__sboURI.getName()

	def setSBOTerm(self, sbo_term):
		self.__sboTerm = sbo_term

	def getCVTerms(self):
		return self.__cvTerms


	def getHasTaxon(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isHasTaxon():
				res += cv_term.getURIs()
		return res

	def getHasPart(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isHasPart():
				res += cv_term.getURIs()
		return res

	def getHasProperty(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isHasProperty():
				res += cv_term.getURIs()
		return res

	def getHasVersion(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isHasVersion():
				res += cv_term.getURIs()
		return res
	
	def getIs(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIs():
				res += cv_term.getURIs()
		return res

	def getIsDescribedBy(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIsDescribedBy():
				res += cv_term.getURIs()
		return res

	def addIsDesribedBy(self, uri):
		t_cv_term = CVTerm(self.__model)
		t_cv_term.setIsDescribedBy()
		t_cv_term.addURI(uri)
		self.__cvTerms.append(t_cv_term)

	def clearIsDescribedBy(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIsDescribedBy():
				self.__cvTerms.remove(cv_term)

	def getIsEncodedBy(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIsEncodedBy():
				res += cv_term.getURIs()
		return res

	def getIsHomologTo(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIsHomologTo():
				res += cv_term.getURIs()
		return res

	def getIsPartOf(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIsPartOf():
				res += cv_term.getURIs()
		return res

	def getIsPropertyOf(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIsPropertyOf():
				res += cv_term.getURIs()
		return res

	def getIsVersionOf(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isIsVersionOf():
				res += cv_term.getURIs()
		return res

	def getOccursIn(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isOccursIn():
				res += cv_term.getURIs()
		return res

	def getUnknown(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isUnknown():
				res += cv_term.getURIs()
		return res

	def getModelHasInstance(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isModelHasInstance():
				res += cv_term.getURIs()
		return res

	def getModelIs(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isModelIs():
				res += cv_term.getURIs()
		return res

	def getModelIsDerivedFrom(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isModelIsDerivedFrom():
				res += cv_term.getURIs()
		return res

	def getModelIsDescribedBy(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isModelIsDescribedBy():
				res += cv_term.getURIs()
		return res

	def getModelIsInstanceOf(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isModelIsInstanceOf():
				res += cv_term.getURIs()
		return res

	def getModelUnknown(self):
		res = []
		for cv_term in self.__cvTerms:
			if cv_term.isModelUnknown():
				res += cv_term.getURIs()
		return res


