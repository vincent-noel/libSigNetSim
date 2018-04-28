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


from os.path import join


class OptimizationParameters(object):

	def __init__(self, workingModel=None, parameters_to_fit=None, model_instance=False):
		self.__model = workingModel
		self.__modelInstance = model_instance
		self.__parameters = parameters_to_fit

	def readOptimizationOutput(self):

		f_optimized_parameters = open(join(self.getTempDirectory(), "logs/params/output"), 'r')

		result = {}
		for line in f_optimized_parameters:
			# Comments
			if line.startswith("#"):
				pass

			# Empty line
			elif not line.strip():
				pass

			else:
				data = line.strip().split(" : ")
				t_var = self.workingModel.parentDoc.getByXPath(data[0].strip(), self.__modelInstance)

				if t_var is not None:
					if self.__modelInstance:
						t_var = self.workingModel.getDefinitionVariable(t_var)[0]
					result.update({t_var: float(data[1].strip())})

		f_optimized_parameters.close()

		return result
