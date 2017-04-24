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

from libsignetsim.tests.sbmltestsuite.TestSuiteCase import TestSuiteCase
from libsignetsim.settings.Settings import Settings

from os.path import join, expanduser, exists
from os import getcwd, mkdir, system


class TestSuite(object):
	""" Tests SED-ML semantic test cases """

	TODO_CASES = [197]
	TODO_VERSIONS = []
	TODO_TAGS = []
	INCOMPATIBLE_CASES = []
	INCOMPATIBLE_TAGS = ['CSymbolDelay', 'FastReactions']

	COMPATIBLE_PACKAGES = ['comp']

	SEMANTIC_CASES_LINK = "http://downloads.sourceforge.net/project/sbml/test-suite/3.2.0/case-archives/sbml-semantic-test-cases-2016-07-27.zip"

	def __init__(self, version):

		self.TODO_VERSIONS.append(version)
		self.testSuitePath = None
		self.testCasesPath = None
		self.testCasesTags = {}
		self.testCasesVersions = {}

		self.testExport = True
		Settings.verbose = 0

	def testSuiteRun(self):

		self.testSuitePath = Settings.tempDirectory
		Settings.sbmlTestCasesPath = "/tmp/"
		if not exists(join(self.testSuitePath, "test-suite-results")):
			mkdir(join(self.testSuitePath, "test-suite-results"))
		if not exists(join(self.testSuitePath, "cases")):
			present_dir = getcwd()
			cmd = "cd %s; wget %s -O temp.zip; unzip -nq temp.zip; rm temp.zip; cd %s" % (
				Settings.tempDirectory, self.SEMANTIC_CASES_LINK, present_dir
			)
			system(cmd)

		self.loadTestCasesInfo()
		return self.runTestCases()

	def loadTestCasesInfo(self, path=None):
		""" Loads cases info from the .cases-tags-map """

		self.testCasesPath = join(
								join(self.testSuitePath, "cases")
								, "semantic")

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
		for case_id, case_tags in self.testCasesTags.items():

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

			if (compatible
				and case_id not in self.INCOMPATIBLE_CASES
				and todo_tag
				and (self.TODO_CASES == [] or case_id in self.TODO_CASES)
			):
				(t_success, t_cases) = self.runCase(case_id)
				nb_success += t_success
				nb_cases += t_cases


		if nb_cases > 0:
			print "\n> %d success out of %d tests (%.0f%%)" % (nb_success, nb_cases, nb_success*100/nb_cases)
		return nb_cases == nb_success

	def runCase(self, case):

		nb_cases = 0
		nb_success = 0

		for versions in self.testCasesVersions[case]:
			if self.TODO_VERSIONS == [] or versions in self.TODO_VERSIONS:

				print "> Running case %05d (%s)" % (case, str(self.TODO_VERSIONS))

				level_version = versions.split('.')
				level = int(level_version[0])
				version = int(level_version[1])

				nb_cases += 1

				# try:
				if Settings.verbose >= 1 or Settings.verboseTiming >= 1:
					print ""

				test = TestSuiteCase(case, str(level), str(version), test_export=self.testExport)
				if test.run():
					nb_success += 1

				# except Exception as e:
				# 	print ">> case %d, %dv%d : ERROR (%s)" % (int(case), level, version, e)

		return nb_success, nb_cases
