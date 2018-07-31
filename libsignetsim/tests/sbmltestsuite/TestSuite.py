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
from __future__ import print_function

from builtins import str
from builtins import object
from libsignetsim.tests.sbmltestsuite.TestSuiteCase import TestSuiteCase
from libsignetsim import Settings

from os.path import join, exists
from os import mkdir


class TestSuite(object):
	""" Tests SED-ML semantic test cases """

	TODO_CASES = [1490]
	TODO_VERSIONS = []
	TODO_TAGS = []

	INCOMPATIBLE_CASES = []

	INCOMPATIBLE_TAGS = [
		'CSymbolDelay'
	]

	# FastReations cases
	INCOMPATIBLE_CASES += [
		986, 987, 988,
		# <<<<<<< Updated upstream
		# =======
		# 		1282,# Case with boolean conversion
		# 		# 1490, 1491, 1494, # Cases with function returning a boolean (but not of a boolean type, since they are functions
		# >>>>>>> Stashed changes
		1398,# Variable stoichiometry, assigned by an event. Not today
		1399,# Two possible choices for initial values, not sure how to choose
		1565,# Problem evaluating sec(0.5) ??!! Also, takes ages
		1568,# Piecewise logic in a conservation law
		1569,# Four possible choices for initial values, not sure again
		1570,# Piecewise login, again
		1571,# Different output type for solve, should be easy
		1572, #Two possible initial conditions
	]

	# RandomEventExecution : This case count twice as much events as it should...
	INCOMPATIBLE_CASES += [1590]

	# VolumeConcentrationRates cases, something to do with event delay...
	INCOMPATIBLE_CASES += [1507, 1508, 1511]

	VERSION_INCOMPATIBLE_TAGS = {}

	COMPATIBLE_PACKAGES = ['comp']

	FAIL_ON_EXCEPTION = True

	def __init__(self, version):

		self.TODO_VERSIONS.append(version)
		self.testCasesPath = None
		self.testCasesTags = {}
		self.testCasesVersions = {}

		self.testExport = True
		Settings.verbose = 0

	def testSuiteRun(self):

		self.testCasesPath = Settings.sbmlTestCasesPath
		if not exists(join(Settings.tempDirectory, "test-suite-results")):
			mkdir(join(Settings.tempDirectory, "test-suite-results"))


		self.loadTestCasesInfo()
		return self.runTestCases()

	def loadTestCasesInfo(self, path=None):
		""" Loads cases info from the .cases-tags-map """


		cases_tags_map_file = join(self.testCasesPath,
											".cases-tags-map")

		if exists(cases_tags_map_file):
			cases_tags_map = open(cases_tags_map_file)
			tags_list = []
			for i, line in enumerate(cases_tags_map.readlines()):

				if i == 0:
					# List of tags. Ignoring
					tags_list = line.strip().split()

				elif line.startswith('+'):
					# Some kind of comment ?
					pass

				elif line.strip() == "README.md":
					pass

				else:
					case_data = line.strip().split()
					case_id = int(case_data[0])
					tags = []
					versions = []
					for data in case_data[1:]:
						if data in tags_list:
							tags.append(data)
						else:
							versions.append(data)

					self.testCasesTags.update({case_id: tags})
					self.testCasesVersions.update({case_id: versions})
			cases_tags_map.close()

	def runTestCases(self):

		nb_success = 0
		nb_cases = 0
		for case_id, case_tags in list(self.testCasesTags.items()):

			compatible = True
			if self.TODO_TAGS != []:
				todo_tag = False
			else:
				todo_tag = True
			for tag in case_tags:

				if tag.strip() in self.TODO_TAGS:
					todo_tag = True

				if tag.strip() in self.INCOMPATIBLE_TAGS:
					compatible = False

				elif (':' in tag.strip()
					  and tag.strip().split(':')[0] not in self.COMPATIBLE_PACKAGES):
					compatible = False

				for todo_version in self.TODO_VERSIONS:
					if todo_version in list(self.VERSION_INCOMPATIBLE_TAGS.keys()) and tag.strip() in self.VERSION_INCOMPATIBLE_TAGS[todo_version]:
						compatible = False


			if (compatible
				and case_id not in self.INCOMPATIBLE_CASES
				and todo_tag
				and (self.TODO_CASES == [] or case_id in self.TODO_CASES)
			):
				(t_success, t_cases) = self.runCase(case_id)
				nb_success += t_success
				nb_cases += t_cases


		if nb_cases > 0:
			print("\n> %d success out of %d tests (%.0f%%)" % (nb_success, nb_cases, nb_success*100/nb_cases))
		return nb_cases == nb_success

	def runCase(self, case):

		nb_cases = 0
		nb_success = 0

		for versions in self.testCasesVersions[case]:
			if self.TODO_VERSIONS == [] or versions in self.TODO_VERSIONS:

				print("> Running case %05d (%s)" % (case, str(self.TODO_VERSIONS)))

				level_version = versions.split('.')
				level = int(level_version[0])
				version = int(level_version[1])

				nb_cases += 1
				if self.FAIL_ON_EXCEPTION:
					if Settings.verbose >= 1 or Settings.verboseTiming >= 1:
						print("")

					test = TestSuiteCase(case, str(level), str(version), test_export=self.testExport)
					if test.run():
						nb_success += 1

				else:
					try:
						if Settings.verbose >= 1 or Settings.verboseTiming >= 1:
							print("")

						test = TestSuiteCase(case, str(level), str(version), test_export=self.testExport)
						if test.run():
							nb_success += 1
					except Exception as e:
						print(">> case %d, %dv%d : ERROR (%s)" % (int(case), level, version, e))

		return nb_success, nb_cases
