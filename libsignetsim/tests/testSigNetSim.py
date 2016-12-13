#!/usr/bin/env python
""" testSigNetSim.py


	This file ...


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

from libsignetsim.model.SbmlDocument import SbmlDocument

class TestSigNetSim(unittest.TestCase):
	""" Tests high level functions """


	def testModelOpen(self):

		doc = SbmlDocument()
		doc.readSbml("libsignetsim/tests/input/Ras--MAPK_v2.sbml")
		self.assertEqual(doc.getModelInstance().getName(), 'Ras--MAPK_v2')
