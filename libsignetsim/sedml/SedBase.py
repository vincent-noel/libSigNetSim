#!/usr/bin/env python
""" SedBase.py


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

class SedBase(object):

	def __init__(self, document):

		self.__document = document
		self.__metaId = None
		self.__notes = None
		self.__annotations = None

	def readSedml(self, sed_base_object, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if sed_base_object.isSetMetaId():
			self.__metaId = sed_base_object.getMetaId()

		if sed_base_object.isSetNotes():
			self.__notes = sed_base_object.getNotes()

		if sed_base_object.isSetAnnotation():
			self.__annotation = sed_base_object.getAnnotation()

	def getMetaId(self):
		return self.__metaId

	def getNotes(self):
		return self.__notes