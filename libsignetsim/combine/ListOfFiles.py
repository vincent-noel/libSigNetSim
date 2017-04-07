#!/usr/bin/env python
""" ListOfFiles.py


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
from libsignetsim.combine.File import File
from libsignetsim.settings.Settings import Settings
from libsignetsim.combine.CombineException import NoManifestFoundException

class ListOfFiles(list):

	MANIFEST = "manifest.xml"

	def __init__(self, archive):

		list.__init__(self)
		self.__archive = archive
		self.__manifest = Manifest(self.__archive)


	def readListOfFiles(self, archive_file):

		if not self.MANIFEST in archive_file.namelist():
			# raise NoManifestFoundException("No manifest found")
			pass
		else:
			self.__manifest.readManifest(archive_file.read(self.MANIFEST))
			# self.__manifest.writeManifest()

		for t_file in archive_file.namelist():
			if not t_file.endswith("/") and t_file != self.MANIFEST:
				file = File(self.__archive, self.__manifest)
				file.readFile(t_file, archive_file)
				list.append(self, file)

		if self.__manifest.getMaster() is None:
			if len(self.getAllSedmls()) > 0:
				new_master = self.getAllSedmls()[0]
				new_master.setMaster()



	def writeManifest(self):
		return self.__manifest.writeManifest()

	def writeListOfFiles(self):
		return [file.getFilename() for file in self]

	# def getManifest(self):
	# 	return self.__manifest

	def getMaster(self):
		for file in self:
			if file.isMaster():
				return file


	def getAllSedmls(self):
		sedmls = []
		for file in self:
			if file.isSedml():
				sedmls.append(file)
		return sedmls