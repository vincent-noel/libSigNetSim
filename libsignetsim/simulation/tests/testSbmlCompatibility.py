#!/usr/bin/env python
""" testSbmlCompatibility.py


	This file is made for the semantic test cases from the SBML Test Suite

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


import unittest, os, time
from libsignetsim.model.Model import Model
from libsignetsim.simulation.tests.SbmlTestCaseSimulation import SbmlTestCaseSimulation
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.settings.Settings import Settings
from multiprocessing import cpu_count


class TestSbmlCompatibility(unittest.TestCase):
	""" Tests SBML semantic test cases """


	TODO_CASES = []
	TODO_VERSIONS = []
	TODO_TAGS = []#['EventIsNotPersistent', 'EventIsPersistent', 'EventNoDelay', 'EventPriority', 'EventT0Firing', 'EventUsesAssignmentTimeValues', 'EventUsesTriggerTimeValues', 'EventWithDelay']

	INCOMPATIBLE_CASES = [962, 987, 988]#962, Not compatible with ubuntu:precise, others not solved yet
	INCOMPATIBLE_TAGS = ['CSymbolDelay']

	COMPATIBLE_PACKAGES = ['comp']

	SEMANTIC_CASES_LINK = "http://downloads.sourceforge.net/project/sbml/test-suite/3.2.0/case-archives/sbml-semantic-test-cases-2016-07-27.zip"

	def __init__(self, *args, **kwargs):

		unittest.TestCase.__init__(self, *args, **kwargs)

		self.testSuitePath = os.path.join(os.path.expanduser('~'),".test-suite/")
		self.testCasesPath = None
		self.testCasesTags = {}
		self.testCasesVersions = {}
		self.nbCores = None
		self.keepFiles = True
		self.testExport = True
		Settings.verbose = 0


	def testSbmlCompatibility(self):

		self.testSuitePath = Settings.tempDirectory
		Settings.sbmlTestCasesPath = "/tmp/"
		if not os.path.exists(os.path.join(self.testSuitePath, "test-suite-results")):
			os.mkdir(os.path.join(self.testSuitePath, "test-suite-results"))
		if not os.path.exists(os.path.join(self.testSuitePath, "cases")):
			present_dir = os.getcwd()
			cmd = "cd %s; wget %s -O temp.zip; unzip -nq temp.zip; rm temp.zip; cd %s" % (Settings.tempDirectory, self.SEMANTIC_CASES_LINK, present_dir)
			os.system(cmd)

		self.loadTestCasesInfo()
		self.assertEqual(self.runTestCases(), True)


	def loadTestCasesInfo(self, path=None):
		""" Loads cases info from the .cases-tags-map """

		self.testCasesPath = os.path.join(
								os.path.join(self.testSuitePath, "cases")
								, "semantic")

		cases_tags_map_file = os.path.join(self.testCasesPath,
											".cases-tags-map")

		if os.path.exists(cases_tags_map_file):
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

		self.nbCores = cpu_count()


		nb_success = 0
		nb_cases = 0
		for case_id, case_tags in self.testCasesTags.items():

			compatible = True
			todoTag = False

			for tag in case_tags:
				if tag.strip() in self.TODO_TAGS:
					todoTag = True

				if tag.strip() in self.INCOMPATIBLE_TAGS:
					compatible = False

				elif (':' in tag.strip()
					and tag.strip().split(':')[0] not in self.COMPATIBLE_PACKAGES):
					compatible = False

			if compatible and case_id not in self.INCOMPATIBLE_CASES and (self.TODO_CASES == [] or case_id in self.TODO_CASES) and (self.TODO_TAGS == [] or todoTag):# in [390]:#[663, 664, 762, 569, 570, 575]:
				(t_success, t_cases) = self.runCase(case_id)
				nb_success += t_success
				nb_cases += t_cases

		if nb_cases > 0:
			print "\n> %d success out of %d tests (%.0f%%)" % (nb_success, nb_cases, nb_success*100/nb_cases)
		return nb_cases == nb_success


	def runCase(self, case):

		nb_cases = 0
		nb_success = 0

		case_path = os.path.join(self.testCasesPath, "%05d" % case)
		print "> Running case %05d (%s)" % (case, str(self.testCasesVersions[case]))
		results = [None]*len(self.testCasesVersions[case])


		for versions in self.testCasesVersions[case]:
			if self.TODO_VERSIONS == [] or versions in self.TODO_VERSIONS:
				start = time.time()
				level_version = versions.split('.')
				level = int(level_version[0])
				version = int(level_version[1])

				sbml_doc = os.path.join(case_path, "%05d-sbml-l%dv%d.xml" % (
													case, level, version))

				if os.path.exists(sbml_doc):

					nb_cases += 1


					# try:
					if Settings.verbose >= 1 or Settings.verboseTiming >= 1:
						print ""
					test = SbmlTestCaseSimulation(case, str(level), str(version), test_export=self.testExport, keep_files=self.keepFiles)
					res_exec = test.run()

					if res_exec:
						nb_success += 1
						# print ">> l%dv%d : OK (%.2gs)" % (level, version, time.time()-start)

					else:
						print ">> l%dv%d : ERROR (%.2gs)" % (level, version, time.time()-start)

					# except Exception as e:
					# 	print ">> case %d, %dv%d : ERROR (%s)" % (int(case), level, version, e)

		return (nb_success, nb_cases)

	def runIndividualCase(self, case, level, version, results, index):
		test = SbmlTestCaseSimulation(case, str(level), str(version), keep_files=self.keepFiles)
		results[index] = test.run()
