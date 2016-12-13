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


class OptimizationParameters(object):

	def __init__ (self, workingModel=None, parameters_to_fit=None):

		self.workingModel = workingModel

		self.constantsToFit = []
		self.constantsLowerBound = []
		self.constantsUpperBound = []

		self.initialValuesToFit_v2 = []
		self.initialValues_v2LowerBound = []
		self.initialValues_v2UpperBound = []

		if parameters_to_fit is not None:
			self.readParametersToFit(parameters_to_fit)

		else:
			self.defaultParametersToFit()


	def defaultParametersToFit(self):

		for parameter in self.workingModel.listOfParameters.values():
			# if parameter.isConstant():
			self.constantsToFit.append((2, parameter.objId))

		for reaction in self.workingModel.listOfReactions.values():
			for local_parameter in reaction.listOfLocalParameters.values():
				self.constantsToFit.append((3, (reaction.objId, local_parameter.objId)))


		self.constantsLowerBound = [Settings.optimizationDefaultConstantLowerBound for _ in range(0, len(self.constantsToFit))]
		self.constantsUpperBound = [Settings.optimizationDefaultConstantUpperBound for _ in range(0, len(self.constantsToFit))]
		self.initialValues_v2LowerBound = [Settings.optimizationDefaultInitialValueLowerBound for _ in range(0, len(self.initialValuesToFit_v2))]
		self.initialValues_v2UpperBound = [Settings.optimizationDefaultInitialValueUpperBound for _ in range(0, len(self.initialValuesToFit_v2))]


	def readParametersToFit(self, parameters_to_fit):

		for parameter in parameters_to_fit:

			(parameter_reaction,
				parameter_objid,
				parameter_active,
				parameter_name,
				parameter_value,
				parameter_min,
				parameter_max) = parameter

			if parameter_active:
				if parameter_reaction == None :
					self.constantsToFit.append((2, parameter_objid))
				else:
					self.constantsToFit.append((3, (parameter_reaction, parameter_objid)))

				self.constantsLowerBound.append(parameter_min)
				self.constantsUpperBound.append(parameter_max)


	def writeOptimizationInput(self):

		f_input = open(join(self.getTempDirectory(), "fit_input"), 'w')

		if len(self.constantsToFit) > 0:
			f_input.write("[constants]\n")
			for (i_constant, (type_constant, constant)) in enumerate(self.constantsToFit):
				if type_constant == 0:
					t_compartment = self.workingModel.listOfCompartments[constant]
					f_input.write(str(t_compartment.ind)
								  + "\t" + str(t_compartment.getValue())
								  + "\t" + str(self.constantsLowerBound[i_constant])
								  + "\t" + str(self.constantsUpperBound[i_constant])
								  + "\n")
				if type_constant == 1:
					t_species = self.workingModel.listOfSpecies[constant]
					f_input.write(str(t_species.ind)
								  + "\t" + str(t_species.getValue())
								  + "\t" + str(self.constantsLowerBound[i_constant])
								  + "\t" + str(self.constantsUpperBound[i_constant])
								  + "\n")
				if type_constant == 2:
					t_parameter = self.workingModel.listOfParameters[constant]
					f_input.write(str(t_parameter.ind)
								  + "\t" + str(t_parameter.getValue())
								  + "\t" + str(self.constantsLowerBound[i_constant])
								  + "\t" + str(self.constantsUpperBound[i_constant])
								  + "\n")
				if type_constant == 3:
					(r_obj_id, lp_obj_id) = constant
					t_local_parameter = self.workingModel.listOfReactions[r_obj_id].listOfLocalParameters[lp_obj_id]
					f_input.write(str(t_local_parameter.ind)
								  + "\t" + str(t_local_parameter.getValue())
								  + "\t" + str(self.constantsLowerBound[i_constant])
								  + "\t" + str(self.constantsUpperBound[i_constant])
								  + "\n")

		if len(self.initialValuesToFit_v2) > 0:
			f_input.write("[initial_values]\n")
			for i_initial_value, (type_initial_value, initial_value) in enumerate(self.initialValuesToFit_v2):
				if type_initial_value == 0:
					t_compartment = self.workingModel.listOfCompartments[initial_value]
					f_input.write(str(t_compartment.ind)
								  + "\t" + str(t_compartment.getValue())
								  + "\t" + str(self.initialValues_v2LowerBound[i_constant])
								  + "\t" + str(self.initialValues_v2UpperBound[i_constant])
								  + "\n")
				if type_initial_value == 1:
					t_species = self.workingModel.listOfSpecies[initial_value]
					f_input.write(str(t_species.ind)
								  + "\t" + str(t_species.getValue())
								  + "\t" + str(self.initialValues_v2LowerBound[i_constant])
								  + "\t" + str(self.initialValues_v2UpperBound[i_constant])
								  + "\n")
				if type_initial_value == 2:
					t_parameter = self.workingModel.listOfParameters[initial_value]
					f_input.write(str(t_parameter.ind)
								  + "\t" + str(t_parameter.getValue())
								  + "\t" + str(self.initialValues_v2LowerBound[i_constant])
								  + "\t" + str(self.initialValues_v2UpperBound[i_constant])
								  + "\n")

		f_input.close()

	def readOptimizationOutput(self):

		f_optimized_parameters = open(join(self.getTempDirectory(), "logs/params/output"), 'r')
		now_reading = 0
		for line in f_optimized_parameters:
			# Comments
			if line.startswith("#"):
				pass

			# Empty line
			elif not line.strip():
				pass

			# Parameter_label
			# elif line.strip() == "[constants]":
			# 	now_reading = 1
			# elif line.strip() == "[initial_values]":
			# 	now_reading = 2
			else:

				data = line.strip().split(":")

				if self.workingModel.listOfVariables.containsSbmlId(data[0].strip()):
					t_var = self.workingModel.listOfVariables.getBySbmlId(data[0].strip())
					print "New value of %s : %g" % (t_var.getNameOrSbmlId(), float(data[1].strip()))
				#
				# if now_reading == 1:
				# 	t_ind = int(data[0])
				# 	t_value = float(data[1])
				#
				# 	self.workingModel.variablesConstant[t_ind].setValue(t_value)
				#
				# elif now_reading == 2:
				# 	t_ind = int(data[0])
				# 	t_value = float(data[1])
				#
				# 	self.initialValuesToFit_v2[t_ind].setValue(t_value)

		f_optimized_parameters.close()
