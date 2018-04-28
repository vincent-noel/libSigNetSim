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

from libsignetsim.model.sbml.EventAssignedVariable import EventAssignedVariable
from libsignetsim.model.sbml.InitiallyAssignedVariable import InitiallyAssignedVariable
from libsignetsim.model.sbml.RuledVariable import RuledVariable
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.HasUnits import HasUnits
from libsignetsim.model.sbml.HasParentObj import HasParentObj
from libsignetsim.model.ModelException import InvalidXPath, SbmlException
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger
from re import match


class Parameter(Variable, SbmlObject, InitiallyAssignedVariable,
						RuledVariable, EventAssignedVariable,
						HasUnits, HasParentObj):
	#
	# BACKWARD = 0
	# FORWARD = 1
	# CATALYSIS = 2
	# MICHAELIS = 3
	#

	def __init__(self, model, parent_obj, obj_id, name=None,
					local_parameter=False, reaction=None):

		SbmlObject.__init__(self, model)
		InitiallyAssignedVariable.__init__(self, model)
		RuledVariable.__init__(self, model)
		EventAssignedVariable.__init__(self, model)
		HasUnits.__init__(self, model)
		HasParentObj.__init__(self, parent_obj)

		self.__model = model
		self.objId = obj_id

		self.localParameter = local_parameter
		self.reaction = reaction

		if self.localParameter:
			Variable.__init__(self, model, Variable.PARAMETER, self.reaction)
		else:
			Variable.__init__(self, model, Variable.PARAMETER)



	def copy(self, parameter, sids_subs={}, symbols_subs={}, usids_subs={}, conversion_factor=None):

		SbmlObject.copy(self, parameter)
		HasUnits.copy(self, parameter, usids_subs=usids_subs)
		Variable.copy(self, parameter, sids_subs=sids_subs, symbols_subs=symbols_subs, conversion_factor=conversion_factor)

		if self.localParameter:
			self.symbol.setInternalMathFormula(
				SympySymbol("_local_%d_%s" % (self.reaction.objId, self.getSbmlId())))


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
		else:
			self.value.setInternalMathFormula(SympyInteger(1))
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

	def toGlobal(self):

		symbol = str(self.symbol.getInternalMathFormula())
		pattern = "_local_%d_(.*)" % self.reaction.objId
		res_match = match(pattern, symbol)

		if res_match is None:
			raise SbmlException("Is the parameter really global ?")

		new_symbol = res_match.groups()[0]
		self.symbol.renameSbmlId(symbol, new_symbol)
		self.__model.renameSbmlId(symbol, new_symbol)

		self.reaction.listOfLocalParameters.remove(self, full_remove=False)
		self.__model.listOfParameters.append(self)
		self.localParameter = False
		self.reaction = None

	def toLocal(self, reaction):

		symbol = str(self.symbol.getInternalMathFormula())
		new_symbol = "_local_%d_%s" % (reaction.objId, symbol)
		self.symbol.renameSbmlId(symbol, new_symbol)

		self.__model.listOfParameters.remove(self, full_remove=False)
		reaction.listOfLocalParameters.add(self)

		self.__model.renameSbmlId(symbol, new_symbol)

		self.localParameter = True
		self.reaction = reaction

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


	def setByXPath(self, xpath, object):

		if len(xpath) == 0:
			return InvalidXPath("/".join(xpath))

		if len(xpath) > 1:
			return InvalidXPath("/".join(xpath))

		if xpath[0] == "@value":
			return self.setValue(object)

		elif xpath[0] == "@name":
			return self.setName(object)

		elif xpath[0] == "@id":
			return self.setSbmlId(object)


	def getXPath(self, attribute=None):

		xpath = "sbml:parameter"
		if self.__model.sbmlLevel == 1:
			xpath += "[@name='%s']" % self.getSbmlId()
		else:
			xpath += "[@id='%s']" % self.getSbmlId()

		if attribute is not None:
			xpath += "/@%s" % attribute

		return "/".join([self.getParentObj().getXPath(), xpath])