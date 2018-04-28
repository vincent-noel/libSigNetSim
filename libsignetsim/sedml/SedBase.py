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
			self.__annotations = sed_base_object.getAnnotation()

	def writeSedml(self, sed_base_object, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		if self.__metaId is not None:
			sed_base_object.setMetaId(self.__metaId)

		if self.__notes is not None:
			sed_base_object.setNotes(self.__notes)

		if self.__annotations is not None:
			sed_base_object.setAnnotation(self.__annotations)


	def getMetaId(self):
		return self.__metaId

	def getNotes(self):
		return self.__notes

	def setMetaId(self, meta_id):
		self.__metaId = meta_id

	def setNotes(self, notes):
		self.__notes = notes