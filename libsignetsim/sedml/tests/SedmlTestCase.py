#!/usr/bin/env python
""" SedTestCase.py


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

from libsignetsim.sedml.SedmlDocument import SedmlDocument
from libsignetsim.settings.Settings import Settings

from os.path import join

class SedTestCase(object):

	def __init__ (self, case_id, sbml_level, sbml_version):

		self.caseId = "%05d" % case_id
		self.sbmlLevel = sbml_level
		self.sbmlVersion = sbml_version

		self.document = None
		self.loadTestCaseModel()

	def loadTestCaseModel(self):

		self.document = SedmlDocument()
		self.document.readSedmlFromFile(self.getFilename())
		self.document.writeSedmlToFile("poil.xml")

	def getFilename(self):

		return join(Settings.sbmlTestCasesPath, "cases/semantic/%s/%s-sbml-l%sv%s-sedml.xml" % (
				self.caseId, self.caseId, self.sbmlLevel, self.sbmlVersion)
		)

