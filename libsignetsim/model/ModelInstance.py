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
from __future__ import print_function
from __future__ import division

from libsignetsim.model.Model import Model
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.FunctionDefinition import FunctionDefinition
from libsignetsim.model.sbml.UnitDefinition import UnitDefinition
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from libsignetsim.model.sbml.SbmlObject import SbmlObject

class ModelInstance(Model):
	""" Sbml model class """

	PREFIX_PATTERN = "%s__"
	DEBUG = False

	def __init__(self, model, document):
		""" Constructor of model class """

		Model.__init__(self, parent_doc=document)
		self.__mainModel = model
		self.__document = document
		self.__submodelInstances = {}
		self.sbmlLevel = model.sbmlLevel
		self.sbmlVersion = model.sbmlVersion
		self.objectsDictionnary = {}
		self.variablesDictionnary = {}
		self.deletions = []

		self.submodel_sids_subs = {}
		self.submodel_symbols_subs = {}
		self.submodel_usids_subs = {}
		self.submodel_timeConversionFactor = {}
		self.submodel_extentConversionFactor = {}
		self.conv_factors = {}

		if self.DEBUG:
			print("\n\n> Instanciating model %s, parent doc is %s" % (model.getNameOrSbmlId(), document.documentFilename))


		if len(self.__mainModel.listOfSubmodels) > 0:

			# Instanciating submodels depth first
			for submodel in self.__mainModel.listOfSubmodels:
				t_submodel_instance = submodel.getModelInstance()
				self.__submodelInstances.update({submodel.getSbmlId(): t_submodel_instance})
				self.submodel_sids_subs.update({submodel.getSbmlId(): {}})
				self.submodel_symbols_subs.update({submodel.getSbmlId(): {}})
				self.submodel_usids_subs.update({submodel.getSbmlId(): {}})

				for deletion in submodel.listOfDeletions:
					self.deletions.append(deletion.getDeletionObjectFromInstance(t_submodel_instance))

				for variable in t_submodel_instance.listOfVariables:
					if variable not in self.deletions:
						self.submodel_sids_subs[submodel.getSbmlId()].update({
							variable.getSbmlId(): (self.PREFIX_PATTERN % submodel.getSbmlId()) + variable.getSbmlId()
						})

						if variable.isParameter() and variable.localParameter:
							old_symbol = variable.symbol.getInternalMathFormula()
							new_symbol = SympySymbol("_local_%d_%s" % (variable.reaction.objId,
								(self.PREFIX_PATTERN % submodel.getSbmlId())
								+ variable.getSbmlId()
							))
						else:
							old_symbol = variable.symbol.getInternalMathFormula()
							new_symbol = SympySymbol(
								(self.PREFIX_PATTERN % submodel.getSbmlId())
								+ variable.symbol.getInternalMathFormula().name
							)
						self.submodel_symbols_subs[submodel.getSbmlId()].update({old_symbol: new_symbol})

				for function_definition in t_submodel_instance.listOfFunctionDefinitions:
					if function_definition not in self.deletions:
						self.submodel_sids_subs[submodel.getSbmlId()].update({
							function_definition.getSbmlId(): (self.PREFIX_PATTERN % submodel.getSbmlId()) + function_definition.getSbmlId()
						})

						old_symbol = SympySymbol(function_definition.getSbmlId())
						new_symbol = SympySymbol(
							(self.PREFIX_PATTERN % submodel.getSbmlId())
							+ function_definition.getSbmlId()
						)
						self.submodel_symbols_subs[submodel.getSbmlId()].update({old_symbol: new_symbol})

				for unit_definition in t_submodel_instance.listOfUnitDefinitions:
					if unit_definition not in self.deletions:
						self.submodel_usids_subs[submodel.getSbmlId()].update({
							unit_definition.getSbmlId(): (self.PREFIX_PATTERN % submodel.getSbmlId()) + unit_definition.getSbmlId()
						})


				if submodel.hasExtentConversionFactor():
					self.submodel_extentConversionFactor.update(
						{submodel.getSbmlId(): submodel.getExtentConversionFactor()}
					)

				else:
					self.submodel_extentConversionFactor.update({submodel.getSbmlId(): None})

				if submodel.hasTimeConversionFactor():
					self.submodel_timeConversionFactor.update(
						{submodel.getSbmlId(): submodel.getTimeConversionFactor()}
					)
					self.submodel_symbols_subs[submodel.getSbmlId()].update(
						{SympySymbol("_time_"): SympySymbol("_time_") / submodel.getTimeConversionFactor().getInternalMathFormula()}
					)


				else:
					self.submodel_timeConversionFactor.update({submodel.getSbmlId(): None})


			self.findReplacements()

			if self.DEBUG:
				print(">> Sids dictionnaries")
				print(self.submodel_sids_subs)
				print(">> Symbols dictionnaries")
				print(self.submodel_symbols_subs)

		self.mergeModels()

		if self.DEBUG:
			print(">> Model's variables : ")
			print(self.listOfVariables.sbmlIds())
			print(self.listOfVariables.symbols())

			print("> Returning instance %s\n" % model.getSbmlId())

	def findReplacements(self):

		for sbmlobject in self.__mainModel.listOfSbmlObjects:

			if isinstance(sbmlobject, SbmlObject) and sbmlobject.hasReplacedElements():

				for replaced_element in sbmlobject.getListOfReplacedElements():

					replaced_object = replaced_element.getReplacedElementObjectFromInstance(self)
					self.deletions.append(replaced_object)

					if isinstance(sbmlobject, Variable):

						old_string = (self.PREFIX_PATTERN % replaced_element.getSubmodelRef()) + replaced_object.getSbmlId()
						new_string = sbmlobject.getSbmlId()

						for old, new in list(self.submodel_sids_subs[replaced_element.getSubmodelRef()].items()):
							if new == old_string:
								self.submodel_sids_subs[replaced_element.getSubmodelRef()].update({
									old: new_string
								})

						if replaced_object.isParameter() and replaced_object.localParameter:
							old_symbol = SympySymbol("_local_%d_%s" % (replaced_object.reaction.objId, old_string))
						else:
							old_symbol = SympySymbol(old_string)

						new_symbol = SympySymbol(new_string)

						for old, new in list(self.submodel_symbols_subs[replaced_element.getSubmodelRef()].items()):
							if new == old_symbol:
								self.submodel_symbols_subs[replaced_element.getSubmodelRef()].update({
									old: new_symbol
								})

						if replaced_element.getConversionFactor() is not None:
							self.conv_factors.update({SympySymbol(sbmlobject.getSbmlId()): SympySymbol(
								replaced_element.getConversionFactor())})

					if isinstance(sbmlobject, FunctionDefinition):

						old_string = (self.PREFIX_PATTERN % replaced_element.getSubmodelRef()) + replaced_object.getSbmlId()
						new_string = sbmlobject.getSbmlId()

						for old, new in list(self.submodel_sids_subs[replaced_element.getSubmodelRef()].items()):
							if new == old_string:
								self.submodel_sids_subs[replaced_element.getSubmodelRef()].update({
									old: new_string
								})


						old_symbol = SympySymbol(old_string)
						new_symbol = SympySymbol(new_string)

						for old, new in list(self.submodel_symbols_subs[replaced_element.getSubmodelRef()].items()):
							if new == old_symbol:
								self.submodel_symbols_subs[replaced_element.getSubmodelRef()].update({
									old: new_symbol
								})

					if isinstance(sbmlobject, UnitDefinition):

						old_string = (self.PREFIX_PATTERN % replaced_element.getSubmodelRef()) + replaced_object.getSbmlId()
						new_string = sbmlobject.getSbmlId()

						for old, new in list(self.submodel_usids_subs[replaced_element.getSubmodelRef()].items()):
							if new == old_string:
								self.submodel_usids_subs[replaced_element.getSubmodelRef()].update({
									old: new_string
								})




			if isinstance(sbmlobject, SbmlObject) and sbmlobject.isReplaced():

				replacing_object = sbmlobject.isReplacedBy().getReplacingElementObjectFromInstance(self)
				self.deletions.append(sbmlobject)

				if isinstance(sbmlobject, Variable) or isinstance(sbmlobject, FunctionDefinition):
					old_string = sbmlobject.getSbmlId()
					new_string = replacing_object.getSbmlId()

					if new_string in list(self.submodel_sids_subs[sbmlobject.isReplacedBy().getSubmodelRef()].keys()):
						self.submodel_sids_subs[sbmlobject.isReplacedBy().getSubmodelRef()].update({new_string: old_string})

					old_symbol = SympySymbol(old_string)
					new_symbol = SympySymbol(new_string)

					if new_symbol in list(self.submodel_symbols_subs[sbmlobject.isReplacedBy().getSubmodelRef()].keys()):
						self.submodel_symbols_subs[sbmlobject.isReplacedBy().getSubmodelRef()].update({new_symbol: old_symbol})

				if isinstance(sbmlobject, UnitDefinition):
					old_string = sbmlobject.getSbmlId()
					new_string = replacing_object.getSbmlId()

					if new_string in list(self.submodel_usids_subs[sbmlobject.isReplacedBy().getSubmodelRef()].keys()):
						self.submodel_usids_subs[sbmlobject.isReplacedBy().getSubmodelRef()].update({new_string: old_string})


	def mergeModels(self):

		# This function copy the main model and the submodels into the instanciated model, one element at a time

		self.listOfUnitDefinitions.copy(
			self.__mainModel.listOfUnitDefinitions,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfUnitDefinitions.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfUnitDefinitions,
				deletions=self.deletions,
				usids_subs=self.submodel_usids_subs[submodel.getSbmlId()]
			)

		self.listOfFunctionDefinitions.copy(
			self.__mainModel.listOfFunctionDefinitions,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfFunctionDefinitions.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfFunctionDefinitions,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()]
			)


		self.listOfCompartments.copy(
			self.__mainModel.listOfCompartments,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfCompartments.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfCompartments,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				usids_subs=self.submodel_usids_subs[submodel.getSbmlId()]
			)

		self.listOfParameters.copy(
			self.__mainModel.listOfParameters,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfParameters.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfParameters,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				usids_subs=self.submodel_usids_subs[submodel.getSbmlId()]
			)

		self.listOfSpecies.copy(
			self.__mainModel.listOfSpecies,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfSpecies.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfSpecies,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				usids_subs=self.submodel_usids_subs[submodel.getSbmlId()]
			)

		self.listOfReactions.copy(
			self.__mainModel.listOfReactions,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfReactions.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfReactions,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				usids_subs=self.submodel_usids_subs[submodel.getSbmlId()],
				conversion_factors=self.conv_factors,
				time_conversion=self.submodel_timeConversionFactor[submodel.getSbmlId()],
				extent_conversion=self.submodel_extentConversionFactor[submodel.getSbmlId()]
			)

		self.listOfInitialAssignments.copy(
			self.__mainModel.listOfInitialAssignments,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfInitialAssignments.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfInitialAssignments,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				conversion_factors=self.conv_factors
			)

		self.listOfRules.copy(
			self.__mainModel.listOfRules,
			deletions=self.deletions,
		)
		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfRules.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfRules,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				conversion_factors=self.conv_factors,
				time_conversion=self.submodel_timeConversionFactor[submodel.getSbmlId()],
			)

		self.listOfEvents.copy(
			self.__mainModel.listOfEvents,
			deletions=self.deletions,
		)

		for submodel in self.__mainModel.listOfSubmodels:
			self.listOfEvents.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfEvents,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				conversion_factors=self.conv_factors,
				time_conversion=self.submodel_timeConversionFactor[submodel.getSbmlId()],
			)

		for variable in self.__mainModel.listOfVariables:
			if self.listOfVariables.containsSbmlId(variable.getSbmlId()):
				self.variablesDictionnary.update({
					variable: self.listOfVariables.getBySbmlId(variable.getSbmlId())
				})

		for submodel in self.__mainModel.listOfSubmodels:
			submodel_instance = self.__submodelInstances[submodel.getSbmlId()]

			for variable_def, variable_instance in list(submodel_instance.variablesDictionnary.items()):
				sids_subs = self.submodel_sids_subs[submodel.getSbmlId()]

				if (
					variable_instance.getSbmlId() in list(sids_subs.keys())
					and self.listOfVariables.containsSbmlId(sids_subs[variable_instance.getSbmlId()])
				):
					self.variablesDictionnary.update({
						variable_def: self.listOfVariables.getBySbmlId(
							sids_subs[variable_instance.getSbmlId()]
						)
					})

	def getSubmodelInstance(self, submodel_ref):
		return self.__submodelInstances[submodel_ref]

	def getInstanceVariable(self, variable):
		return self.variablesDictionnary[variable]

	def getInstanceVariableByXPath(self, xpath):
		variable = self.__mainModel.parentDoc.getByXPath(xpath)
		return self.getInstanceVariable(variable)

	def getDefinitionVariable(self, variable):
		res = []
		for key, value in list(self.variablesDictionnary.items()):
			if value == variable:
				res.append(key)
		return res

	def getDefinitionVariableByXPath(self, xpath):
		variable = self.parentDoc.getByXPath(xpath, instance=True)
		return self.getDefinitionVariable(variable)
