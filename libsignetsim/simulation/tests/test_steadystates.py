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


import unittest


class TestlibSigNetSim(unittest.TestCase):
	""" Tests high level functions """


	# def testModelOpen(self):
	#
	# 	doc = SbmlDocument()
	# 	doc.readSbml("libsignetsim/tests/input/Ras--MAPK_v2.sbml")
	# 	self.assertEqual(doc.getModelInstance().getName(), 'Ras--MAPK_v2')
	#
	#
	# def testOptimization(self):
	#     """ Tests optimizations """
	#
	#     #Lulu's case
	#     sigNetSimInstance = SigNetSim()
	#     res = sigNetSimInstance.runModelVsModelOptimization("SigNetSim/tests/input/ListReaction1.sbml",
	#                                                         "SigNetSim/tests/input/EGFR_IGF1R_v1.sbml",
	#                                                         "SigNetSim/tests/output/model.sbml", 2, 30)
	#
	#     self.assertEqual(res, 0.522500)
	#
	#     #Ras--MAPK_v2 case
	#     sigNetSimInstance = SigNetSim()
	#     res = sigNetSimInstance.runModelVsDataOptimization("SigNetSim/tests/input/Ras--MAPK_v2.sbml",
	#                                                         "SigNetSim/tests/input/Ras--MAPK_v2_observed_concentrations.txt",
	#                                                         "SigNetSim/tests/output/model.sbml", 2, 30)
	#
	#     self.assertEqual(res, 0.522500)
	#
	# def testSimulation(self):
	#     """ Tests simulations """
	#
	#     sigNetSimInstance = SigNetSim()
	#     resOpen = sigNetSimInstance.openSbmlModel("SigNetSim/tests/input/Chen_2004.sbml")
	#     resSim = sigNetSimInstance.runModelSimulation()
	#     print resSim
	#     self.assertEqual(resSim, 0)
	#     self.assertEqual(resOpen, 0)


if __name__ == '__main__':
	pass
