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

from libsignetsim.sedml.Change import Change
from libsignetsim.sedml.NewXML import NewXML
from libsignetsim.settings.Settings import Settings
from lxml import etree


class AddXML(Change):

	def __init__(self, document):

		Change.__init__(self, document)
		self.__document = document
		self.__newXML = NewXML(document)

	def readSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		Change.readSedml(self, change, level, version)
		self.__newXML.readSedml(change.getNewXML(), level, version)

	def writeSedml(self, change, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):
		Change.writeSedml(self, change, level, version)
		change.setNewXML(self.__newXML.writeSedml(level, version))

	def setNewXMLFromString(self, xml_string):
		self.__newXML.setFromString(xml_string)

	def applyChange(self, sbml_tree):

		namespace = {etree.QName(sbml_tree).localname: etree.QName(sbml_tree).namespace}

		if len(sbml_tree.xpath(self.getTarget().getXPath(), namespaces=namespace)) == 0:
			grand_parent = sbml_tree.xpath(self.getTarget().getParentXPath(), namespaces=namespace)[0]
			parent = etree.Element(self.getTarget().getElementTag())
			grand_parent.append(parent)
			new_child = etree.fromstring(self.__newXML.getAsString())
			parent.append(new_child)

		else:
			new_child = etree.fromstring(self.__newXML.getAsString())
			parent = sbml_tree.xpath(self.getTarget().getXPath(), namespaces=namespace)[0]
			parent.append(new_child)
