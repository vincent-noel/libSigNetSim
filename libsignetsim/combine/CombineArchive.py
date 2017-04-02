#!/usr/bin/env python
""" CombineArchive.py


	Initialization of the combine archive module


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
from libsignetsim.combine.Manifest import Manifest
from libsignetsim.combine.ListOfFiles import ListOfFiles
from libsignetsim.combine.CombineException import (
	FileNotFoundException, NotAZipFileException, NoManifestFoundException, NoMasterSedmlFoundException,
	NoSedmlFoundException
)
from libsignetsim.sedml.SedmlDocument import SedmlDocument
from libsignetsim.settings.Settings import Settings

from zipfile import is_zipfile, ZipFile
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from os.path import exists, join

class CombineArchive(object):

	MANIFEST = "manifest.xml"

	SEDML = "sed-ml"

	def __init__(self):

		self.__file = None
		self.__listOfFiles = ListOfFiles(self)
		self.__manifest = Manifest(self)
		self.__path = Settings.tempDirectory + ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(12))
		self.__master = None

	def readFile(self, file):

		if not exists(file):
			raise FileNotFoundException("File %s not found" % file)

		if not is_zipfile(file):
			raise NotAZipFileException("File %s is not a zip file" % file)

		self.__file = ZipFile(file)
		if not self.MANIFEST in self.__file.namelist():
			raise NoManifestFoundException("No manifest found in archive %s" % file)

		self.__manifest.readManifest(self.__file.read(self.MANIFEST))
		self.__master = self.__manifest.getMaster()

		self.extractArchive()

		#TODO : browse the manifest, check if the archive exists, then create add the file to the list of files ?


	def extractArchive(self):

		self.__file.extractall(self.__path)

	def getMasterSedml(self):

		if self.__master is not None and self.__master[1] == self.SEDML:
			return join(self.__path, self.__master[0])

	def getAllSedmls(self):

		all_sedmls = self.__manifest.getAllSedmls()
		if len(all_sedmls) > 0:
			return [join(self.__path, sedml) for sedml in all_sedmls]

	# def getAllSbmls(self):
	#
	# 	all_sbmls = self.__manifest.getAllSbmls()
	# 	if len(all_sbmls) > 0:
	# 		return [join(self.__path, sbml) for sbml in all_sbmls]

	# def getTestSuiteExpectedResults(self):
	#
	# 	if self.__manifest.getTestSuiteExpectedResults() is not None:
	# 		return join(self.__path, self.__manifest.getTestSuiteExpectedResults())


	def runMasterSedml(self):

		if self.__master is not None and self.__master[1] == self.SEDML:

			filename = join(self.__path, self.__master[0])
			if exists(filename):
				# print "Running SED-ML file %s" % self.__master[0]
				sedml_doc = SedmlDocument()
				sedml_doc.readSedmlFromFile(filename)
				sedml_doc.run()
				return sedml_doc
		else:
			raise NoMasterSedmlFoundException()



	def runAllSedmls(self):

		all_sedmls = self.__manifest.getAllSedmls()
		sedml_docs = []
		if len(all_sedmls) > 0:

			for sedml_file in all_sedmls:
				filename = join(self.__path, sedml_file)
				if exists(filename):
					# print "Running SED-ML file %s" % sedml_file
					sedml_doc = SedmlDocument()
					sedml_doc.readSedmlFromFile(filename)
					sedml_doc.run()
					sedml_docs.append(sedml_doc)
			return sedml_docs
		else:
			raise NoSedmlFoundException()