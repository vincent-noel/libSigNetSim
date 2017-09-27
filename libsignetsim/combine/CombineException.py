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


class CombineException(LibSigNetSimException):
	pass

class FileNotFoundException(CombineException):
	pass

class NotAZipFileException(CombineException):
	pass

class NoManifestFoundException(CombineException):
	pass

class NoMasterSedmlFoundException(CombineException):
	pass

class NoMasterSbmlFoundException(CombineException):
	pass

class NoMasterNumlFoundException(CombineException):
	pass

class NoSedmlFoundException(CombineException):
	pass