#!/usr/bin/env python
""" SimpleSbmlObject.py


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
from libsignetsim.model.sbml.CVTerm import CVTerm
from libsbml import CVTerm as LibsbmlCVTerm
class SbmlAnnotation(object):


	def __init__(self, model):

		self.__model = model
		self.__cvTerms = []
		self.__sboTerm = None

	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		for cvterm in sbml_object.getCVTerms():
			t_cvterm = CVTerm(self.__model)
			t_cvterm.readSbml(cvterm, sbml_level, sbml_version)
			self.__cvTerms.append(t_cvterm)

		if sbml_object.isSetSBOTerm():
			self.__sboTerm = sbml_object.getSBOTerm()


	def writeSbml(self, sbml_object, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if self.__sboTerm is not None:
			sbml_object.setSBOTerm(self.__sboTerm)

		for cv_term in self.__cvTerms:
			t_cvterm = LibsbmlCVTerm()
			cv_term.writeSbml(t_cvterm, sbml_level, sbml_version)
			sbml_object.addCVTerm(t_cvterm)

	def getSBOTerm(self):
		return self.__sboTerm

	def setSBOTerm(self, sbo_term):
		self.__sboTerm = sbo_term