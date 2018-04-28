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

	Retryiving GO URI informations

"""


import requests
from json import loads
from lxml import etree

class GoResolver(object):


	# URL = "https://www.ebi.ac.uk/QuickGO-Old/GTerm?id=%s&format=oboxml"
	URL = "http://amigo.geneontology.org/amigo/term/%s/json"
	def __init__(self, go_id):
		self.__id = go_id
		self.__xmlTree = None
		self.__json = None
		self.__name = None
		self.__definition = None

	def lookup(self):

		if self.__id is not None:
			self.getJSON()
			self.parseJSON()

	def getJSON(self):

		r = requests.get(self.URL % self.__id, headers={"Content-Type": "application/json"})
		if r.ok:
			self.__json = loads(r.content.decode('utf-8'))

	def parseJSON(self):

		if self.__json is not None:
			self.__name = self.__json[u'results'][u'name']
			self.__definition = self.__json[u'results'][u'definition']

	# def getXMLTree(self):
	#
	# 	r = requests.get(self.URL % self.__id, headers={"Content-Type": "application/xml"})
	# 	if r.ok:
	# 		self.__xmlTree = etree.fromstring(r.content)
	#
	# def parseXMLTree(self):
	#
	# 	term = self.__xmlTree.find("term")
	# 	self.__name = term.find("name").text
	# 	self.__definition = term.find("def").find("defstr").text

	def getName(self):
		return self.__name

	def getDefinition(self):
		return self.__definition