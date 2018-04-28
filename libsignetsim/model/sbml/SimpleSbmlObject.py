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



from libsignetsim.model.sbml.SbmlAnnotation import SbmlAnnotation
from libsignetsim.settings.Settings import Settings
from libsbml import SyntaxChecker
from libsbml import XMLNode
from libsignetsim.model.ModelException import CannotCreateException

class SimpleSbmlObject(object):

	def __init__(self, model):

		self.__model = model
		self.__metaId = None
		self.__notes = None
		self.__annotation = SbmlAnnotation(self)
		self.newMetaId()
		self.__model.listOfSbmlObjects.addSbmlObject(self)

	def new(self, notes=None):

		self.__notes = notes

	def copy(self, obj):

		self.__notes = obj.getNotes()
		self.__model.objectsDictionnary.update({obj.getMetaId(): self.getMetaId()})

	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		if sbml_level >= 2:
			if sbml_object.isSetMetaId():
				self.setMetaId(sbml_object.getMetaId(), force=True)

		if sbml_object.isSetNotes():
			t_notes = sbml_object.getNotes().getChild(0)

			self.__notes = ""
			for note in range(t_notes.getNumChildren()):
				self.__notes += t_notes.getChild(note).toXMLString()

		if sbml_object.isSetAnnotation():
			self.__annotation.readSbml(sbml_object, sbml_level, sbml_version)

	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):


		if sbml_level >= 2 and self.__metaId is not None:
			sbml_object.setMetaId(str(self.__metaId))

		if self.__notes is not None and self.__notes != "":
			sbml_object.setNotes(self.buildNotes(self.__notes))

		self.__annotation.writeSbml(sbml_object, sbml_level, sbml_version)

	def newMetaId(self):
		self.__metaId = self.__model.listOfSbmlObjects.nextMetaId()

	def setMetaId(self, meta_id, force=False):

		if meta_id is not None:
			t_meta_id = meta_id

			if SyntaxChecker.isValidXMLID(t_meta_id):

				if self.__model.listOfSbmlObjects.containsMetaId(t_meta_id) and force:
				# Here is a case where we probably choosed a meta id for an object, not knowing that the SBML file
				# already had that meta id reserved for another object. So we need to rename the first one, so that
				# we can keep the meta id of the reserved one.
					t_object = self.__model.listOfSbmlObjects.getByMetaId(t_meta_id)

					t_new_meta_id = self.__model.listOfSbmlObjects.nextMetaId()
					while self.__model.listOfSbmlObjects.containsMetaId(t_new_meta_id):
						t_new_meta_id = self.__model.listOfSbmlObjects.nextMetaId()

					t_object.setMetaId(t_new_meta_id)

					self.__metaId = t_meta_id

				else:
					while self.__model.listOfSbmlObjects.containsMetaId(t_meta_id):
						t_meta_id = self.__model.listOfSbmlObjects.nextMetaId()

					self.__metaId = t_meta_id

			else:
				raise CannotCreateException("MetaId is not valid !!")

	def rawSetMetaId(self, meta_id):
		self.__metaId = meta_id
		
	def unsetMetaId(self):
		self.__metaId = None


	def getMetaId(self):
		return self.__metaId

	def getNotes(self):
		return self.__notes

	def setNotes(self, notes):

		if (notes is not None
			and SyntaxChecker.hasExpectedXHTMLSyntax(self.buildNotes(notes))):
			self.__notes = notes


	def buildNotes(self, string):

		t_string = ("<notes><body xmlns=\"http://www.w3.org/1999/xhtml\">"
						+ string
					+ "</body></notes>")

		return XMLNode.convertStringToXMLNode(t_string)

	def getAnnotation(self):
		return self.__annotation