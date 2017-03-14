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
from libsbml import SyntaxChecker
from libsbml import XMLNode
from libsignetsim.model.ModelException import CannotCreateException

class SimpleSbmlObject(object):

	def __init__(self, model):

		self.__model = model
		self.__metaId = None#self.newMetaId()
		self.__notes = None


	def new(self, notes=None):

		self.newMetaId()
		self.__model.listOfSbmlObjects.addSbmlObject(self)
		self.__notes = notes


	def copy(self, obj, prefix="", shift=0):

		self.setMetaId(obj.getMetaId(), prefix)
		self.__model.listOfSbmlObjects.addSbmlObject(self, prefix)
		self.__notes = obj.getNotes()


	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		if sbml_level >= 2:
			if sbml_object.isSetMetaId():
				self.setMetaId(sbml_object.getMetaId())

		self.__model.listOfSbmlObjects.addSbmlObject(self)

		if sbml_object.isSetNotes():
			t_notes = sbml_object.getNotes().getChild(0)

			self.__notes = ""
			for note in range(t_notes.getNumChildren()):
				self.__notes += t_notes.getChild(note).toXMLString()


	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):


		if sbml_level >= 2 and self.__metaId is not None:
		    sbml_object.setMetaId(str(self.__metaId))

		if self.__notes is not None and self.__notes != "":
			sbml_object.setNotes(self.buildNotes(self.__notes))


	def newMetaId(self):
		self.__metaId = self.__model.listOfSbmlObjects.nextMetaId()


	def setMetaId(self, meta_id, prefix=""):

		if meta_id is not None:
			t_meta_id = prefix + meta_id

			if SyntaxChecker.isValidXMLID(t_meta_id):

				while t_meta_id in self.__model.listOfSbmlObjects.keys():
					t_meta_id = prefix + self.__model.listOfSbmlObjects.nextMetaId()

				if t_meta_id not in self.__model.listOfSbmlObjects.keys():

					if self.__metaId is not None and self.__model.listOfSbmlObjects.containsMetaId(self.__metaId):
						self.__metaId = t_meta_id

						self.__model.listOfSbmlObjects.updateMetaId(self, t_meta_id)

					self.__metaId = t_meta_id
				else:
					raise CannotCreateException("MetaId already exists !!")

			else:
				raise CannotCreateException("MetaId is not valid !!")


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
