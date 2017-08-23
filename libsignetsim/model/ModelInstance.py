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


	def __init__ (self, model, document):
		""" Constructor of model class """

		Model.__init__(self, parent_doc=document, is_model_instance=True, is_main_model=True)
		self.__mainModel = model
		self.__document = document
		self.__submodelInstances = {}
		self.sbmlLevel = model.sbmlLevel
		self.sbmlVersion = model.sbmlVersion
		self.objectsDictionnary = {}
		if Settings.verbose >= 2:
			print "\n\n> Instanciating model %s, parent doc is %s" % (model.getSbmlId(), document.documentFilename)

		var_subs_main_simples = {}

		if len(self.__mainModel.listOfSubmodels) > 0:

			# Instanciating submodels depth first
			for submodel in self.__mainModel.listOfSubmodels.values():
				t_submodel_instance = submodel.getModelInstance()
				self.__submodelInstances.update({submodel.getSbmlId(): t_submodel_instance})

			# Looking for substitutions
			deletions = []
			var_subs_main = {}
			var_subs_main_simples = {}
			conv_factors = {}
			for sbmlobject in self.__mainModel.listOfSbmlObjects.values():

				if isinstance(sbmlobject, SbmlObject) and sbmlobject.hasReplacedElements():

					for replaced_element in sbmlobject.getListOfReplacedElements().values():

						replaced_object = replaced_element.getReplacedElementObject(self)
						deletions.append(replaced_object)

						if isinstance(sbmlobject, Variable):

							if sbmlobject.isConcentration():
								var_subs_main.update({SympySymbol("_speciesForcedConcentration_%s__%s_" % (replaced_element.getSubmodelRef(), replaced_object.getSbmlId())):SympySymbol("_speciesForcedConcentration_%s_" % sbmlobject.getSbmlId())})


							if replaced_object.isParameter() and replaced_object.localParameter:
								var_subs_main.update({SympySymbol("_local_%d_%s__%s" % (replaced_object.reaction.objId, replaced_element.getSubmodelRef(), replaced_object.getSbmlId())): SympySymbol("_local_%d_%s" % (replaced_object.reaction.objId, replaced_element.getSubmodelRef() + "__" +sbmlobject.getSbmlId()))})
								var_subs_main.update({SympySymbol("_local_%d_%s" % (replaced_object.reaction.objId, replaced_object.getSbmlId())): SympySymbol("_local_%d_%s" % (replaced_object.reaction.objId, sbmlobject.getSbmlId()))})

								# In this case we don't just rename the variables in the model's math, we also need to actually create the variable in the local scope
								replaced_object.isMarkedToBeReplaced = True
								replaced_object.isMarkedToBeReplacedBy = sbmlobject
								deletions.remove(replaced_object)

							else:
								var_subs_main.update({SympySymbol("%s__%s" % (replaced_element.getSubmodelRef(), replaced_object.getSbmlId())): SympySymbol(sbmlobject.getSbmlId())})
								var_subs_main_simples.update({SympySymbol(replaced_object.getSbmlId()):SympySymbol(sbmlobject.getSbmlId())})

							# Should only work on variables, right ??!!
							if replaced_element.getConversionFactor() is not None:
								conv_factors.update({SympySymbol(sbmlobject.getSbmlId()): SympySymbol(replaced_element.getConversionFactor())})


				if isinstance(sbmlobject, SbmlObject) and sbmlobject.isReplaced():

					replacing_object = sbmlobject.isReplacedBy().getReplacingElementObject(self)

					sbmlobject.isMarkedToBeReplaced = True
					sbmlobject.isMarkedToBeRenamed = True # Should be true ?
					# sbmlobject.isMarkedToBeRenamed = False # Should be true ?
					sbmlobject.isMarkedToBeReplacedBy = replacing_object

					if isinstance(sbmlobject, Variable):
						if sbmlobject.isConcentration():
							var_subs_main.update({SympySymbol("_speciesForcedConcentration_%s__%s_" % (sbmlobject.isReplacedBy().getSubmodelRef(), sbmlobject.getSbmlId())):SympySymbol("_speciesForcedConcentration_%s_" % replacing_object.getSbmlId())})

						var_subs_main.update({SympySymbol("%s__%s" % (sbmlobject.isReplacedBy().getSubmodelRef(), sbmlobject.getSbmlId())):SympySymbol(replacing_object.getSbmlId())})
						var_subs_main_simples.update({SympySymbol(sbmlobject.getSbmlId()):SympySymbol(replacing_object.getSbmlId())})

		# First let's copy the model...
		self.copyMainModel(var_subs_main_simples)

		if len(self.__mainModel.listOfSubmodels) > 0:
			for i, submodel in enumerate(self.__mainModel.listOfSubmodels.values()):

				# print "Generating submodel instance"
				submodel_instance = self.__submodelInstances[submodel.getSbmlId()]
				prefix = submodel.getSbmlId() + "__"
				var_subs_submodel = {}

				if submodel.hasTimeConversionFactor():
					var_subs_submodel.update({SympySymbol("_time_"): SympySymbol("_time_")/submodel.getTimeConversionFactor().getInternalMathFormula()})

				for var in submodel_instance.listOfVariables.values():

					if var.isParameter() and var.localParameter:
						var_subs_submodel.update({SympySymbol("_local_%d_%s" % (var.reaction.objId, var.getSbmlId())): SympySymbol("_local_%d_%s" % (var.reaction.objId, prefix+var.getSbmlId()))})

					elif var.isConcentration():
						var_subs_submodel.update({SympySymbol("_speciesForcedConcentration_%s_" % var.getSbmlId()):SympySymbol("_speciesForcedConcentration_%s_" % (prefix+var.getSbmlId()))})
						var_subs_submodel.update({SympySymbol(var.getSbmlId()):SympySymbol(prefix+var.getSbmlId())})

					else:
						var_subs_submodel.update({SympySymbol(var.getSbmlId()):SympySymbol(prefix+var.getSbmlId())})


				t_deletions = submodel.getDeletionsMetaIds()
				for t_deletion in t_deletions:
					deletions.append(submodel_instance.listOfSbmlObjects.getByMetaId(t_deletion))

				for deletion in deletions:
					# If we just delete a local parameter, that means we are switching to a global parameter with the same sbml id
					if isinstance(deletion, Variable) and deletion.isParameter() and deletion.localParameter:
						var_subs_submodel.update({SympySymbol("_local_%d_%s" % (deletion.reaction.objId, deletion.getSbmlId())):SympySymbol(prefix+deletion.getSbmlId())})


				t_factor = SympyInteger(1)
				if submodel.hasExtentConversionFactor():
					t_factor *= submodel.getExtentConversionFactor().getInternalMathFormula()

				if submodel.hasTimeConversionFactor():
					t_factor /= submodel.getTimeConversionFactor().getInternalMathFormula()


				for reaction in submodel_instance.listOfReactions.values():
					if t_factor != MathFormula.ONE:
						conv_factors.update({SympySymbol(prefix+reaction.getSbmlId()):t_factor})

				# Then copy the submodel
				self.copySubmodel(submodel, submodel_instance, prefix, var_subs_submodel, deletions, var_subs_main, conv_factors)


		if Settings.verbose >= 2:
			print "\n > Model's variables : "
			print self.listOfVariables.sbmlIds()

			print "\n > Returning instance %s\n" % model.getSbmlId()


	def copyMainModel(self, var_subs_main_simples):

		# First let's copy the model...
		self.listOfFunctionDefinitions.copy(self.__mainModel.listOfFunctionDefinitions)
		self.listOfUnitDefinitions.copy(self.__mainModel.listOfUnitDefinitions)
		self.listOfCompartments.copy(self.__mainModel.listOfCompartments, subs=var_subs_main_simples)
		self.listOfParameters.copy(self.__mainModel.listOfParameters)

		# TODO
		# here it's really weird
		# I thought I need both species and reactions with the ability to substitute the right sbml id or compartments and speciesReferences
		# Actually, species seems to work ok, but reactions don't
		# Maybe for a lack of a good test for the species references ?
		# Here we still have to do something.
		# The obvious solution is to add yet another variable to the copy of the objects whivh have a variable replacement covered by this case

		self.listOfSpecies.copy(self.__mainModel.listOfSpecies, subs=var_subs_main_simples)
		self.listOfReactions.copy(self.__mainModel.listOfReactions, replacements=var_subs_main_simples)
		self.listOfInitialAssignments.copy(self.__mainModel.listOfInitialAssignments)
		self.listOfRules.copy(self.__mainModel.listOfRules)
		self.listOfEvents.copy(self.__mainModel.listOfEvents)

		if self.__mainModel.conversionFactor is not None:
			self.conversionFactor = MathFormula(self)
			self.conversionFactor.setInternalMathFormula(self.__mainModel.conversionFactor.getInternalMathFormula())

	def copySubmodel(self, submodel, submodel_instance, prefix, var_subs_submodel, deletions, var_subs_main, conv_factors):

		self.listOfFunctionDefinitions.copy(
			submodel_instance.listOfFunctionDefinitions,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions
		)

		self.listOfUnitDefinitions.copy(submodel_instance.listOfUnitDefinitions, prefix=prefix)
		self.listOfCompartments.copy(
			submodel_instance.listOfCompartments,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions,
			replacements=var_subs_main
		)

		self.listOfParameters.copy(
			submodel_instance.listOfParameters,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions,
			replacements=var_subs_main
		)

		self.listOfSpecies.copy(
			submodel_instance.listOfSpecies,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions,
			replacements=var_subs_main
		)

		self.listOfReactions.copy(
			submodel_instance.listOfReactions,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions,
			replacements=var_subs_main,
			conversions=conv_factors,
			extent_conversion=submodel.getExtentConversionFactor(),
			time_conversion=submodel.getTimeConversionFactor()
		)

		self.listOfInitialAssignments.copy(
			submodel_instance.listOfInitialAssignments,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions,
			replacements=var_subs_main,
			conversions=conv_factors
		)

		self.listOfRules.copy(
			submodel_instance.listOfRules,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions,
			replacements=var_subs_main,
			conversions=conv_factors,
			time_conversion=submodel.getTimeConversionFactor()
		)

		self.listOfEvents.copy(
			submodel_instance.listOfEvents,
			prefix=prefix,
			subs=var_subs_submodel,
			deletions=deletions,
			replacements=var_subs_main,
			conversions=conv_factors,
			time_conversion=submodel.getTimeConversionFactor()
		)

	def getSubmodelInstance(self, submodel_ref):
		return self.__submodelInstances[submodel_ref]
