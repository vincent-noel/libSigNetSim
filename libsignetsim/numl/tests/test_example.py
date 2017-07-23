#!/usr/bin/env python
""" TestReadExample.py


	This file is a simple example of reading and writing a basic NuML doc


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

from libsignetsim.numl.NuMLDocument import NuMLDocument

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir

class TestExample(TestCase):
	""" Tests high level functions """

	def testExample(self):

		if not isdir(join(dirname(__file__), "files")):
			mkdir(join(dirname(__file__), "files"))

		numl_doc = NuMLDocument()
		numl_doc.readNuMLFromFile(join(join(dirname(__file__), "files"), "example.xml"))

		numl_doc.writeNuMLToFile(join(join(dirname(__file__), "files"), "example_copy.xml"))




