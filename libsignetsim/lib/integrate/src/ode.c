/******************************************************************************
 *                                                                            *
 *   ode.h                                                                    *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Fonction for integrating ODE model with CVODE                            *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)           *
 *                                                                            *
 *   This file is part of libSigNetSim.                                       *
 *                                                                            *
 *   libSigNetSim is free software: you can redistribute it and/or modify     *
 *   it under the terms of the GNU General Public License as published by     *
 *   the Free Software Foundation, either version 3 of the License, or        *
 *   (at your option) any later version.                                      *
 *                                                                            *
 *   libSigNetSim is distributed in the hope that it will be useful,          *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of           *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            *
 *   GNU General Public License for more details.                             *
 *                                                                            *
 *   You should have received a copy of the GNU General Public License        *
 *   along with SigNetSim.  If not, see <http://www.gnu.org/licenses/>.       *
 *                                                                            *
 ******************************************************************************/

#define Ith(v,i)    NV_Ith_S(v,i-1)       /* Ith numbers components 1..NEQ */
#define MAX(a,b) (((a)>(b))?(a):(b))
#define MIN(a,b) (((a)<(b))?(a):(b))

#include <cvode/cvode.h>             /* prototypes for CVODE fcts., consts. */
#include <cvode/cvode_dense.h>       /* prototype for CVDense */
#include <stdlib.h>
#include <float.h>                   /* for DBL_MAX */
#include <limits.h>                  /* for INT_MAX */
#include "ode.h"
#include "shared.h"

int func_empty(realtype t, N_Vector y, N_Vector ydot, void *user_data)
{
	Ith(ydot, 1) = RCONST(0);
	return 0;
}


int roots_wrapper_cvode(realtype t, N_Vector y, realtype * gout, void * user_data)
{
  IntegrationData * data = (IntegrationData *) user_data;

  if (data->nb_events > 0)
	(*data->rootsEventsPtr)(t, y, gout, user_data);

  roots_wrapper(data, t, gout);

  return 0;
}


void * InitializeCVODE(ModelDefinition * model, IntegrationData * user_data, ExperimentalCondition * condition, FILE * errLog)
{
	int flag;

	/* Call CVodeCreate to create the solver memory and specify the
	 * Backward Differentiation Formula and the use of a Newton iteration */
	void * cvode_mem = CVodeCreate(CV_BDF, CV_NEWTON);
	//  void * cvode_mem = CVodeCreate(CV_ADAMS, CV_FUNCTIONAL);

	if (check_flag((void *)cvode_mem, "CVodeCreate", 0, errLog))
		return NULL;

	/* Call CVodeInit to initialize the integrator memory and specify the
	 * user's right hand side function in y'=f(t,y), the inital time T0, and
	 * the initial dependent variable vector y. */
	if (model->nb_derivative_variables > 0)
		flag = CVodeInit(cvode_mem, model->integration_functions->funcPtr,
						  RCONST(model->integration_settings->t_min),
						  user_data->derivative_variables);
	else
		flag = CVodeInit(cvode_mem, func_empty,
						  RCONST(model->integration_settings->t_min),
						  user_data->derivative_variables);

	if (check_flag(&flag, "CVodeInit", 1, errLog))
		return NULL;

	/* Call SVtolerances to specify the scalar relative tolerance
	 * and vector absolute tolerances */
	flag = CVodeSVtolerances(cvode_mem, user_data->rel_tol, user_data->abs_tol);
	if (check_flag(&flag, "CVodeSVtolerances", 1, errLog))
		return NULL;

	/* Call SetErrTestFails to set the max value of failed error test */
	flag = CVodeSetMaxErrTestFails(cvode_mem, model->integration_options->max_err_test_fails);
	if (check_flag(&flag, "CvodeSetMaxErrTestFails", 1, errLog))
		return NULL;

	/* Call SetMaxConvFails to set the max value of convergence failures */
	flag = CVodeSetMaxConvFails(cvode_mem, model->integration_options->max_conv_fails);
	if (check_flag(&flag, "CvodeSetMaxConvFails", 1, errLog))
		return NULL;

	/* Call CVodeSetMaxNumSteps to set the max number of internal steps */
	flag = CVodeSetMaxNumSteps(cvode_mem, model->integration_options->max_num_steps);
	if (check_flag(&flag, "CvodeSetMaxNumSteps", 1, errLog))
		return NULL;

	/* Call Dense to specify the dense linear solver */
	flag = CVDense(cvode_mem, MAX(model->nb_derivative_variables, 1));
	if (check_flag(&flag, "CVDense", 1, errLog))
		return NULL;

	// /* Set the Jacobian routine to Jac (user-supplied) */
	// if (model->integration_functions->hasJacobian == 1)
	// {
	//     flag = CVDlsSetDenseJacFn(cvode_mem, model->integration_functions->jacPtr);
	//     if (check_flag(&flag, "CVDlsSetDenseJacFn", 1, errLog))
	//         return NULL;
	// }

	if (user_data->nb_events > 0 || user_data->nb_timed_treatments > 0)
	{
		/* Call RootInit to specify the root function g with 2 components */
		flag = CVodeRootInit(cvode_mem, (getNbRoots(user_data) + getNbTimedTreatments(user_data)), &roots_wrapper_cvode);
		if (check_flag(&flag, "CVodeRootInit", 1, errLog))
			return NULL;
	}

	/* Call SetUserData to specify the object accessible during the integration */
	flag = CVodeSetUserData(cvode_mem,user_data);
	if (check_flag(&flag, "CvodeSetUserData", 1, errLog))
		return NULL;

	//Redirect StdErr printing
	flag = CVodeSetErrFile(cvode_mem,errLog);
	if (check_flag(&flag, "CvodeSetErrFile", 1, errLog))
		return NULL;

	return cvode_mem;
}

