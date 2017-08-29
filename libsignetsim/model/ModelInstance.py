#!/usr/bin/env python
""" ModelInstance.py


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


from libsignetsim.model.Model import Model
from libsignetsim.model.Variable import Variable
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.sbml.container.ListOfReplacedElements import ListOfReplacedElements
from libsignetsim.model.math.sympy_shortcuts import SympySymbol, SympyInteger
from libsignetsim.model.sbml.SbmlObject import SbmlObject
from libsignetsim.model.sbml.SpeciesReference import SpeciesReference
from libsignetsim.settings.Settings import Settings


class ModelInstance(Model):
	""" Sbml model class """

	PREFIX_PATTERN = "%s__"
	DEBUG = False

	def __init__(self, model, document):
		""" Constructor of model class """

		Model.__init__(self, parent_doc=document, is_model_instance=True, is_main_model=True)
		self.__mainModel = model
		self.__document = document
		self.__submodelInstances = {}
		self.sbmlLevel = model.sbmlLevel
		self.sbmlVersion = model.sbmlVersion
		self.objectsDictionnary = {}
		self.deletions = []
		self.substitutions = []

		self.dict_sids = {}
		self.dict_symbols = {}
		self.dict_usids = {}
		self.submodel_sids_subs = {}
		self.submodel_symbols_subs = {}
		self.submodel_usids_subs = {}
		self.submodel_timeConversionFactor = {}
		self.submodel_extentConversionFactor = {}
		self.conv_factors = {}

		if self.DEBUG:
			print "\n\n> Instanciating model %s, parent doc is %s" % (model.getSbmlId(), document.documentFilename)


		if len(self.__mainModel.listOfSubmodels) > 0:

			# Instanciating submodels depth first
			for submodel in self.__mainModel.listOfSubmodels.values():
				t_submodel_instance = submodel.getModelInstance()
				self.__submodelInstances.update({submodel.getSbmlId(): t_submodel_instance})
				self.submodel_sids_subs.update({submodel.getSbmlId(): {}})
				self.submodel_symbols_subs.update({submodel.getSbmlId(): {}})
				self.submodel_usids_subs.update({submodel.getSbmlId(): {}})

				for deletion in submodel.listOfDeletions.values():
					self.deletions.append(deletion.getDeletionObjectFromInstance(t_submodel_instance))

				for variable in t_submodel_instance.listOfVariables.values():
					if variable not in self.deletions:
						self.submodel_sids_subs[submodel.getSbmlId()].update({
							variable.getSbmlId(): (self.PREFIX_PATTERN % submodel.getSbmlId()) + variable.getSbmlId()
						})

						if variable.isParameter() and variable.localParameter:
							old_symbol = variable.symbol.getInternalMathFormula()
							new_symbol = SympySymbol("_local_%d_%s" % (variable.reaction.objId,
								(self.PREFIX_PATTERN % submodel.getSbmlId())
								+ str(variable.getSbmlId())
							))
						else:
							old_symbol = variable.symbol.getInternalMathFormula()
							new_symbol = SympySymbol(
								(self.PREFIX_PATTERN % submodel.getSbmlId())
								+ str(variable.symbol.getInternalMathFormula())
							)
						self.submodel_symbols_subs[submodel.getSbmlId()].update({old_symbol: new_symbol})


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
					self.submodel_symbols_subs[submodel.getSbmlId()].update({SympySymbol("_time_"): SympySymbol("_time_")/submodel.getTimeConversionFactor().getInternalMathFormula()})

				else:
					self.submodel_timeConversionFactor.update({submodel.getSbmlId(): None})


			self.findReplacements()

			if self.DEBUG:
				print ">> Sids dictionnaries"
				print self.dict_sids
				print self.submodel_sids_subs
				print ">> Symbols dictionnaries"
				print self.dict_symbols
				print self.submodel_symbols_subs

		self.mergeModels()

		if self.DEBUG:
			print ">> Model's variables : "
			print self.listOfVariables.sbmlIds()
			print self.listOfVariables.symbols()

			print "> Returning instance %s\n" % model.getSbmlId()


	def findReplacements(self):

		for sbmlobject in self.__mainModel.listOfSbmlObjects.values():

			if isinstance(sbmlobject, SbmlObject) and sbmlobject.hasReplacedElements():

				for replaced_element in sbmlobject.getListOfReplacedElements().values():

					replaced_object = replaced_element.getReplacedElementObjectFromInstance(self)
					self.substitutions.append((replaced_object, sbmlobject))
					self.deletions.append(replaced_object)

					if isinstance(sbmlobject, Variable):

						old_string = (self.PREFIX_PATTERN % replaced_element.getSubmodelRef()) + replaced_object.getSbmlId()
						new_string = sbmlobject.getSbmlId()

						for old, new in self.submodel_sids_subs[replaced_element.getSubmodelRef()].items():
							if new == old_string:
								self.submodel_sids_subs[replaced_element.getSubmodelRef()].update({
									old: new_string
								})

						if replaced_object.isParameter() and replaced_object.localParameter:
							old_symbol = SympySymbol("_local_%d_%s" % (replaced_object.reaction.objId, old_string))
						else:
							old_symbol = SympySymbol(old_string)

						new_symbol = SympySymbol(new_string)

						for old, new in self.submodel_symbols_subs[replaced_element.getSubmodelRef()].items():
							if new == old_symbol:
								self.submodel_symbols_subs[replaced_element.getSubmodelRef()].update({
									old: new_symbol
								})

						if replaced_element.getConversionFactor() is not None:
							self.conv_factors.update({SympySymbol(sbmlobject.getSbmlId()): SympySymbol(
								replaced_element.getConversionFactor())})

			if isinstance(sbmlobject, SbmlObject) and sbmlobject.isReplaced():

				replacing_object = sbmlobject.isReplacedBy().getReplacingElementObjectFromInstance(self)
				self.substitutions.append((sbmlobject, replacing_object))
				self.deletions.append(sbmlobject)

				if isinstance(sbmlobject, Variable):
					old_string = sbmlobject.getSbmlId()
					new_string = replacing_object.getSbmlId()

					if new_string in self.submodel_sids_subs[sbmlobject.isReplacedBy().getSubmodelRef()].keys():
						self.submodel_sids_subs[sbmlobject.isReplacedBy().getSubmodelRef()].update({new_string: old_string})

					old_symbol = SympySymbol(old_string)
					new_symbol = SympySymbol(new_string)

					if new_symbol in self.submodel_symbols_subs[sbmlobject.isReplacedBy().getSubmodelRef()].keys():
						self.submodel_symbols_subs[sbmlobject.isReplacedBy().getSubmodelRef()].update({new_symbol: old_symbol})



	def mergeModels(self):

		# This function copy the main model and the submodels into the instanciated model, one element at a time

		# self.listOfUnitDefinitions.copy(
		# 	self.__mainModel.listOfUnitDefinitions,
		# 	deletions=self.deletions,
		# )
		# for submodel in self.__mainModel.listOfSubmodels.values():
		# 	self.listOfUnitDefinitions.copy(
		# 		self.__submodelInstances[submodel.getSbmlId()].listOfUnitDefinitions,
		# 		prefix=self.PREFIX_PATTERN % submodel.getSbmlId(),
		# 		deletions=self.deletions,
		# 	)

		self.listOfCompartments.copy(
			self.__mainModel.listOfCompartments,
			deletions=self.deletions,
			sids_subs=self.dict_sids,
			symbols_subs=self.dict_symbols,
			usids_subs=self.dict_usids
		)
		for submodel in self.__mainModel.listOfSubmodels.values():
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
			sids_subs=self.dict_sids,
			symbols_subs=self.dict_symbols,
			usids_subs=self.dict_usids
		)
		for submodel in self.__mainModel.listOfSubmodels.values():
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
			sids_subs=self.dict_sids,
			symbols_subs=self.dict_symbols,
			usids_subs=self.dict_usids
		)
		for submodel in self.__mainModel.listOfSubmodels.values():
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
			sids_subs=self.dict_symbols,
			symbols_subs=self.dict_symbols,
			usids_subs=self.dict_usids,
		)
		for submodel in self.__mainModel.listOfSubmodels.values():
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
			sids_subs=self.dict_sids,
			symbols_subs=self.dict_symbols,
		)
		for submodel in self.__mainModel.listOfSubmodels.values():
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
			sids_subs=self.dict_sids,
			symbols_subs=self.dict_symbols,
		)
		for submodel in self.__mainModel.listOfSubmodels.values():
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
			sids_subs=self.dict_sids,
			symbols_subs=self.dict_symbols,
		)

		for submodel in self.__mainModel.listOfSubmodels.values():
			self.listOfEvents.copy(
				self.__submodelInstances[submodel.getSbmlId()].listOfEvents,
				deletions=self.deletions,
				sids_subs=self.submodel_sids_subs[submodel.getSbmlId()],
				symbols_subs=self.submodel_symbols_subs[submodel.getSbmlId()],
				conversion_factors=self.conv_factors,
				time_conversion=self.submodel_timeConversionFactor[submodel.getSbmlId()],
			)

	def getSubmodelInstance(self, submodel_ref):
		return self.__submodelInstances[submodel_ref]
