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
from libsignetsim.sedml.XPath import XPath
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
		# self.__symbolv2 =
		self.__target = XPath(self.__document)


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
			self.__target.readSedml(variable.getTarget(), level, version)

	def writeSedml(self, variable, level=Settings.defaultSedmlLevel, version=Settings.defaultSedmlVersion):

		SedBase.writeSedml(self, variable, level, version)
		HasId.writeSedml(self, variable, level, version)

		if self.__taskReference is not None:
			variable.setTaskReference(self.__taskReference)

		if self.__modelReference is not None:
			variable.setModelReference(self.__modelReference)

		if self.__symbol is not None:
			variable.setSymbol(self.__symbol)

		if self.__target.writeSedml(level, version) is not None:
			variable.setTarget(self.__target.writeSedml(level, version))

	def getTaskReference(self):
		return self.__taskReference

	def getTask(self):
		return self.__document.listOfTasks.getTask(self.__taskReference)

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
			# print symbol_tokens
			if len(symbol_tokens) == 4 and symbol_tokens[1] == 'sedml' and symbol_tokens[2] == 'symbol':

				symbol = self.__symbol.split(':')[3]

				if symbol == 'time':
					return {self : simulation.getTimes()}

				else:
					raise SedmlUnknownURI("Unknown symbol %s" % symbol)

			else:

				raise SedmlUnknownURI("Unknown URI %s" % self.__symbol)

		elif self.__target.getXPath() is not None:
			sbml_model = self.__document.listOfModels.getByModelReference(simulation.getModelReference())
			sbml_object = self.__target.getModelObject(sbml_model)
			return {self: simulation.getResultsByVariable(sbml_object.getSbmlId())}

	def setTaskReference(self, task_reference):
		self.__taskReference = task_reference

	def setTask(self, task):
		self.__taskReference = task.getId()

	def setModelReference(self, model_reference):
		self.__modelReference = model_reference

	def setModel(self, model):
		self.__modelReference = model.getId()

	def setTarget(self, object):
		self.__target.setModelObject(object)

	def setSymbol(self, symbol):
		self.__symbol = symbol



