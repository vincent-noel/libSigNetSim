#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" TestAnnotation.py


	Testing the reading/writing of miriam annotations of the model


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
from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir, getcwd

from libsignetsim.settings.Settings import Settings

class TestAnnotation(TestCase):
	""" Tests high level functions """


	def testReadWrite(self):

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(testfiles_path, "BIOMD0000000001.xml"))
		sbml_model = sbml_doc.getModelInstance()

		self.assertEqual(sbml_model.modelHistory.getDateCreated(), "2005-02-02T14:56:11Z")
		self.assertEqual(sbml_model.modelHistory.getListOfCreators()[0].getEmail(), "lenov@ebi.ac.uk")
		self.assertEqual(sbml_model.modelHistory.getListOfCreators()[0].getGivenName(), "Nicolas")
		self.assertEqual(sbml_model.modelHistory.getListOfCreators()[0].getFamilyName(), "Le Novère")
		sbml_doc.writeSbmlToFile(join(Settings.tempDirectory, "BIOMD0000000001.xml"))




