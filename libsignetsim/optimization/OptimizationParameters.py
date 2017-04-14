#!/usr/bin/env python
""" OptimizationParameters.py


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


from os.path import join
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.sympy_shortcuts import SympySymbol

class OptimizationParameters(object):

	def __init__ (self, workingModel=None, parameters_to_fit=None):
		pass

	def readOptimizationOutput(self):

		f_optimized_parameters = open(join(self.getTempDirectory(), "logs/params/output"), 'r')
		now_reading = 0
		result = {}
		for line in f_optimized_parameters:
			# Comments
			if line.startswith("#"):
				pass

			# Empty line
			elif not line.strip():
				pass

			else:

				data = line.strip().split(":")

				if self.workingModel.listOfVariables.containsSymbol(SympySymbol(data[0].strip())):
					t_var = self.workingModel.listOfVariables.getBySymbol(SympySymbol(data[0].strip()))
					result.update({t_var: float(data[1].strip())})

		f_optimized_parameters.close()
		return result
