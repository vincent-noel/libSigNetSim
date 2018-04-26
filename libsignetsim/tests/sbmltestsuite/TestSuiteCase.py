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

	This file ...

"""
from __future__ import print_function

from builtins import str
from builtins import object
from libsignetsim import SedmlDocument, Settings

from os.path import join, exists, isdir
from os import mkdir

class TestSuiteCase(object):

	def __init__ (self, case_id, sbml_level, sbml_version, test_export=True):

		self.caseId = "%05d" % case_id
		self.sbmlLevel = sbml_level
		self.sbmlVersion = sbml_version
		self.testExport = test_export

		self.document = None
		self.sbmlIdToCheck = None
		self.loadSBMLTestSuiteSettings()
		self.loadTestCaseModel()

	def run(self):

		self.document.run()
		return self.checkResults()

	def runTestSuiteWraper(self):

		self.document.run()
		self.writeSbmlTestOutput()

	def getFilename(self):

		return join(Settings.sbmlTestCasesPath, "%s/%s-sbml-l%sv%s-sedml.xml" % (
				self.caseId, self.caseId, self.sbmlLevel, self.sbmlVersion)
		)

	def getResultsFilename(self):
		return join(Settings.sbmlTestResultsPath, "%s.csv" % self.caseId)

	def getExpectedResultsFilename(self):
		return join(Settings.sbmlTestCasesPath, "%s/%s-results.csv" % (
				self.caseId, self.caseId)
		)

	def getSettingsFilename(self):

		return join(Settings.sbmlTestCasesPath, "%s/%s-settings.txt" % (
				self.caseId, self.caseId)
		)

	def getTemporarySedmlFilename(self):
		return join(Settings.sbmlTestResultsPath, "%s/%s-sbml-l%sv%s-sedml.xml" % (self.caseId, self.caseId, self.sbmlLevel, self.sbmlVersion))

	def getTemporaryPath(self):
		return join(Settings.sbmlTestResultsPath, "%s" % self.caseId)

	def loadSBMLTestSuiteSettings(self):

		self.sbmlIdToCheck = []
		settings = open(self.getSettingsFilename(), 'r')

		for line in settings:

			if line.startswith("variables:"):
				res_split = line.split(":", 2)
				if len(res_split[1].strip()) > 0:
					res_split = res_split[1].strip().split(",")
					for t_var in res_split:
						self.sbmlIdToCheck.append(t_var.strip())

			if line.startswith("absolute:"):
				res_split = line.split(":", 2)
				self.testAbsTol = float(res_split[1].strip())

			if line.startswith("relative:"):
				res_split = line.split(":", 2)
				self.testRelTol = float(res_split[1].strip())

		settings.close()


	def loadTestCaseModel(self):

		self.document = SedmlDocument()
		self.document.readSedmlFromFile(self.getFilename())

		if self.testExport:

			if not isdir(self.getTemporaryPath()):
				mkdir(self.getTemporaryPath())

			self.document.writeSedmlToFile(
				self.getTemporarySedmlFilename(),
				write_sbml_dependencies=True
			)

			self.document = SedmlDocument()
			self.document.readSedmlFromFile(self.getTemporarySedmlFilename())

	def checkResults(self):

		expected_results = open(self.getExpectedResultsFilename())

		variables = []
		timepoints = []
		for i, line in enumerate(expected_results.readlines()):

			if i == 0:
				t_variables = line.strip().split(',')
				if t_variables[len(t_variables)-1] == '':
					t_variables = t_variables[:-1]
				variables = [t_variable.strip() for t_variable in t_variables]
			else:
				t_timepoints = line.strip().split(',')
				if t_timepoints[len(t_timepoints)-1] == '':
					t_timepoints = t_timepoints[:-1]
				timepoints.append([float(t_timepoint) for t_timepoint in t_timepoints])

		expected_results.close()

		simulated_results = self.document.listOfOutputs.getReports()[0].getData()

		result = True
		precisionError = False
		precisionErrorVariables = []

		for i_timepoint, timepoint in enumerate(timepoints):

			for i_var, var in enumerate(variables):

				t_expected_value = float(timepoint[i_var])

				if var == 'time':
					pass

				else:
					t_value = simulated_results[var][i_timepoint]

					if abs(t_value-t_expected_value) > (self.testAbsTol + self.testRelTol*abs(t_expected_value)):
						result = False
						precisionError = True
						if var not in precisionErrorVariables:
							precisionErrorVariables.append(var)
						# print "%.10g, %.10g (%10g, %.2g)" % (t_value, t_expected_value, abs(t_value-t_expected_value), simulated_results['Time'][i_timepoint])



		if precisionError:
			print("> Precision error in variables : %s" % str(precisionErrorVariables))
			return False

		return result

	def writeSbmlTestOutput(self):

		data = self.document.listOfOutputs.getReports()[0].getData()

		if not exists(Settings.sbmlTestResultsPath):
			mkdir(Settings.sbmlTestResultsPath)

		results_file = open(self.getResultsFilename(), 'w')
		# (traj_times, trajs) = self.rawData[0]

		# Writing header
		line = "time"

		for sbml_id in self.sbmlIdToCheck:
			line += ",%s" % sbml_id

		results_file.write(line + "\n")

		for i_t, t_time in enumerate(data['Time']):
			line = "%.14f" % t_time

			for sbml_id in self.sbmlIdToCheck:
				line += ",%.14f" % data[sbml_id][i_t]

			results_file.write(line + "\n")

		results_file.close()
