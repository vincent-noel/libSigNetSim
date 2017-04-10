#!/usr/bin/env python
""" SbmlModelHistory.py


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

from libsignetsim.model.sbml.SbmlModelCreator import SbmlModelCreator
from libsignetsim.settings.Settings import Settings

from libsbml import RDFAnnotationParser, ModelHistory, ModelCreator, Date
import libsbml
class SbmlModelHistory(object):
	""" Sbml model class """


	def __init__ (self, model):
		""" Constructor of model class """

		self.__model = []
		self.__listOfCreators = []
		self.__listOfModifiedDates = []
		self.__createdDate = None

	def addCreator(self, family_name, given_name, email, organisation=None, name=None):

		t_creator = SbmlModelCreator()
		t_creator.new(family_name, given_name, email, organisation, name)
		self.__listOfCreators.append(t_creator)

	def readSbml(self, model, level=Settings.defaultSbmlLevel, version=Settings.defaultSbmlVersion):

		if model.isSetModelHistory():
			history = model.getModelHistory()

			if history.isSetCreatedDate():
				self.__createdDate = history.getCreatedDate().getDateAsString()

			for creator in history.getListCreators():
				t_creator = SbmlModelCreator()
				t_creator.readSbml(creator, level, version)
				self.__listOfCreators.append(t_creator)

			for modified_date in history.getListModifiedDates():
				self.__listOfModifiedDates.append(modified_date.getDateAsString())

	def writeSbml(self, model, level=Settings.defaultSbmlLevel, version=Settings.defaultSbmlVersion):

		if len(self.__listOfCreators) > 0 and len(self.__listOfModifiedDates) > 0 and self.__createdDate is not None:
			history = ModelHistory()

			for creator in self.__listOfCreators:
				t_creator = ModelCreator()
				creator.writeSbml(t_creator, level, version)
				history.addCreator(t_creator)

			if self.__createdDate is not None:
				t_date = Date()
				t_date.setDateAsString(self.__createdDate)
				history.setCreatedDate(t_date)

			for modifiedDate in self.__listOfModifiedDates:
				t_date = Date()
				t_date.setDateAsString(modifiedDate)
				history.addModifiedDate(t_date)

			model.setModelHistory(history)

	def getListOfCreators(self):
		return self.__listOfCreators

	def getDateCreated(self):
		return self.__createdDate

	def getListOfDateModified(self):
		return self.__listOfModifiedDates

	def __str__(self):
		if len(self.__listOfCreators) > 0 and len(self.__listOfModifiedDates) > 0 and self.__createdDate is not None:

			res = ">Creators : \n"
			for creator in self.__listOfCreators:
				res += ">> %s\n" % str(creator)

			res += "\n> Created : %s\n" % self.__createdDate
			res += "> Modified : \n"
			for modified in self.__listOfModifiedDates:
				res += ">> %s\n" % modified

		return res

