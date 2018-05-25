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


from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.numl.NuMLDocument import NuMLDocument
from libsignetsim.figure.SigNetSimFigure import SigNetSimFigure
from matplotlib.pyplot import show


class Experiment(object):

	def __init__ (self, name=""):

		self.listOfConditions = {}
		self.currentId = 0
		self.name = name
		self.notes = ""

	def createCondition(self, name=""):
		condition = ExperimentalCondition(name)
		self.addCondition(condition)
		return condition

	def addCondition(self, condition):
		self.listOfConditions.update({self.currentId: condition})
		self.currentId += 1

	def readNuMLFromFile(self, filename):

		numl_doc = NuMLDocument()
		numl_doc.readNuMLFromFile(filename)
		result = numl_doc.listOfResultComponents[0]
		data = result.getDimensions()[0]
		self.name = data.getIndexValue()
		self.notes = data.getNotes()

		for data_condition in data.getContents():
			condition = self.createCondition(data_condition.getIndexValue())
			condition.readNuML(data_condition)

	def writeNuMLToFile(self, filename):

		numl_doc = NuMLDocument()

		time_term = numl_doc.listOfOntologyTerms.createOntologyTerm()
		time_term.defineAsTime()

		concentration_term = numl_doc.listOfOntologyTerms.createOntologyTerm()
		concentration_term.defineAsConcentration()

		result = numl_doc.listOfResultComponents.createResultComponent()

		self.writeNuMLDescription(result)
		experiment = result.createCompositeValue(result.getDimensionsDescriptions()[0], self.name)

		if self.notes is not None and len(self.notes) > 0:
			experiment.setNotes(self.notes)

		for condition in list(self.listOfConditions.values()):
			t_condition = experiment.createCompositeValue(experiment.getDescription().getContent(), condition.name)

			condition.writeNuML(t_condition)
		numl_doc.writeNuMLToFile(filename)

	def writeNuMLDescription(self, result_component):

		desc_experiment = result_component.createCompositeDescription("Experiment", "string")
		desc_condition = desc_experiment.createCompositeDescription("Condition", "string")
		desc_type = desc_condition.createCompositeDescription("Data type", "string")
		desc_time = desc_type.createCompositeDescription("Time", "double")
		desc_species = desc_time.createCompositeDescription("Species", "xpath")
		desc_values = desc_species.createTupleDescription()
		desc_values.createAtomicDescription("Concentration", "double")
		desc_values.createAtomicDescription("Standard deviation", "double")


	def getMaxTime(self):

		max_time = 0
		for condition in list(self.listOfConditions.values()):
			if condition.getMaxTime() > max_time:
				max_time = condition.getMaxTime()

		return max_time


	def getTimes(self):
		times = []
		for condition in list(self.listOfConditions.values()):
			times += condition.getTimes()
		return list(set(times))

	def getTreatedVariables(self):
		species = []
		for condition in list(self.listOfConditions.values()):
			species += condition.getTreatedVariables()

		if len(species) > 1:
			return list(set(species))
		else:
			return species

	def getVariables(self):
		species = []
		for condition in list(self.listOfConditions.values()):
			species += condition.getVariables()

		if len(species) > 1:
			return list(set(species))
		else:
			return species


	def plot(self, figure=None, suffix="", marker="-"):

		if figure is None:
			figure = SigNetSimFigure()

		plots = []
		for condition in list(self.listOfConditions.values()):
			plots.append(condition.plot(figure, suffix=suffix, marker=marker))

		show()

		return plots