void updateRootsCVODE(IntegrationData * user_data, realtype t)
{

	realtype * t_roots = malloc(sizeof(realtype)*(getNbRoots(user_data) + getNbTimedTreatments(user_data)));
	roots_wrapper_cvode(t, user_data->derivative_variables,
								  t_roots, (void *) user_data);

	updateRoots(user_data, t_roots);

	free(t_roots);

	roots_wrapper_cvode(t, user_data->derivative_variables,
						  user_data->roots_values, (void *) user_data);

	activate_wrapper(user_data, t);

}

void executeEventsCVODE(IntegrationData * user_data, realtype t)
{
	int i;
	int nb_events_activated = INT_MAX;

	roots_wrapper_cvode(t, user_data->derivative_variables,
								user_data->roots_values, (void *) user_data);

	while(nb_events_activated > 0)
	{

		activate_wrapper(user_data, t);

		Events * events_activated = getActivatedEvents(user_data);
		nb_events_activated = events_activated->len;

		int * executed_events = calloc(nb_events_activated, sizeof(int));
		int nb_executed = 0;

		while (nb_executed < nb_events_activated)
		{

			Events * concurrent_events = getNextConcurrentEvents(user_data,
										  events_activated, executed_events, t);

			shuffle(concurrent_events);

			for (i=0; i < concurrent_events->len; i++)
			{
				int t_event = concurrent_events->list[i];
				if (user_data->events_triggers[t_event] > 0)
				{
					execute(user_data, t, t_event);
					updateRootsCVODE(user_data, t);
					mark_executed(user_data, t_event);
				}
				nb_executed++;
			}
			freeEvents(concurrent_events);
		}
		free(executed_events);
		freeEvents(events_activated);
	}

	// here we execute the timed treatments, last events to execute
	executeTimedTreatments(user_data);

}

