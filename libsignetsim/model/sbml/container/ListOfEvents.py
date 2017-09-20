#!/usr/bin/env python
""" ListOfEvents.py


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


from libsignetsim.model.sbml.container.ListOf import ListOf
from libsignetsim.model.sbml.container.HasIds import HasIds
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.ModelException import InvalidXPath
from libsignetsim.model.sbml.Event import Event
from libsignetsim.settings.Settings import Settings

from re import match

class ListOfEvents(ListOf, HasIds, SbmlObject):
	""" Class for the listOfEvents in a sbml model """

	def __init__ (self, model=None):

		self.__model = model
		ListOf.__init__(self, model)
		HasIds.__init__(self, model)
		SbmlObject.__init__(self, model)


	def readSbml(self, sbml_list_of_events,
					sbmlLevel=Settings.defaultSbmlLevel,
					sbmlVersion=Settings.defaultSbmlVersion):
		""" Reads the list of events from a sbml model """

		for sbml_event in sbml_list_of_events:
			event = Event(self.__model, self.nextId())
			event.readSbml(sbml_event, sbmlLevel, sbmlVersion)
			ListOf.add(self, event)

		SbmlObject.readSbml(self, sbml_list_of_events, sbmlLevel, sbmlVersion)

	def writeSbml(self, sbmlModel,
					sbmlLevel=Settings.defaultSbmlLevel,
					sbmlVersion=Settings.defaultSbmlVersion):
		""" Writes the list of events to a sbml model """

		for event in ListOf.values(self):
			event.writeSbml(sbmlModel, sbmlLevel, sbmlVersion)

		if len(ListOf.values(self)):
			SbmlObject.writeSbml(self, sbmlModel.getListOfEvents(), sbmlLevel, sbmlVersion)


	def new(self, name=None):
		event = Event(self.__model, self.nextId())
		event.new(name)
		ListOf.add(self, event)
		# SbmlObject.new(event)
		return event


	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={}, conversion_factors={}, time_conversion=None):

		if obj not in deletions:

			SbmlObject.copy(self, obj)

			for event in obj.values():
				if event not in deletions:

					t_event = Event(self.__model, self.nextId())
					t_event.copy(
						event,
						deletions=deletions,
						sids_subs=sids_subs,
						symbols_subs=symbols_subs,
						conversion_factors=conversion_factors,
						time_conversion=time_conversion
					)
					ListOf.add(self, t_event)

	def withDelay(self):
		return [obj.objId for obj in self.validEvents() if obj.delay is not None]

	def nbRoots(self):

		res = 0
		for event in self.validEvents():
			res += event.trigger.nbRoots()
		return res

	def getRootsOperators(self):
		res = []
		for event in self.validEvents():
			res += event.trigger.getRootsOperator()
		return res

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		for obj in ListOf.values(self):
			obj.renameSbmlId(old_sbml_id, new_sbml_id)

	# Events can have ids, but they are optionals !
	def sbmlIds(self):
		""" Return a set of import ids of the sbml objects """
		return [obj.getSbmlId() for obj in self.values() if obj.getSbmlId() is not None]

	def getBySbmlId(self, sbml_id, pos=0):
		""" Find sbml objects by their import Id """

		res = []
		for obj in self.values():
			if obj.getSbmlId() is not None and obj.getSbmlId() == sbml_id:
				res.append(obj)

		if len(res) > 0:
			return res[pos]
		else:
			return None

	def containsSbmlId(self, sbml_id):
		""" Test if an sbml id is in the list """

		res = False
		for obj in self.values():
			if obj.getSbmlId() is not None and sbml_id == obj.getSbmlId():
				res = True

		return res

	def validEvents(self):

		return [
			event
			for event in self.values()
			if event.isValid()
		]

	def nbValidEvents(self):

		res = 0
		for event in self.values():
			if event.isValid():
				res += 1
		return res

	def resolveXPath(self, selector):

		if not (selector.startswith("event") or selector.startswith("sbml:event")):
			raise InvalidXPath(selector)

		res_match = match(r'(.*)\[@(.*)=(.*)\]', selector)
		if res_match is None:
			raise InvalidXPath(selector)

		tokens = res_match.groups()
		if len(tokens) != 3:
			raise InvalidXPath(selector)

		object = None
		if tokens[1] == "id":
			object = self.getBySbmlId(tokens[2][1:-1])
		elif tokens[1] == "name":
			object = self.getByName(tokens[2][1:-1])
		elif tokens[1] == "metaid":
			object = self.getByMetaId(tokens[2][1:-1])

		if object is not None:
			return object

		# If not returned yet
		raise InvalidXPath(selector)

	def getByXPath(self, xpath):
		return self.resolveXPath(xpath[0]).getByXPath(xpath[1:])

	def setByXPath(self, xpath, object):
		self.resolveXPath(xpath[0]).setByXPath(xpath[1:], object)
