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

from libsignetsim import SbmlDocument, SedmlDocument, Settings

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir, getcwd

class TestSteadyStatesScan(TestCase):
	""" Tests high level functions """


	def testExampleSpecification(self):

		testfiles_path = join(dirname(join(getcwd(), __file__)), "files")

		if not isdir(testfiles_path):
			mkdir(testfiles_path)

		# Setting up the model
		sbml_doc = SbmlDocument()
		m = sbml_doc.model
		m.setName("Enzymatic Reaction")

		e = m.listOfSpecies.new("E")
		s = m.listOfSpecies.new("S")
		p = m.listOfSpecies.new("P")

		vmax = m.listOfParameters.new("vmax")
		km = m.listOfParameters.new("km")

		r = m.listOfReactions.new("Enzymatic reaction")
		r.listOfReactants.add(s)
		r.listOfModifiers.add(e)
		r.listOfProducts.add(p)
		r.kineticLaw.setPrettyPrintMathFormula("vmax*E*S/(km+S)")

		e.setValue(10)
		s.setValue(12)
		p.setValue(0)
		vmax.setValue(0.211)
		km.setValue(1.233)

		sbml_filename = join(Settings.tempDirectory, "enzymatic.xml")
		sbml_doc.writeSbmlToFile(sbml_filename)

		sedml_doc = SedmlDocument()

		simulation = sedml_doc.listOfSimulations.createSteadyState()
		simulation.getAlgorithm().setKinSol()

		model = sedml_doc.listOfModels.createModel()
		model.setLanguageSbml()
		model.setSource(sbml_filename)

		task = sedml_doc.listOfTasks.createTask()
		task.setModel(model)
		task.setSimulation(simulation)

		repeated_task = sedml_doc.listOfTasks.createRepeatedTask()
		repeated_task.setResetModel(True)

		uniform_range = repeated_task.listOfRanges.createUniformRange()
		uniform_range.setStart(0)
		uniform_range.setEnd(100)
		uniform_range.setNumberOfPoints(5)
		uniform_range.setLinear()
		repeated_task.setRange(uniform_range)

		set_value = repeated_task.listOfSetValueChanges.createSetValue()
		set_value.setModel(model)
		set_value.getTarget().setModelObject(s)
		set_value.setRange(uniform_range)
		set_value.getMath().setInternalMathFormula(uniform_range.getSymbol())

		sub_task = repeated_task.listOfSubTasks.createSubTask()
		sub_task.setTask(task)
		sub_task.setOrder(1)

		data_generator_p = sedml_doc.listOfDataGenerators.createDataGenerator()
		var_p = data_generator_p.listOfVariables.createVariable("P")
		var_p.setName("P")
		var_p.setTask(repeated_task)
		var_p.setModel(model)
		var_p.setTarget(p)
		data_generator_p.getMath().setInternalMathFormula(var_p.getSympySymbol())

		data_generator_s = sedml_doc.listOfDataGenerators.createDataGenerator()
		var_s = data_generator_s.listOfVariables.createVariable("S")
		var_s.setName("S")
		var_s.setTask(repeated_task)
		var_s.setModel(model)
		var_s.setTarget(s)
		data_generator_s.getMath().setInternalMathFormula(var_s.getSympySymbol())

		plot = sedml_doc.listOfOutputs.createPlot2D()
		curve_s = plot.listOfCurves.createCurve()
		curve_s.setXData(data_generator_s)
		curve_s.setYData(data_generator_p)

		report = sedml_doc.listOfOutputs.createReport()
		dataset_p = report.listOfDataSets.createDataSet()
		dataset_p.setLabel("P")
		dataset_p.setData(data_generator_p)

		sedml_doc.run()

		simulated_data = sedml_doc.listOfOutputs.getReports()[0].getData()["P"]
		expected_data = [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]

		# print "Expected data : %s" % str(expected_data)
		# print "Simulated data : %s" % str(simulated_data)


		for i, data in enumerate(expected_data):
			self.assertAlmostEqual(data, simulated_data[i], delta=Settings.defaultTestAbsTol+(Settings.defaultTestRelTol*data))

		sedml_doc.writeSedmlToFile(join(testfiles_path, "steadystatesscan.xml"))


