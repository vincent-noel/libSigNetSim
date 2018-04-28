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

	Initialization of the combine archive module

"""

from .Manifest import Manifest
from .File import File
from libsignetsim.settings.Settings import Settings
from .CombineException import NoManifestFoundException

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
			# with archive_file.read(self.MANIFEST) as manifest_file:
			# 	self.__manifest.readManifest(manifest_file)
			self.__manifest.readManifest(archive_file.read(self.MANIFEST))
		# self.__manifest.writeManifest()

		for t_file in archive_file.namelist():
			if not t_file.endswith("/") and t_file != self.MANIFEST:
				file = File(self.__archive, self.__manifest)
				file.readFile(t_file, archive_file)
				list.append(self, file)

		if self.getMasterSedml() is None and self.__archive.isSEDMLArchive():
			if len(self.getAllSedmls()) > 0:
				new_master = self.getAllSedmls()[0]
				new_master.setMaster()

	def addFile(self, filename):

		file = File(self.__archive, self.__manifest)
		file.newFile(filename)
		list.append(self, file)
		return file

	def writeManifest(self):
		return self.__manifest.writeManifest()

	def writeListOfFiles(self):
		return [file.getFilename() for file in self]

	# def getManifest(self):
	# 	return self.__manifest

	def getMasterSedml(self):
		for file in self:
			if file.isMaster() and file.isSedml():
				return file

	def getAllSedmls(self):
		return [file for file in self if file.isSedml()]

	def getMasterSbml(self):
		for file in self:
			if file.isMaster() and file.isSbml():
				return file

	def getAllSbmls(self):
		return [file for file in self if file.isSbml()]

	def getAllNumls(self):
		return [file for file in self if file.isNuml()]

	def getMasterNuml(self):
		for file in self:
			if file.isMaster() and file.isNuml():
				return file