IntegrationResult * simulateModelCVODE(ModelDefinition * model,
										ExperimentalCondition * condition,
										FILE * errLog,
										IntegrationResult * result)
{
	realtype t, tout;
	int flag, iout, i;

	IntegrationData * user_data = InitializeIntegrationData(model, condition, errLog);
	if (user_data == NULL)
		return result;

	void * cvode_mem = InitializeCVODE(model, user_data, condition, errLog);

	iout = 0;
	t = RCONST(result->time_min);

////	 Firing Initial Assignments
//	 if (model->nb_init_assignments > 0) {
//	 	model->integration_functions->initAssPtr(t, user_data->derivative_variables, (void *) user_data);
//	 	flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);
//	 	if (check_flag(&flag, "CVodeReInit", 1, errLog)) return NULL;
//	 }

	if ((user_data->nb_events + user_data->nb_timed_treatments) > 0)
	{
		// priority_wrapper(user_data, t);
		(*user_data->priorityEventsPtr)(t, user_data->derivative_variables, (void *) user_data);

		realtype * t_roots = malloc(sizeof(realtype)*(getNbRoots(user_data) + getNbTimedTreatments(user_data)));

		roots_wrapper_cvode(t, user_data->derivative_variables,
											  t_roots, (void *) user_data);

		initRoots(user_data, t_roots);
		free(t_roots);

		/* We inactivate the events which are not off at t0 */
		for (i=0; i < model->nb_events; i++)
			if (model->events_init[i] == 1)
				user_data->events_ready[i] = 0;

		executeEventsCVODE(user_data, t);

		for (i=0; i < model->nb_events; i++)
			if (model->events_init[i] == 1)
			{
			  user_data->events_triggers[i] = 0;
			  user_data->events_ready[i] = 1;
			}

		//And we reinit the solver to accept this change of value
		flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);

		if (check_flag(&flag, "CVode", 1, errLog))
		{
			FinalizeIntegrationData(model, user_data);
			CVodeFree(&cvode_mem);
			return result;
		}


		/* Call RootInit to update the root function */
		flag = CVodeRootInit(cvode_mem,
							  (getNbRoots(user_data) + getNbTimedTreatments(user_data)),
							  &roots_wrapper_cvode);
		if (check_flag(&flag, "CVodeRootInit", 1, errLog))
			return NULL;

	}
//	 Firing Initial Assignments
	 if (model->nb_init_assignments > 0) {
	 	model->integration_functions->initAssPtr(t, user_data->derivative_variables, (void *) user_data);
	 	flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);
	 	if (check_flag(&flag, "CVodeReInit", 1, errLog)) return NULL;
	 }

	model->integration_functions->assPtr(t,user_data->derivative_variables, (void *) user_data);
	if (t == result->list_samples[0]){
	    writeResultSample(model, result, user_data, t, iout);
	    iout++;
    }

	tout = RCONST(result->list_samples[iout]);

	while(1)
	{
		if (model->nb_derivative_variables > 0 || model->nb_events > 0)
		{
			// printf("> Integrate from t=%.16g to t=%.16g\n", t, (double) tout);

			flag = CVode(cvode_mem, tout,
						  user_data->derivative_variables,
						  &t, CV_NORMAL);

			if (check_flag(&flag, "CVode", 1, errLog))
			{
				FinalizeIntegrationData(model, user_data);
				CVodeFree(&cvode_mem);
				return result;
			}

			if (flag == CV_ROOT_RETURN)
			{
				// One event has been detected.
				printf("> Event at t=%.16g\n", t);

				// Updating roots
				int * new_roots = calloc((getNbRoots(user_data) + getNbTimedTreatments(user_data)), sizeof(int));

				CVodeGetRootInfo(cvode_mem, new_roots);

				int i, strict;
				for (i=0; i < getNbRoots(user_data); i++)
					if (new_roots[i] != 0)
					{
						user_data->roots_triggers[i] = new_roots[i];
						if (user_data->roots_operators[i] == 1 || user_data->roots_operators[i] == 3)
						    strict = 1;
						else
						    strict = 0;
					}

				free(new_roots);




				if (t == tout)
				{

					model->integration_functions->assPtr(t, user_data->derivative_variables, (void *) user_data);

					if (strict == 0)
					{
                        executeEventsCVODE(user_data, t);
					    writeResultSample(model, result, user_data, t, iout);
					}
					else
					{
					    writeResultSample(model, result, user_data, t, iout);
					    executeEventsCVODE(user_data, t);
					}
					iout++;

				}
				else executeEventsCVODE(user_data, t);



				//And we reinit the solver to accept this change of value
				flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);
				if (check_flag(&flag, "CVode", 1, errLog))
				{
					FinalizeIntegrationData(model, user_data);
					CVodeFree(&cvode_mem);
					return result;
				}

				/* Call RootInit to update the root function */
				flag = CVodeRootInit(cvode_mem,
									  (getNbRoots(user_data) + getNbTimedTreatments(user_data)),
									  &roots_wrapper_cvode);
				if (check_flag(&flag, "CVodeRootInit", 1, errLog))
					return NULL;

			}

			else if (flag == CV_SUCCESS)
			{
				model->integration_functions->assPtr(t, user_data->derivative_variables, (void *) user_data);
				writeResultSample(model, result, user_data, t, iout);
				iout++;
			}

			else
			{
				FinalizeIntegrationData(model, user_data);
				CVodeFree(&cvode_mem);
				return result;
			}
		}
		else
		{
    		model->integration_functions->assPtr(tout, user_data->derivative_variables, (void *) user_data);
			t = RCONST(result->list_samples[iout]);
			writeResultSample(model, result, user_data, t, iout);
			iout++;
		}

		if (iout == (result->nb_samples))
		    break;
		else
		    tout = RCONST(result->list_samples[iout]);


	}

	FinalizeIntegrationData(model, user_data);
	CVodeFree(&cvode_mem);
	result->return_code = 0;

	return result;
}




