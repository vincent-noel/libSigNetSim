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

	Retryiving Pubmed URI informations

"""


import requests
from json import loads

class PubmedResolver(object):

	URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=%s"
	URL_ABSTRACTS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=text&rettype=abstract&id=%s"

	def __init__(self, pubmed_id):
		self.__id = pubmed_id
		self.__json = None
		self.__text_abstract = None
		self.__name = None
		self.__definition = None

	def lookup(self):

		if self.__id is not None:
			# self.getJSON()
			# self.parseJSON()
			self.getRawAbstract()
			self.parseRawAbstract()

	def getJSON(self):

		r = requests.get(self.URL % self.__id, headers={"Content-Type": "application/json"})

		if r.ok:
			self.__json = loads(r.content.decode('utf-8'))
			print(self.__json)
			self.__json = self.__json[u'result'][str(self.__id)]

	def parseJSON(self):

		if self.__json is not None:

			self.__name = (self.__json[u'sortfirstauthor']
						   + ', '
						   + self.__json[u'sorttitle']
						   + ", "
						   + self.__json[u'fulljournalname']
						   + ", "
						   + self.__json[u'pubdate'])

			self.__definition = self.__json[u'sortfirstauthor']

	def getRawAbstract(self):

		r = requests.get(self.URL_ABSTRACTS % self.__id, headers={"Content-Type": "application/json"})

		if r.ok:
			self.__text_abstract = r.content.decode('utf-8')

	def parseRawAbstract(self):

		lines = self.__text_abstract.strip().split("\n\n")
		self.__name = (
			lines[2].replace('\n', ' ').replace('\r', '')
			+ ", " + lines[1].replace('\n', ' ').replace('\r', '')
			+ ", " + lines[0].replace('\n', ' ').replace('\r', '')
		)
		self.__definition = lines[-2].replace('\n', ' ').replace('\r', '')

	def getName(self):
		return self.__name

	def getDefinition(self):
		return self.__definition