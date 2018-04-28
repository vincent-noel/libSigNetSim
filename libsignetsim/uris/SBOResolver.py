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

	Retryiving SBO URI informations

"""


import requests
from json import loads

class SBOResolver(object):

	URL = "https://www.ebi.ac.uk/ols/api/ontologies/sbo/terms?iri=http://biomodels.net/SBO/%s"

	def __init__(self, sbo_id):
		self.__id = sbo_id
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
			self.__name = self.__json[u'_embedded'][u'terms'][0][u'label']
			self.__definition = self.__json[u'_embedded'][u'terms'][0][u'description'][0]

	def getName(self):
		return self.__name

	def getDefinition(self):
		return self.__definition