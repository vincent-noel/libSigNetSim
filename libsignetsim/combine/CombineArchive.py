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
from os.path import exists, join, isdir
from os import mkdir

class CombineArchive(object):

	OMEX = "Default combine archive"
	SEDX = "SED-ML archive"
	SBEX = "SBML archive"
	CMEX = "CellML archive"
	NEUX = "NeuroML archive"
	PHEX = "PharmaML archive"
	SBOX = "SBOL archive"

	ARCHIVE_EXTENSIONS = {
		"omex": OMEX,
		"sedx": SEDX,
		"sbex": SBEX,
		"cmex": CMEX,
		"neux": NEUX,
		"phex": PHEX,
		"sbox": SBOX
	}

	SEDML = "sed-ml"

	def __init__(self):

		self.__file = None
		self.__listOfFiles = ListOfFiles(self)
		self.__path = Settings.tempDirectory + ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(12))
		if not isdir(self.__path):
			mkdir(self.__path)
		self.__extension = None

	def readArchive(self, file):

		if not exists(file):
			raise FileNotFoundException("File %s not found" % file)

		if not is_zipfile(file):
			raise NotAZipFileException("File %s is not a zip file" % file)

		self.__file = ZipFile(file)
		self.__extension = file.split(".")[-1]
		self.__listOfFiles.readListOfFiles(self.__file)

		self.extractArchive()
		#TODO : browse the manifest, check if the archive exists, then create add the file to the list of files ?

	def getListOfFiles(self):
		return self.__listOfFiles

	def extractArchive(self):
		self.__file.extractall(self.__path)

	def writeArchive(self, filename):

		manifest_file= open(join(self.__path, "manifest.xml"), "w")
		manifest_file.write(self.__listOfFiles.writeManifest())
		manifest_file.close()

		self.__file = ZipFile(filename, mode='w')
		self.__file.write(join(self.__path, "manifest.xml"), "manifest.xml")

		for file in self.__listOfFiles.writeListOfFiles():

			self.__file.write(join(self.__path, file), file)

		self.__file.close()

	def getMasterSedml(self):

		if self.__listOfFiles.getMasterSedml() is not None:
			return join(self.__path, self.__listOfFiles.getMasterSedml().getFilename())
		else:
			raise NoMasterSedmlFoundException("No master Sedml found")


	def getAllSedmls(self):

		all_sedmls = self.__listOfFiles.getAllSedmls()
		return [join(self.__path, sedml.getFilename()) for sedml in all_sedmls]

	def runMasterSedml(self):

		filename = self.getMasterSedml()

		if exists(filename):
			return self.runSedml(filename)

	def runAllSedmls(self):

		all_sedmls = self.__listOfFiles.getAllSedmls()
		sedml_docs = []

		if len(all_sedmls) > 0:

			for sedml_file in all_sedmls:
				filename = join(self.__path, sedml_file.getFilename())
				if exists(filename):
					sedml_docs.append(self.runSedml(filename))

			return sedml_docs

		else:
			raise NoSedmlFoundException()

	def getMasterSedmlDoc(self):

		filename = self.getMasterSedml()

		if exists(filename):
			return self.getSedmlDoc(filename)

	def getSedmlDoc(self, filename):

		sedml_doc = SedmlDocument()
		sedml_doc.readSedmlFromFile(filename)
		return sedml_doc

	def runSedml(self, filename):

		sedml_doc = self.getSedmlDoc(filename)
		sedml_doc.run()
		return sedml_doc


	def getAllSbmls(self):

		all_sbmls = self.__listOfFiles.getAllSbmls()
		return [join(self.__path, sbml.getFilename()) for sbml in all_sbmls]

	def getAllNumls(self):

		all_numls = self.__listOfFiles.getAllNumls()
		return [join(self.__path, numl.getFilename()) for numl in all_numls]

	def getPath(self):
		return self.__path

	def isDefaultCombineArchive(self):
		return self.__extension in self.ARCHIVE_EXTENSIONS and self.ARCHIVE_EXTENSIONS[self.__extension] == self.OMEX

	def isSEDMLArchive(self):
		return self.__extension in self.ARCHIVE_EXTENSIONS and self.ARCHIVE_EXTENSIONS[self.__extension] == self.SEDX

	def isSBMLArchive(self):
		return self.__extension in self.ARCHIVE_EXTENSIONS and self.ARCHIVE_EXTENSIONS[self.__extension] == self.SBEX

	def isCellMLArchive(self):
		return self.__extension in self.ARCHIVE_EXTENSIONS and self.ARCHIVE_EXTENSIONS[self.__extension] == self.CMEX

	def isNeuroMLArchive(self):
		return self.__extension in self.ARCHIVE_EXTENSIONS and self.ARCHIVE_EXTENSIONS[self.__extension] == self.NEUX

	def isPharmaMLArchive(self):
		return self.__extension in self.ARCHIVE_EXTENSIONS and self.ARCHIVE_EXTENSIONS[self.__extension] == self.PHEX

	def isSBOLArchive(self):
		return self.__extension in self.ARCHIVE_EXTENSIONS and self.ARCHIVE_EXTENSIONS[self.__extension] == self.SBOX

	def addFile(self, filename):

		self.__listOfFiles.addFile(filename)
