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

	This file ...

"""

from libsignetsim.LibSigNetSimException import LibSigNetSimException


class ModelException(LibSigNetSimException):
	pass

class CannotCreateException(ModelException):

	pass

class CannotDeleteException(ModelException):

	pass

class SbmlException(ModelException):

	pass

class FileException(ModelException):

	pass

class TagNotImplementedModelException(ModelException):

	def __init__(self, tag):
		self.tag = tag

	def __str__(self):
		return "The sbml tag %s is not implemented in libSigNetSim" % self.tag

class PackageNotImplementedModelException(ModelException):


	def __init__(self, package):
		self.package = package

	def __str__(self):
		return "The sbml package %s is not implemented in libSigNetSim" % self.package

class MissingModelException(ModelException):

	def __init__(self, filename):
		self.filename = filename

	def __str__(self):
		return self.filename


class MissingSubmodelException(ModelException):

	def __init__(self, filename):
		self.filename = filename

	def __str__(self):
		return self.filename

class UnknownSubmodelRefException(ModelException):
	pass

class UnknownSIdRefException(ModelException):
	pass

class InvalidXPath(ModelException):
	pass