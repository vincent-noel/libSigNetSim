#!/usr/bin/env python
""" Parameter.py


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


from libsignetsim.model.sbmlobject.EventAssignedVariable import EventAssignedVariable
from libsignetsim.model.sbmlobject.InitiallyAssignedVariable import InitiallyAssignedVariable
from libsignetsim.model.sbmlobject.RuledVariable import RuledVariable
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbmlobject.SbmlObject import SbmlObject
from libsignetsim.model.sbmlobject.HasUnits import HasUnits
from libsignetsim.settings.Settings import Settings
from copy import copy

class Parameter(Variable, SbmlObject, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable,
						HasUnits):
	#
	# BACKWARD = 0
	# FORWARD = 1
	# CATALYSIS = 2
	# MICHAELIS = 3
	#

	def __init__ (self, model, obj_id, name=None,
					local_parameter=False, reaction=None):

		SbmlObject.__init__(self, model)
		InitiallyAssignedVariable.__init__(self, model)
		RuledVariable.__init__(self, model)
		EventAssignedVariable.__init__(self, model)
		HasUnits.__init__(self, model)

		self.model = model
		self.objId = obj_id

		self.localParameter = local_parameter
		self.reaction = reaction

		if self.localParameter:
			Variable.__init__(self, model, Variable.PARAMETER, self.reaction)
		else:
			Variable.__init__(self, model, Variable.PARAMETER)



	def copy(self, parameter, prefix="", shift=0, subs={}, deletions=[], replacements={}, conversion_factor=None):

		#
		# self.localParameter = parameter.localParameter
		# self.reaction = parameter.reaction


		SbmlObject.copy(self, parameter, prefix, shift)
		InitiallyAssignedVariable.copy(self, parameter, prefix, shift)
		EventAssignedVariable.copy(self, parameter, prefix, shift)
		RuledVariable.copy(self, parameter, prefix, shift)
		HasUnits.copy(self, parameter, prefix, shift)
		Variable.copy(self, parameter, prefix, shift, subs, deletions, replacements, conversion_factor)


	def new(self, name, value=1, constant=True, unit=None):

		""" Creates new compartment with default options """

		SbmlObject.new(self)
		Variable.new(self, name, Variable.PARAMETER)
		HasUnits.new(self, unit)

		self.setValue(value)
		self.constant = constant


	def getReactionId(self):

		if self.localParameter:
			return self.reaction.objId
		else:
			return None

	def readSbml(self, sbml_parameter, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Reads a parameter from a sbml file """

		Variable.readSbml(self, sbml_parameter, sbml_level, sbml_version)
		SbmlObject.readSbml(self, sbml_parameter, sbml_level, sbml_version)
		HasUnits.readSbml(self, sbml_parameter, sbml_level, sbml_version)


	def readSbmlVariable(self, sbml_parameter, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if self.localParameter:
			self.symbol.readSbml("_local_%d_%s" % (self.reaction.objId, sbml_parameter.getId()), sbml_level, sbml_version)
		else:
			self.symbol.readSbml(sbml_parameter.getId(), sbml_level, sbml_version)

		if sbml_parameter.isSetValue():
			self.isInitialized = True
			self.value.readSbml(sbml_parameter.getValue(), sbml_level, sbml_version)

		if sbml_parameter.isSetConstant():
			self.constant = sbml_parameter.getConstant()
		elif sbml_level == 2:
			self.constant = True
		elif sbml_level == 1:
			self.constant = False

		if self.localParameter:
			self.constant = True

	def writeSbml(self, sbml_model, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):
		""" Writes a parameter to  a sbml file """

		sbml_param = sbml_model.createParameter()

		SbmlObject.writeSbml(self, sbml_param, sbml_level, sbml_version)
		Variable.writeSbml(self, sbml_param, sbml_level, sbml_version)
		HasUnits.writeSbml(self, sbml_param, sbml_level, sbml_version)


	def writeSbmlVariable(self, sbml_param, sbml_level=Settings.defaultSbmlLevel, sbml_version=Settings.defaultSbmlVersion):

		if self.isInitialized:
			sbml_param.setValue(self.getValue())

		if self.constant is not None and (sbml_level == 3 or (sbml_level == 2 and not self.constant)):
			sbml_param.setConstant(self.constant)


	def setLocalParameter(self, choice):
		""" Switches the local property of the parameter """
		self.localParameter = choice


	def isLocalParameter(self):
		""" Tests the local property of the parameter """
		return self.localParameter

	#
	# def getNameOrSbmlId(self):
	#
	#     # If there is no name, we need to return the sbmlId
	#     if SbmlObject.getName(self) is None:
	#         return Variable.getSbmlId(self)
	#     else:
	#         return SbmlObject.getName(self)
