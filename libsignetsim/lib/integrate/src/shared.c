/******************************************************************************
 *                                                                            *
 *   shared.h                                                                 *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Shared functions for integrating models                                  *
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
#include <stdlib.h>
#include <float.h>
#include <time.h>
#include "shared.h"


int check_flag(void *flagvalue, char *funcname, int opt, FILE * errLog)
{
    int *errflag;

    /* Check if SUNDIALS function returned NULL pointer - no memory allocated */
    if (opt == 0 && flagvalue == NULL)
    {
        if (errLog != NULL)
          fprintf(errLog, "\nSUNDIALS_ERROR: %s() failed - returned NULL pointer\n\n", funcname);
        return(1);
    }

    /* Check if flag < 0 */
    else if (opt == 1)
    {
        errflag = (int *) flagvalue;
        if (*errflag < 0)
        {
            if (errLog != NULL)
              fprintf(errLog, "\nSUNDIALS_ERROR: %s() failed with flag = %d\n\n", funcname, *errflag);
            return(1);
        }
    }

    /* Check if function returned NULL pointer - no memory allocated */
    else if (opt == 2 && flagvalue == NULL)
    {
        if (errLog != NULL)
          fprintf(errLog, "\nMEMORY_ERROR: %s() failed - returned NULL pointer\n\n", funcname);
        return(1);
    }

    return(0);
}


