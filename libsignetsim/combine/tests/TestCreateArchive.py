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

	Test of combine archive : create a new combine archive

"""

from libsignetsim import CombineArchive, Settings

from unittest import TestCase
from os.path import join, dirname, basename


class TestCreateArchive(TestCase):

	def testCreateArchive(self):

		archive = CombineArchive()
		sbml_file = archive.addFile(join(dirname(__file__), "files", "00001-sbml-l3v1.xml"))
		sbml_file.setMaster()

		sedml_file = archive.addFile(join(dirname(__file__), "files", "00001-sbml-l3v1-sedml.xml"))
		sedml_file.setMaster()

		numl_file = archive.addFile(join(dirname(__file__), "files", "experiment_0.xml"))
		numl_file.setMaster()

		archive.writeArchive(join(Settings.tempDirectory, "test_00001.omex"))

		create_archive = CombineArchive()
		create_archive.readArchive(join(Settings.tempDirectory, "test_00001.omex"))

		files = create_archive.getListOfFiles()
		for file in files:

			if file.isSbml():
				self.assertTrue(file.getFilename() == basename(create_archive.getMasterSbml()))
				self.assertTrue(file.getFilename() == basename(create_archive.getAllSbmls()[0]))

			elif file.isSedml():
				self.assertTrue(file.getFilename() == basename(create_archive.getMasterSedml()))
				self.assertTrue(file.getFilename() == basename(create_archive.getAllSedmls()[0]))

			elif file.isNuml():
				self.assertTrue(file.getFilename() == basename(create_archive.getMasterNuml()))
				self.assertTrue(file.getFilename() == basename(create_archive.getAllNumls()[0]))

