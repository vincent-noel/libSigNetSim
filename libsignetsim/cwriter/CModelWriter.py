#!/usr/bin/env python
""" CModelWriter.py


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


from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula

class CModelWriter(object):
	""" Sbml model class """

	def __init__ (self, obj_id=0):
		""" Constructor of model class """

		self.objId = obj_id


	def writeCCode(self, f_h, f_c, i_model, timeMin, timeEch, timeMax, absTol, relTol):


		self.writeSimulationInitialization(f_h, f_c, i_model, timeMin, timeEch, timeMax, absTol, relTol)
		self.writeSimulationFinalization(f_h, f_c, i_model)

		# self.writeInitialAssignments(f_h, f_c, i_model)

		if self.getMathModel().hasDAEs:
			self.writeIdaSimulationFunction(f_h, f_c, i_model)
		else:
			self.writeCVodeSimulationFunction(f_h, f_c, i_model)

		self.writeSimulationComputeRules(f_h, f_c, i_model)
		self.writeEventsTriggersFunction(f_h, f_c, i_model)
		self.writeEventsActivationFunction(f_h, f_c, i_model)
		self.writeEventsAssignmentFunction(f_h, f_c, i_model)
		self.writeEventsPriorityFunction(f_h, f_c, i_model)

	def writeSimulationInitialization(self, f_h, f_c, model_id, time_min, time_ech, time_max, abs_tol, rel_tol):
		""" Writes the model initialization function in C files """

		variable_name = "model_%d" % model_id

		f_h.write("void init_model_%d();\n" % model_id)
		f_c.write("void init_model_%d()\n{\n" % model_id)

		f_c.write("  %s.nb_derivative_variables = %d;\n" % (variable_name, self.getMathModel().nbOdes))
		f_c.write("  %s.nb_assignment_variables = %d;\n" % (variable_name, self.getMathModel().nbAssignments))
		f_c.write("  %s.nb_constant_variables = %d;\n" % (variable_name, self.getMathModel().nbConstants))
		f_c.write("  %s.nb_algebraic_variables = %d;\n" % (variable_name, self.getMathModel().nbAlgebraics))

		if self.getMathModel().nbOdes > 0:
			f_c.write("  %s.derivative_variables = (ModelVariable *) malloc(sizeof(ModelVariable) * %s.nb_derivative_variables);\n" % (variable_name, variable_name))

		if self.getMathModel().nbAssignments > 0:
			f_c.write("  %s.assignment_variables = (ModelVariable *) malloc(sizeof(ModelVariable) * %s.nb_assignment_variables);\n" % (variable_name, variable_name))

		if self.getMathModel().nbConstants > 0:
			f_c.write("  %s.constant_variables = (ModelVariable *) malloc(sizeof(ModelVariable) * %s.nb_constant_variables);\n" % (variable_name, variable_name))

		if self.getMathModel().nbAlgebraics > 0:
			f_c.write("  %s.algebraic_variables = (ModelVariable *) malloc(sizeof(ModelVariable) * %s.nb_algebraic_variables);\n" % (variable_name, variable_name))

		if self.getMathModel().hasDAEs:
			if self.getMathModel().nbOdes > 0:
				f_c.write("  %s.der_der_variables = (ModelVariable *) malloc(sizeof(ModelVariable) * %s.nb_derivative_variables);\n" % (variable_name, variable_name))
			if self.getMathModel().nbAlgebraics > 0:
				f_c.write("  %s.alg_der_variables = (ModelVariable *) malloc(sizeof(ModelVariable) * %s.nb_algebraic_variables);\n" % (variable_name, variable_name))

		for i_var, variable_ode in enumerate(self.getMathModel().variablesOdes):
			t_value = self.getMathModel().solvedInitialConditions[variable_ode]

			f_c.write("  %s.derivative_variables[%d] = (ModelVariable) {%s, \"%s\", VAR_DERIVATIVE};\n" % (
							variable_name, i_var, t_value.getCMathFormula(), variable_ode.symbol.getPrettyPrintMathFormula()))

			if self.getMathModel().hasDAEs:
				# print variable_ode.getSbmlId()
				# print variable_ode.getDerivativeCValue()
				# f_c.write("  %s.der_der_variables[%d] = (ModelVariable) {%s, \"%s\", VAR_DER_DER};\n" % (
				# 				variable_name, i_var, variable_ode.getDerivativeCValue(), variable_ode.symbol.getPrettyPrintMathFormula()))
				f_c.write("  %s.der_der_variables[%d] = (ModelVariable) {RCONST(0.0), \"%s\", VAR_DER_DER};\n" % (
								variable_name, i_var, variable_ode.symbol.getPrettyPrintMathFormula()))

		for i_var, variable_ass in enumerate(self.getMathModel().variablesAssignment):
			# if variable_ass.isReaction():
			# 	t_value = MathFormula(self)

			# 	t_value.setInternalMathFormula(MathFormula.ZERO)
			# else:
			t_value = self.getMathModel().solvedInitialConditions[variable_ass]

			f_c.write("  %s.assignment_variables[%d] = (ModelVariable) {%s, \"%s\", VAR_ASSIGNMENT};\n" % (
								variable_name, i_var, t_value.getCMathFormula(), variable_ass.symbol.getPrettyPrintMathFormula()))

		for i_var, variable_cst in enumerate(self.getMathModel().variablesConstant):

			# if variable_cst in self.solvedInitialConditions:
			t_value = self.getMathModel().solvedInitialConditions[variable_cst]
			# else:
				# t_value = variable_cst.value

			f_c.write("  %s.constant_variables[%d] = (ModelVariable) {%s, \"%s\", VAR_CONSTANT};\n" % (
								variable_name, i_var, t_value.getCMathFormula(), variable_cst.symbol.getPrettyPrintMathFormula()))


		for i_var, variable_alg in enumerate(self.getMathModel().variablesAlgebraic):
			t_value = self.getMathModel().solvedInitialConditions[variable_alg]

			f_c.write("  %s.algebraic_variables[%d] = (ModelVariable) {%s, \"%s\", VAR_ALGEBRAIC};\n" % (
								variable_name, i_var, t_value.getCMathFormula(), variable_alg.symbol.getPrettyPrintMathFormula()))


			if self.getMathModel().hasDAEs:
				# f_c.write("  %s.alg_der_variables[%d] = (ModelVariable) {%s, \"%s\", VAR_ALG_DER};\n" % (
				# 				variable_name, i_var, variable_alg.getDerivativeCValue(), variable_alg.symbol.getPrettyPrintMathFormula()))
				f_c.write("  %s.alg_der_variables[%d] = (ModelVariable) {RCONST(0.0), \"%s\", VAR_ALG_DER};\n" % (
								variable_name, i_var, variable_alg.symbol.getPrettyPrintMathFormula()))





		f_c.write("  %s.nb_init_assignments = 0;\n" % (variable_name))

		f_c.write("  %s.nb_events = %d;\n" % (variable_name, len(self.listOfEvents.keys())))
		f_c.write("  %s.nb_roots = %d;\n" % (variable_name, self.listOfEvents.nbRoots()))
		if self.listOfEvents.nbRoots() > 0:
			f_c.write("  %s.roots_operators = calloc(%d, sizeof(int));\n" % (variable_name, self.listOfEvents.nbRoots()))
			for i, roots_operators in enumerate(self.listOfEvents.getRootsOperators()):
				f_c.write("  %s.roots_operators[%d] = %d;\n" % (variable_name, i, roots_operators))

		if len(self.listOfEvents.keys()) > 0:
			f_c.write("  %s.events_init = calloc(%s.nb_events, sizeof(int));\n" % (variable_name, variable_name))
			for i, event in enumerate(self.listOfEvents.values()):
				f_c.write("  %s.events_init[%d] = %d;\n" % (variable_name, i, event.trigger.initialValue))


			f_c.write("  %s.memory_size_per_event = calloc(%s.nb_events, sizeof(int));\n" % (variable_name, variable_name))
			for event in self.listOfEvents.values():
				f_c.write("  %s.memory_size_per_event[%d] = %d;\n" % (variable_name, event.objId, event.memorySize()))

			f_c.write("  %s.events_has_priority = calloc(%s.nb_events, sizeof(int));\n" % (variable_name, variable_name))
			for event in self.listOfEvents.values():
				f_c.write("  %s.events_has_priority[%d] = %d;\n" % (variable_name, event.objId, event.priority is not None))


		f_c.write("  %s.integration_settings = malloc(sizeof(IntegrationSettings));\n" % variable_name)
		f_c.write("  %s.integration_settings->t_min = %g;\n" % (variable_name, time_min))
		f_c.write("  %s.integration_settings->t_max = %g;\n" % (variable_name, time_max))
		f_c.write("  %s.integration_settings->t_sampling = %g;\n" % (variable_name, time_ech))
		f_c.write("  %s.integration_settings->nb_samples = (int) round((%s.integration_settings->t_max-%s.integration_settings->t_min)/%s.integration_settings->t_sampling)+1;\n" % (variable_name, variable_name, variable_name, variable_name))
		f_c.write("  %s.integration_settings->abs_tol = %g;\n" % (variable_name, abs_tol))
		f_c.write("  %s.integration_settings->rel_tol = %g;\n" % (variable_name, rel_tol))
		f_c.write("  %s.integration_functions = malloc(sizeof(IntegrationFunctions));\n" % variable_name)

		if self.getMathModel().hasDAEs:
			f_c.write("  %s.integration_functions->funcIdaPtr = &func_ida_%d;\n" % (variable_name, model_id))
			f_c.write("  %s.integration_functions->isDAE = 1;\n" % variable_name)
			f_c.write("  %s.integration_functions->init_conditions_solved = 0;\n" % (variable_name))
		else:
			f_c.write("  %s.integration_functions->isDAE = 0;\n" % variable_name)
			f_c.write("  %s.integration_functions->funcPtr = &func_cvode_%d;\n" % (variable_name, model_id))
			# f_c.write("  %s.integration_functions->jacPtr = &jac_cvode_%d;\n" % (variable_name, model_id))
		f_c.write("  %s.integration_functions->assPtr = &compute_rules_%d;\n" % (variable_name, model_id))
		f_c.write("  %s.integration_functions->hasJacobian = 0;\n" % variable_name)

		if self.getMathModel().hasDAEs:
			f_c.write("  %s.integration_functions->rootsEventsIDAPtr = &roots_events_%d;\n" % (variable_name, model_id))
		else:
			f_c.write("  %s.integration_functions->rootsEventsPtr = &roots_events_%d;\n" % (variable_name, model_id))
		f_c.write("  %s.integration_functions->activateEventsPtr = &activate_events_%d;\n" % (variable_name, model_id))
		f_c.write("  %s.integration_functions->assignEventsPtr = &assign_events_%d;\n" % (variable_name, model_id))
		f_c.write("  %s.integration_functions->priorityEventsPtr = &priority_events_%d;\n" % (variable_name, model_id))

		f_c.write("  %s.integration_options = malloc(sizeof(IntegrationOptions));\n" % variable_name)
		f_c.write("  %s.integration_options->max_num_steps = %g;\n" % (variable_name, Settings.defaultCVODEmaxNumSteps))
		f_c.write("  %s.integration_options->max_conv_fails = %g;\n" % (variable_name, Settings.defaultCVODEMaxConvFails))
		f_c.write("  %s.integration_options->max_err_test_fails = %g;\n" % (variable_name, Settings.defaultCVODEMaxErrFails))
		# f_c.write("  rt_set_precision(RCONST(1e-16));\n")
		f_c.write("  rt_set_precision(RCONST(%g), RCONST(%g));\n" % (abs_tol, rel_tol))
		f_c.write("}\n\n")

	def writeSimulationFinalization(self, f_h, f_c, model_id):
		""" Writes the model initialization function in C files """

		variable_name = "model_%d" % model_id

		f_h.write("void finalize_model_%d();\n" % model_id)
		f_c.write("void finalize_model_%d()\n{\n" % model_id)

		if self.getMathModel().nbOdes > 0:
			f_c.write("  free(%s.derivative_variables);\n" % variable_name)

		if self.getMathModel().nbAssignments > 0:
			f_c.write("  free(%s.assignment_variables);\n" % variable_name)

		if self.getMathModel().nbConstants > 0:
			f_c.write("  free(%s.constant_variables);\n" % variable_name)

		if self.getMathModel().hasDAEs and self.getMathModel().nbOdes > 0:
			f_c.write("  free(%s.der_der_variables);\n" % variable_name)


		if self.listOfEvents.nbRoots() > 0:
			f_c.write("  free(%s.roots_operators);\n" % variable_name)

		if len(self.listOfEvents.keys()) > 0:
			f_c.write("  free(%s.events_init);\n" % variable_name)
			f_c.write("  free(%s.memory_size_per_event);\n" % variable_name)
			f_c.write("  free(%s.events_has_priority);\n" % variable_name)

		f_c.write("  free(%s.integration_settings);\n" % variable_name)

		f_c.write("  free(%s.integration_functions);\n" % variable_name)

		f_c.write("  free(%s.integration_options);\n" % variable_name)

		f_c.write("}\n\n")


	def writeIdaSimulationFunction(self, f_h, f_c, model_id):
		""" Writes the daes definition is C files """

		f_h.write("int func_ida_%d(realtype t, N_Vector y, N_Vector ydot, N_Vector r, void *user_data);\n" % model_id)
		f_c.write("int func_ida_%d(realtype t, N_Vector y, N_Vector ydot, N_Vector r, void *user_data)\n" % model_id)
		f_c.write("{\n")
		f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
		f_c.write("  N_Vector cst = data->constant_variables;\n")
		f_c.write("  N_Vector ass = data->assignment_variables;\n")
		# f_c.write("  N_Vector alg = data->algebraic_variables;\n")
		f_c.write("  compute_rules_%d(t, y, user_data);\n" % model_id)

		i_var = 0
		for i_ode, t_ode in enumerate(self.getMathModel().listOfODEs):
			# t_var = self.listOfVariables[str(self.ODE_vars[i_ode].getFinalMathFormula().func)]
			t_var = t_ode.getVariable()
			f_c.write("  // ODE\n")
			f_c.write("  Ith(r, %d) = %s - Ith(ydot, %d);\n\n" % (i_var+1, t_ode.getDefinition().getCMathFormula(), t_var.ind+1))
			i_var += 1

		for i_dae, t_dae in enumerate(self.getMathModel().listOfDAEs):
			f_c.write("  // DAE\n")
			f_c.write("  Ith(r, %d) = %s;\n\n" % (i_var+1, t_dae.getDefinition().getCMathFormula()))
			i_var += 1

		f_c.write("  return 0;\n")
		f_c.write("}\n\n")


	def writeCVodeSimulationFunction(self, f_h, f_c, model_id):
		""" Writes the odes definition in C files """

		f_h.write("int func_cvode_%d(realtype t, N_Vector y, N_Vector ydot, void *user_data);\n" % model_id)
		f_c.write("int func_cvode_%d(realtype t, N_Vector y, N_Vector ydot, void *user_data)\n" % model_id)
		f_c.write("{\n")

		if len(self.getMathModel().listOfODEs) > 0:

			f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
			f_c.write("  N_Vector cst = data->constant_variables;\n")
			f_c.write("  N_Vector ass = data->assignment_variables;\n")
			f_c.write("  compute_rules_%d(t,y, user_data);\n" % model_id)

			i_var = 0
			for i_ode, t_ode in enumerate(self.getMathModel().listOfODEs):
				t_var = t_ode.getVariable()
				f_c.write("  // ODE\n")
				f_c.write("  Ith(ydot, %d) = %s;\n\n" % ( t_var.ind+1, t_ode.getDefinition().getCMathFormula()))
				i_var += 1

		f_c.write("  return 0;\n")
		f_c.write("}\n\n")



	def writeSimulationJacobianMatrixFunction(self, f_h, f_c, model_id):
		""" Writes the jacobian matrix definition in C files """

		variable_name="model_%d" % model_id

		f_h.write(("int jac_cvode_%d(long int N, realtype t, N_Vector y, N_Vector fy, "
				   "DlsMat J, void *user_data, N_Vector tmp1, N_Vector tmp2, N_Vector tmp3);\n") % model_id)

		#Writing cvode_jacobian_matrix
		f_c.write(("int jac_cvode_%d(long int N, realtype t, N_Vector y, N_Vector fy, "
				   "DlsMat J, void *user_data, N_Vector tmp1, N_Vector tmp2, N_Vector tmp3)\n") % model_id)
		f_c.write("{\n")

		# f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
		# f_c.write("  N_Vector cst = data->constant_variables;\n")
		# f_c.write("  N_Vector ass = data->assignment_variables;\n")
		# f_c.write("  compute_rules_%d(t,y, user_data);\n" % model_id)
		#
		# i_var = 0
		# for variable in self.listOfVariables.values():
		#     if variable.isRateRuled() or (not variable.constant and not variable.isRuled()):
		#
		#         i_var_der = 0
		#         for variable_der in self.listOfVariables.values():
		#             if variable_der.isRateRuled() or (not variable.constant and not variable.isRuled()):
		#
		#                 f_c.write("  IJth(J, %d, %d) = %s;\n\n" % (i_var+1, i_var_der+1, variable.getODEDerivative(MathFormula.MATH_C, variable_der)))
		#                 i_var_der += 1
		#
		#         i_var += 1

		f_c.write("  return 0;\n")
		f_c.write("}\n\n")


	def writeSimulationComputeRules(self, f_h, f_c, model_id):
		""" Writes the rules definition function in C files """

		f_h.write("int compute_rules_%d(realtype t, N_Vector y, void * user_data);\n" % model_id)
		f_c.write("int compute_rules_%d(realtype t, N_Vector y, void * user_data)\n{\n" % model_id)
		if len(self.getMathModel().listOfCFEs) > 0:
			f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
			f_c.write("  N_Vector cst = data->constant_variables;\n")
			f_c.write("  N_Vector ass = data->assignment_variables;\n")

			for i_cfe, t_cfe in enumerate(self.getMathModel().listOfCFEs.developpedCFEs):

				t_var = t_cfe.getVariable()
				f_c.write("  Ith(ass, %s) = %s;\n" % (
								t_var.ind+1,
								t_cfe.getDefinition().getCMathFormula()
				))

		f_c.write("  return 0;\n}\n")


	def writeEventsTriggersFunction(self, f_h, f_c, model_id):
		""" Writes the events conditions function in C files """

		variable_name="model_%d" % model_id

		if self.getMathModel().hasDAEs:
			f_h.write("int roots_events_%d(realtype t, N_Vector y, N_Vector yp, realtype *gout,void *user_data);\n" % model_id)
			f_c.write("int roots_events_%d(realtype t, N_Vector y, N_Vector yp, realtype *gout,void *user_data)\n{\n" % model_id)
		else:
			f_h.write("int roots_events_%d(realtype t, N_Vector y, realtype *gout,void *user_data);\n" % model_id)
			f_c.write("int roots_events_%d(realtype t, N_Vector y, realtype *gout,void *user_data)\n{\n" % model_id)
		if len(self.listOfEvents) > 0:

			f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
			f_c.write("  N_Vector cst = data->constant_variables;\n")
			f_c.write("  N_Vector ass = data->assignment_variables;\n")
			f_c.write("  compute_rules_%d(t,y, user_data);\n" % model_id)

			i_event = 0
			for event in self.listOfEvents.values():
				t_distances = event.trigger.getRootsFunctions()
				for t_distance in t_distances:
					f_c.write("  gout[%d] = %s;\n" % (i_event, t_distance))
					i_event += 1

		f_c.write("  return 0;\n}\n")



	def writeEventsActivationFunction(self, f_h, f_c, model_id):
		""" Writes the events conditions function in C files """

		variable_name="model_%d" % model_id


		f_h.write("int activate_events_%d(realtype t, N_Vector y, void * user_data);\n" % model_id)
		f_c.write("int activate_events_%d(realtype t, N_Vector y, void * user_data)\n{\n" % model_id)
		f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
		f_c.write("  N_Vector cst = data->constant_variables;\n")
		f_c.write("  N_Vector ass = data->assignment_variables;\n")

		i_roots = 0
		i_roots2 = 0

		for i_event, event in enumerate(self.listOfEvents.values()):

			# Events deactivation
			(t_deactivation_condition, i_roots) = event.trigger.getDeactivationCondition(i_roots)

			f_c.write(("  if ((data->events_ready[%d] == 0) && %s)\n  {\n"
					+ "    data->events_ready[%d] = 1;\n")
					% (i_event, t_deactivation_condition, i_event))

			if not event.trigger.isPersistent:
				f_c.write("    data->events_triggers[%d]--;\n" % i_event)
				f_c.write("    untriggerChildren(data, %d);\n" % i_event)

			f_c.write("  }\n\n")


			# Events activation
			# Condition
			(t_activation_condition, i_roots2) = event.trigger.getActivationCondition(i_roots2)

			f_c.write(("  else if ((data->events_ready[%d] == 1) && %s)\n  {\n"
						+ "    data->events_ready[%d] = 0;\n")
						% (i_event, t_activation_condition, i_event))

			if event.delay is not None:
				if not event.trigger.isPersistent:
					f_c.write("    retriggerChildren(data, %d);\n" % i_event)

				f_c.write("    realtype * memory = addTimedEvent(t+%s, %d, %d, user_data);\n"
							% (event.delay.getCMathFormula(), i_event, event.memorySize()))

			else:
				f_c.write("    data->events_triggers[%d]++;\n" % i_event)

			for i_assignment, event_assignment in enumerate(event.listOfEventAssignments):
				if event.useValuesFromTriggerTime:
					if event.delay is not None:
						f_c.write("    memory[%d] = %s;\n"
								% (i_assignment,
								event_assignment.getDefinition().getCMathFormula()))

					else:
						# print "event assignment = %s" % event_assignment.definition.getCMathFormula()
						f_c.write("    data->events_memory[%d][%d] = %s;\n"
								% (i_event, i_assignment,
								event_assignment.getDefinition().getCMathFormula()))


			f_c.write("  }\n\n")

		f_c.write("  return 0;\n}\n")


	def writeEventsAssignmentFunction(self, f_h, f_c, model_id):
		""" Writes the events assignments function in C files """

		variable_name="model_%d" % model_id

		f_h.write("int assign_events_%d(realtype t, N_Vector y, void *user_data, int assignment_id, realtype * memory);\n" % model_id)
		f_c.write("int assign_events_%d(realtype t, N_Vector y, void *user_data, int assignment_id, realtype * memory)\n{\n" % model_id)
		if len(self.listOfEvents) > 0:

			f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
			f_c.write("  N_Vector cst = data->constant_variables;\n")
			f_c.write("  N_Vector ass = data->assignment_variables;\n")

			f_c.write("  switch(assignment_id) {\n")

			i_event = 0
			i_roots2 = 0
			for event in self.listOfEvents.values():

				f_c.write("    case %d :\n" % i_event)

				for i_assignment, event_assignment in enumerate(event.listOfEventAssignments):
					if event.useValuesFromTriggerTime:
						if event.delay is not None:
							f_c.write("      %s = memory[%d];\n"
								% (event_assignment.getVariable().symbol.getCMathFormula(),
									i_assignment))

						else:
							f_c.write("      %s = data->events_memory[%d][%d];\n"
								% (event_assignment.getVariable().symbol.getCMathFormula(),
									i_event, i_assignment))

					else:
						# We need to put an empty statement for some weird rule
						# about a declaration not being allowed as first instruction
						f_c.write("      ;\n")
						f_c.write("      realtype t_var_%d_%d = %s;\n"
								% (i_event, i_assignment,
									event_assignment.getDefinition().getCMathFormula()))
				for i_assignment, event_assignment in enumerate(event.listOfEventAssignments):
					if not event.useValuesFromTriggerTime:

						f_c.write("      %s = t_var_%d_%d;\n"
								% (event_assignment.getVariable().symbol.getCMathFormula(),
									i_event, i_assignment))

				f_c.write("      break;\n")
				i_event += 1

			f_c.write("  }\n")

		f_c.write("  return 0;\n}\n")


	def writeEventsPriorityFunction(self, f_h, f_c, model_id):

		variable_name="model_%d" % model_id

		f_h.write("int priority_events_%d(realtype t, N_Vector y, void *user_data);\n" % model_id)
		f_c.write("int priority_events_%d(realtype t, N_Vector y, void *user_data)\n{\n" % model_id)
		if len(self.listOfEvents) > 0:

			f_c.write("  IntegrationData * data = (IntegrationData *) user_data;\n")
			f_c.write("  N_Vector cst = data->constant_variables;\n")
			f_c.write("  N_Vector ass = data->assignment_variables;\n")
			# f_c.write("  N_Vector alg = data->algebraic_variables;\n")

			for i, event in enumerate(self.listOfEvents.values()):

				if event.priority is not None:
					f_c.write("  *(data->events_priorities[%d]) = %s;\n" % (i, event.priority.getCMathFormula()))

		f_c.write("  return 0;\n}\n")
