/******************************************************************************
 *                                                                            *
 *   integrate.h                                                              *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Fonction for integrating models                                          *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 * Copyright (C) 2012-2014 Vincent Noel                                       *
 * the full GPL copyright notice can be found in lsa.c                        *
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

#define LOGGING_UNACTIVE      0
#define LOGGING_ACTIVE        1

#include <stdlib.h>
#include <time.h>

#include "integrate.h"
#include "ode.h"
#include "dae.h"

int       log_integration_duration = LOGGING_UNACTIVE;
char *    log_integration_duration_filename = "integration_duration.log";
int       log_integration_errors = LOGGING_ACTIVE;
char *    log_integration_errors_filename = "integration_errors.log";
char *    log_directory = ".";
char *    working_directory = ".";

void setIntegrationDurationLog(int mode)
{
  log_integration_duration = mode;
}


void setIntegrationDurationLogFilename(char * filename)
{
  log_integration_duration_filename = filename;
}

void setWorkingDirectory(char * directory)
{
  working_directory = directory;
}

void writeIntegrationDurationLog(int duration, int return_code)
{
  if (log_integration_duration == LOGGING_ACTIVE)
  {
	char filename[MAX_RECORD];
	sprintf(filename, "%s/%s/%s", working_directory,
								  log_directory,
								  log_integration_duration_filename);

	FILE * f_log_integration_duration = fopen(filename, "a");
	fprintf(f_log_integration_duration, "%d\t%d\n", duration, return_code);
	fclose(f_log_integration_duration);
  }
}


void setIntegrationErrorsLog(int mode) {
  log_integration_errors = mode;
}

void setIntegrationErrorsLogFilename(char * filename) {
  log_integration_errors_filename = filename;
}

IntegrationResult * InitializeIntegrationResult(ModelDefinition * model)
{
  int i;
  IntegrationResult * integration_result = malloc(sizeof(IntegrationResult));
  integration_result->nb_dimensions = model->nb_constant_variables
									 + model->nb_assignment_variables
									 + model->nb_derivative_variables
									 + model->nb_algebraic_variables;
  integration_result->nb_constant_variables = model->nb_constant_variables;
  integration_result->nb_assignment_variables = model->nb_assignment_variables;
  integration_result->nb_derivative_variables = model->nb_derivative_variables + model->nb_algebraic_variables;

//  if (model->integration_settings->list_samples == NULL)
//  {
//
//	  integration_result->nb_samples = model->integration_settings->nb_samples;
//	  integration_result->sampling_frequency = model->integration_settings->t_sampling;
//	  integration_result->list_samples = malloc(sizeof(double)*(model->integration_settings->nb_samples+1));
//	  for (i=0; i < model->integration_settings->nb_samples; i++)
//	  {
//		  if (i==0){
//			integration_result->list_samples[i] = model->integration_settings->t_min;}
//		  else
//		  { //printf("%g\n", (integration_result->list_samples[i-1] + model->integration_settings->t_sampling));
//			integration_result->list_samples[i] = (integration_result->list_samples[i-1]
//									+ model->integration_settings->t_sampling);
////            printf("initialization sample %d : %g\n", i, integration_result->list_samples[i]);
//
//		  }
//	  }
//  }
//  else
//  {
    integration_result->time_min = model->integration_settings->t_min;
	integration_result->nb_samples = model->integration_settings->nb_samples;
	integration_result->list_samples = malloc(sizeof(double)*(model->integration_settings->nb_samples));

	for (i=0; i < model->integration_settings->nb_samples; i++)
	{
		integration_result->list_samples[i] = model->integration_settings->list_samples[i];
	}

  integration_result->return_code = 1;
  integration_result->t = malloc(sizeof(double)*integration_result->nb_samples);
  integration_result->y = malloc(sizeof(double*)*integration_result->nb_dimensions);
  for (i=0; i < integration_result->nb_dimensions; i++)
	integration_result->y[i] = malloc(sizeof(double)*integration_result->nb_samples);

  integration_result->names = malloc(sizeof(char *)*integration_result->nb_dimensions);
  for  (i=0; i < integration_result->nb_dimensions; i++)
  {
	  if (i < model->nb_derivative_variables)
		  integration_result->names[i] = model->derivative_variables[i].name;
	  else if (i < model->nb_derivative_variables + model->nb_algebraic_variables)
		  integration_result->names[i] = model->algebraic_variables[i-model->nb_derivative_variables].name;
	  else if  (i < model->nb_derivative_variables + model->nb_algebraic_variables + model->nb_assignment_variables)
		  integration_result->names[i] = model->assignment_variables[i-model->nb_derivative_variables-model->nb_algebraic_variables].name;
	  else if  (i < model->nb_derivative_variables + model->nb_algebraic_variables + model->nb_assignment_variables+model->nb_constant_variables)
		  integration_result->names[i] = model->constant_variables[i-model->nb_derivative_variables-model->nb_algebraic_variables-model->nb_assignment_variables].name;
  }

  return integration_result;

}


void FinalizeIntegrationResult(IntegrationResult * integration_result)
{
  int i;
  free(integration_result->t);
  for (i=0; i < integration_result->nb_dimensions; i++)
	free(integration_result->y[i]);

  free(integration_result->y);
  free(integration_result->list_samples);
  free(integration_result->names);

  free(integration_result);

}

SteadyStatesIntegrationResult * InitializeSteadyStatesIntegrationResult(ModelDefinition * model, double * list_samples, int nb_samples)
{
  SteadyStatesIntegrationResult * integration_result = malloc(sizeof(SteadyStatesIntegrationResult));
  integration_result->nb_dimensions = model->nb_constant_variables
									 + model->nb_assignment_variables
									 + model->nb_derivative_variables
									 + model->nb_algebraic_variables;
  integration_result->nb_constant_variables = model->nb_constant_variables;
  integration_result->nb_assignment_variables = model->nb_assignment_variables;
  integration_result->nb_derivative_variables = model->nb_derivative_variables + model->nb_algebraic_variables;

  integration_result->return_code = 1;
  integration_result->y = malloc(sizeof(double)*integration_result->nb_dimensions);
  integration_result->names = malloc(sizeof(char *)*integration_result->nb_dimensions);
  int i;
  for  (i=0; i < integration_result->nb_dimensions; i++)
  {
	  if (i < model->nb_derivative_variables)
		  integration_result->names[i] = model->derivative_variables[i].name;
	  else if (i < model->nb_derivative_variables + model->nb_algebraic_variables)
		  integration_result->names[i] = model->algebraic_variables[i-model->nb_derivative_variables].name;
	  else if  (i < model->nb_derivative_variables + model->nb_algebraic_variables + model->nb_assignment_variables)
		  integration_result->names[i] = model->assignment_variables[i-model->nb_derivative_variables-model->nb_algebraic_variables].name;
	  else if  (i < model->nb_derivative_variables + model->nb_algebraic_variables + model->nb_assignment_variables+model->nb_constant_variables)
		  integration_result->names[i] = model->constant_variables[i-model->nb_derivative_variables-model->nb_algebraic_variables-model->nb_assignment_variables].name;
  }

  return integration_result;

}


void FinalizeSteadyStatesIntegrationResult(SteadyStatesIntegrationResult * integration_result)
{
  free(integration_result->y);
  free(integration_result->names);
  free(integration_result);
}

void WriteTrajectories(IntegrationResult * result, char * fileName)
{
	int t,y;
	FILE * f_res = fopen(fileName,"w");
	fprintf(f_res, "time");
	for(y=0;y < result->nb_dimensions;y++)
		fprintf(f_res, ", %s", result->names[y]);

	fprintf(f_res, "\n");

	for(t=0;t< result->nb_samples;t++)
	{
		fprintf(f_res, "%g ", result->t[t]);

		for(y=0;y < result->nb_dimensions;y++)
			fprintf(f_res, "%.16g ",result->y[y][t]);

		fprintf(f_res, "\n");
	}
	fclose(f_res);
}

void WriteSteadyStates(SteadyStatesIntegrationResult * result, char * fileName)
{
	int y;
	FILE * f_res = fopen(fileName,"w");

	for(y=0;y < result->nb_dimensions;y++){
	    if (y == 0)	fprintf(f_res, "%s", result->names[y]);
	    else fprintf(f_res, " %s", result->names[y]);
	}
	fprintf(f_res, "\n");

	for(y=0;y < result->nb_dimensions;y++)
		fprintf(f_res, "%.16g ",result->y[y]);

	fprintf(f_res, "\n");
	fclose(f_res);
}


IntegrationResult * simulateModel(ModelDefinition * model,
								  ExperimentalCondition * condition,
								  IntegrationResult * result)
{
	// IntegrationResult * result;

	// Integration duration logging initialization
	int start_time = (int) time(NULL);

	// Integration error logging initialization

	FILE * f_log_integration_errors = NULL;
	char filename[MAX_RECORD];

	if (log_integration_errors == 1)
	{

		sprintf(filename, "%s/%s/%s", working_directory,
									  log_directory,
									  log_integration_errors_filename);
		// printf("> filename = %s\n", filename);
		f_log_integration_errors = fopen(filename, "w");
	}

	if (result == NULL)
	  result = InitializeIntegrationResult(model);

	// Integration
	if (model->integration_functions->isDAE == 1)
	  simulateModelIDA(model, condition, f_log_integration_errors, result);
	else
	  simulateModelCVODE(model, condition, f_log_integration_errors, result);

	/*
	// If simulation failed, let's try another time without the Jacobian matrix
	if (t_params->decidedJacobian == 0 && result->return_code < 0)
	{
		// We don't want to use the jacobian anymore
		t_params->useJacobian = 0;

		// And we won't change our mind
		t_params->decidedJacobian = 1;

		// Integration without jacobian
		result = simulateModelCVODE_v2(model, f_log_integration_errors);
	}
	*/

	// Integration error logging finalization
	if (log_integration_errors == 1)
	{
		fclose(f_log_integration_errors);
		//free(filename);
	}
	// Integration duration logging finalization
	int stop_time = (int) time(NULL);
	result->duration = stop_time - start_time;
	writeIntegrationDurationLog(result->duration, result->return_code);

	// Return integration result
	return result;
}