SteadyStatesIntegrationResult * simulateModelCVODE_SteadyStates(ModelDefinition * model,
										ExperimentalCondition * condition,
										FILE * errLog,
										SteadyStatesIntegrationResult * result)
{
	realtype t, tout;
	int flag, i, iout;

	IntegrationData * user_data = InitializeIntegrationData(model, condition, errLog);
	if (user_data == NULL)
		return result;

	void * cvode_mem = InitializeCVODE(model, user_data, condition, errLog);

	t = RCONST(0);

	// Firing Initial Assignments
	// if (model->nb_init_assignments > 0) {
	// 	model->integration_functions->initAssPtr(t, user_data->derivative_variables, (void *) user_data);
	// 	flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);
	// 	if (check_flag(&flag, "CVodeReInit", 1, errLog)) return NULL;
	// }

	if ((user_data->nb_events + user_data->nb_timed_treatments) > 0)
	{
		// priority_wrapper(user_data, t);
		(*user_data->priorityEventsPtr)(t, user_data->derivative_variables, (void *) user_data);

		realtype * t_roots = malloc(sizeof(realtype)*(getNbRoots(user_data) + getNbTimedTreatments(user_data)));

		roots_wrapper_cvode(t, user_data->derivative_variables,
											  t_roots, (void *) user_data);

		initRoots(user_data, t_roots);
		free(t_roots);

		/* We inactivate the events which are not off at t0 */
		for (i=0; i < model->nb_events; i++)
			if (model->events_init[i] == 1)
				user_data->events_ready[i] = 0;

		executeEventsCVODE(user_data, t);

		for (i=0; i < model->nb_events; i++)
			if (model->events_init[i] == 1)
			{
			  user_data->events_triggers[i] = 0;
			  user_data->events_ready[i] = 1;
			}

		//And we reinit the solver to accept this change of value
		flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);

		if (check_flag(&flag, "CVode", 1, errLog))
		{
			FinalizeIntegrationData(model, user_data);
			CVodeFree(&cvode_mem);
			return result;
		}


		/* Call RootInit to update the root function */
		flag = CVodeRootInit(cvode_mem,
							  (getNbRoots(user_data) + getNbTimedTreatments(user_data)),
							  &roots_wrapper_cvode);
		if (check_flag(&flag, "CVodeRootInit", 1, errLog))
			return NULL;

	}

