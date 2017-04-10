#!/usr/bin/env python
""" TestRunSedmls.py


	Test of combine archive : run all sedml files


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

from libsignetsim.settings.Settings import Settings
from libsignetsim.combine.CombineArchive import CombineArchive
from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir

class TestNoManifest(TestCase):

	def testNoManifest(self):

		ca = CombineArchive()
		ca.readArchive(join(join(dirname(__file__), "files"), "BIOMD0000000003.sedx"))
		ca.writeArchive(join(join(dirname(__file__), "files"), "BIOMD0000000003_fixed.sedx"))

		ca_fixed = CombineArchive()
		ca_fixed.readArchive(join(join(dirname(__file__), "files"), "BIOMD0000000003_fixed.sedx"))

		expected_results = {
			"BIOMD0000000003.sedx.xml": ("http://identifiers.org/combine.specifications/sed-ml.level-1.version-1", True),
			"model1.xml": ("http://identifiers.org/combine.specifications/sbml.level-2.version-4", False)
		}
		for file in ca_fixed.getListOfFiles():
			self.assertEqual(expected_results[file.getFilename()][0], file.getFormat())
			self.assertEqual(expected_results[file.getFilename()][1], file.isMaster())





