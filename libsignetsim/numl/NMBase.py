#!/usr/bin/env python
""" NMBase.py


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
# import libsbml, libnuml
from libnuml import XMLNode
# reload(libsbml)
class NMBase (object):

	def __init__(self, document):

		self.__document = document
		self.__metaId = None
		self.__annotation = None
		self.__notes = None


	def readNuML(self, object, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		if object.isSetMetaId():
			self.__metaId = object.getMetaId()
		#
		# if object.isSetAnnotation():
		# 	self.__annotation = object.getAnnotation()

		reload(libnuml)
		if object.isSetNotes():
			self.__notes = XMLNode.convertXMLNodeToString(object.getNotes().getChild(0).getChild(0).getChild(0))

	def writeNuML(self, object, level=Settings.defaultNuMLLevel, version=Settings.defaultNuMLVersion):

		if self.__metaId is not None:
			object.setMetaId(self.__metaId)

		# if self.__annotation is not None:
		# 	object.setAnnotation(self.__annotation)

		if self.__notes is not None:
			xml_string = "<notes><body xmlns=\"http://www.w3.org/1999/xhtml\">%s</body></notes>" % self.__notes
			xml_node = XMLNode.convertStringToXMLNode(xml_string)
			object.setNotes(xml_node)


	def getNotes(self):
		return self.__notes

	def setNotes(self, notes=""):
		self.__notes = notes

