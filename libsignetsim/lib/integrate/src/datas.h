/******************************************************************************
 *                                                                            *
 *   datas.h                                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Data generic definitions                                                 *
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

#ifndef DATA_STRUCT
#define DATA_STRUCT

// Data observation
typedef struct ExperimentalObservation
{
    double    t;
    double    value;
    double    value_dev;      /* -1 = NULL */
    int       isSteadyState;  /* 0 = false, 1 = true */
    double    min_steady_state;
    double    max_steady_state;
    //
    int       variable_type; /* Type of formula : 0 = derivative, 1 = assignment*/
    int       variable_ind;    /* Position of the variable in derivative or assignment array */
    int       variable_id;    /* Position of the variable in the complete array */
    int       variable_pos; /* Index of the variable in the list of observables */

    char  *   variable_name;

} ExperimentalObservation;


// Treatment
typedef struct Treatment
{
    double    value;

    int       variable_type; /* Type of formula : 0 = derivative, 1 = assignment*/
    int       variable_ind;    /* Position of the variable in derivative or assignment array */
    char  *   variable_name;
} Treatment;


// Data initial condition
typedef struct TimedTreatments
{
    double        t;
    int           nb_treatments;
    Treatment  *  treatments;

} TimedTreatments;


// Condition
typedef struct ExperimentalCondition
{
    int nb_observed_values;
    int nb_timed_treatments;

    ExperimentalObservation * observed_values;
    TimedTreatments * timed_treatments;

    char * name;
} ExperimentalCondition;


// Experiment
typedef struct Experiment
{
    int nb_conditions;
    ExperimentalCondition * conditions;

    char * name;

} Experiment;

#endif //DATA_STRUCT
