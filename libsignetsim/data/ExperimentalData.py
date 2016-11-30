#!/usr/bin/env python
""" ExperimentalData.py


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

class ExperimentalData(object):

	def __init__ (self):

		self.value = 0
		self.value_dev = None
		self.t = 0
		self.quantification_ratio = 1

		self.steady_state = False
		self.min_steady_state = 0
		self.max_steady_state = 0

		self.variableName = ""
		self.variableId = None
		self.name = ""


	def readDB(self, name, time, value, value_dev=0, steady_state=False, min_steady_state=0, max_steady_state=0,quantification_ratio=1):

		self.name = name
		self.t = time
		self.value = value
		self.value_dev = value_dev
		self.steady_state = steady_state
		if steady_state:
			self.min_steady_state = min_steady_state
			self.max_steady_state = max_steady_state
		self.quantification_ratio = quantification_ratio
