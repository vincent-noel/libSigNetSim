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

	Testing the XPath building and resolution

"""

from libsignetsim import SbmlDocument
from libsignetsim.model.sbml.ReplacedElement import ReplacedElement
from libsignetsim.model.sbml.ReplacedBy import ReplacedBy

from unittest import TestCase
from os.path import join, dirname


class TestSubstitutions(TestCase):
	""" Tests high level functions """

	def testSubstitutions(self):

		doc_comp_external = SbmlDocument()
		doc_comp_external.readSbmlFromFile(join(dirname(__file__), "files", "comp_model", "modelz9xdww.xml"))

		subs = doc_comp_external.model.listOfSbmlObjects.getListOfSubstitutions()
		for substitution in subs:
			if isinstance(substitution, ReplacedElement):
				obj = substitution.getReplacedElementObject()


			elif isinstance(substitution, ReplacedBy):
				obj = substitution.getReplacingElementObject()
