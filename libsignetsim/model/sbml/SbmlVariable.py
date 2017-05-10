#!/usr/bin/env python
""" SbmlVariable.py


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
from libsignetsim.settings.Settings import Settings
from sympy import Symbol

class SbmlVariable(HasId):

	SPECIES             = 0
	COMPARTMENT         = 1
	PARAMETER           = 2
	STOICHIOMERY        = 3
	REACTION            = 4

	def __init__(self, model, sbml_type, is_from_reaction=None):

		self.__model = model
		HasId.__init__(self, model)
		self.sbmlType = sbml_type
		self.reaction = is_from_reaction



	def new(self, name, sbml_type=PARAMETER):

		self.sbmlType = sbml_type
		t_sbmlId = self.__model.listOfVariables.addVariable(self, name)
		HasId.new(self, name, t_sbmlId)


	def copy(self, obj, prefix="", shift=0, subs={}, deletions=[],
				replacements={}):


		HasId.copy(self, obj, prefix, shift, subs, deletions, replacements)

		if self.isParameter() and self.localParameter:
			self.__model.listOfVariables.addVariable(self,
			"_local_%d_%s" % (self.reaction.objId, prefix + obj.getSbmlId()))

		else:
			t_sbml_id = prefix + obj.getSbmlId()
			# print "> Adding variable %s : %s" % (t_sbml_id, self.symbol.getInternalMathFormula())
			self.__model.listOfVariables.addVariable(self, t_sbml_id)
		self.sbmlType = obj.sbmlType




	def readSbml(self, sbml_variable,
						sbml_level=Settings.defaultSbmlLevel,
						sbml_version=Settings.defaultSbmlVersion):

		HasId.readSbml(self, sbml_variable, sbml_level, sbml_version)

		if self.isParameter() and self.localParameter:
			self.__model.listOfVariables.addVariable(self,
					"_local_%d_%s" % (self.reaction.objId, self.getSbmlId()))
		else:
			self.__model.listOfVariables.addVariable(self, self.getSbmlId())


	def writeSbml(self, sbml_variable,
						sbml_level=Settings.defaultSbmlLevel,
						sbml_version=Settings.defaultSbmlVersion):

		HasId.writeSbml(self, sbml_variable, sbml_level, sbml_version)


	def isSpecies(self):
		return self.sbmlType == self.SPECIES

	def isParameter(self):
		return self.sbmlType == self.PARAMETER

	def isCompartment(self):
		return self.sbmlType == self.COMPARTMENT

	def isStoichiometry(self):
		from libsignetsim.model.sbml.SpeciesReference import SpeciesReference

		return isinstance(self, SpeciesReference)

	def isReaction(self):
		return self.sbmlType == self.REACTION

	def isGlobal(self):
		return self.reaction is None


	def setSbmlId(self, sbml_id, prefix="", model_wide=True):

		# print "Inside setSbmlId"
		if self.isParameter() and self.isLocalParameter():
			# print "is local parameter"
			self.reaction.renameSbmlId(self.getSbmlId(), sbml_id)
			HasId.setSbmlId(self, sbml_id)
		else:
			HasId.setSbmlId(self, sbml_id, prefix, model_wide)

	def renameSbmlId(self, sbml_id):
		HasId.setSbmlId(self, sbml_id, model_wide=False, list_of_var=False)
