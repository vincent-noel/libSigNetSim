#!/usr/bin/env python
""" BiomodelsTestCaseSimulation.py


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
from os.path import join, exists
from os import mkdir
import numpy

class BiomodelsTestCaseSimulation(TimeseriesSimulation):

	CASES_PATH = "libsignetsim/tests/biomodels/cases"

	def __init__ (self, model_id, time_ech=0.01, time_max=10, abs_tol=1e-12, rel_tol=1e-6, test_export=False, keep_files=True):

		self.model_id = str(model_id)
		self.testExport = test_export
		self.timeMin = 0
		self.timeEch = time_ech
		self.timeMax = time_max
		self.testAbsTol = 1e-2
		self.testRelTol = 1e-6
		self.sbmlIdToPlot = []
		self.sbmlIdToPlotAmount = []
		self.sbmlIdToPlotConcentrations = []

		self.simulatedData = None
		self.expectedData = None

		self.loadTestCaseModel()
		self.loadTestCaseResults()
		# self.testExport= True
		TimeseriesSimulation.__init__(self,
										list_of_models=[self.model],
										time_min=self.timeMin,
										time_max=self.timeMax,
										time_ech=self.timeEch,
										abs_tol=abs_tol,
										rel_tol=rel_tol,
										keep_files=keep_files)

	def run(self):

		res_exec = TimeseriesSimulation.run(self)

		if res_exec == 0:
			self.simulatedData = self.rawData[0]
			# # print self.simulatedData
			# self.writeTestOutput()
			return self.checkResults()

		else:
			return -1


	def loadTestCaseModel(self):


		# if self.testExport:
		# 	self.model = self.loadSbmlModel_v2(self.getModelFilename(), modelDefinition=True)
		# 	t_filename = self.getTemporaryModelFilename()
		# 	t_document = self.model.parentDoc
		# 	t_document.writeSbml(t_filename)
		# 
		# 	self.model = self.loadSbmlModel_v2(t_filename)
		# 
		# else:
		self.model = self.loadSbmlModel_v2(self.getModelFilename())



	def loadTestCaseResults(self):

		results = open(self.getExpectedResultsFilename(), "r")
		header = results.readline()
		results.close()

		header = header[3:len(header)-2].split(',')
		header = [head.strip() for head in header]
		header = [head[1:len(head)-1] for head in header]

		for var in header:
			if var == "time":
				pass

			else:
				self.sbmlIdToPlot.append(var)
				self.sbmlIdToPlotConcentrations.append(var)

		data = numpy.genfromtxt(self.getExpectedResultsFilename(), skip_header=1)
		self.expectedData = (data[:,0], data[:,1:data.shape[0]-1])

	def getModelFilename(self):
		return "%s/%s/model.xml" % (self.CASES_PATH, self.model_id)

	def getExpectedResultsFilename(self):
		return "%s/%s/results.csv" % (self.CASES_PATH, self.model_id)

	def getResultsFilename(self):
		return "%s/%s/results_simulated.csv" % (self.CASES_PATH, self.model_id)
	#
	# def getTemporaryModelFilename(self):
	# 	return "%s/t_%s.xml" % (self.CASES_PATH, self.model_id)

	def checkResults(self):

		DEBUG = False
		precisionError = False

		if self.expectedData is not None and self.simulatedData is not None:

			(traj_times, trajs) = self.simulatedData
			(etraj_times, etrajs) = self.expectedData

			# for i, t in enumerate(traj_times):
			# 	if etraj_times[i] != t:
			# 		return -3


			for t in range(etrajs.shape[0]):

				if etraj_times[t] in traj_times:

					traj_pos = traj_times.index(etraj_times[t])

					for i_var in range(etrajs.shape[1]):

						t_expected_value = float(etrajs[t,i_var])
						var = self.sbmlIdToPlot[i_var]

						if var in self.listOfModels[0].listOfVariables.keys():
							t_var = self.listOfModels[0].listOfVariables[var]

							t_value = None
							if t_var.isSpecies():
								t_compartment = t_var.getCompartment()

								# Here we ask for the concentration but it's declared an amount
								if t_var.symbol.getPrettyPrintMathFormula() in self.sbmlIdToPlotConcentrations and t_var.hasOnlySubstanceUnits:
									t_value = trajs[t_var.symbol.getPrettyPrintMathFormula()][traj_pos]/trajs[t_compartment.symbol.getPrettyPrintMathFormula()][traj_pos]

								else:
									t_value = trajs[t_var.symbol.getPrettyPrintMathFormula()][traj_pos]
							else:
								t_value = trajs[t_var.symbol.getPrettyPrintMathFormula()][traj_pos]

							if abs(t_value-t_expected_value) > (self.testAbsTol + self.testRelTol*abs(t_expected_value)):
								if DEBUG:
									print "%s : %.10g, %.10g (%.0f%%, %.2g)" % (var, t_value, t_expected_value, abs(t_value-t_expected_value)/t_expected_value*100, etraj_times[t])

								precisionError = True
						else:
							print "cannot find variable %s" % var
			if precisionError:
				return -2
			return 0
		else:
			return -1


	def writeTestOutput(self):

		if self.rawData is not None:

			if not exists(join(self.CASES_PATH, "biomodels_signetsim")):
				mkdir(join(self.CASES_PATH, "biomodels_signetsim"))

			results_file = open(self.getResultsFilename(), 'w')
			(traj_times, trajs) = self.rawData[0]

			# Writing header
			line = "# ['time'"

			for sbml_id in self.sbmlIdToPlot:
				if sbml_id in self.listOfModels[0].listOfVariables.keys():
					t_var = self.listOfModels[0].listOfVariables[sbml_id]
					if t_var.isSpecies():
						line += ",'%s'" % sbml_id

			results_file.write(line + "]\n")

			for i_t, t_time in enumerate(traj_times):
				line = "%.14f" % t_time

				for sbml_id in self.sbmlIdToPlot:
					if sbml_id in self.listOfModels[0].listOfVariables.keys():
						t_var = self.listOfModels[0].listOfVariables[sbml_id]
						if t_var.isSpecies():

							t_compartment = t_var.getCompartment()
							# Here we ask for the concentration but it's declared an amount
							if t_var.getSbmlId() in self.sbmlIdToPlotConcentrations and t_var.hasOnlySubstanceUnits:
								line += " %.16g" % (trajs[t_var.getSbmlId()][i_t]/trajs[t_compartment.getSbmlId()][i_t])

							else:
								line += " %.16g" % trajs[t_var.getSbmlId()][i_t]

				results_file.write(line + "\n")

			results_file.close()
