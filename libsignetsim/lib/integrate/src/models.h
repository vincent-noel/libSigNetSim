/******************************************************************************
 *                                                                            *
 *   models.h                                                                 *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Models generic definitions                                               *
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

#include "types.h"

#define VAR_DERIVATIVE      0
#define VAR_ASSIGNMENT      1
#define VAR_CONSTANT        2
#define VAR_DER_DER         3
#define VAR_ALGEBRAIC       4
#define VAR_ALG_DER         5

#ifndef MODEL_STRUCT
#define MODEL_STRUCT

typedef struct ModelVariable
{
    double          value;
    char    *       name;
    int             type;

} ModelVariable;


typedef struct ModelDefinition
{
    int                        nb_derivative_variables;
    int                        nb_assignment_variables;
    int                        nb_constant_variables;
    int                        nb_algebraic_variables;

    ModelVariable   *         derivative_variables;
    ModelVariable   *         der_der_variables;
    ModelVariable   *         assignment_variables;
    ModelVariable   *         constant_variables;
    ModelVariable   *         algebraic_variables;
    ModelVariable   *         alg_der_variables;

    int                       nb_init_assignments;
    int		                    nb_events;
    int                       nb_roots;
    int       *               roots_operators;
    int       *               events_init;
    int       *               memory_size_per_event;
    int       *               events_has_priority;

    IntegrationFunctions *    integration_functions;
    IntegrationSettings *     integration_settings;
    IntegrationOptions *      integration_options;


} ModelDefinition;

typedef struct list_of_models
{
    ModelDefinition ** models;
    int                     nb_models;

} list_of_models;


// Data initial condition
typedef struct InitialValue
{
    double value;

    int       model_id;
    int       variable_type; /* Type of formula : 0 = derivative, 1 = assignment*/
    int       variable_ind;    /* Position of the variable in derivative or assignment array */
    char  *   variable_name;

} InitialValue;

typedef struct InitialValues
{
    InitialValue * initial_values;
    int             nb_initial_values;

} InitialValues;

typedef struct ListOfInitialValues
{
  InitialValues *  sets_of_initial_values;
  int               nb_sets_initial_values;

} ListOfInitialValues;
#endif
