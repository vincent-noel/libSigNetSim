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

class TestRunSedmls(TestCase):

	def testRunSedmls(self):

		ca = CombineArchive()
		ca.readFile(join(join(dirname(__file__), "files"), "00001.omex"))
		sedmls = ca.runAllSedmls()
		for sedml in sedmls:
			self.assertTrue(sedml.listOfOutputs.getReports() is not None)

	def testMasterSedml(self):

		ca = CombineArchive()
		ca.readFile(join(join(dirname(__file__), "files"), "00001.omex"))
		sedml = ca.runMasterSedml()
		self.assertTrue(sedml.listOfOutputs.getReports() is not None)






