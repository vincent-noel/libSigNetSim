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
from __future__ import print_function
import libnuml
from libnuml import readNUMLFromFile, writeNUML, writeNUMLToString, XMLNode, NUMLDocument
from libsignetsim import Settings
from unittest import TestCase
from os.path import join, dirname
from six.moves import reload_module


class TestExampleNotes(TestCase):
	""" Tests high level functions """

	def testExampleNotes(self):

		print("\n\n")
		numl_doc = NUMLDocument()
		reload_module(libnuml)
		time_term = numl_doc.createOntologyTerm()
		time_term.setId("time_term")
		time_term.setTerm("time")
		time_term.setSourceTermId("SBO:0000345")
		time_term.setOntologyURI("http://www.ebi.ac.uk/sbo/")
		notes = "<notes><body xmlns=\"http://www.w3.org/1999/xhtml\"><p>This needs to be noted</p></body></notes>"
		xml_notes = XMLNode.convertStringToXMLNode(notes)
		numl_doc.setNotes(xml_notes)

		numl_doc_string = writeNUMLToString(numl_doc)
		numl_doc_filename = join(Settings.tempDirectory, "example_notes.xml")
		writeNUML(numl_doc, numl_doc_filename)

		numl_doc_copy_file = readNUMLFromFile(numl_doc_filename)

