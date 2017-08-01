#!/usr/bin/env python
""" ExperimentalData.py


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
import re

class ExperimentalData(object):

	def __init__(self, t=0, name="", value=0, value_dev=0, quantification_ratio=1):

		self.name = name
		self.t = t
		self.value = value
		self.value_dev = value_dev
		self.quantification_ratio = quantification_ratio

		self.steady_state = False
		self.min_steady_state = 0
		self.max_steady_state = 0


		# Not used ?
		self.variableName = ""
		self.variableId = None

	def readNuML(self, composite_value):
		self.t = float(composite_value.getIndexValue())
		res = re.match(
			r"/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species\[@name=\'(.*)\'\]",
			composite_value.getContents()[0].getIndexValue()
		)
		self.name = res.groups()[0]
		tuple = composite_value.getContents()[0].getContents()[0].getAtomicValues()


		self.value = tuple[0].getValue()
		self.value_dev = tuple[1].getValue()
		# print "t=%.2g, var=%s, value=%s, dev=%s" % (self.t, self.name, str(self.value), str(self.value_dev))

	def writeNuML(self, composite_value):

		time_desc = composite_value.getDescription().getContent()
		time_index = composite_value.createCompositeValue(time_desc, self.t)

		species_desc = time_desc.getContent()
		species_index = time_index.createCompositeValue(
			species_desc,
			"/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@name='%s']" % self.name
		)

		tuple_desc = species_desc.getContent()
		tuple = species_index.createTupleValue(tuple_desc)

		value_desc = tuple_desc.getAtomicDescriptions()[0]
		value = tuple.createAtomicValue(
			value_desc,
			self.value
		)

		std_desc = tuple_desc.getAtomicDescriptions()[1]
		std = tuple.createAtomicValue(
			std_desc,
			self.value_dev
		)

	def readDB(self, name, time, value, value_dev=0, steady_state=False,
				min_steady_state=0, max_steady_state=0, quantification_ratio=1):

		self.name = name
		self.t = time
		self.value = value
		self.value_dev = value_dev
		self.steady_state = steady_state
		if steady_state:
			self.min_steady_state = min_steady_state
			self.max_steady_state = max_steady_state
		self.quantification_ratio = quantification_ratio
