#!/usr/bin/env python
""" TestSuite.py


	This file is made for the test cases from the SED-ML files
	in the SBmL Test Suite

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

from libsignetsim.tests.sbmltestsuite.TestSuite import TestSuite
from unittest import TestCase


class TestSuite_l3v2(TestCase):
	""" Tests SED-ML semantic test cases """

	def __init__(self, *args, **kwargs):

		TestCase.__init__(self, *args, **kwargs)

		self.testSuite = TestSuite('3.2')

	def testSuiteRun(self):

		self.assertTrue(self.testSuite.testSuiteRun())

