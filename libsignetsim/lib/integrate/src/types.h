/******************************************************************************
 *                                                                            *
 *   types.h                                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Types used by the integration code                                       *
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

 #include <nvector/nvector_serial.h>  /* serial N_Vector types, fcts., macros */
#include <sundials/sundials_dense.h> /* definitions DlsMat DENSE_ELEM */
#include <sundials/sundials_types.h> /* definition of type realtype */
#include <stdlib.h>
#include "datas.h"
#include "realtype_math.h"

#ifndef INTEGRATION_STRUCT
#define INTEGRATION_STRUCT

#define RESULT_OK           0
#define RESULT_ERR_INIT     1
#define RESULT_ERR_SIM      2
#define RESULT_ERR_EVENT    3
#define RESULT_CONSTRAINT   4


// Struct for integration result
typedef struct IntegrationResult
{
	double    *             t;                          /* Array for time points  */
	double    **            y;                          /* Array for trajectories */
	char 	  **			names;

	int                     nb_dimensions;              /* number of dimensions */
	int                     nb_derivative_variables;
	int                     nb_assignment_variables;
	int                     nb_constant_variables;
	// int                     nb_algebraic_variables;

    double                  time_min;                   /* beginning of the simulation */
	int                     nb_samples;                 /* number of samples */
//	double                  sampling_frequency;         /* sampling frequency */
	double    *             list_samples;               /* list of time samples, alternative to sampling_frequency */


	int                     duration;
	int                     return_code;                /* return code */
	char      *             return_message;             /* return message */

} IntegrationResult;

typedef struct SteadyStatesIntegrationResult
{
	double    *             y;                          /* Array for values */
	char 	  **			names;

	int                     nb_dimensions;              /* number of dimensions */
	int                     nb_derivative_variables;
	int                     nb_assignment_variables;
	int                     nb_constant_variables;

	int                     duration;
	int                     return_code;                /* return code */
	char      *             return_message;             /* return message */

} SteadyStatesIntegrationResult;


typedef struct IntegrationData
{
	N_Vector                constant_variables;
	N_Vector                assignment_variables;
	N_Vector                derivative_variables;
	N_Vector                derivative_derivatives;
	// N_Vector                algebraic_variables;
	N_Vector                type_variables;


	int                     nb_roots;
	realtype  *             roots_values;
	int       *             roots_triggers;
	int       *             roots_operators;

	int                     nb_events;
	int       *             events_ready;     /* Event can only be fire if once  */
	int       *             events_triggers;
	realtype  **            events_memory;

	int       *             events_has_priority;
	realtype  **            events_priorities;

	int       **            events_children;
	int       *             events_nb_children;

	int                     nb_timed_events;
	realtype  *             t_events_time;
	int       *             t_events_assignment;
	realtype  **            t_events_memory;

	int                     nb_timed_treatments;
	TimedTreatments **      timed_treatments;

	// Events roots functions
	int                     (*rootsEventsPtr)(realtype, N_Vector, realtype *, void *);
	// Events roots functions for IDA
	int                     (*rootsEventsIDAPtr)(realtype, N_Vector, N_Vector, realtype *,void *);

	// Events activation function
	int                     (*activateEventsPtr)(realtype t, N_Vector y, void *);

	// Events assignment function
	int                     (*assignEventsPtr)(realtype, N_Vector, void *, int assignment_id, realtype * memory);

	// Events priority function
	int                     (*priorityEventsPtr)(realtype, N_Vector, void *);

	realtype                rel_tol;
	N_Vector                abs_tol;

} IntegrationData;


typedef struct IntegrationSettings
{
	double                t_min;
	int                   nb_samples;
	double                abs_tol;
	double                rel_tol;
	double *              list_samples;

} IntegrationSettings;

typedef struct IntegrationOptions
{
	int                   max_num_steps; //500
	int                   max_conv_fails; //10
	int                   max_err_test_fails; //7

} IntegrationOptions;

typedef struct IntegrationFunctions
{
  // CVODE integration functions
  // Initial assignments function
  int                     (*initAssPtr)       (realtype t, N_Vector y, void * user_data);

  // Ordinary differential equations function
  int                     (*funcPtr)          (realtype, N_Vector, N_Vector, void *);

  // Differential algebraic equations function
  int                     (*funcIdaPtr)        (realtype, N_Vector, N_Vector, N_Vector, void *);

  // Jacobian matrix function
  int                     (*jacPtr)           (long int, realtype, N_Vector, N_Vector, DlsMat, void *, N_Vector, N_Vector, N_Vector);

  // Assignments functions
  int                     (*assPtr)           (realtype, N_Vector, void *);

  // Indicates if the jacobian matrix function has been provided
  int                     hasJacobian;

  // Indicates if the model should use IDA
  int                     isDAE;
  int                     init_conditions_solved;

  // Events roots functions
  int                     (*rootsEventsPtr)(realtype, N_Vector, realtype *, void *);

  // Events roots functions for IDA
  int                     (*rootsEventsIDAPtr)(realtype, N_Vector, N_Vector, realtype *,void *);

  // Events activation function
  int                     (*activateEventsPtr)(realtype t, N_Vector y, void *);

  // Events assignment function
  int                     (*assignEventsPtr)(realtype, N_Vector, void *, int assignment_id, realtype * memory);

  // Events priority function
  int                     (*priorityEventsPtr)(realtype, N_Vector, void *);

} IntegrationFunctions;

// C Flexible array
typedef struct Events {
	int len;
	int * list;
} Events;

typedef struct Integration
{
	IntegrationFunctions *    integration_functions;
	IntegrationSettings *     integration_settings;
	IntegrationOptions *      integration_options;

} Integration;


#endif //INTEGRATION_STRUCT
