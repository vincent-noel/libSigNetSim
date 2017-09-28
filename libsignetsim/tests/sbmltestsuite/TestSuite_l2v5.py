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

	This file is made for the test cases from the SED-ML files
	in the SBmL Test Suite

"""

from libsignetsim.tests.sbmltestsuite.TestSuite import TestSuite
from unittest import TestCase


class TestSuite_l2v5(TestCase):
	""" Tests SED-ML semantic test cases """

	def __init__(self, *args, **kwargs):

		TestCase.__init__(self, *args, **kwargs)

		self.testSuite = TestSuite('2.5')

	def testSuiteRun(self):

		self.assertTrue(self.testSuite.testSuiteRun())

