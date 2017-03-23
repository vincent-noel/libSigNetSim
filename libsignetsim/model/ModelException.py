#!/usr/bin/env python
""" ModelException.py


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

from libsignetsim.LibSigNetSimException import LibSigNetSimException


class CannotCreateException(LibSigNetSimException):

	pass

class CannotDeleteException(LibSigNetSimException):

	pass

class SbmlException(LibSigNetSimException):

	pass

class MathException(LibSigNetSimException):

	pass

class FileException(LibSigNetSimException):

	pass

#
# class ModelException(Exception):
#
# 	def __init__(self, value, message):
#
# 		self.value = value
# 		self.message = message
#
# 	def __str__(self):
# 		return "%d : %s" % (self.value, self.message)

class TagNotImplementedModelException(Exception):


	def __init__(self, tag):
		self.tag = tag

	def __str__(self):
		return "The sbml tag %s is not implemented in libSigNetSim" % self.tag

class PackageNotImplementedModelException(Exception):


	def __init__(self, package):
		self.package = package

	def __str__(self):
		return "The sbml package %s is not implemented in libSigNetSim" % self.package

class MissingModelException(Exception):

	def __init__(self, filename):
		self.filename = filename

	def __str__(self):
		return self.filename


class MissingSubmodelException(Exception):

	def __init__(self, filename):
		self.filename = filename

	def __str__(self):
		return self.filename
