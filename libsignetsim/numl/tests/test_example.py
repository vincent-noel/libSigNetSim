#!/usr/bin/env python
""" TestReadExample.py


	This file is a simple example of reading and writing a basic NuML doc


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

from libsignetsim.numl.NuMLDocument import NuMLDocument

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir

class TestExample(TestCase):
	""" Tests high level functions """

	def testExample(self):

		if not isdir(join(dirname(__file__), "files")):
			mkdir(join(dirname(__file__), "files"))

		numl_doc = NuMLDocument()
		numl_doc.readNuMLFromFile(join(join(dirname(__file__), "files"), "example.xml"))

		# Trying to reproduce the example 5.2 from the specification,
		# but libnuml doesn't allow a tuple description as the root description,
		# seems like we need a composite description in the middle
		result = numl_doc.listOfResultComponents.createResultComponent()
		result.setId("main_fitting_result")
		main = result.createCompositeDescription(name=None, index_type="double")
		tuple = main.createTupleDescription()
		objective_value = tuple.createAtomicDescription("Objective value", "float")
		root_square_mean = tuple.createAtomicDescription("Root mean square", "float")
		standard_deviation = tuple.createAtomicDescription("Standard deviation", "float")

		main_value = result.createCompositeValue(main, index_value="0")
		tuple_value = main_value.createTupleValue(tuple)
		tuple_value.createAtomicValue(objective_value, 12.5015)
		tuple_value.createAtomicValue(root_square_mean, 0.158123)
		tuple_value.createAtomicValue(standard_deviation, 0.159242)

		numl_doc.writeNuMLToFile(join(join(dirname(__file__), "files"), "example_copy.xml"))
		numl_doc = NuMLDocument()
		numl_doc.readNuMLFromFile(join(join(dirname(__file__), "files"), "example_copy.xml"))
		numl_doc.writeNuMLToFile(join(join(dirname(__file__), "files"), "example_copy_copy.xml"))





