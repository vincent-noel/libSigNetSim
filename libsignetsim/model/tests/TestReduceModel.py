#!/usr/bin/env python
""" TestReduceModel.py


	Testing the research for conservation laws, and the subsequent reduction


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
# from libsignetsim.sedml.SedmlDocument import SedmlDocument

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir, getcwd

class TestReduceModel(TestCase):
	""" Tests high level functions """


	def testReduceModel(self):

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(testfiles_path, "modelqlzB7i.xml"))

		sbml_model = sbml_doc.getModelInstance()
		sbml_model.build()

		sbml_model.stoichiometryMatrix.build()
		sbml_model.listOfConservationLaws.build()
		sbml_model.assymetricModel.build()

		# print sbml_model.listOfConservationLaws
		# print sbml_model.prettyPrint()
		# print sbml_model.assymetricModel.prettyPrint()

