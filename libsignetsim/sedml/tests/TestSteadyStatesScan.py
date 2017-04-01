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


	def testExampleSpecification(self):

		if not isdir(join(dirname(__file__), "files")):
			mkdir(join(dirname(__file__), "files"))

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

		sbml_doc.writeSbml(join(join(dirname(__file__), "files"), "enzymatic.xml"))

		sedml_doc = SedmlDocument()
		sedml_doc.writeSedmlToFile(join(join(dirname(__file__), "files"), "steadystatesscan.xml"))

		simulation = sedml_doc.listOfSimulations.createSteadyState()
		simulation.getAlgorithm().setKinSol()

		model = sedml_doc.listOfModels.createModel()
		model.setLanguageSbml()
		model.setSource("enzymatic.xml")

		task = sedml_doc.listOfTasks.createTask()
		task.setModel(model)
		task.setSimulation(simulation)

		repeated_task = sedml_doc.listOfTasks.createRepeatedTask()
		repeated_task.setResetModel(True)

		uniform_range = repeated_task.listOfRanges.createUniformRange()
		uniform_range.setStart(0)
		uniform_range.setEnd(100)
		uniform_range.setNumberOfPoints(100)
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

		sedml_doc.writeSedmlToFile(join(join(dirname(__file__), "files"), "steadystatesscan.xml"))



