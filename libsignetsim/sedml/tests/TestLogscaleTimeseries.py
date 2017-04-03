#!/usr/bin/env python
""" TestSteadyStatesScan.py


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

from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.sedml.SedmlDocument import SedmlDocument

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir

class TestSteadyStatesScan(TestCase):
	""" Tests high level functions """


	def testFig4BPubli(self):

		testfiles_path = join(dirname(__file__), "files")
		if not isdir(testfiles_path):
			mkdir(testfiles_path)

		sedml_doc = SedmlDocument()

		simulation = sedml_doc.listOfSimulations.createOneStep()
		simulation.getAlgorithm().setCVODE()

		model = sedml_doc.listOfModels.createModel()
		model.setLanguageSbml()
		model.setSource("urn:miriam:biomodels.db:BIOMD0000000001")
		sbml_model = model.getSbmlModel()

		change = model.listOfChanges.createChangeAttribute()
		change.getTarget().setModelObject(sbml_model.listOfParameters.getBySbmlId("t2"), attribute="value")
		change.setNewValue(100.0)

		task = sedml_doc.listOfTasks.createTask()
		task.setModel(model)
		task.setSimulation(simulation)

		repeated_task = sedml_doc.listOfTasks.createRepeatedTask()
		repeated_task.setResetModel(False)

		uniform_range = repeated_task.listOfRanges.createUniformRange()
		uniform_range.setStart(0)
		uniform_range.setEnd(100)
		uniform_range.setNumberOfPoints(10)
		uniform_range.setLog()
		repeated_task.setRange(uniform_range)

		sub_task = repeated_task.listOfSubTasks.createSubTask()
		sub_task.setTask(task)
		sub_task.setOrder(1)

		data_time = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_time.setName("Time")
		var_time = data_time.listOfVariables.createVariable("time")
		var_time.setTask(repeated_task)
		var_time.setModel(model)
		var_time.setSymbolTime()
		data_time.getMath().setInternalMathFormula(var_time.getSympySymbol())

		data_basal = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_basal.setName("Basal")
		var_basal = data_basal.listOfVariables.createVariable("B")
		var_basal.setTask(repeated_task)
		var_basal.setModel(model)
		var_basal.setTarget(sbml_model.listOfSpecies.getBySbmlId("B"))
		data_basal.getMath().setInternalMathFormula(var_basal.getSympySymbol())

		data_basalAch = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_basalAch.setName("BasalACh")
		var_basalAch = data_basalAch.listOfVariables.createVariable("BL")
		var_basalAch.setTask(repeated_task)
		var_basalAch.setModel(model)
		var_basalAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("BL"))
		data_basalAch.getMath().setInternalMathFormula(var_basalAch.getSympySymbol())

		data_DLL = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_DLL.setName("DesensitisedACh2")
		var_DLL = data_DLL.listOfVariables.createVariable("DLL")
		var_DLL.setTask(repeated_task)
		var_DLL.setModel(model)
		var_DLL.setTarget(sbml_model.listOfSpecies.getBySbmlId("DLL"))
		data_DLL.getMath().setInternalMathFormula(var_DLL.getSympySymbol())

		data_ILL = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_ILL.setName("IntermediateACh2")
		var_ILL = data_ILL.listOfVariables.createVariable("ILL")
		var_ILL.setTask(repeated_task)
		var_ILL.setModel(model)
		var_ILL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ILL"))
		data_ILL.getMath().setInternalMathFormula(var_ILL.getSympySymbol())

		data_ALL = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_ALL.setName("ActiveACh2")
		var_ALL = data_ALL.listOfVariables.createVariable("ALL")
		var_ALL.setTask(repeated_task)
		var_ALL.setModel(model)
		var_ALL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ALL"))
		data_ALL.getMath().setInternalMathFormula(var_ALL.getSympySymbol())


		plot = sedml_doc.listOfOutputs.createPlot2D()
		curve_basal = plot.listOfCurves.createCurve()
		curve_basal.setXData(data_time)
		curve_basal.setYData(data_basal)

		curve_basalAch = plot.listOfCurves.createCurve()
		curve_basalAch.setXData(data_time)
		curve_basalAch.setYData(data_basalAch)

		curve_dll = plot.listOfCurves.createCurve()
		curve_dll.setXData(data_time)
		curve_dll.setYData(data_DLL)

		curve_ill = plot.listOfCurves.createCurve()
		curve_ill.setXData(data_time)
		curve_ill.setYData(data_ILL)

		curve_all = plot.listOfCurves.createCurve()
		curve_all.setXData(data_time)
		curve_all.setYData(data_ALL)

		# report = sedml_doc.listOfOutputs.createReport()
		# dataset_p = report.listOfDataSets.createDataSet()
		# dataset_p.setLabel("P")
		# dataset_p.setData(data_generator_p)
		#
		# sedml_doc.run()
		sedml_doc.writeSedmlToFile(join(testfiles_path, "BIOMD0000000001_curation_1.xml"))
		#
		# simulated_data = sedml_doc.listOfOutputs.getReports()[0].getData()["P"]
		# expected_data = [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]
		#
		# for i, data in enumerate(expected_data):
		# 	self.assertAlmostEqual(data, simulated_data[i])

		sedml_doc = SedmlDocument()
		sedml_doc.readSedmlFromFile(join(testfiles_path, "BIOMD0000000001_curation_1.xml"))


