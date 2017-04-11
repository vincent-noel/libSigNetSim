#!/usr/bin/env python
""" TestMath.py


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
from os import mkdir, getcwd

class TestMath(TestCase):
	""" Tests high level functions """

	def testMath(self):

		testfiles_path = join(dirname(join(getcwd(), __file__)), "files")

		if not isdir(testfiles_path):
			mkdir(testfiles_path)

		# Setting up the model
		sbml_doc = SbmlDocument()
		m = sbml_doc.model
		m.setName("Test")

		e = m.listOfSpecies.new("E", value=10)
		s = m.listOfSpecies.new("S", value=12)
		p = m.listOfSpecies.new("P", value=0)

		sbml_filename = join(testfiles_path, "testMath.sbml")
		sbml_doc.writeSbmlToFile(sbml_filename)

		sedml_doc = SedmlDocument()

		simulation = sedml_doc.listOfSimulations.createUniformTimeCourse()
		simulation.setInitialTime(0)
		simulation.setOutputStartTime(0)
		simulation.setOutputEndTime(10)
		simulation.setNumberOfPoints(100)
		simulation.getAlgorithm().setCVODE()
		simulation.getAlgorithm().listOfAlgorithmParameters.setRelTol(1e-6)
		simulation.getAlgorithm().listOfAlgorithmParameters.setAbsTol(1e-30)

		model = sedml_doc.listOfModels.createModel()
		model.setLanguageSbml()
		model.setSource(sbml_filename)

		task = sedml_doc.listOfTasks.createTask()
		task.setModel(model)
		task.setSimulation(simulation)

		# >> pi
		data_0 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_0.setName("data_0")
		time_0 = data_0.listOfVariables.createVariable("time")
		time_0.setTask(task)
		time_0.setModel(model)
		time_0.setSymbolTime()
		data_0.getMath().setPrettyPrintMathFormula("pi")

		# # >> piecewise(2, 1 > 0.5, 3)
		# data_1 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_1.setName("data_1")
		# data_1.getMath().setPrettyPrintMathFormula("piecewise(2, 1 > 0.5, 3)")
		#
		# # >> piecewise(2, 1 >= 0.5, 3)
		# data_2 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_2.setName("data_2")
		# data_2.getMath().setPrettyPrintMathFormula("piecewise(2, 1 >= 0.5, 3)")
		#
		# # >> piecewise(2, 1 < 0.5, 3)
		# data_3 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_3.setName("data_3")
		# data_3.getMath().setPrettyPrintMathFormula("piecewise(2, 1 < 0.5, 3)")
		#
		# # >> piecewise(2, 1 <= 0.5, 3)
		# data_4 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_4.setName("data_4")
		# data_4.getMath().setPrettyPrintMathFormula("piecewise(2, 1 <= 0.5, 3)")
		#
		# >> piecewise(2, time == pi, 3)
		data_5 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_5.setName("data_5")
		time_5 = data_5.listOfVariables.createVariable("time")
		time_5.setTask(task)
		time_5.setModel(model)
		time_5.setSymbolTime()
		data_5.getMath().setPrettyPrintMathFormula("piecewise(2, time == pi, 3)")

		# # >> piecewise(2, P1 != pi, 3)
		# data_6 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_6.setName("data_6")
		# param_6 = data_6.listOfParameters.createParameter("p1")
		# param_6.setValue(2)
		# data_6.getMath().setPrettyPrintMathFormula("piecewise(2, p1 != pi, 3)")
		#
		# >> factorial(4)
		# data_7 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_7.setName("data_7")
		# time_7 = data_7.listOfVariables.createVariable("time")
		# time_7.setTask(task)
		# time_7.setModel(model)
		# time_7.setSymbolTime()
		# data_7.getMath().setPrettyPrintMathFormula("factorial(4)")

		# # >> piecewise(3, true && false, 3)
		# data_8 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_8.setName("data_8")
		# data_8.getMath().setPrettyPrintMathFormula("piecewise(3, true && false, 3)")
		#
		# # >> piecewise(2, true || false, 3)
		# data_9 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_9.setName("data_9")
		# data_9.getMath().setPrettyPrintMathFormula("piecewise(2, true || false, 3)")
		#
		# # >> piecewise(2, xor(true, false), 3)
		# data_10 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_10.setName("data_10")
		# data_10.getMath().setPrettyPrintMathFormula("piecewise(2, xor(true, false), 3)")
		#
		# # >> piecewise(2, !false, 3)
		# data_11 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_11.setName("data_11")
		# data_11.getMath().setPrettyPrintMathFormula("piecewise(2, !false, 3)")

		# >> sec(0.5)
		data_12 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_12.setName("data_12")
		time_12 = data_12.listOfVariables.createVariable("time")
		time_12.setTask(task)
		time_12.setModel(model)
		time_12.setSymbolTime()
		data_12.getMath().setPrettyPrintMathFormula("sec(time)")

		# >> csc(4.5)
		data_13 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_13.setName("data_13")
		time_13 = data_13.listOfVariables.createVariable("time")
		time_13.setTask(task)
		time_13.setModel(model)
		time_13.setSymbolTime()
		data_13.getMath().setPrettyPrintMathFormula("csc(time)")

		# >> cot(0.2)
		data_14 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_14.setName("data_14")
		time_14 = data_14.listOfVariables.createVariable("time")
		time_14.setTask(task)
		time_14.setModel(model)
		time_14.setSymbolTime()
		data_14.getMath().setPrettyPrintMathFormula("cot(time)")

		# >> sinh(0.3)
		data_15 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_15.setName("data_15")
		time_15 = data_15.listOfVariables.createVariable("time")
		time_15.setTask(task)
		time_15.setModel(model)
		time_15.setSymbolTime()
		data_15.getMath().setPrettyPrintMathFormula("sinh(time)")

		# >> cosh(1.7)
		data_16 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_16.setName("data_16")
		time_16 = data_16.listOfVariables.createVariable("time")
		time_16.setTask(task)
		time_16.setModel(model)
		time_16.setSymbolTime()
		data_16.getMath().setPrettyPrintMathFormula("cosh(time)")

		# >> arcsec(2.3)
		data_17 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_17.setName("data_17")
		time_17 = data_17.listOfVariables.createVariable("time")
		time_17.setTask(task)
		time_17.setModel(model)
		time_17.setSymbolTime()
		data_17.getMath().setPrettyPrintMathFormula("arcsec(time)")

		# >> arccsc(1.1)
		data_18 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_18.setName("data_18")
		time_18 = data_18.listOfVariables.createVariable("time")
		time_18.setTask(task)
		time_18.setModel(model)
		time_18.setSymbolTime()
		data_18.getMath().setPrettyPrintMathFormula("arccsc(time+1)")

		# >> arccot(-0.1)
		data_19 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_19.setName("data_19")
		time_19 = data_19.listOfVariables.createVariable("time")
		time_19.setTask(task)
		time_19.setModel(model)
		time_19.setSymbolTime()
		data_19.getMath().setPrettyPrintMathFormula("arccot(time+1)")

		# >> arcsinh(99)
		data_20 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_20.setName("data_20")
		time_20 = data_20.listOfVariables.createVariable("time")
		time_20.setTask(task)
		time_20.setModel(model)
		time_20.setSymbolTime()
		data_20.getMath().setPrettyPrintMathFormula("arcsinh(time)")

		# >> arccosh(1.34)
		data_21 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_21.setName("data_21")
		time_21 = data_21.listOfVariables.createVariable("time")
		time_21.setTask(task)
		time_21.setModel(model)
		time_21.setSymbolTime()
		data_21.getMath().setPrettyPrintMathFormula("arccosh(time)")

		# >> arctanh(-0.7)
		data_22 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_22.setName("data_22")
		time_22 = data_22.listOfVariables.createVariable("time")
		time_22.setTask(task)
		time_22.setModel(model)
		time_22.setSymbolTime()
		data_22.getMath().setPrettyPrintMathFormula("arctanh(time)")

		# >> arcsech(0.42)
		data_23 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_23.setName("data_23")
		time_23 = data_23.listOfVariables.createVariable("time")
		time_23.setTask(task)
		time_23.setModel(model)
		time_23.setSymbolTime()
		data_23.getMath().setPrettyPrintMathFormula("arcsech(time+1)")

		# >> arccsch(0.01)
		data_24 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_24.setName("data_24")
		time_24 = data_24.listOfVariables.createVariable("time")
		time_24.setTask(task)
		time_24.setModel(model)
		time_24.setSymbolTime()
		data_24.getMath().setPrettyPrintMathFormula("arccsc(time+1)")

		# >> arccoth(8.2)
		data_25 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_25.setName("data_25")
		time_25 = data_25.listOfVariables.createVariable("time")
		time_25.setTask(task)
		time_25.setModel(model)
		time_25.setSymbolTime()
		data_25.getMath().setPrettyPrintMathFormula("arccoth(time+1)")

		# >> exponentiale
		data_26 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_26.setName("data_26")
		time_26 = data_26.listOfVariables.createVariable("time")
		time_26.setTask(task)
		time_26.setModel(model)
		time_26.setSymbolTime()
		data_26.getMath().setPrettyPrintMathFormula("exponentiale")

		# >> exp(exponentiale)
		data_27 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_27.setName("data_27")
		time_27 = data_27.listOfVariables.createVariable("time")
		time_27.setTask(task)
		time_27.setModel(model)
		time_27.setSymbolTime()
		data_27.getMath().setPrettyPrintMathFormula("exp(exponentiale)")

		# >> 3.7
		data_28 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_28.setName("data_28")
		time_28 = data_28.listOfVariables.createVariable("time")
		time_28.setTask(task)
		time_28.setModel(model)
		time_28.setSymbolTime()
		data_28.getMath().setPrettyPrintMathFormula("3.7")

		# >> abs(-1)
		data_29 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_29.setName("data_29")
		time_29 = data_29.listOfVariables.createVariable("time")
		time_29.setTask(task)
		time_29.setModel(model)
		time_29.setSymbolTime()
		data_29.getMath().setPrettyPrintMathFormula("abs(-time)")

		# >> abs(1)
		data_30 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_30.setName("data_30")
		time_30 = data_30.listOfVariables.createVariable("time")
		time_30.setTask(task)
		time_30.setModel(model)
		time_30.setSymbolTime()
		data_30.getMath().setPrettyPrintMathFormula("abs(time)")

		# >> acos(-1)
		data_31 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_31.setName("data_31")
		time_31 = data_31.listOfVariables.createVariable("time")
		time_31.setTask(task)
		time_31.setModel(model)
		time_31.setSymbolTime()
		data_31.getMath().setPrettyPrintMathFormula("acos(time)")

		# >> acos(0.5)
		data_32 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_32.setName("data_32")
		time_32 = data_32.listOfVariables.createVariable("time")
		time_32.setTask(task)
		time_32.setModel(model)
		time_32.setSymbolTime()
		data_32.getMath().setPrettyPrintMathFormula("acos(time)")

		# >> asin(1)
		data_33 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_33.setName("data_33")
		time_33 = data_33.listOfVariables.createVariable("time")
		time_33.setTask(task)
		time_33.setModel(model)
		time_33.setSymbolTime()
		data_33.getMath().setPrettyPrintMathFormula("asin(time)")

		# >> asin(-0.5)
		data_34 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_34.setName("data_34")
		time_34 = data_34.listOfVariables.createVariable("time")
		time_34.setTask(task)
		time_34.setModel(model)
		time_34.setSymbolTime()
		data_34.getMath().setPrettyPrintMathFormula("asin(time)")

		# >> atan(2.8)
		data_35 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_35.setName("data_35")
		time_35 = data_35.listOfVariables.createVariable("time")
		time_35.setTask(task)
		time_35.setModel(model)
		time_35.setSymbolTime()
		data_35.getMath().setPrettyPrintMathFormula("atan(time)")

		# >> atan(-7.09)
		data_36 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_36.setName("data_36")
		time_36 = data_36.listOfVariables.createVariable("time")
		time_36.setTask(task)
		time_36.setModel(model)
		time_36.setSymbolTime()
		data_36.getMath().setPrettyPrintMathFormula("atan(time)")

		# >> ceil(0.5)
		data_37 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_37.setName("data_37")
		time_37 = data_37.listOfVariables.createVariable("time")
		time_37.setTask(task)
		time_37.setModel(model)
		time_37.setSymbolTime()
		data_37.getMath().setPrettyPrintMathFormula("ceil(time)")

		# >> ceil(3.55)
		data_38 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_38.setName("data_38")
		time_38 = data_38.listOfVariables.createVariable("time")
		time_38.setTask(task)
		time_38.setModel(model)
		time_38.setSymbolTime()
		data_38.getMath().setPrettyPrintMathFormula("ceil(time+0.05)")

		# >> ceil(-4.6)
		data_39 = sedml_doc.listOfDataGenerators.createDataGenerator()
		data_39.setName("data_39")
		time_39 = data_39.listOfVariables.createVariable("time")
		time_39.setTask(task)
		time_39.setModel(model)
		time_39.setSymbolTime()
		data_39.getMath().setPrettyPrintMathFormula("ceil(-time)")

		# # >> cos(9.1)
		# data_40 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_40.setName("data_40")
		# data_40.getMath().setPrettyPrintMathFormula("cos(9.1)")
		# 
		# # >> cos(-0.22)
		# data_41 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_41.setName("data_41")
		# data_41.getMath().setPrettyPrintMathFormula("cos(-0.22)")
		# 
		# # >> exp(0)
		# data_42 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_42.setName("data_42")
		# data_42.getMath().setPrettyPrintMathFormula("exp(0)")
		# 
		# # >> exp(1)
		# data_43 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_43.setName("data_43")
		# data_43.getMath().setPrettyPrintMathFormula("exp(1)")
		# 
		# # >> exp(0.77)
		# data_44 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_44.setName("data_44")
		# data_44.getMath().setPrettyPrintMathFormula("exp(0.77)")
		# 
		# # >> floor(-4.6)
		# data_45 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_45.setName("data_45")
		# data_45.getMath().setPrettyPrintMathFormula("floor(-4.6)")
		# 
		# # >> floor(9.1)
		# data_46 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_46.setName("data_46")
		# data_46.getMath().setPrettyPrintMathFormula("floor(9.1)")
		# 
		# # >> ln(0.2)
		# data_47 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_47.setName("data_47")
		# data_47.getMath().setPrettyPrintMathFormula("ln(0.2)")
		# 
		# # >> ln(1)
		# data_48 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_48.setName("data_48")
		# data_48.getMath().setPrettyPrintMathFormula("ln(1)")
		# 
		# # >> log10(0.2)
		# data_49 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_49.setName("data_49")
		# data_49.getMath().setPrettyPrintMathFormula("log10(0.2)")
		# 
		# # >> log10(1)
		# data_50 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_50.setName("data_50")
		# data_50.getMath().setPrettyPrintMathFormula("log10(1)")

		# # >> 1^2
		# data_51 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_51.setName("data_51")
		# data_51.getMath().setPrettyPrintMathFormula("1^2")

		# # >> 2^2
		# data_52 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_52.setName("data_52")
		# data_52.getMath().setPrettyPrintMathFormula("2^2")

		# # >> 1.4^5.1
		# data_53 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_53.setName("data_53")
		# data_53.getMath().setPrettyPrintMathFormula("1.4^5.1")

		# # >> 4^2
		# data_54 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_54.setName("data_54")
		# data_54.getMath().setPrettyPrintMathFormula("4^2")
		#
		# # >> 3.1^2
		# data_55 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_55.setName("data_55")
		# data_55.getMath().setPrettyPrintMathFormula("3.1^2")

		# # >> sqrt(4)
		# data_56 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_56.setName("data_56")
		# data_56.getMath().setPrettyPrintMathFormula("sqrt(4)")
		# 
		# # >> sqrt(7.4)
		# data_57 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_57.setName("data_57")
		# data_57.getMath().setPrettyPrintMathFormula("sqrt(7.4)")
		# 
		# # >> sin(2.1)
		# data_58 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_58.setName("data_58")
		# data_58.getMath().setPrettyPrintMathFormula("sin(2.1)")
		# 
		# # >> sin(0)
		# data_59 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_59.setName("data_59")
		# data_59.getMath().setPrettyPrintMathFormula("sin(0)")
		# 
		# # >> sin(-5.9)
		# data_60 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_60.setName("data_60")
		# data_60.getMath().setPrettyPrintMathFormula("sin(-5.9)")
		# 
		# # >> tan(0)
		# data_61 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_61.setName("data_61")
		# data_61.getMath().setPrettyPrintMathFormula("tan(0)")
		# 
		# # >> tan(1.11)
		# data_62 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_62.setName("data_62")
		# data_62.getMath().setPrettyPrintMathFormula("tan(1.11)")
		# 
		# # >> tan(-6)
		# data_63 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_63.setName("data_63")
		# data_63.getMath().setPrettyPrintMathFormula("tan(-6)")
		# 
		# # >> 1 + 2
		# data_64 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_64.setName("data_64")
		# data_64.getMath().setPrettyPrintMathFormula("1+2")
		# 
		# # >> 1 + -2
		# data_65 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_65.setName("data_65")
		# data_65.getMath().setPrettyPrintMathFormula("1 + -2")
		# 
		# # # >> (5/2)
		# # data_66 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# # data_66.setName("data_66")
		# # data_66.getMath().setPrettyPrintMathFormula("(5/2)")
		# 
		# # >> 8 * 3
		# data_67 = sedml_doc.listOfDataGenerators.createDataGenerator()
		# data_67.setName("data_67")
		# data_67.getMath().setPrettyPrintMathFormula("8.3")

		report = sedml_doc.listOfOutputs.createReport()
		dataset_0 = report.listOfDataSets.createDataSet()
		dataset_0.setLabel("data_0")
		dataset_0.setData(data_0)


		sedml_doc.run()
		sedml_filename = join(testfiles_path, "testMath.sedml")
		sedml_doc.writeSedmlToFile(sedml_filename)

		# sedml_doc_2 = SedmlDocument()
		# sedml_doc_2.readSedmlFromFile(sedml_filename)
		# sedml_doc.run()