SteadyStatesIntegrationResult * simulateModelSteadyStates(ModelDefinition * model,
								  ExperimentalCondition * condition,
								  SteadyStatesIntegrationResult * result)
{
	// IntegrationResult * result;

	// Integration duration logging initialization
	int start_time = (int) time(NULL);

	// Integration error logging initialization

	FILE * f_log_integration_errors = NULL;
	char filename[MAX_RECORD];

	if (log_integration_errors == 1)
	{

		sprintf(filename, "%s/%s/%s", working_directory,
									  log_directory,
									  log_integration_errors_filename);
		// printf("> filename = %s\n", filename);
		f_log_integration_errors = fopen(filename, "w");
	}

	if (result == NULL)
	  result = InitializeSteadyStatesIntegrationResult(model, NULL, 0);

	// Integration
	// if (model->integration_functions->isDAE == 1)
	//   simulateModelIDA(model, condition, f_log_integration_errors, result);
	// else
	  simulateModelCVODE_SteadyStates(model, condition, f_log_integration_errors, result);

	/*
	// If simulation failed, let's try another time without the Jacobian matrix
	if (t_params->decidedJacobian == 0 && result->return_code < 0)
	{
		// We don't want to use the jacobian anymore
		t_params->useJacobian = 0;

		// And we won't change our mind
		t_params->decidedJacobian = 1;

		// Integration without jacobian
		result = simulateModelCVODE_v2(model, f_log_integration_errors);
	}
	*/

	// Integration error logging finalization
	if (log_integration_errors == 1)
	{
		fclose(f_log_integration_errors);
		//free(filename);
	}
	// Integration duration logging finalization
	int stop_time = (int) time(NULL);
	result->duration = stop_time - start_time;
	writeIntegrationDurationLog(result->duration, result->return_code);

	// Return integration result
	return result;
}

