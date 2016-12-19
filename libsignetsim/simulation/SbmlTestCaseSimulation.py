#!/usr/bin/env python
""" SbmlTestCaseSimulation.py


	This file ...


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

from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula

from os.path import join, expanduser, exists
from os import mkdir

class SbmlTestCaseSimulation(TimeseriesSimulation):

	def __init__ (self, case_id, sbml_level, sbml_version, test_export=False, keep_files=True):#Settings.simulationKeepFiles):

		self.caseId = "%05d" % case_id
		self.sbmlLevel = sbml_level
		self.sbmlVersion = sbml_version
		self.testExport = test_export
		self.model = None
		self.timeMin = None
		self.timeEch = None
		self.timeMax = None
		self.testAbsTol = 1e-8
		self.testRelTol = 1e-6
		self.sbmlIdToPlot = []
		self.sbmlIdToPlotAmount = []
		self.sbmlIdToPlotConcentrations = []

		self.loadSBMLTestSuiteSettings()
		self.loadTestCaseModel()

		TimeseriesSimulation.__init__(self,
										list_of_models=[self.model],
										time_min=self.timeMin,
										time_max=self.timeMax,
										time_ech=self.timeEch,
										abs_tol=min(self.testAbsTol/1000, 1e-8),
										rel_tol=min(self.testRelTol/1000, 1e-6),
										keep_files=keep_files)


	def runTestSuiteWraper(self):

		res_exec = TimeseriesSimulation.run(self)
		self.writeSbmlTestOutput()


	def run(self):

		res_exec = TimeseriesSimulation.run(self)
		res_compare = False
		if res_exec == 0:
			return self.checkResults()

		else:
			print "Simulation failed !"
			return res_exec == 0

	def loadTestCaseModel(self):


		if self.testExport:
			self.model = self.loadSbmlModel_v2(self.getModelFilename(), modelDefinition=True)
			t_filename = self.getTemporaryModelFilename()
			t_document = self.model.parentDoc
			t_document.writeSbml(t_filename)

			self.model = self.loadSbmlModel_v2(t_filename)
		else:
			# print "opening %s" % self.getModelFilename()
			self.model = self.loadSbmlModel_v2(self.getModelFilename())



	def getModelFolder(self):

		return join(Settings.sbmlTestCasesPath, "cases/semantic/%s/" % (self.caseId))



	def getModelFilename(self):

		return join(Settings.sbmlTestCasesPath, "cases/semantic/%s/%s-sbml-l%sv%s.xml" % (
				self.caseId, self.caseId, self.sbmlLevel, self.sbmlVersion)
		)


	def getSettingsFilename(self):

		return join(Settings.sbmlTestCasesPath, "cases/semantic/%s/%s-settings.txt" % (
				self.caseId, self.caseId)
		)


	def getResultsFilename(self):
		return join(Settings.sbmlTestResultsPath, "%s.csv" % self.caseId)

	def getExpectedResultsFilename(self):
		return join(Settings.sbmlTestCasesPath, "cases/semantic/%s/%s-results.csv" % (
				self.caseId, self.caseId)
		)


	def getTemporaryModelFilename(self):
		return join(Settings.sbmlTestResultsPath, "test-suite-results/%s.xml" % self.caseId)


	def loadSBMLTestSuiteSettings(self):

		settings = open(self.getSettingsFilename(), 'r')

		for line in settings:

			if line.startswith("start:"):
				res_split = line.split(":", 2)
				self.timeMin = float(res_split[1].strip())

			if line.startswith("duration:"):
				res_split = line.split(":", 2)
				self.timeMax = float(res_split[1].strip()) + self.timeMin

			if line.startswith("steps:"):
				res_split = line.split(":", 2)
				self.timeEch = (self.timeMax - self.timeMin)/int(res_split[1].strip())

			if line.startswith("variables:"):
				res_split = line.split(":", 2)
				if len(res_split[1].strip()) > 0:
					res_split = res_split[1].strip().split(",")
					for t_var in res_split:
						self.sbmlIdToPlot.append(t_var.strip())

			if line.startswith("amount:"):
				res_split = line.split(":", 2)
				if len(res_split[1].strip()) > 0:
					res_split = res_split[1].strip().split(",")
					for t_var in res_split:
						self.sbmlIdToPlotAmount.append(t_var.strip())

			if line.startswith("concentration:"):
				res_split = line.split(":", 2)
				if len(res_split[1].strip()) > 0:
					res_split = res_split[1].strip().split(",")
					for t_var in res_split:
						self.sbmlIdToPlotConcentrations.append(t_var.strip())

			if line.startswith("absolute:"):
				res_split = line.split(":", 2)
				self.testAbsTol = float(res_split[1].strip())

			if line.startswith("relative:"):
				res_split = line.split(":", 2)
				self.testRelTol = float(res_split[1].strip())

		settings.close()

	def checkResults(self):

		expected_results = open(self.getExpectedResultsFilename())
		result = True

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

		if self.rawData is not None and len(self.rawData) > 0:
			(traj_times, trajs) = self.rawData[0]

			showAlert = False
			timeError = False
			for i_timepoint, timepoint in enumerate(timepoints):

				for i_var, var in enumerate(variables):

					t_expected_value = float(timepoint[i_var])

					if var in self.listOfModels[0].listOfVariables.keys():
						t_var = self.listOfModels[0].listOfVariables[var]

						t_value = None
						if t_var.isSpecies():

							t_compartment = t_var.getCompartment()
							# Here we ask for the concentration but it's declared an amount
							if t_var.symbol.getPrettyPrintMathFormula() in self.sbmlIdToPlotConcentrations and t_var.hasOnlySubstanceUnits:
								t_value = trajs[t_var.symbol.getPrettyPrintMathFormula()][i_timepoint]/trajs[t_compartment.symbol.getPrettyPrintMathFormula()][i_timepoint]

							# Here we ask for an amout but it's declared a concentration
							elif t_var.symbol.getPrettyPrintMathFormula() in self.sbmlIdToPlotAmount and not t_var.hasOnlySubstanceUnits:
								# print "Yeah we need to plot the amount (%s)= %.5g" % (t_var.getSbmlId(),(trajs[t_var.getSbmlId()][i_t]*trajs[t_compartment.getSbmlId()][i_t]) )
								t_value = trajs[t_var.symbol.getPrettyPrintMathFormula()][i_timepoint]*trajs[t_compartment.symbol.getPrettyPrintMathFormula()][i_timepoint]

							else:
								t_value = trajs[t_var.symbol.getPrettyPrintMathFormula()][i_timepoint]
						else:
							# print len(trajs[t_var.getSbmlId()])
							# print len(timepoints)

							t_value = trajs[t_var.symbol.getPrettyPrintMathFormula()][i_timepoint]


	# T_a stand for the absolute tolerance for a test case,

	# T_r stand for the relative tolerance for a test case,

	# C_ij stand for the expected correct value for row i, column j, of
	# the result data set for the test case

	# U_ij stand for the corresponding value produced by a given
	# software simulation system run by the user

	# These absolute and relative tolerances are used in the following way:
	# a data point U_ij is considered to be within tolerances if and only if
	# the following expression is true:

	#            |C_ij - U_ij| <= (T_a + T_r * |C_ij|)

						if abs(t_value-t_expected_value) > (self.testAbsTol + self.testRelTol*t_expected_value):
							result = False
							showAlert = True
							# print "%.10g, %.10g (%10g, abs)" % (t_value, t_expected_value, abs(t_value-t_expected_value))

					elif var == 'time':
						if traj_times[i_timepoint] != t_expected_value:
							result = False
							timeError = True
							# print "TIME !!!!!!!!!!!!!!!!!!"
					else:
						print "cannot find variable %s" % var

			if showAlert:
				print "precision error"
			if timeError:
				print "time error"
				# print variables
				# print trajs.keys()
				# print self.listOfModels[0].listOfVariables.keys()
				# print traj_times
				# print [timepoint[variables.index('time')] for timepoint in timepoints]
				# for i_var, var in enumerate(variables):
				# 	if var != 'time':
				# 		t_var = self.listOfModels[0].listOfVariables[var]
				# 		print ""
				# 		print trajs[t_var.getSbmlId()]
				# 		print [timepoint[variables.index(var)] for timepoint in timepoints]


		else:
			# print "Something wrong with rawData"
			result = False





		return result

	def writeSbmlTestOutput(self):

		if self.rawData is not None:

			if not exists(Settings.sbmlTestResultsPath):
				mkdir(Settings.sbmlTestResultsPath)

			results_file = open(self.getResultsFilename(), 'w')
			(traj_times, trajs) = self.rawData[0]

			# Writing header
			line = "time"

			for sbml_id in self.sbmlIdToPlot:
				if sbml_id in self.listOfModels[0].listOfVariables.keys():
					t_var = self.listOfModels[0].listOfVariables[sbml_id]
					line += ",%s" % t_var.getSbmlId()

			results_file.write(line + "\n")

			for i_t, t_time in enumerate(traj_times):
				line = "%.14f" % t_time

				for sbml_id in self.sbmlIdToPlot:
					if sbml_id in self.listOfModels[0].listOfVariables.keys():
						t_var = self.listOfModels[0].listOfVariables[sbml_id]
						if t_var.isSpecies():

							t_compartment = t_var.getCompartment()
							# Here we ask for the concentration but it's declared an amount
							if t_var.getSbmlId() in self.sbmlIdToPlotConcentrations and t_var.hasOnlySubstanceUnits:
								line += ",%.14f" % (trajs[t_var.getSbmlId()][i_t]/trajs[t_compartment.getSbmlId()][i_t])

							# Here we ask for an amout but it's declared a concentration
							elif t_var.getSbmlId() in self.sbmlIdToPlotAmount and not t_var.hasOnlySubstanceUnits:
								# print "Yeah we need to plot the amount (%s)= %.5g" % (t_var.getSbmlId(),(trajs[t_var.getSbmlId()][i_t]*trajs[t_compartment.getSbmlId()][i_t]) )
								line += ",%.14f" % (trajs[t_var.getSbmlId()][i_t]*trajs[t_compartment.getSbmlId()][i_t])

							else:
								line += ",%.14f" % trajs[t_var.getSbmlId()][i_t]
						else:
							line += ",%.14f" % trajs[t_var.getSbmlId()][i_t]

				results_file.write(line + "\n")

			results_file.close()