//	 Firing Initial Assignments
	 if (model->nb_init_assignments > 0) {
	 	model->integration_functions->initAssPtr(t, user_data->derivative_variables, (void *) user_data);
	 	flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);
	 	if (check_flag(&flag, "CVodeReInit", 1, errLog)) return NULL;
	 }

	// model->integration_functions->assPtr(t,user_data->derivative_variables, (void *) user_data);
	// writeResultSample(model, result, user_data, t, iout);
	realtype * last_values = malloc(sizeof(realtype)*model->nb_derivative_variables);
	for (i=0; i < model->nb_derivative_variables; i++)
	  last_values[i] = Ith(user_data->derivative_variables, i+1);
	int freeze_count = 0;

	tout = RCONST(1e+16);
	iout=0;

	if (model->nb_derivative_variables > 0 || model->nb_events > 0)
	{
		while(1)
		{

			flag = CVode(cvode_mem, tout,
						  user_data->derivative_variables,
						  &t, CV_ONE_STEP);


			if (check_flag(&flag, "CVode", 1, errLog))
				break;

			if (flag == CV_ROOT_RETURN)
			{
				// One event has been detected.
				//printf("> Event at t=%.16g\n", t);

				// Updating roots
				int * new_roots = calloc((getNbRoots(user_data) + getNbTimedTreatments(user_data)), sizeof(int));

				CVodeGetRootInfo(cvode_mem, new_roots);

				int ii;
				for (ii=0; ii < getNbRoots(user_data); ii++)
					if (new_roots[ii] != 0)
						user_data->roots_triggers[ii] = new_roots[ii];

				free(new_roots);

				executeEventsCVODE(user_data, t);

				//And we reinit the solver to accept this change of value
				flag = CVodeReInit(cvode_mem, t, user_data->derivative_variables);
				if (check_flag(&flag, "CVode", 1, errLog))
					break;

				/* Call RootInit to update the root function */
				flag = CVodeRootInit(cvode_mem,
									  (getNbRoots(user_data) + getNbTimedTreatments(user_data)),
									  &roots_wrapper_cvode);
				if (check_flag(&flag, "CVodeRootInit", 1, errLog))
					break;

			}

			else if (flag == CV_SUCCESS)
			{
				// If the estimated next piece is at infinity. That's sundials clue that we reach stability
				if (isinf(t))
				{
					model->integration_functions->assPtr(t, user_data->derivative_variables, (void *) user_data);
					writeResultSteadyState(model, result, user_data);
					result->return_code = 0;
					break;
				}

				// We just give up at some point... return the worst result (2)
				else if (iout > 10000)
				{
				  model->integration_functions->assPtr(t, user_data->derivative_variables, (void *) user_data);
				  writeResultSteadyState(model, result, user_data);
				  result->return_code = 2;
				  break;
				}

				// If we can freeze the system (sum of relative differences < 1e-4) for long enough (20 steps)
				// then it's good enough and we return 1
				else
				{
					double t_diff = 0;
					int ii;
					for (ii=0; ii < model->nb_derivative_variables; ii++)
					{
						if (last_values[ii] != 0)
							t_diff += fabs((Ith(user_data->derivative_variables, ii+1) - last_values[ii]))/last_values[ii];
						else
							t_diff += fabs((Ith(user_data->derivative_variables, ii+1) - last_values[ii]))/1e-15;
					}


					if (t_diff < 1e-4)
						freeze_count++;

					else
						freeze_count=0;


					if (freeze_count > 20)
					{
					  model->integration_functions->assPtr(t, user_data->derivative_variables, (void *) user_data);
					  writeResultSteadyState(model, result, user_data);
					  result->return_code = 1;
					  break;
					}

					else
					{
					  for (ii=0; ii < model->nb_derivative_variables; ii++)
						last_values[ii] = Ith(user_data->derivative_variables, ii+1);


					}

				}
			}

			else break;

			iout += 1;
		}

	}

	free(last_values);
	FinalizeIntegrationData(model, user_data);
	CVodeFree(&cvode_mem);

	return result;
}
