#!/usr/bin/env python
""" SedmlException.py


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


class SedmlException(LibSigNetSimException):
	pass

class SedmlMathException(SedmlException):
	pass

class SedmlModelLanguageNotSupported(SedmlException):
	pass

class SedmlModelNotFound(SedmlException):
	pass

class SedmlFileNotFound(SedmlException):
	pass

class SedmlUnknownURI(SedmlException):
	pass

class SedmlUnknownXPATH(SedmlException):
	pass

class SedmlNotImplemented(SedmlException):
	pass

# One step simulations cannot be executed as a single task, they must be part of a repeated task
# At least, that's what I understand
class SedmlOneStepTaskException(SedmlException):
	pass

# Mixed subtasks are not implemented yet
class SedmlMixedSubtasks(SedmlNotImplemented):
	pass

class SedmlMultipleModels(SedmlNotImplemented):
	pass
