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

	This file is a simple example of reading and writing a basic NuML doc

"""

from libsignetsim import NuMLDocument, Settings

from unittest import TestCase
from os.path import join, dirname


class TestExample(TestCase):
	""" Tests high level functions """

	def testExample(self):

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

		numl_doc.writeNuMLToFile(join(Settings.tempDirectory, "example_copy.xml"))
		numl_doc = NuMLDocument()
		numl_doc.readNuMLFromFile(join(Settings.tempDirectory, "example_copy.xml"))
		numl_doc.writeNuMLToFile(join(Settings.tempDirectory, "example_copy_copy.xml"))