realtype * addTimedEvent(realtype t, int assignment, int memory_size, void * user_data)
{
	IntegrationData * data = (IntegrationData *) user_data;

	data->nb_timed_events++;
	realtype * t_times = realloc(data->t_events_time,
					  sizeof(realtype)*data->nb_timed_events);
	t_times[data->nb_timed_events-1] = t;
	data->t_events_time = t_times;

	data->t_events_assignment = realloc(data->t_events_assignment,
							sizeof(realtype)*data->nb_timed_events);
	data->t_events_assignment[data->nb_timed_events-1] = assignment;

	realtype ** t_events_memory = realloc(data->t_events_memory,
						sizeof(realtype *)*data->nb_timed_events);
	t_events_memory[data->nb_timed_events-1] = malloc(sizeof(realtype)*memory_size);
	data->t_events_memory = t_events_memory;

	// Here we modify the global events objects that we need to activate
	// the timed events with all the others
	int * roots_triggers = realloc(data->roots_triggers,
						  sizeof(int)*(data->nb_roots + data->nb_timed_events));
	roots_triggers[data->nb_roots + data->nb_timed_events-1] = 0;
	data->roots_triggers = roots_triggers;

	// Root values are a little special, since we need to add the timed treatments
	realtype * roots_values = realloc(data->roots_values,
						  sizeof(realtype)*(data->nb_roots + data->nb_timed_events + data->nb_timed_treatments));
	roots_values[data->nb_roots + data->nb_timed_events-1] = 0;
	data->roots_values = roots_values;

	int nb_total_events = data->nb_events + data->nb_timed_events;

	// - events_triggers
	int * events_triggers = realloc(data->events_triggers,
							  sizeof(int)*nb_total_events);
	events_triggers[nb_total_events-1] = 0;
	data->events_triggers = events_triggers;

	// - events_has_priority
	data->events_has_priority = realloc(data->events_has_priority,
								  sizeof(int)*nb_total_events);
	data->events_has_priority[nb_total_events-1] = data->events_has_priority[assignment];
	// data->events_has_priority = events_has_priority;

	// - events_priorities
	data->events_priorities = realloc(data->events_priorities,
											sizeof(realtype *)*nb_total_events);

	data->events_priorities[nb_total_events-1] = malloc(sizeof(realtype));

	if (data->events_has_priority[assignment] == 1)
	  data->events_priorities[nb_total_events-1] = data->events_priorities[assignment];

	data->events_nb_children[assignment]++;
	data->events_children[assignment] = realloc(data->events_children[assignment],
												  sizeof(int)*data->events_nb_children[assignment]);
	data->events_children[assignment][data->events_nb_children[assignment]-1] = nb_total_events-1;

	return t_events_memory[data->nb_timed_events-1];
}

void untriggerChildren(IntegrationData * data, int event_id)
{
	// data->events_triggers[event_id]--;
	int i;
	for (i=0; i < data->events_nb_children[event_id]; i++)
	  data->events_triggers[data->events_children[event_id][i]]--;
}
void retriggerChildren(IntegrationData * data, int event_id)
{
	// data->events_triggers[event_id]--;
	int i;
	for (i=0; i < data->events_nb_children[event_id]; i++)
	  data->events_triggers[data->events_children[event_id][i]]++;
}
