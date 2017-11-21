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

	This file is a simple example of reading and writing a basic NuML doc

"""

from libsignetsim import NuMLDocument, Settings
from unittest import TestCase
from os.path import join, dirname


class TestExperiment(TestCase):
	""" Tests high level functions """

	def testExperiment(self):

		numl_doc = NuMLDocument()
		numl_doc.readNuMLFromFile(join(join(dirname(__file__), "files"), "experiment_0.xml"))
		numl_doc.writeNuMLToFile(join(Settings.tempDirectory, "experiment_0_copy.xml"))
		numl_doc = NuMLDocument()
		numl_doc.readNuMLFromFile(join(Settings.tempDirectory, "experiment_0_copy.xml"))
		numl_doc.writeNuMLToFile(join(Settings.tempDirectory, "experiment_0_copy_copy.xml"))





