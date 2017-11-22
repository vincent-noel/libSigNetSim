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

	This file is made for 'high level' tests, using various components

"""

from libsignetsim import SedmlDocument

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir


class TestBiomodelsURI(TestCase):
	""" Tests high level functions """

	def testBiomodelsURI(self):

		sedml_doc = SedmlDocument()

		model = sedml_doc.listOfModels.createModel()
		model.setLanguageSbml()
		model.setSource("urn:miriam:biomodels.db:BIOMD0000000048")

		sbml_model = model.getSbmlModel()
		self.assertEqual(sbml_model.getName(), "Kholodenko1999 - EGFR signaling")





