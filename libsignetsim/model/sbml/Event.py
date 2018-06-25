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

from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.sbml.EventAssignment import EventAssignment
from libsignetsim.model.sbml.EventTrigger import EventTrigger
from libsignetsim.model.sbml.EventDelay import EventDelay
from libsignetsim.model.sbml.EventPriority import EventPriority
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.ModelException import InvalidXPath


class Event(Variable, SbmlObject, HasParentObj):

	""" Events definition """

	def __init__ (self, model, parent_obj, obj_id, math_only=False):

		self.__model = model
		self.objId = obj_id

		Variable.__init__(self, model, Variable.EVENT)
		HasParentObj.__init__(self, parent_obj)

		self.trigger = EventTrigger(model, math_only=math_only)
		self.listOfEventAssignments = []

		self.delay = None
		self.priority = None
		self.useValuesFromTriggerTime = True

		# For math submodels, where objects are not sbml objects
		self.mathOnly = math_only
		if not self.mathOnly:
			SbmlObject.__init__(self, model)

	def new(self, name=None):

		Variable.new(self, name, Variable.EVENT)
		SbmlObject.new(self)

	def readSbml(self, sbml_event,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Reads an event definition from a sbml file """

		SbmlObject.readSbml(self, sbml_event, sbml_level, sbml_version)

		if sbml_event.getTrigger() is not None:
			self.trigger.readSbml(sbml_event.getTrigger(), sbml_level, sbml_version)

		Variable.readSbml(self, sbml_event, sbml_level, sbml_version)

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

	def readSbmlVariable(self, variable, sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		# variable id
		self.symbol.readSbml(variable.getId(), sbml_level, sbml_version)

		if self.trigger is not None:
			self.value = MathFormula(self.__model)
			self.value.setInternalMathFormula(self.trigger.getInternalMathFormula())
			self.constant = False
		else:
			self.constant = True

	def writeSbml(self, sbml_model,
					sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		""" Writes an event definition to a sbml file """

		sbml_event = sbml_model.createEvent()

		Variable.writeSbml(self, sbml_event, sbml_level, sbml_version)
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

	def writeSbmlVariable(self, sbml_var, sbml_level=Settings.defaultSbmlLevel,
					sbml_version=Settings.defaultSbmlVersion):
		pass

	def copy(self, obj, deletions=[], sids_subs={}, symbols_subs={},
				conversion_factors={}, time_conversion=None):

		Variable.copy(self, obj, sids_subs=sids_subs, symbols_subs=symbols_subs)

		# if not self.mathOnly:
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

		self.value = MathFormula(self.__model)
		self.value.setInternalMathFormula(self.trigger.getInternalMathFormula())
		self.constant = obj.constant

	def copySubmodel(self, obj):

		self.trigger.copySubmodel(obj.trigger)

		if obj.delay is not None:
			self.delay = EventDelay(self.__model, math_only=self.mathOnly)
			self.delay.copySubmodel(obj.delay)

		if obj.priority is not None:
			self.priority = EventPriority(self.__model, math_only=self.mathOnly)
			self.priority.copySubmodel(obj.priority)

		for event_assignment in obj.listOfEventAssignments:
				t_event_assignment = EventAssignment(self.__model, event_assignment.objId, self, math_only=self.mathOnly)
				t_event_assignment.copySubmodel(event_assignment)
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
		return (
			self.trigger is not None and self.trigger.isValid()
			and len([ass for ass in self.listOfEventAssignments if ass.isValid()]) > 0
		)

	def getByXPath(self, xpath):

		if len(xpath) == 0:
			return self

		if len(xpath) > 1:
			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@value":
			return self.getValue()

		elif xpath[0] == "@name":
			return self.getName()

		elif xpath[0] == "@id":
			return self.getSbmlId()


	def getXPath(self, attribute=None):

		xpath = "sbml:event"
		if self.__model.sbmlLevel == 1:
			xpath += "[@name='%s']" % self.getSbmlId()
		else:
			xpath += "[@id='%s']" % self.getSbmlId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])