IntegrationData * InitializeIntegrationData(ModelDefinition * model, ExperimentalCondition * condition, FILE * errLog)
{
    IntegrationData * integration_data = malloc(sizeof(IntegrationData));
    int i;

    // Variable initialization
    // Constants
    if (model->nb_constant_variables > 0)
    {
        N_Vector constant_variables = N_VNew_Serial(model->nb_constant_variables);
        if (check_flag((void *)constant_variables, "N_VNew_Serial", 0, errLog))
          return NULL;

        for(i=0; i < model->nb_constant_variables; i++)
            Ith(constant_variables, i+1) = RCONST(model->constant_variables[i].value);

        integration_data->constant_variables = constant_variables;
    }

    // Variables with closed forms
    if (model->nb_assignment_variables > 0)
    {
        N_Vector assignment_variables = N_VNew_Serial(model->nb_assignment_variables);
        if (check_flag((void *)assignment_variables, "N_VNew_Serial", 0, errLog))
            return NULL;

        for(i=0; i < model->nb_assignment_variables; i++)
            Ith(assignment_variables, i+1) = RCONST(model->assignment_variables[i].value);
        integration_data->assignment_variables = assignment_variables;
    }


    // Derivatives/Algebraic variables
    N_Vector derivative_variables = N_VNew_Serial(MAX((model->nb_derivative_variables + model->nb_algebraic_variables),1));
    if (check_flag((void *)derivative_variables, "N_VNew_Serial", 0, errLog))
        return NULL;

    if ((model->nb_derivative_variables + model->nb_algebraic_variables) == 0)
        Ith(derivative_variables, 1) = RCONST(0.0);
    else
    {
        for(i=0; i < model->nb_derivative_variables; i++)
            Ith(derivative_variables, i+1) = RCONST(model->derivative_variables[i].value);

        for(i=0; i < model->nb_algebraic_variables; i++)
            Ith(derivative_variables, model->nb_derivative_variables+i+1) = RCONST(model->algebraic_variables[i].value);
    }

    integration_data->derivative_variables = derivative_variables;


    if (model->integration_functions->isDAE == 1)
    {
        // Derivatives initial values
        N_Vector derivative_derivatives = N_VNew_Serial(MAX((model->nb_derivative_variables + model->nb_algebraic_variables),1));
        if (check_flag((void *)derivative_derivatives, "N_VNew_Serial", 0, errLog))
            return NULL;

        if ((model->nb_derivative_variables + model->nb_algebraic_variables) == 0)
            Ith(derivative_derivatives, 1) = RCONST(0.0);
        else
        {
            for(i=0; i < model->nb_derivative_variables; i++)
                Ith(derivative_derivatives, i+1) = RCONST(model->der_der_variables[i].value);
            for(i=0; i < model->nb_algebraic_variables; i++)
                Ith(derivative_derivatives, model->nb_derivative_variables+i+1) = RCONST(model->alg_der_variables[i].value);
        }

        integration_data->derivative_derivatives = derivative_derivatives;

        // Variables type : Algebraic or Derivatives
        // Right now useless I think
        // TODO
        N_Vector type_variables = N_VNew_Serial(MAX(model->nb_derivative_variables+model->nb_algebraic_variables,1));
        if (check_flag((void *)type_variables, "N_VNew_Serial", 0, errLog))
            return NULL;

        if ((model->nb_derivative_variables+model->nb_algebraic_variables) == 0)
            Ith(type_variables, 1) = 1;

        else
        {

          for(i=0; i < model->nb_derivative_variables; i++)
              Ith(type_variables, i+1) = 1;

          for(i=0; i < model->nb_algebraic_variables; i++)
              Ith(type_variables, model->nb_derivative_variables+i+1) = 0;
        }

        integration_data->type_variables = type_variables;
    }


    // Tolerances initialization
    realtype rel_tol = RCONST(model->integration_settings->rel_tol);
    integration_data->rel_tol = rel_tol;

    N_Vector abs_tol = N_VNew_Serial(MAX((model->nb_derivative_variables + model->nb_algebraic_variables),1));
    if (check_flag((void *)abs_tol, "N_VNew_Serial", 0, errLog))
        return NULL;

    for(i=0; i < MAX((model->nb_derivative_variables + model->nb_algebraic_variables),1); i++)
        Ith(abs_tol,i+1) = RCONST(model->integration_settings->abs_tol);

    integration_data->abs_tol = abs_tol;


    // Timed treatments
    if (condition != NULL && condition->nb_timed_treatments > 0)
    {
      integration_data->nb_timed_treatments = condition->nb_timed_treatments;
      integration_data->timed_treatments = malloc(sizeof(TimedTreatments *)*condition->nb_timed_treatments);
      if (integration_data->timed_treatments == NULL)
          return NULL;

      for (i=0; i < condition->nb_timed_treatments; i++)
          integration_data->timed_treatments[i] = &(condition->timed_treatments[i]);
    }
    else integration_data->nb_timed_treatments = 0;


    // Event roots
    integration_data->nb_roots = model->nb_roots;

    if ((model->nb_roots + integration_data->nb_timed_treatments) > 0)
    {
        integration_data->roots_values = malloc(sizeof(realtype)*(model->nb_roots + integration_data->nb_timed_treatments));
        if (integration_data->roots_values == NULL)
            return NULL;
    }

    if (model->nb_roots > 0)
    {
        integration_data->roots_triggers = calloc(model->nb_roots, sizeof(int));
        if (integration_data->roots_triggers == NULL)
            return NULL;

        integration_data->roots_operators = malloc(sizeof(int)*model->nb_roots);
        if (integration_data->roots_operators == NULL)
            return NULL;

        for(i=0; i < model->nb_roots; i++)
          integration_data->roots_operators[i] = model->roots_operators[i];

    }
    // Events
    integration_data->nb_events = model->nb_events;

    if (model->nb_events > 0)
    {
        integration_data->events_triggers = calloc(model->nb_events, sizeof(int));
        if (integration_data->events_triggers == NULL)
            return NULL;

        integration_data->events_ready = calloc(model->nb_events, sizeof(int));
        if (integration_data->events_ready == NULL)
            return NULL;

        for (i=0; i < model->nb_events; i++)
          integration_data->events_ready[i] = 1;

        integration_data->events_memory = malloc(sizeof(realtype *)*model->nb_events);
        if (integration_data->events_memory == NULL)
            return NULL;

        for (i=0; i < model->nb_events; i++)
        {
            integration_data->events_memory[i] = malloc(sizeof(realtype)*model->memory_size_per_event[i]);
            if (integration_data->events_memory[i] == NULL)
                return NULL;
        }

        integration_data->events_has_priority = calloc(model->nb_events, sizeof(int));
        if (integration_data->events_has_priority == NULL)
            return NULL;

        for (i=0; i < model->nb_events; i++)
            integration_data->events_has_priority[i] = model->events_has_priority[i];

        integration_data->events_priorities = malloc(sizeof(realtype *)*model->nb_events);
        if (integration_data->events_priorities == NULL)
            return NULL;

        for (i=0; i < model->nb_events; i++)
        {
            integration_data->events_priorities[i] =  malloc(sizeof(realtype));
            if (integration_data->events_priorities[i] == NULL)
                return NULL;
        }
        integration_data->events_nb_children = calloc(model->nb_events, sizeof(int));
        if (integration_data->events_nb_children == NULL)
            return NULL;

        integration_data->events_children = malloc(sizeof(int *)*model->nb_events);
        if (integration_data->events_children == NULL)
            return NULL;

        for (i=0; i < model->nb_events; i++)
        {
            integration_data->events_children[i] = malloc(sizeof(int)*0);
            if (integration_data->events_children[i] == NULL)
                return NULL;
        }
    }

    // Timed events
  //  int nb_timed_events = 0;
    integration_data->nb_timed_events = 0;

    /*integration_data->t_events_time = calloc(nb_timed_events, sizeof(realtype));
    if (integration_data->t_events_time == NULL)
        return NULL;


    integration_data->t_events_assignment = calloc(nb_timed_events, sizeof(int));
    if (integration_data->t_events_assignment == NULL)
        return NULL;

    integration_data->t_events_memory = malloc(sizeof(realtype *)*nb_timed_events);
    if (integration_data->t_events_memory == NULL)
        return NULL;
*/

    // Functions
    if (model->integration_functions->isDAE == 1)
        integration_data->rootsEventsIDAPtr = model->integration_functions->rootsEventsIDAPtr;
    else
        integration_data->rootsEventsPtr = model->integration_functions->rootsEventsPtr;
    integration_data->activateEventsPtr = model->integration_functions->activateEventsPtr;
    integration_data->assignEventsPtr = model->integration_functions->assignEventsPtr;
    integration_data->priorityEventsPtr = model->integration_functions->priorityEventsPtr;

    srand(time(NULL));

    return integration_data;
}



