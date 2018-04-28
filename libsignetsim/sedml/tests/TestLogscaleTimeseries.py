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

	This file is made for 'high level' tests, using various components

"""
from __future__ import division

from past.utils import old_div
from libsignetsim import SedmlDocument, Settings
from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir


class TestSteadyStatesScan(TestCase):
	""" Tests high level functions """


	def testFig4BPubli(self):

		testfiles_path = join(dirname(__file__), "files")

		sedml_doc = SedmlDocument()

		simulations = []

		simulation = sedml_doc.listOfSimulations.createUniformTimeCourse()
		simulation.setInitialTime(0)
		simulation.setOutputStartTime(0)
		simulation.setOutputEndTime(100)
		simulation.setNumberOfPoints(5)
		simulation.getAlgorithm().setCVODE()
		simulation.getAlgorithm().listOfAlgorithmParameters.setRelTol(1e-7)
		simulation.getAlgorithm().listOfAlgorithmParameters.setAbsTol(1e-30)

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

		data_time = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_time.setName("Time")
		var_time = data_time.listOfVariables.createVariable("time")
		var_time.setTask(task)
		var_time.setModel(model)
		var_time.setSymbolTime()
		data_time.getMath().setInternalMathFormula(var_time.getSympySymbol())

		# Let's try to first reproduce the Basal on the figure, aka the fraction of total receptors
		# So we need all vars to compute the fraction
		data_basal = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_basal.setName("Basal")

		data_basal_var_basal = data_basal.listOfVariables.createVariable("B")
		data_basal_var_basal.setTask(task)
		data_basal_var_basal.setModel(model)
		data_basal_var_basal.setTarget(sbml_model.listOfSpecies.getBySbmlId("B"))

		data_basal_var_basalAch = data_basal.listOfVariables.createVariable("BL")
		data_basal_var_basalAch.setTask(task)
		data_basal_var_basalAch.setModel(model)
		data_basal_var_basalAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("BL"))

		data_basal_var_DLL = data_basal.listOfVariables.createVariable("DLL")
		data_basal_var_DLL.setTask(task)
		data_basal_var_DLL.setModel(model)
		data_basal_var_DLL.setTarget(sbml_model.listOfSpecies.getBySbmlId("DLL"))

		data_basal_var_ILL = data_basal.listOfVariables.createVariable("ILL")
		data_basal_var_ILL.setTask(task)
		data_basal_var_ILL.setModel(model)
		data_basal_var_ILL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ILL"))

		data_basal_var_ALL = data_basal.listOfVariables.createVariable("ALL")
		data_basal_var_ALL.setTask(task)
		data_basal_var_ALL.setModel(model)
		data_basal_var_ALL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ALL"))

		t_formula = old_div(data_basal_var_basal.getSympySymbol(), (
			data_basal_var_basal.getSympySymbol()
			+ data_basal_var_basalAch.getSympySymbol()
			+ data_basal_var_DLL.getSympySymbol()
			+ data_basal_var_ILL.getSympySymbol()
			+ data_basal_var_ALL.getSympySymbol()
		))
		data_basal.getMath().setInternalMathFormula(t_formula)


		data_basalAch = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_basalAch.setName("BasalACh")

		data_basalAch_var_basal = data_basalAch.listOfVariables.createVariable("B")
		data_basalAch_var_basal.setTask(task)
		data_basalAch_var_basal.setModel(model)
		data_basalAch_var_basal.setTarget(sbml_model.listOfSpecies.getBySbmlId("B"))

		data_basalAch_var_basalAch = data_basalAch.listOfVariables.createVariable("BL")
		data_basalAch_var_basalAch.setTask(task)
		data_basalAch_var_basalAch.setModel(model)
		data_basalAch_var_basalAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("BL"))

		data_basalAch_var_DLL = data_basalAch.listOfVariables.createVariable("DLL")
		data_basalAch_var_DLL.setTask(task)
		data_basalAch_var_DLL.setModel(model)
		data_basalAch_var_DLL.setTarget(sbml_model.listOfSpecies.getBySbmlId("DLL"))

		data_basalAch_var_ILL = data_basalAch.listOfVariables.createVariable("ILL")
		data_basalAch_var_ILL.setTask(task)
		data_basalAch_var_ILL.setModel(model)
		data_basalAch_var_ILL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ILL"))

		data_basalAch_var_ALL = data_basalAch.listOfVariables.createVariable("ALL")
		data_basalAch_var_ALL.setTask(task)
		data_basalAch_var_ALL.setModel(model)
		data_basalAch_var_ALL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ALL"))

		t_formula = old_div(data_basalAch_var_basalAch.getSympySymbol(), (
			data_basalAch_var_basal.getSympySymbol()
			+ data_basalAch_var_basalAch.getSympySymbol()
			+ data_basalAch_var_DLL.getSympySymbol()
			+ data_basalAch_var_ILL.getSympySymbol()
			+ data_basalAch_var_ALL.getSympySymbol()
		))
		data_basalAch.getMath().setInternalMathFormula(t_formula)


		data_DLL = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_DLL.setName("DesensitisedACh2")

		data_DLL_var_basal = data_DLL.listOfVariables.createVariable("B")
		data_DLL_var_basal.setTask(task)
		data_DLL_var_basal.setModel(model)
		data_DLL_var_basal.setTarget(sbml_model.listOfSpecies.getBySbmlId("B"))

		data_DLL_var_basalAch = data_DLL.listOfVariables.createVariable("BL")
		data_DLL_var_basalAch.setTask(task)
		data_DLL_var_basalAch.setModel(model)
		data_DLL_var_basalAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("BL"))

		data_DLL_var_DLL = data_DLL.listOfVariables.createVariable("DLL")
		data_DLL_var_DLL.setTask(task)
		data_DLL_var_DLL.setModel(model)
		data_DLL_var_DLL.setTarget(sbml_model.listOfSpecies.getBySbmlId("DLL"))

		data_DLL_var_ILL = data_DLL.listOfVariables.createVariable("ILL")
		data_DLL_var_ILL.setTask(task)
		data_DLL_var_ILL.setModel(model)
		data_DLL_var_ILL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ILL"))

		data_DLL_var_ALL = data_DLL.listOfVariables.createVariable("ALL")
		data_DLL_var_ALL.setTask(task)
		data_DLL_var_ALL.setModel(model)
		data_DLL_var_ALL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ALL"))

		t_formula = old_div(data_DLL_var_DLL.getSympySymbol(), (
			data_DLL_var_basal.getSympySymbol()
			+ data_DLL_var_basalAch.getSympySymbol()
			+ data_DLL_var_DLL.getSympySymbol()
			+ data_DLL_var_ILL.getSympySymbol()
			+ data_DLL_var_ALL.getSympySymbol()
		))
		data_DLL.getMath().setInternalMathFormula(t_formula)


		data_ILL = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_ILL.setName("IntermediateACh2")

		data_ILL_var_basal = data_ILL.listOfVariables.createVariable("B")
		data_ILL_var_basal.setTask(task)
		data_ILL_var_basal.setModel(model)
		data_ILL_var_basal.setTarget(sbml_model.listOfSpecies.getBySbmlId("B"))

		data_ILL_var_basalAch = data_ILL.listOfVariables.createVariable("BL")
		data_ILL_var_basalAch.setTask(task)
		data_ILL_var_basalAch.setModel(model)
		data_ILL_var_basalAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("BL"))

		data_ILL_var_DLL = data_ILL.listOfVariables.createVariable("DLL")
		data_ILL_var_DLL.setTask(task)
		data_ILL_var_DLL.setModel(model)
		data_ILL_var_DLL.setTarget(sbml_model.listOfSpecies.getBySbmlId("DLL"))

		data_ILL_var_ILL = data_ILL.listOfVariables.createVariable("ILL")
		data_ILL_var_ILL.setTask(task)
		data_ILL_var_ILL.setModel(model)
		data_ILL_var_ILL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ILL"))

		data_ILL_var_ALL = data_ILL.listOfVariables.createVariable("ALL")
		data_ILL_var_ALL.setTask(task)
		data_ILL_var_ALL.setModel(model)
		data_ILL_var_ALL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ALL"))

		t_formula = old_div(data_ILL_var_ILL.getSympySymbol(), (
			data_ILL_var_basal.getSympySymbol()
			+ data_ILL_var_basalAch.getSympySymbol()
			+ data_ILL_var_DLL.getSympySymbol()
			+ data_ILL_var_ILL.getSympySymbol()
			+ data_ILL_var_ALL.getSympySymbol()
		))
		data_ILL.getMath().setInternalMathFormula(t_formula)


		data_ALL = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_ALL.setName("ActiveACh2")

		data_ALL_var_basal = data_ALL.listOfVariables.createVariable("B")
		data_ALL_var_basal.setTask(task)
		data_ALL_var_basal.setModel(model)
		data_ALL_var_basal.setTarget(sbml_model.listOfSpecies.getBySbmlId("B"))

		data_ALL_var_basalAch = data_ALL.listOfVariables.createVariable("BL")
		data_ALL_var_basalAch.setTask(task)
		data_ALL_var_basalAch.setModel(model)
		data_ALL_var_basalAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("BL"))

		data_ALL_var_DLL = data_ALL.listOfVariables.createVariable("DLL")
		data_ALL_var_DLL.setTask(task)
		data_ALL_var_DLL.setModel(model)
		data_ALL_var_DLL.setTarget(sbml_model.listOfSpecies.getBySbmlId("DLL"))

		data_ALL_var_ILL = data_ALL.listOfVariables.createVariable("ILL")
		data_ALL_var_ILL.setTask(task)
		data_ALL_var_ILL.setModel(model)
		data_ALL_var_ILL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ILL"))

		data_ALL_var_ALL = data_ALL.listOfVariables.createVariable("ALL")
		data_ALL_var_ALL.setTask(task)
		data_ALL_var_ALL.setModel(model)
		data_ALL_var_ALL.setTarget(sbml_model.listOfSpecies.getBySbmlId("ALL"))

		t_formula = old_div(data_ALL_var_ALL.getSympySymbol(), (
			data_ALL_var_basal.getSympySymbol()
			+ data_ALL_var_basalAch.getSympySymbol()
			+ data_ALL_var_DLL.getSympySymbol()
			+ data_ALL_var_ILL.getSympySymbol()
			+ data_ALL_var_ALL.getSympySymbol()
		))
		data_ALL.getMath().setInternalMathFormula(t_formula)



		plot = sedml_doc.listOfOutputs.createPlot2D()
		curve_basal = plot.listOfCurves.createCurve()
		curve_basal.setXData(data_time)
		curve_basal.setYData(data_basal)
		curve_basal.setLogX(True)

		curve_basalAch = plot.listOfCurves.createCurve()
		curve_basalAch.setXData(data_time)
		curve_basalAch.setYData(data_basalAch)
		curve_basalAch.setLogX(True)

		curve_dll = plot.listOfCurves.createCurve()
		curve_dll.setXData(data_time)
		curve_dll.setYData(data_DLL)
		curve_dll.setLogX(True)

		curve_ill = plot.listOfCurves.createCurve()
		curve_ill.setXData(data_time)
		curve_ill.setYData(data_ILL)
		curve_ill.setLogX(True)

		curve_all = plot.listOfCurves.createCurve()
		curve_all.setXData(data_time)
		curve_all.setYData(data_ALL)
		curve_all.setLogX(True)


		report = sedml_doc.listOfOutputs.createReport()

		dataset_time = report.listOfDataSets.createDataSet()
		dataset_time.setLabel("Time")
		dataset_time.setData(data_time)

		dataset_basal = report.listOfDataSets.createDataSet()
		dataset_basal.setLabel("Basal")
		dataset_basal.setData(data_basal)

		dataset_basalAch = report.listOfDataSets.createDataSet()
		dataset_basalAch.setLabel("BasalACh")
		dataset_basalAch.setData(data_basalAch)

		dataset_DLL = report.listOfDataSets.createDataSet()
		dataset_DLL.setLabel("DesensitisedACh2")
		dataset_DLL.setData(data_DLL)

		dataset_ILL = report.listOfDataSets.createDataSet()
		dataset_ILL.setLabel("IntermediateACh2")
		dataset_ILL.setData(data_ILL)

		dataset_ALL = report.listOfDataSets.createDataSet()
		dataset_ALL.setLabel("ActiveACh2")
		dataset_ALL.setData(data_ALL)
		sedml_doc.run()

		# expected_data = {
		# 	"Basal": [1.0, 0.8703929751604004, 0.7749423419177442, 0.6946061123069424, 0.597290529625008, 0.4537850318551511,
		#  0.34750139692209975, 0.29949244626945737, 0.22270499980202377, 0.10951146314675342, 0.03412836890172797,
		#  0.024200752996025095, 0.022706292875704824, 0.019314868585969504, 0.012743352308043987, 0.004557742803571135,
		#  0.000838864752742402],
		# 	"BasalACh": [0.0, 0.12733989706088109, 0.20860665566561312, 0.23515925558680748, 0.208278208041077, 0.1632517601817593,
		#  0.12918341396276756, 0.11193037804649376, 0.08324269397045204, 0.04095051744993127, 0.012785114865493191,
		#  0.009075094010791105, 0.00851472322023259, 0.007242960070971262, 0.004778682083793607, 0.0017091291129665094,
		#  0.00031457282942824776],
		# 	"DesensitisedACh2": [0.0, 5.276504575778524e-13, 3.331032690025042e-11, 1.3348713563479085e-09, 3.390793915547514e-08,
		#  5.913794319390883e-07, 7.374447747054566e-06, 6.638876496189277e-05, 0.00046273880818307436,
		#  0.0025754514927221668, 0.010801340789850395, 0.034193460998989275, 0.09266196884291755, 0.22816586990710194,
		#  0.49072979203151695, 0.8177845618016254, 0.9663717628010179],
		# 	"IntermediateACh2": [0.0, 7.928585437579911e-07, 1.7394771632477156e-05, 0.00023455456576278516, 0.002016484487472414,
		#  0.012106619410986482, 0.05107905183405494, 0.15467605453139202, 0.3705004603739618, 0.68727111950252,
		#  0.8914220977379401, 0.8960358851611324, 0.8418739633309424, 0.7161477843260169, 0.4725300197675206,
		#  0.16907495528569005, 0.031209549157480712],
		# 	"ActiveACh2": [0.0, 0.0022663349196470604, 0.016433607611699937, 0.070000076205616, 0.1924147439385037, 0.3708559971726711,
		#  0.47222876283333054, 0.43383473238769515, 0.32308910704537935, 0.15969144840807312, 0.050863077704988394,
		#  0.03649480683306223, 0.034243051730202576, 0.029128517109940463, 0.019218153809124724, 0.006873610996146915,
		#  0.0012652504593307923]
		# }
		#
		# simulated_data = sedml_doc.listOfOutputs.getReports()[0].getData()
		#
		#
		# for var, values in expected_data.items():
		# 	if var != "Time":
		# 		for i, value in enumerate(values):
		# 			self.assertAlmostEqual(value, simulated_data[var][i])

		sedml_doc.writeSedmlToFile(join(Settings.tempDirectory, "BIOMD0000000001_fig4b.xml"))
		sedml_doc = SedmlDocument()
		sedml_doc.readSedmlFromFile(join(Settings.tempDirectory, "BIOMD0000000001_fig4b.xml"))
		sedml_doc.run()
	#
	# def testFig4CPubli(self):
	# 	""" Here the tricky part is that we must integrate the first 20 seconds,
	# 		until the event (with whatever timescale I guess),
	# 		and then integrate 100s with a log scale
	#
	# 	 	Maybe and idea is to have a repeated task, containing :
	# 	 	- a simulation for the first 20s, with just two time points
	# 	 	- a repeated task, containing the log scale simulation
	#
	# 	 	Should work, but not sure how to just plot discarding the first simulation
	# 	"""
	# 	testfiles_path = join(dirname(__file__), "files")
	# 	if not isdir(testfiles_path):
	# 		mkdir(testfiles_path)
	#
	# 	sedml_doc = SedmlDocument()
	#
	#
	# 	simulation_init = sedml_doc.listOfSimulations.createUniformTimeCourse()
	# 	simulation_init.setInitialTime(0)
	# 	simulation_init.setOutputStartTime(20)
	# 	simulation_init.setOutputEndTime(20)
	# 	simulation_init.setNumberOfPoints(1)
	#
	# 	simulation_onestep = sedml_doc.listOfSimulations.createOneStep()
	# 	simulation_onestep.getAlgorithm().setCVODE()
	# 	simulation_onestep.getAlgorithm().listOfAlgorithmParameters.setRelTol(1e-6)
	# 	simulation_onestep.getAlgorithm().listOfAlgorithmParameters.setAbsTol(1e-30)
	#
	#
	# 	model = sedml_doc.listOfModels.createModel()
	# 	model.setLanguageSbml()
	# 	model.setSource("urn:miriam:biomodels.db:BIOMD0000000001")
	# 	sbml_model = model.getSbmlModel()
	#
	# 	task_init = sedml_doc.listOfTasks.createTask()
	# 	task_init.setModel(model)
	# 	task_init.setSimulation(simulation_init)
	#
	# 	task_onestep = sedml_doc.listOfTasks.createTask()
	# 	task_onestep.setModel(model)
	# 	task_onestep.setSimulation(simulation_onestep)
	#
	# 	task_logscale = sedml_doc.listOfTasks.createRepeatedTask()
	# 	task_logscale.setResetModel(False)
	#
	# 	uniform_range = task_logscale.listOfRanges.createUniformRange()
	# 	uniform_range.setStart(6e-5)
	# 	uniform_range.setEnd(1e+2)
	# 	uniform_range.setNumberOfPoints(15)
	# 	uniform_range.setLog()
	# 	task_logscale.setRange(uniform_range)
	#
	# 	sub_task_onestep = task_logscale.listOfSubTasks.createSubTask()
	# 	sub_task_onestep.setTask(task_onestep)
	# 	sub_task_onestep.setOrder(1)
	#
	# 	master_task = sedml_doc.listOfTasks.createRepeatedTask()
	# 	master_task.setResetModel(False)
	#
	# 	sub_task_init = master_task.listOfSubTasks.createSubTask()
	# 	sub_task_init.setTask(task_init)
	# 	sub_task_init.setOrder(1)
	#
	# 	sub_task_log = master_task.listOfSubTasks.createSubTask()
	# 	sub_task_log.setTask(task_logscale)
	# 	sub_task_log.setOrder(2)
	#
	#
	# 	data_time = sedml_doc.listOfDataGenerators.createDataGenerator()
	# 	data_time.setName("Time")
	# 	var_time = data_time.listOfVariables.createVariable("time")
	# 	var_time.setTask(master_task)
	# 	var_time.setModel(model)
	# 	var_time.setSymbolTime()
	# 	data_time.getMath().setInternalMathFormula(var_time.getSympySymbol())
	#
	#
	#
	# 	# Let's try to first reproduce the Basal on the figure, aka the fraction of total receptors
	# 	# So we need all vars to compute the fraction
	# 	data_basal = sedml_doc.listOfDataGenerators.createDataGenerator()
	# 	data_basal.setName("Basal")
	#
	#
	# 	data_basal_var_basal = data_basal.listOfVariables.createVariable("B")
	# 	data_basal_var_basal.setTask(master_task)
	# 	data_basal_var_basal.setModel(model)
	# 	data_basal_var_basal.setTarget(sbml_model.listOfSpecies.getBySbmlId("B"))
	#
	# 	data_basal_var_intermediate = data_basal.listOfVariables.createVariable("I")
	# 	data_basal_var_intermediate.setTask(master_task)
	# 	data_basal_var_intermediate.setModel(model)
	# 	data_basal_var_intermediate.setTarget(sbml_model.listOfSpecies.getBySbmlId("I"))
	#
	# 	data_basal_var_desensitised = data_basal.listOfVariables.createVariable("D")
	# 	data_basal_var_desensitised.setTask(master_task)
	# 	data_basal_var_desensitised.setModel(model)
	# 	data_basal_var_desensitised.setTarget(sbml_model.listOfSpecies.getBySbmlId("D"))
	#
	#
	# 	data_basal_var_intermediateAch = data_basal.listOfVariables.createVariable("IL")
	# 	data_basal_var_intermediateAch.setTask(master_task)
	# 	data_basal_var_intermediateAch.setModel(model)
	# 	data_basal_var_intermediateAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("IL"))
	#
	# 	data_basal_var_desensitisedAch = data_basal.listOfVariables.createVariable("DL")
	# 	data_basal_var_desensitisedAch.setTask(master_task)
	# 	data_basal_var_desensitisedAch.setModel(model)
	# 	data_basal_var_desensitisedAch.setTarget(sbml_model.listOfSpecies.getBySbmlId("DL"))
	#
	#
	# 	data_basal_var_desensitisedAch2 = data_basal.listOfVariables.createVariable("DLL")
	# 	data_basal_var_desensitisedAch2.setTask(master_task)
	# 	data_basal_var_desensitisedAch2.setModel(model)
	# 	data_basal_var_desensitisedAch2.setTarget(sbml_model.listOfSpecies.getBySbmlId("DLL"))
	#
	# 	data_basal_var_intermediateAch2 = data_basal.listOfVariables.createVariable("ILL")
	# 	data_basal_var_intermediateAch2.setTask(master_task)
	# 	data_basal_var_intermediateAch2.setModel(model)
	# 	data_basal_var_intermediateAch2.setTarget(sbml_model.listOfSpecies.getBySbmlId("ILL"))
	#
	# 	data_basal_var_activeAch2 = data_basal.listOfVariables.createVariable("ALL")
	# 	data_basal_var_activeAch2.setTask(master_task)
	# 	data_basal_var_activeAch2.setModel(model)
	# 	data_basal_var_activeAch2.setTarget(sbml_model.listOfSpecies.getBySbmlId("ALL"))
	#
	#
	# 	t_formula = data_basal_var_basal.getSympySymbol() / (
	# 		data_basal_var_basal.getSympySymbol()
	# 		+ data_basal_var_intermediate.getSympySymbol()
	# 		+ data_basal_var_desensitised.getSympySymbol()
	# 		+ data_basal_var_intermediateAch.getSympySymbol()
	# 		+ data_basal_var_desensitisedAch.getSympySymbol()
	# 		+ data_basal_var_desensitisedAch2.getSympySymbol()
	# 		+ data_basal_var_intermediateAch2.getSympySymbol()
	# 		+ data_basal_var_activeAch2.getSympySymbol()
	# 	)
	# 	data_basal.getMath().setInternalMathFormula(t_formula)
	#
	# 	report = sedml_doc.listOfOutputs.createReport()
	#
	# 	dataset_time = report.listOfDataSets.createDataSet()
	# 	dataset_time.setLabel("Time")
	# 	dataset_time.setData(data_time)
	#
	# 	dataset_basal = report.listOfDataSets.createDataSet()
	# 	dataset_basal.setLabel("Basal")
	# 	dataset_basal.setData(data_basal)
	#
	# 	# sedml_doc.run()
	# 	# simulated_data = sedml_doc.listOfOutputs.getReports()[0].getData()
	#
	# 	sedml_doc.writeSedmlToFile(join(testfiles_path, "BIOMD0000000001_fig4c.xml"))
	# 	sedml_doc = SedmlDocument()
	# 	sedml_doc.readSedmlFromFile(join(testfiles_path, "BIOMD0000000001_fig4c.xml"))
	#
		pass