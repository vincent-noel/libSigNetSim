# Copyright 2014-2016 Vincent Noel (vincent.noel@butantan.gov.br)

# This file is part of SigNetSim.

# libSigNetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# libSigNetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SigNetSim.  If not, see <http://www.gnu.org/licenses/>.

""" testModel.py

This file ...

"""

import unittest

from libsignetsim.model.SbmlDocument import SbmlDocument

class TestModel(unittest.TestCase):

	def testLoadSbmlModel(self):

		modelFilename = "libsignetsim/tests/input/EGFR_IGF1R_v1.sbml"

		doc = SbmlDocument()
		doc.readSbml(modelFilename)

		self.assertEqual(len(doc.model.listOfReactions), 22)
		self.assertEqual(len(doc.model.listOfSpecies), 21)
		self.assertEqual(len(doc.model.listOfParameters), 39)


		modelFilename = "libsignetsim/tests/input/Chen_2004.sbml"

		doc = SbmlDocument()
		doc.readSbml(modelFilename)

		self.assertEqual(len(doc.model.listOfReactions), 94)
		self.assertEqual(len(doc.model.listOfSpecies), 54)
		self.assertEqual(len(doc.model.listOfParameters), 163)


		modelFilename = "libsignetsim/tests/input/Ras--MAPK_v2.sbml"

		doc = SbmlDocument()
		doc.readSbml(modelFilename)

		self.assertEqual(len(doc.model.listOfReactions), 23)
		self.assertEqual(len(doc.model.listOfSpecies), 40)
		self.assertEqual(len(doc.model.listOfParameters), 81)


if __name__ == '__main__':
	unittest.main()
