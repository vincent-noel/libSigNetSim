#!/usr/bin/env python
""" testSigNetSim.py


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


import unittest, bioservices, time, os
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.ModelException import (MathException, SbmlException, TagNotImplementedModelException,
											PackageNotImplementedModelException)
from libsignetsim.simulation.tests.BiomodelsTestCaseSimulation import BiomodelsTestCaseSimulation

class TestTimeseriesBiomodels(unittest.TestCase):
	""" Tests high level functions """

	""" Incompatible cases, for now :
	BIOMD0000000019: Something related to piecewise apparently : https://github.com/sympy/sympy/issues/11745
	"""

	# Read/Write issue
	INCOMPATIBLE_CASES = [
							# 'BIOMD0000000051', #Seems to work after fixing the constant concentrations cases
							# 'BIOMD0000000055',
							# 'BIOMD0000000056', 'BIOMD0000000071',
							# 'BIOMD0000000089' # Stuck

							# 'BIOMD0000000169', 'BIOMD0000000215',
							# 'BIOMD0000000256', 'BIOMD0000000257',
							# 'BIOMD0000000258', 'BIOMD0000000300',
							# 'BIOMD0000000329', 'BIOMD0000000340',
							# 'BIOMD0000000389', 'BIOMD0000000392',
							# 'BIOMD0000000405', 'BIOMD0000000410',
							# 'BIOMD0000000447', 'BIOMD0000000450',
							# 'BIOMD0000000474', 'BIOMD0000000480',
							# 'BIOMD0000000498', 'BIOMD0000000539',
							# 'BIOMD0000000542', 'BIOMD0000000552',
							# 'BIOMD0000000553', 'BIOMD0000000556',
							# 'BIOMD0000000570', 'BIOMD0000000573',
							# 'BIOMD0000000574', 'BIOMD0000000582',
							# 'BIOMD0000000586', 'BIOMD0000000587'
							# 'BIOMD0000000607', 'BIOMD0000000609',
							# 'BIOMD0000000610'
	]

	# CSymbolDelay
	INCOMPATIBLE_CASES += ['BIOMD0000000024', 'BIOMD0000000025',
							'BIOMD0000000034', 'BIOMD0000000154',
							'BIOMD0000000155', 'BIOMD0000000196',]

	# FastReactions (We can't test them yet)
	INCOMPATIBLE_CASES += ['BIOMD0000000137', 'BIOMD0000000424', 'BIOMD0000000490', 'BIOMD0000000512', 'BIOMD0000000588']

	# Consistency issue
	INCOMPATIBLE_CASES += ['BIOMD0000000094', 'BIOMD0000000539', 'BIOMD0000000596']

	# Simulator issue
	INCOMPATIBLE_CASES += ['BIOMD0000000339', 'BIOMD0000000404', 'BIOMD0000000527', 'BIOMD0000000589']

	# Missing initial value issue
	INCOMPATIBLE_CASES += ['BIOMD0000000266', 'BIOMD0000000338']

	# Unknown issue (Kernel crash)
	INCOMPATIBLE_CASES += ['BIOMD0000000446']

	RESTART = 'BIOMD0000000234'

	def testTimeseriesBiomodels(self):

		Settings.verbose=0
		db = bioservices.BioModels()
		curatedModelsIds = db.getAllCuratedModelsId()

		for i_modelId, modelId in enumerate(sorted(curatedModelsIds)):

  			if i_modelId < sorted(curatedModelsIds).index(self.RESTART):
				print "> %s : [Skipped]" % modelId

			elif modelId not in self.INCOMPATIBLE_CASES:

				try:
					t0 = time.time()
					case = BiomodelsTestCaseSimulation(modelId)
					res = case.run()

					if res >= 0:
						print "> %s : [OK] (%.2gs)" % (modelId, time.time()-t0)
					elif res == -1:
						print "> %s : [ERR, Simulation failed] (%.2gs)" % (modelId, time.time()-t0)
					elif res == -2:
						print "> %s : [ERR, Incorrect values] (%.2gs)" % (modelId, time.time()-t0)

				except MathException as e:
					print "> %s : [ERR, Math] (%s)" % (modelId, e)

				except SbmlException as e:
					print "> %s : [ERR, SBML] (%s)" % (modelId, e)

				except TagNotImplementedModelException as e:
					print "> %s : [ERR, TAG INCOMPATIBLE] (%s)" % (modelId, e)

				except PackageNotImplementedModelException as e:
					print "> %s : [ERR, PACKAGE INCOMPATIBLE] (%s)" % (modelId, e)

				except Exception as e:
					print "> %s : [ERR] (%s)" % (modelId, e)


			else:
				print "> %s : [Not Compatible]" % modelId
