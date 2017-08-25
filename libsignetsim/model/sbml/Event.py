#!/usr/bin/env python
""" Event.py


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


from libsignetsim.model.sbml.HasId import HasId
from libsignetsim.model.sbml.SbmlObject import SbmlObject

from libsignetsim.model.sbml.EventAssignment import EventAssignment
from libsignetsim.model.sbml.EventTrigger import EventTrigger
from libsignetsim.model.sbml.EventDelay import EventDelay
from libsignetsim.model.sbml.EventPriority import EventPriority

from libsignetsim.settings.Settings import Settings

class Event(HasId, SbmlObject):
	""" Events definition """

	def __init__ (self, model, obj_id):

		self.__model = model
		self.objId = obj_id

		HasId.__init__(self, model)
		SbmlObject.__init__(self, model)

		self.trigger = EventTrigger(model)
		self.listOfEventAssignments = []

		self.delay = None
		self.priority = None
		self.useValuesFromTriggerTime = True


	def readSbml(self, sbml_event,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads an event definition from a sbml file """

		HasId.readSbml(self, sbml_event, sbml_level, sbml_version)
		SbmlObject.readSbml(self, sbml_event, sbml_level, sbml_version)

		if sbml_event.getTrigger() is not None:
			self.trigger.readSbml(sbml_event.getTrigger(), sbml_level, sbml_version)
		else:
			self.trigger = None

		if sbml_event.isSetDelay():
			self.delay = EventDelay(self.__model)
			self.delay.readSbml(sbml_event.getDelay(), sbml_level, sbml_version)

		if sbml_event.isSetPriority():
			self.priority = EventPriority(self.__model)
			self.priority.readSbml(sbml_event.getPriority(), sbml_level, sbml_version)

		if sbml_event.isSetUseValuesFromTriggerTime():
			self.useValuesFromTriggerTime = sbml_event.getUseValuesFromTriggerTime()
		else:
			self.useValuesFromTriggerTime = True

		self.listOfEventAssignments = []
		for event_assignment in sbml_event.getListOfEventAssignments():

			t_event_assignment = EventAssignment(self.__model, len(self.listOfEventAssignments), self)
			t_event_assignment.readSbml(event_assignment, sbml_level, sbml_version)
			self.listOfEventAssignments.append(t_event_assignment)


	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes an event definition to a sbml file """

		sbml_event = sbml_model.createEvent()

		HasId.writeSbml(self, sbml_event, sbml_level, sbml_version)
		SbmlObject.writeSbml(self, sbml_event, sbml_level, sbml_version)

		if self.trigger is not None:
			self.trigger.writeSbml(sbml_event, sbml_level, sbml_version)

		if self.delay is not None:
			self.delay.writeSbml(sbml_event, sbml_level, sbml_version)

		if self.priority is not None:
			self.priority.writeSbml(sbml_event, sbml_level, sbml_version)

		for event_assignment in self.listOfEventAssignments:
			event_assignment.writeSbml(sbml_event, sbml_level, sbml_version)

		if sbml_level == 2 and self.useValuesFromTriggerTime == True:
			pass
		else:
			sbml_event.setUseValuesFromTriggerTime(self.useValuesFromTriggerTime)


	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={},
				conversion_factors={}, time_conversion=None):

		HasId.copy(self, obj, sids_subs=sids_subs)
		SbmlObject.copy(self, obj)

		self.trigger.copy(obj.trigger, symbols_subs=symbols_subs, conversion_factors=conversion_factors)

		if obj.delay is not None and obj.delay not in deletions:
			self.delay = EventDelay(self.__model)
			self.delay.copy(obj.delay, symbols_subs=symbols_subs, conversion_factors=conversion_factors, time_conversion=time_conversion)

		if obj.priority is not None and obj.priority not in deletions:
			self.priority = EventPriority(self.__model)
			self.priority.copy(obj.priority, symbols_subs=symbols_subs, conversion_factors=conversion_factors)

		for event_assignment in obj.listOfEventAssignments:
			if event_assignment not in deletions:
				t_event_assignment = EventAssignment(self.__model, len(self.listOfEventAssignments), self)
				t_event_assignment.copy(
					event_assignment,
					sids_subs=sids_subs,
					symbols_subs=symbols_subs,
					conversion_factors=conversion_factors,
					time_conversion=time_conversion
				)
				self.listOfEventAssignments.append(t_event_assignment)

		self.useValuesFromTriggerTime = obj.useValuesFromTriggerTime



	def setTrigger(self, trigger):

		if self.trigger is None:
			self.trigger = EventTrigger(self.__model)

		self.trigger.setPrettyPrintMathFormula(trigger)

	def getTrigger(self):

		if self.trigger is not None:
			return self.trigger.getPrettyPrintMathFormula()

	def getTriggerMath(self):

		return self.trigger

	def getTriggerInitialValue(self):

		return self.trigger.initialValue

	def setTriggerInitialValue(self, value):

		self.trigger.initialValue = value

	def getUseValuesFromTriggerTime(self):

		return self.useValuesFromTriggerTime

	def setUseValuesFromTriggerTime(self, value):

		self.useValuesFromTriggerTime = value

	def isTriggerPersistent(self):

		return self.trigger.isPersistent

	def setTriggerPersistent(self, value):

		self.trigger.isPersistent = value


	def setDelay(self, delay):

		if delay is not None:

			if self.delay is None:
				self.delay = MathFormula(self.__model)
			self.delay.setPrettyPrintMathFormula(delay)

		else:
			self.delay = delay

	def getDelay(self):

		if self.delay is not None:
			return self.delay.getPrettyPrintMathFormula()

	def getDelayMath(self):

		return self.delay

	def setPriority(self, priority):

		if priority is not None:

			if self.priority is None:
				self.priority = MathFormula(self.__model)
			self.priority.setPrettyPrintMathFormula(priority)

		else:
			self.priority = priority


	def getPriority(self):

		if self.priority is not None:
			return self.priority.getPrettyPrintMathFormula()

	def getPriorityMath(self):

		return self.priority

	def addEventAssignment(self, variable=None, definition=None):

		t_assignment = EventAssignment(self.__model, len(self.listOfEventAssignments), self)
		self.listOfEventAssignments.append(t_assignment)
		if variable is not None and definition is not None:
			t_assignment.setVariable(variable)
			t_assignment.setPrettyPrintAssignment(definition)
		return t_assignment

	def renameSbmlId(self, old_sbml_id, new_sbml_id):

		self.trigger.renameSbmlId(old_sbml_id, new_sbml_id)

		for event_assignment in self.listOfEventAssignments:
			event_assignment.renameSbmlId(old_sbml_id, new_sbml_id)

		if self.delay is not None:
			self.delay.renameSbmlId(old_sbml_id, new_sbml_id)

		if self.priority is not None:
			self.priority.renameSbmlId(old_sbml_id, new_sbml_id)

	def memorySize(self):

		size = 0
		if self.useValuesFromTriggerTime:
			size += len(self.listOfEventAssignments)
		return size

	def isValid(self):

		return self.trigger is not None and len([ass for ass in self.listOfEventAssignments if ass.getDefinition() is None]) == 0