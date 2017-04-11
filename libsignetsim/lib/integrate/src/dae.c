/******************************************************************************
 *                                                                            *
 *   dae.c                                                                    *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Fonction for integrating DAE model with IDA                              *
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

#include <ida/ida.h>
#include <ida/ida_dense.h>
#include <stdlib.h>
#include <float.h>                   /* for DBL_MAX */
#include <limits.h>                  /* for INT_MAX */
#include "dae.h"
#include "shared.h"


int func_dae_empty(realtype t, N_Vector y, N_Vector ydot, N_Vector r, void *user_data)
{
    Ith(ydot, 1) = RCONST(0);
    return 0;
}


int roots_wrapper_ida(realtype t, N_Vector y, N_Vector ydot, realtype * gout, void * user_data)
{
  IntegrationData * data = (IntegrationData *) user_data;

  if (data->nb_events > 0)
    (*data->rootsEventsIDAPtr)(t, y, ydot, gout, user_data);

  roots_wrapper(data, t, gout);

  return 0;
}


void * InitializeIDA(ModelDefinition * model, IntegrationData * user_data, ExperimentalCondition * condition, FILE * errLog)
{
    int flag;

    /* Call IDACreate and IDAInit to initialize IDA memory */
    void * ida_mem = IDACreate();

    if (check_flag((void *)ida_mem, "IDACreate", 0, errLog))
        return NULL;

    if ((model->nb_derivative_variables + model->nb_algebraic_variables) > 0)
        flag = IDAInit(ida_mem, model->integration_functions->funcIdaPtr,
                    RCONST(model->integration_settings->t_min),
                    user_data->derivative_variables,
                    user_data->derivative_derivatives);
    else
        flag = IDAInit(ida_mem, func_dae_empty,
                    RCONST(model->integration_settings->t_min),
                    user_data->derivative_variables,
                    user_data->derivative_derivatives);

    if (check_flag(&flag, "IdaInit", 1, errLog))
        return NULL;

    /* Call SVtolerances to specify the scalar relative tolerance
     * and vector absolute tolerances */
    flag = IDASVtolerances(ida_mem, user_data->rel_tol, user_data->abs_tol);
    if (check_flag(&flag, "IDASVtolerances", 1, errLog))
        return NULL;

    /* Call SetErrTestFails to set the max value of failed error test */
    flag = IDASetMaxErrTestFails(ida_mem, model->integration_options->max_err_test_fails);
    if (check_flag(&flag, "IDASetMaxErrTestFails", 1, errLog))
        return NULL;

    /* Call SetMaxConvFails to set the max value of convergence failures */
    flag = IDASetMaxConvFails(ida_mem, model->integration_options->max_conv_fails);
    if (check_flag(&flag, "IDASetMaxConvFails", 1, errLog))
        return NULL;

    /* Call CVodeSetMaxNumSteps to set the max number of internal steps */
    flag = IDASetMaxNumSteps(ida_mem, model->integration_options->max_num_steps);
    if (check_flag(&flag, "IDASetMaxNumSteps", 1, errLog))
        return NULL;

    /* Call Dense to specify the dense linear solver */
    flag = IDADense(ida_mem, MAX((model->nb_derivative_variables + model->nb_algebraic_variables), 1));
    if (check_flag(&flag, "IDADense", 1, errLog))
        return NULL;

    // /* Set the Jacobian routine to Jac (user-supplied) */
    // if (model->integration_functions->hasJacobian == 1)
    // {
    //     flag = CVDlsSetDenseJacFn(ida_mem, model->integration_functions->jacPtr);
    //     if (check_flag(&flag, "CVDlsSetDenseJacFn", 1, errLog))
    //         return NULL;
    // }

    if (model->nb_events > 0 || (condition != NULL && condition->timed_treatments != NULL && condition->nb_timed_treatments > 0))
    {
        /* Call RootInit to specify the root function g with 2 components */
        flag = IDARootInit(ida_mem, model->nb_events, &roots_wrapper_ida);
        if (check_flag(&flag, "IDARootInit", 1, errLog))
            return NULL;
    }

    /* Call SetUserData to specify the object accessible during the integration */
    flag = IDASetUserData(ida_mem, user_data);
    if (check_flag(&flag, "IDASetUserData", 1, errLog))
        return NULL;

    //Redirect StdErr printing
    flag = IDASetErrFile(ida_mem, errLog);
    if (check_flag(&flag, "IDASetErrFile", 1, errLog))
        return NULL;

    return ida_mem;
}

