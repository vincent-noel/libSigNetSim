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

	This file is the parent class for all objects having refs

"""
from __future__ import print_function


from libsignetsim.settings.Settings import Settings
from libsignetsim.model.sbml.HasSBaseRef import HasSBaseRef

class HasRef(object):

	def __init__(self, model):

		self.__model = model

		self.__portRef = None
		self.__idRef = None
		self.__unitRef = None
		self.__metaIdRef = None
		self.__SBaseRef = None


	def readSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		if sbml_object.isSetIdRef():
			self.__idRef = sbml_object.getIdRef()

		if sbml_object.isSetPortRef():
			self.__portRef = sbml_object.getPortRef()

		if sbml_object.isSetUnitRef():
			self.__unitRef = sbml_object.getUnitRef()

		if sbml_object.isSetMetaIdRef():
			self.__metaIdRef = sbml_object.getMetaIdRef()

		if sbml_object.isSetSBaseRef():
			self.__SBaseRef = HasSBaseRef(self.__model)
			self.__SBaseRef.readSbml(sbml_object.getSBaseRef(), sbml_level, sbml_version)


	def writeSbml(self, sbml_object,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):

		if self.__portRef is not None:
			sbml_object.setPortRef(self.__portRef)

		if self.__idRef is not None:
			sbml_object.setIdRef(self.__idRef)

		if self.__unitRef is not None:
			sbml_object.setUnitRef(self.__unitRef)

		if self.__metaIdRef is not None:
			sbml_object.setMetaIdRef(self.__metaIdRef)

		if self.__SBaseRef is not None:
			sbml_sbaseref = sbml_object.createSBaseRef()
			self.__SBaseRef.writeSbml(sbml_sbaseref, sbml_level, sbml_version)


	def copy(self, obj, prefix="", shift=0):
		self.setPortRef(obj.getPortRef())
		self.setIdRef(obj.getIdRef(), prefix)
		self.setUnitRef(obj.getUnitRef(), prefix)
		self.setMetaIdRef(obj.getMetaIdRef(), prefix)

	def getRef(self):
		if self.hasIdRef():
			return self.getIdRef()

		elif self.hasPortRef():
			return self.getPortRef()

		elif self.hasMetaIdRef():
			return self.getMetaIdRef()

	def getRefMetaId(self):

		if self.hasIdRef():
			return self.__model.listOfVariables.getBySbmlId(self.getIdRef()).getMetaId()

		elif self.hasPortRef():
			return self.__model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject().getMetaId()

		elif self.hasMetaIdRef():
			return self.__model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef()).getMetaId()

	def getRefObject(self):

		if self.hasIdRef():

			if self.hasSBaseRef():
				print(self.getSBaseRef().getRef())

			if self.__model.listOfVariables.containsSbmlId(self.getIdRef()):
				return self.__model.listOfVariables.getBySbmlId(self.getIdRef())

			elif self.__model.listOfEvents.containsSbmlId(self.getIdRef()):
				return self.__model.listOfEvents.getBySbmlId(self.getIdRef())

		elif self.hasPortRef():
			return self.__model.listOfPorts.getBySbmlId(self.getPortRef()).getRefObject()

		elif self.hasMetaIdRef():
			return self.__model.listOfSbmlObjects.getByMetaId(self.getMetaIdRef())

	def HasRef(self):
		return self.hasIdRef() or self.hasPortRef() or self.hasMetaIdRef()

	def hasPortRef(self):
		return self.__portRef is not None

	def getPortRef(self):
		return self.__portRef

	def setPortRef(self, port_ref):
		self.__portRef = port_ref


	def hasIdRef(self):
		return self.__idRef is not None

	def getIdRef(self):
		return self.__idRef

	def setIdRef(self, id_ref, prefix=""):
		if id_ref is not None:
			self.__idRef = prefix + id_ref


	def hasUnitRef(self):
		return self.__unitRef is not None

	def getUnitRef(self):
		return self.__unitRef

	def setUnitRef(self, unit_ref, prefix=""):
		if unit_ref is not None:
			self.__unitRef = prefix + unit_ref


	def hasMetaIdRef(self):
		return self.__metaIdRef is not None

	def getMetaIdRef(self):
		return self.__metaIdRef

	def setMetaIdRef(self, meta_id_ref, prefix=""):
		if meta_id_ref is not None:
			self.__metaIdRef = prefix + meta_id_ref

	def hasSBaseRef(self):
		return self.__SBaseRef is not None

	def getSBaseRef(self):
		return self.__SBaseRef

	def setSBaseRef(self, sbase_ref, prefix=""):
		if sbase_ref is not None:
			self.__SBaseRef = prefix + sbase_ref
