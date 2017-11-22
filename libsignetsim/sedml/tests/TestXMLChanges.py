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


class TestXMLChanges(TestCase):
	""" Tests high level functions """

	def testAddXML(self):

		testfiles_path = join(dirname(join(getcwd(), __file__)), "files")

		if not isdir(testfiles_path):
			mkdir(testfiles_path)

		# Setting up the model
		sbml_doc = SbmlDocument()
		m = sbml_doc.model
		m.setName("Test")

		s = m.listOfSpecies.new("S", value=5)
		p0 = m.listOfParameters.new("P0")
		sbml_filename = join(Settings.tempDirectory, "testChanges.sbml")
		sbml_doc.writeSbmlToFile(sbml_filename)

		sedml_doc = SedmlDocument()

		simulation = sedml_doc.listOfSimulations.createUniformTimeCourse()
		simulation.setInitialTime(0)
		simulation.setOutputStartTime(0)
		simulation.setOutputEndTime(1)
		simulation.setNumberOfPoints(1)
		simulation.getAlgorithm().setCVODE()

		model = sedml_doc.listOfModels.createModel()
		model.setLanguageSbml()
		model.setSource(sbml_filename)

		addXMLParameter = model.listOfChanges.createAddXML()
		addXMLParameter.setTarget(m.listOfParameters)
		addXMLParameter.setNewXMLFromString("<parameter id=\"test\" name=\"Test\" value=\"2\"/>")

		addXMLInitialAssignment = model.listOfChanges.createAddXML()
		addXMLInitialAssignment.setTarget(m.listOfInitialAssignments)
		addXMLInitialAssignment.setNewXMLFromString(
			"<initialAssignment symbol=\"%s\">" % s.getSbmlId()
			+ "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><ci>test</ci></math>"
			+ "</initialAssignment>"
		)

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
		data_s = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_s.setName("S")

		var_s = data_s.listOfVariables.createVariable("S")
		var_s.setTask(task)
		var_s.setModel(model)
		var_s.setTarget(s)

		data_s.getMath().setInternalMathFormula(var_s.getSympySymbol())

		plot = sedml_doc.listOfOutputs.createPlot2D()
		curve_basal = plot.listOfCurves.createCurve()
		curve_basal.setXData(data_time)
		curve_basal.setYData(data_s)

		model.getSbmlModel()
		sedml_doc.run()
		self.assertEqual(sedml_doc.listOfOutputs[0].listOfCurves[0].getXData(),	[0, 1])
		self.assertEqual(sedml_doc.listOfOutputs[0].listOfCurves[0].getYData(), [2, 2])

		sedml_filename = join(Settings.tempDirectory, "testChanges.sedml")
		sedml_doc.writeSedmlToFile(sedml_filename)

		sedml_doc_2 = SedmlDocument()
		sedml_doc_2.readSedmlFromFile(sedml_filename)
		sedml_doc_2.run()
		self.assertEqual(sedml_doc_2.listOfOutputs[0].listOfCurves[0].getXData(), [0, 1])
		self.assertEqual(sedml_doc_2.listOfOutputs[0].listOfCurves[0].getYData(), [2, 2])
