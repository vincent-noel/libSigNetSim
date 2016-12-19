#!/usr/bin/env python
""" testSbmlCompatibility.py


	This file is made for 'high level' tests, using various components


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
from libsignetsim.simulation.SbmlTestCaseSimulation import SbmlTestCaseSimulation
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.settings.Settings import Settings

class TestSbmlCompatibility(unittest.TestCase):
	""" Tests high level functions """

	INCOMPATIBLE_CASES = [917, 918, 919, 936, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 967, 1000, 1121, 1122, 1123, 1214, 1215, 1217, 1160, 1169]
	INCOMPATIBLE_TAGS = ['CSymbolDelay', 'UncommonMathML', 'VolumeConcentrationRates', 'FastReaction', 'AlgebraicRule']
	INCOMPATIBLE_PACKAGES = ['fbc']


	def __init__(self, *args, **kwargs):

		unittest.TestCase.__init__(self, *args, **kwargs)

		self.testSuitePath = os.path.join(os.path.expanduser('~'),".test-suite/")
		self.testCasesPath = None
		self.testCasesTags = {}
		self.testCasesVersions = {}

	def testSbmlCompatibility(self):

		# if not os.path.exists(self.testSuitePath):
		present_dir = os.getcwd()
		cmd = "cd %s; wget http://downloads.sourceforge.net/project/sbml/test-suite/3.1.1/cases-archive/sbml-test-cases-2014-10-22.zip -O temp.zip; unzip -n temp.zip; rm temp.zip; cd %s" % (Settings.tempDirectory, present_dir)
		os.system(cmd)
		self.testSuitePath = Settings.tempDirectory
		Settings.sbmlTestCasesPath = "/tmp/"

		self.loadTestCasesInfo()
		self.assertEqual(self.runTestCases(), True)

		os.system("rm -r /tmp/cases/; rm -r test-suite-results")

	def loadTestCasesInfo(self, path=None):

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

		nb_success = 0
		nb_cases = 0
		for case_id, case_tags in self.testCasesTags.items():

			compatible = True
			for tag in case_tags:
				if tag.strip() in self.INCOMPATIBLE_TAGS:
					compatible = False

				elif (':' in tag.strip()
					and tag.strip().split(':')[0] in self.INCOMPATIBLE_PACKAGES):
					compatible = False

			if compatible and case_id not in self.INCOMPATIBLE_CASES:# in [390]:#[663, 664, 762, 569, 570, 575]:
				(t_success, t_cases) = self.runCase(case_id)
				nb_success += t_success
				nb_cases += t_cases

		print "\n> %d success out of %d tests (%.0f%%)" % (nb_success, nb_cases, nb_success*100/nb_cases)
		return nb_cases == nb_success

	def runCase(self, case):

		keep_files = False

		nb_cases = 0
		nb_success = 0

		case_path = os.path.join(self.testCasesPath, "%05d" % case)
		print "> Running case %05d (%s)" % (case, str(self.testCasesVersions[case]))

		for versions in self.testCasesVersions[case]:

			start = time.time()
			level_version = versions.split('.')
			level = int(level_version[0])
			version = int(level_version[1])

			sbml_doc = os.path.join(case_path, "%05d-sbml-l%dv%d.xml" % (
												case, level, version))

			if os.path.exists(sbml_doc):

				nb_cases += 1

				try:
					test = SbmlTestCaseSimulation(case, str(level), str(version), keep_files=keep_files)
					res_exec = test.run()

					if res_exec:

						nb_success += 1


					else:
						print ">> l%dv%d : ERROR (%.2gs)" % (level, version, time.time()-start)
				except:
					print ">> case %d, %dv%d : ERROR" % (int(case), level, version)

		return (nb_success, nb_cases)
