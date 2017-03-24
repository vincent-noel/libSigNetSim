#!/usr/bin/env python
""" HasId.py


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

class HasId(object):

	def __init__(self, document):

		self.__document = document
		self.__id = None
		self.__name = None

	def readSedml(self, has_id_object, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if has_id_object.isSetId():
			self.__id = has_id_object.getId()

		if has_id_object.isSetName():
			self.__name = has_id_object.getName()

	def writeSedml(self, has_id_object, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if self.__id is not None:
			has_id_object.setId(self.__id)

		if self.__name is not None:
			has_id_object.setName(self.__name)

	def getId(self):
		return self.__id

	def getName(self):
		return self.__name

	def setId(self, id):
		self.__id = id

	def setName(self, name):
		self.__name = name