void updateRootsIDA(IntegrationData * user_data, realtype t)
{

    realtype * t_roots = malloc(sizeof(realtype)*getNbRoots(user_data));
    roots_wrapper_ida(t, user_data->derivative_variables,
                                  user_data->derivative_derivatives,
                                  t_roots, (void *) user_data);

    updateRoots(user_data, t_roots);

    free(t_roots);

    roots_wrapper_ida(t, user_data->derivative_variables,
                      user_data->derivative_derivatives,
                      user_data->roots_values, (void *) user_data);

    activate_wrapper(user_data, t);

}

void executeEventsIDA(IntegrationData * user_data, realtype t)
{
    int i;
    int nb_events_activated = INT_MAX;

    roots_wrapper_ida(t, user_data->derivative_variables,
                      user_data->derivative_derivatives,
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
                    updateRootsIDA(user_data, t);
                    mark_executed(user_data, t_event);
                }
                nb_executed++;
            }
            freeEvents(concurrent_events);
        }
        free(executed_events);
        freeEvents(events_activated);
    }

}


IntegrationResult * simulateModelIDA(ModelDefinition * model,
                                      ExperimentalCondition * condition,
                                      FILE * errLog,
                                      IntegrationResult * result)
{
    realtype t, tout;
    void * ida_mem;
//    int flag, iout, nout, i;
    int flag, iout, i;

    // IntegrationResult * result = InitializeIntegrationResult(model, NULL, 0);

    IntegrationData * user_data = InitializeIntegrationData(model, condition, errLog);

    ida_mem = InitializeIDA(model, user_data, condition, errLog);

    iout = 0;
    t = RCONST(result->time_min);
//    t = (realtype) model->integration_settings->t_min;


    // Firing Initial Assignments
    // if (model->nb_init_assignments > 0) {
    //     model->integration_functions->initAssPtr(t, user_data->derivative_variables, (void *) user_data);
    //     flag = IDAReInit(ida_mem, t, user_data->derivative_variables, user_data->derivative_derivatives);
    //     if (check_flag(&flag, "IDAReInit", 1, errLog)) return NULL;
    // }

    if (model->nb_events > 0)
    {
        // priority_wrapper(user_data, t);
        (*user_data->priorityEventsPtr)(t, user_data->derivative_variables, (void *) user_data);

        int total_roots = model->nb_roots;
        realtype * t_roots = malloc(sizeof(realtype)*(total_roots));

        roots_wrapper_ida(t,user_data->derivative_variables,
                                user_data->derivative_derivatives,
                                t_roots, (void *) user_data);

        initRoots(user_data, t_roots);

        free(t_roots);

        /* We inactivate the events which are not off at t0 */
        for (i=0; i < model->nb_events; i++)
            if (model->events_init[i] == 1)
                user_data->events_ready[i] = 0;

        executeEventsIDA(user_data, t);

        for (i=0; i < model->nb_events; i++)
            if (model->events_init[i] == 1)
            {
              user_data->events_triggers[i] = 0;
              user_data->events_ready[i] = 1;
            }

        //And we reinit the solver to accept this change of value
        flag = IDAReInit(ida_mem, t, user_data->derivative_variables,
                                    user_data->derivative_derivatives);

        if (check_flag(&flag, "IDAReInit", 1, errLog))
        {
            FinalizeIntegrationData(model, user_data);
            IDAFree(&ida_mem);
            return result;
        }

        // We update the number of roots which might have changed
        // during execution
        total_roots = (user_data->nb_roots + user_data->nb_timed_events);

        /* Call RootInit to update the root function */
        flag = IDARootInit(ida_mem,
                              total_roots,
                              &roots_wrapper_ida);
        if (check_flag(&flag, "IDARootInit", 1, errLog))
            return NULL;

    }

//    nout = model->integration_settings->nb_samples - 1;
    model->integration_functions->assPtr(t,user_data->derivative_variables, (void *) user_data);
    if (t == result->list_samples[0]){
        writeResultSample(model, result, user_data, t, iout);
        iout++;
    }
    tout = RCONST(result->list_samples[iout]);

    while(1)
    {
        if ((model->nb_derivative_variables + model->nb_algebraic_variables) > 0 || model->nb_events > 0)
        {
            flag = IDASolve(ida_mem, tout, &t,
                              user_data->derivative_variables,
                              user_data->derivative_derivatives,
                              IDA_NORMAL);

            if (check_flag(&flag, "IDASolve", 1, errLog))
            {
                FinalizeIntegrationData(model, user_data);
                IDAFree(&ida_mem);
                return result;
            }

            if (flag == IDA_ROOT_RETURN)
            {
                // One event has been detected.
                //printf("> Event at t=%.16g\n", t);

                // Updating roots
                int i, strict;
                int total_roots = (user_data->nb_roots + user_data->nb_timed_events);
                int * new_roots = calloc(total_roots, sizeof(int));

                flag = IDAGetRootInfo(ida_mem, new_roots);

                for (i=0; i < total_roots; i++)
                    if (new_roots[i] != 0){
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
                        executeEventsIDA(user_data, t);
					    writeResultSample(model, result, user_data, t, iout);
					}
					else
					{
					    writeResultSample(model, result, user_data, t, iout);
					    executeEventsIDA(user_data, t);
					}
					iout++;

				}
				else executeEventsIDA(user_data, t);

//                executeEventsIDA(user_data, t);

                //And we reinit the solver to accept this change of value
                flag = IDAReInit(ida_mem, t, user_data->derivative_variables,
                                            user_data->derivative_derivatives);

                if (check_flag(&flag, "IDAReInit", 1, errLog))
                {
                    FinalizeIntegrationData(model, user_data);
                    IDAFree(&ida_mem);
                    return result;
                }

                // We update the number of roots which might have changed
                // during execution
                total_roots = (user_data->nb_roots + user_data->nb_timed_events);
                /* Call RootInit to update the root function */
                flag = IDARootInit(ida_mem,
                                      total_roots,
                                      &roots_wrapper_ida);
                if (check_flag(&flag, "IDARootInit", 1, errLog))
                    return NULL;

//                if (t == tout)
//                {
//                    model->integration_functions->assPtr(tout, user_data->derivative_variables, (void *) user_data);
//                    iout++;
////                    tout += RCONST(model->integration_settings->t_sampling);
//                    writeResultSample(model, result, user_data, t, iout);
//                }

                // Computing derivatives if need be
                flag = IDASetId(ida_mem, user_data->type_variables);
                if (check_flag(&flag, "IDASetId", 1, errLog))
                {
                    FinalizeIntegrationData(model, user_data);
                    IDAFree(&ida_mem);
                    return NULL;
                }

                flag = IDACalcIC(ida_mem, IDA_YA_YDP_INIT , tout);
                if (check_flag(&flag, "IDACalcIC", 1, errLog))
                {
                    FinalizeIntegrationData(model, user_data);
                    IDAFree(&ida_mem);
                    return NULL;
                }
            }

            else if (flag == IDA_SUCCESS)
            {
                model->integration_functions->assPtr(tout, user_data->derivative_variables, (void *) user_data);
                writeResultSample(model, result, user_data, t, iout);
                iout++;
            }

            else
            {
                FinalizeIntegrationData(model, user_data);
                IDAFree(&ida_mem);
                return result;
            }
        }
        else
        {
            model->integration_functions->assPtr(tout, user_data->derivative_variables, (void *) user_data);
			t = RCONST(result->list_samples[iout]);
            writeResultSample(model, result, user_data, tout, iout);
            iout++;
        }
		if (iout == (result->nb_samples)) break;
		else tout = RCONST(result->list_samples[iout]);
    }

    FinalizeIntegrationData(model, user_data);
    IDAFree(&ida_mem);
    result->return_code = 0;

    return result;
}
