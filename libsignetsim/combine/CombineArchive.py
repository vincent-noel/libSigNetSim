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
	FileNotFoundException, NotAZipFileException, NoMasterSedmlFoundException,
	NoSedmlFoundException
)
from libsignetsim.sedml.SedmlDocument import SedmlDocument
from libsignetsim.settings.Settings import Settings

from zipfile import is_zipfile, ZipFile
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from os.path import exists, join

class CombineArchive(object):


	SEDML = "sed-ml"

	def __init__(self):

		self.__file = None
		self.__listOfFiles = ListOfFiles(self)
		self.__path = Settings.tempDirectory + ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(12))

	def readFile(self, file):

		if not exists(file):
			raise FileNotFoundException("File %s not found" % file)

		if not is_zipfile(file):
			raise NotAZipFileException("File %s is not a zip file" % file)

		self.__file = ZipFile(file)
		self.__listOfFiles.readListOfFiles(self.__file)

		self.extractArchive()
		self.__listOfFiles.writeListOfFiles()
		#TODO : browse the manifest, check if the archive exists, then create add the file to the list of files ?

	def getListOfFiles(self):
		return self.__listOfFiles

	def extractArchive(self):

		self.__file.extractall(self.__path)

	def getMasterSedml(self):

		if self.__listOfFiles.getMaster() is not None and self.__listOfFiles.getMaster().isSedml():
			return join(self.__path, self.__listOfFiles.getMaster().getFilename())
		else:
			raise NoMasterSedmlFoundException("No master Sedml found")


	def getAllSedmls(self):

		all_sedmls = self.__listOfFiles.getAllSedmls()
		if len(all_sedmls) > 0:
			return [join(self.__path, sedml.getFilename()) for sedml in all_sedmls]

	def runMasterSedml(self):

		filename = self.getMasterSedml()
		if exists(filename):
			return self.runSedml(filename)

	def runAllSedmls(self):

		all_sedmls = self.__manifest.getAllSedmls()
		sedml_docs = []

		if len(all_sedmls) > 0:

			for sedml_file in all_sedmls:
				filename = join(self.__path, sedml_file)
				if exists(filename):
					sedml_docs.append(self.runSedml(filename))

			return sedml_docs

		else:
			raise NoSedmlFoundException()

	def runSedml(self, filename):

		sedml_doc = SedmlDocument()
		sedml_doc.readSedmlFromFile(filename)
		sedml_doc.run()
		return sedml_doc
	#
	# def getfileContent(self, filename):
	#
	# 	file = open(filename, 'r')
	# 	return f