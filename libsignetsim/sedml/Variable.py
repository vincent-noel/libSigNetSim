#!/usr/bin/env python
""" Variable.py


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
from libsignetsim.sedml.SedBase import SedBase
from libsignetsim.sedml.HasId import HasId
from libsignetsim.sedml.SedmlException import SedmlUnknownURI, SedmlUnknownXPATH
from libsignetsim.settings.Settings import Settings

from libsignetsim.sedml.math.sympy_shortcuts import SympySymbol
from re import match

class Variable(SedBase, HasId):

	def __init__(self, document):

		SedBase.__init__(self, document)
		HasId.__init__(self, document)

		self.__document = document
		self.__taskReference = None
		self.__modelReference = None
		self.__symbol = None
		self.__target = None


	def readSedml(self, variable, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.readSedml(self, variable, level, version)
		HasId.readSedml(self, variable, level, version)

		if variable.isSetTaskReference():
			self.__taskReference = variable.getTaskReference()

		if variable.isSetModelReference():
			self.__modelReference = variable.getModelReference()

		if variable.isSetSymbol():
			self.__symbol = variable.getSymbol()

		if variable.isSetTarget():
			self.__target = variable.getTarget()

	def writeSedml(self, variable, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, variable, level, version)
		HasId.writeSedml(self, variable, level, version)

		if self.__taskReference is not None:
			variable.setTaskReference(self.__taskReference)

		if self.__modelReference is not None:
			variable.setModelReference(self.__modelReference)

		if self.__symbol is not None:
			variable.setSymbol(self.__symbol)

		if self.__target is not None:
			variable.setTarget(self.__target)

	def getTaskReference(self):
		return self.__taskReference

	def getModelReference(self):
		return self.__modelReference

	def getSymbol(self):
		return self.__symbol

	def getTarget(self):
		return self.__target

	def getSympySymbol(self):
		return SympySymbol(self.getId())

	def getData(self):

		simulation = self.__document.listOfTasks.getTask(self.__taskReference)

		if self.__symbol is not None:

			symbol_tokens = self.__symbol.split(':')

			if len(symbol_tokens) == 4 and symbol_tokens[1] == 'sedml' and symbol_tokens[2] == 'symbol':

				symbol = self.__symbol.split(':')[3]

				if symbol == 'time':
					return {self : simulation.getTimes()}

				else:
					raise SedmlUnknownURI("Unknown symbol %s" % symbol)

			else:

				raise SedmlUnknownURI("Unknown URI %s" % self.__symbol)

		elif self.__target is not None:
			target_tokens = self.__target.split(':')

			if target_tokens[0] == "/sbml" and target_tokens[1] == "sbml/sbml":

				last_token = target_tokens[len(target_tokens)-1]
				res_match = match(r"([a-zA-Z]+)\[@([a-zA-Z]+)=\'(.*)\'\]", last_token)

				if res_match is not None and len(res_match.groups()) == 3:
					if res_match.groups()[1] == 'id':
						sbml_id = res_match.groups()[2]
						return {self: simulation.getResultsByVariable(sbml_id)}
					elif res_match.groups()[1] == 'name':

						sbml_model = self.__document.listOfModels.getByModelReference(simulation.getModelReference())
						sbml_id = sbml_model.listOfVariables.getByName(res_match.groups()[2]).getSbmlId()
						return {self: simulation.getResultsByVariable(sbml_id)}

				else:
					raise SedmlUnknownXPATH("Unknown variable in XPATH %s" % last_token)
			else:
				return SedmlUnknownXPATH("Unknown XPATH %s" % self.__target)





