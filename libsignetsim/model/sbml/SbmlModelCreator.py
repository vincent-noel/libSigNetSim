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

class SbmlModelCreator(object):
	""" Sbml model creator class """


	def __init__ (self):
		""" Constructor of model class """

		self.__familyName = None
		self.__givenName = None
		self.__email = None
		self.__organisation = None
		self.__name = None

	def new(self, family_name, given_name, email, organisation=None, name=None):

		self.__familyName = family_name
		self.__givenName = given_name
		self.__email = email
		self.__organisation = organisation
		self.__name = name

	def readSbml(self, creator, level=Settings.defaultSbmlLevel, version=Settings.defaultSbmlVersion):

		if creator.isSetFamilyName():
			self.__familyName = creator.getFamilyName()

		if creator.isSetGivenName():
			self.__givenName = creator.getGivenName()

		if creator.isSetEmail():
			self.__email = creator.getEmail()

		if creator.isSetOrganisation():
			self.__organisation = creator.getOrganisation()

	def writeSbml(self, creator, level=Settings.defaultSbmlLevel, version=Settings.defaultSbmlVersion):

		if self.__familyName is not None:
			creator.setFamilyName(str(self.__familyName))

		if self.__givenName is not None:
			creator.setGivenName(str(self.__givenName))

		if self.__email is not None:
			creator.setEmail(str(self.__email))

		if self.__organisation is not None:
			creator.setOrganisation(str(self.__organisation))

	def getFamilyName(self):
		return self.__familyName

	def getGivenName(self):
		return self.__givenName

	def getEmail(self):
		return self.__email

	def getOrganisation(self):
		return self.__organisation

	def getName(self):
		return self.__name

	def setFamilyName(self, family_name):
		self.__familyName = family_name

	def setGivenName(self, given_name):
		self.__givenName = given_name

	def setEmail(self, email):
		self.__email = email

	def setOrganization(self, organisation):
		self.__organisation = organisation


	def __str__(self):

		return "%s %s (%s)" % (self.__givenName, self.__familyName, self.__email)