void FinalizeIntegrationData(ModelDefinition * model, IntegrationData * integration_data)
{
    int i;

    if (model->nb_constant_variables > 0)
        N_VDestroy_Serial(integration_data->constant_variables);

    if (model->nb_assignment_variables > 0)
        N_VDestroy_Serial(integration_data->assignment_variables);

    N_VDestroy_Serial(integration_data->derivative_variables);

    if (model->integration_functions->isDAE == 1) {
      N_VDestroy_Serial(integration_data->derivative_derivatives);
      N_VDestroy_Serial(integration_data->type_variables);
    }

    N_VDestroy_Serial(integration_data->abs_tol);

    if (model->nb_roots > 0){
      free(integration_data->roots_triggers);
      free(integration_data->roots_operators);}

    if ((model->nb_roots + integration_data->nb_timed_treatments) > 0)
      free(integration_data->roots_values);

    if (model->nb_events > 0)
    {
        free(integration_data->events_ready);
        free(integration_data->events_triggers);

        for(i=0; i < model->nb_events; i++)
          free(integration_data->events_memory[i]);
        free(integration_data->events_memory);

        for(i=0; i < model->nb_events; i++)
            free(integration_data->events_priorities[i]);
        free(integration_data->events_priorities);

        free(integration_data->events_has_priority);

        for (i=0; i < model->nb_events; i++)
            if (integration_data->events_nb_children[i] > 0)
              free(integration_data->events_children[i]);

        free(integration_data->events_children);
        free(integration_data->events_nb_children);
        // printf("events\n");

    }

    if (integration_data->nb_timed_events > 0)
    {
        free(integration_data->t_events_time);
        free(integration_data->t_events_assignment);

        for(i=0; i < integration_data->nb_timed_events; i++)
          free(integration_data->t_events_memory[i]);
        free(integration_data->t_events_memory);
        // printf("timed events\n");

    }

    if (integration_data->nb_timed_treatments > 0)
    {
      free(integration_data->timed_treatments);
      // printf("timed treatments\n");
    }
    free(integration_data);
}




void writeResultSample(ModelDefinition * model, IntegrationResult * result, IntegrationData * user_data, realtype t, int sample)
{
    int i;

//    printf("> Writing sample %d : %.2g\n", sample, t);
    // Writing initial data point to the results variable
    result->t[sample] = t;
    for (i=0; i < model->nb_derivative_variables; i++)
        result->y[i][sample] = (double) Ith(user_data->derivative_variables,i+1);

    for (i=0; i < model->nb_algebraic_variables; i++)
        result->y[i + model->nb_derivative_variables][sample] = (double) Ith(user_data->derivative_variables, model->nb_derivative_variables+i+1);

    for (i=0; i < model->nb_assignment_variables; i++)
        result->y[i + model->nb_derivative_variables + model->nb_algebraic_variables][sample] = (double) Ith(user_data->assignment_variables,i+1);

    for (i=0; i < model->nb_constant_variables; i++)
        result->y[i + model->nb_derivative_variables + model->nb_algebraic_variables + model->nb_assignment_variables][sample] = (double) Ith(user_data->constant_variables,i+1);
}

void writeResultSteadyState(ModelDefinition * model, SteadyStatesIntegrationResult * result, IntegrationData * user_data)
{
    int i;

    for (i=0; i < model->nb_derivative_variables; i++)
        result->y[i] = (double) Ith(user_data->derivative_variables,i+1);

    for (i=0; i < model->nb_algebraic_variables; i++)
        result->y[i + model->nb_derivative_variables] = (double) Ith(user_data->derivative_variables, model->nb_derivative_variables+i+1);

    for (i=0; i < model->nb_assignment_variables; i++)
        result->y[i + model->nb_derivative_variables + model->nb_algebraic_variables] = (double) Ith(user_data->assignment_variables,i+1);

    for (i=0; i < model->nb_constant_variables; i++)
        result->y[i + model->nb_derivative_variables + model->nb_algebraic_variables + model->nb_assignment_variables] = (double) Ith(user_data->constant_variables,i+1);
}
