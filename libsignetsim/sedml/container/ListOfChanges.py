#!/usr/bin/env python
""" ListOfChanges.py


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

from libsignetsim.sedml.container.ListOf import ListOf

from libsignetsim.sedml.ChangeAttribute import ChangeAttribute
from libsignetsim.sedml.ComputeChange import ComputeChange

from libsignetsim.settings.Settings import Settings

import libsbml
from libsedml import SEDML_CHANGE_ATTRIBUTE, SEDML_CHANGE_COMPUTECHANGE
reload(libsbml)

class ListOfChanges(ListOf):

	def __init__(self, document):

		ListOf.__init__(self, document)

		self.__document = document

	def readSedml(self, list_of_changes, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.readSedml(self, list_of_changes, level, version)

		for change in list_of_changes:

			if change.getTypeCode() == SEDML_CHANGE_ATTRIBUTE:
				t_change = ChangeAttribute(self.__document)
				t_change.readSedml(change, level, version)
				ListOf.append(self, t_change)

			elif change.getTypeCode() == SEDML_CHANGE_COMPUTECHANGE:
				t_change = ComputeChange(self.__document)
				t_change.readSedml(change, level, version)
				ListOf.append(self, t_change)

	def writeSedml(self, list_of_changes, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		ListOf.writeSedml(self, list_of_changes, level, version)

		for change in self:
			if isinstance(change, ChangeAttribute):
				t_change = list_of_changes.createChangeAttribute()
				t_change.writeSedml(change, level, version)

			elif isinstance(change, ComputeChange):
				t_change = list_of_changes.createComputeChange()
				t_change.writeSedml(change, level, version)