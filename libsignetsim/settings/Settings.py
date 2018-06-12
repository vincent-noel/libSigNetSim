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


from os.path import abspath, join, dirname, expanduser

class Settings(object):

	basePath = abspath(join(dirname(__file__), ".."))

	# Main paths
	# tempDirectory = join(basePath, "tmp/")
	tempDirectory = "/tmp/"

	# C source files
	C_srcPath = join(basePath,"cwriter/src/")
	C_optimizationSrcDirectory = join(C_srcPath,"C_optimization/")
	C_sharedSrcDirectory = join(C_srcPath, "C_shared/")
	C_simulationSrcDirectory = join(C_srcPath, "C_simulation/")

	# C destination paths
	C_optimizationDirectory = "C_optimization/"
	C_sharedDirectory = "C_shared/"
	C_simulationDirectory = "C_simulation/"
	C_simulationResultsDirectory = "results/"
	C_generatedDirectory = "C_generated/"

	# let's remake all this C links
	# C source files
	C_srcPath_v2 = join(basePath,"lib/plsa")
	C_generatedDirectory_v2 = "src/"

	# C destination paths
	C_optimizationDirectory_v2 = "plsa/"


	# SBML settings
	defaultSbmlLevel = 3
	defaultSbmlVersion = 1

	# SED-ML settings
	defaultSedmlLevel = 1
	defaultSedmlVersion = 2

	# NuML settings
	defaultNuMLLevel = 1
	defaultNuMLVersion = 1

	# Test settings
	defaultTestAbsTol = 1e-6
	defaultTestRelTol = 1e-3

	defaultAbsTol = 1e-12
	defaultRelTol = 1e-10

	simulationTimeMin = 0
	simulationTimeMax = 4000
	simulationLogScale = False
	simulationTimeEch = None
	simulationNbSamples = 101
	simulationKeepFiles = True

	steadyStatesMaxTime = 100000
	defaultMaxProcNumbers = 2

	plotTimeMin = 0
	plotTimeEch = 10
	plotTimeMax = 100
	plotTitle = ""

	optimizationDefaultConstantLowerBound = 1e-8
	optimizationDefaultConstantUpperBound = 1e+8

	optimizationDefaultParamLowerBound = 1e-8
	optimizationDefaultParamUpperBound = 1e+8

	optimizationDefaultInitialValueLowerBound = 1e-8
	optimizationDefaultInitialValueUpperBound = 1e+8

	optimizationDefaultCompartmentLowerBound = 1e-8
	optimizationDefaultCompartmentUpperBound = 1e+8

	verbose = 0
	verboseTiming = 0
	showSbmlErrors = False
	reduceByDefault = False


	sbmlTestCasesPath = join('/', 'tmp',"sbml-test-suite", "cases", "semantic")
	sbmlTestResultsPath = join('/', 'tmp',"test-suite-results")

	defaultCVODEmaxNumSteps = 5000
	defaultCVODEMaxConvFails = 100
	defaultCVODEMaxErrFails = 70

	defaultScoreNegativePenalty = 0

	defaultPlsaSeed = 0
	defaultPlsaInitialTemperature = 1
	defaultPlsaGainForJumpSizeControl = 5
	defaultPlsaInterval = 100
	# For enzyme, 0.005 is very good (95% of good results)
	# you can also use 0.01, but that's like 80% good results
	defaultPlsaLambda = 0.001
	defaultPlsaLambdaMemU = 200
	defaultPlsaLambdaMemV = 1000
	defaultPlsaControl = 1
	defaultPlsaInitialMoves = 2000
	defaultPlsaTau = 1000
	defaultPlsaFreezeCount = 100
	defaultPlsaUpdateSSkip = 1
	defaultPlsaCriterion = 0.001
	defaultPlsaPrecision = 7
	defaultPlsaMixInterval = 10
	defaultPlsaDistribution = 1
	defaultPlsaQ = 1.0

	defaultPlsaTraceLog = 0
	defaultPlsaParamsLog = 0

	color_scheme = (["#FFB300", "#803E75", "#FF6800", "#A6BDD7"]
					+ ["#C10020", "#CEA262", "#817066", "#007D34"]
					+ ["#F6768E", "#00538A", "#FF7A5C", "#53377A"]
					+ ["#FF8E00", "#B32851", "#F4C800", "#7F180D"]
					+ ["#93AA00", "#593315", "#F13A13", "#232C16"])

	color_scheme_light = ['#67b6ce']