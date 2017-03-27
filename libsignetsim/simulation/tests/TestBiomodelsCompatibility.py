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

from libsignetsim.settings.Settings import Settings
from libsignetsim.model.ModelException import (
	MathException, SbmlException, TagNotImplementedModelException, PackageNotImplementedModelException
)
from libsignetsim.simulation.tests.BiomodelsTestCaseSimulation import BiomodelsTestCaseSimulation

from unittest import TestCase
from time import time
from bioservices import BioModels


class TestBiomodelsCompatibility(TestCase):
	""" Tests high level functions """

	TIME_ECH = 0.1
	TIME_MAX = 100

	ABS_TOL = 1e-12
	REL_TOL = 1e-6

	KEEP_FILES = True
	TEST_EXPORT = False

	# Read/Write issue
	INCOMPATIBLE_CASES = []

	# CSymbolDelay
	INCOMPATIBLE_CASES += ['BIOMD0000000024', 'BIOMD0000000025',
							'BIOMD0000000034', 'BIOMD0000000154',
							'BIOMD0000000155', 'BIOMD0000000196',]

	# COPASI Errors
	## Invalid states
	INCOMPATIBLE_CASES += ['BIOMD0000000226', 'BIOMD0000000227',
						   'BIOMD0000000248', 'BIOMD0000000250',
						   'BIOMD0000000277', 'BIOMD0000000527',
						   'BIOMD0000000577', 'BIOMD0000000603',
						   'BIOMD0000000604', 'BIOMD0000000605',
						   'BIOMD0000000606', 'BIOMD0000000607',
						   'BIOMD0000000610']

	## Numerical instability
	INCOMPATIBLE_CASES += ['BIOMD0000000474']

	## Unknown error
	INCOMPATIBLE_CASES += ['BIOMD0000000428', 'BIOMD0000000510',
						   'BIOMD0000000511', 'BIOMD0000000512',
						   'BIOMD0000000513', 'BIOMD0000000514',
						   'BIOMD0000000515', 'BIOMD0000000516',
						   'BIOMD0000000562', 'BIOMD0000000592',
						   'BIOMD0000000593']

	START = ''
	STOP = ''

	def testTimeseriesBiomodels(self):

		result = True

		db = BioModels()
		curatedModelsIds = db.getAllCuratedModelsId()

		for i_modelId, modelId in enumerate(sorted(curatedModelsIds)):

			if (
					(self.START != '' and i_modelId < sorted(curatedModelsIds).index(self.START))
				or
					(self.STOP != '' and i_modelId > sorted(curatedModelsIds).index(self.STOP))
			):
				pass

			elif modelId not in self.INCOMPATIBLE_CASES:

				if Settings.verbose >= 1 or Settings.verboseTiming >= 1:
					print ""

				try:
					t0 = time()
					case = BiomodelsTestCaseSimulation(

						modelId, time_ech=self.TIME_ECH, time_max=self.TIME_MAX,
						abs_tol=self.ABS_TOL, rel_tol=self.REL_TOL,
						test_export=self.TEST_EXPORT, keep_files=self.KEEP_FILES
					)
					res = case.run()

					if res >= 0:
						print "> %s : [OK] (%.2gs)" % (modelId, time()-t0)

					elif res == -1:
						print "> %s : [ERR, Simulation failed] (%.2gs)" % (modelId, time()-t0)
						result = False

					elif res == -2:
						print "> %s : [ERR, Incorrect values] (%.2gs)" % (modelId, time()-t0)
						result = False

					elif res == -2:
						print "> %s : [ERR, Incorrect times] (%.2gs)" % (modelId, time()-t0)
						result = False

				except MathException as e:
					print "> %s : [ERR, Math] (%s) (%.2gs)" % (modelId, e, time()-t0)
					result = False

				except SbmlException as e:
					print "> %s : [ERR, SBML] (%s) (%.2gs)" % (modelId, e, time()-t0)
					result = False

				except TagNotImplementedModelException as e:
					# print "> %s : [ERR, TAG INCOMPATIBLE] (%s)" % (modelId, e)
					result = False

				except PackageNotImplementedModelException as e:
					# print "> %s : [ERR, PACKAGE INCOMPATIBLE] (%s)" % (modelId, e)
					result = False

				except Exception as e:
					print "> %s : [ERR] (%s) (%.2gs)" % (modelId, e, time()-t0)
					result = False

			# else:
			# 	print "> %s : [Not Compatible]" % modelId

		self.assertEqual(result, True)