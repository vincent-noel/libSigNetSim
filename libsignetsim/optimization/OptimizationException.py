#!/usr/bin/env python
""" OptimizationException.py


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

class OptimizationException(Exception):

	COMP_ERROR  =   0
	EXEC_ERROR   =   1

	def __init__(self, value, message):

		self.value = value
		self.message = message

		def __str__(self):
			return "%d : %s" % (self.value, self.message)
