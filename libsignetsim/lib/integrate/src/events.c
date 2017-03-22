/******************************************************************************
 *                                                                            *
 *   events.c                                                                 *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Fonctions for integrating models with events                             *
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
#include "realtype_math.h"

void initRoots(IntegrationData * user_data, realtype * t_roots)
{
    int i;
    for (i=0; i < user_data->nb_roots; i++)
    {
        if (user_data->roots_operators[i] == 0)
        {
//            if (t_roots[i] >= RCONST(0.0))
            if (rt_geq(t_roots[i], RCONST(0.0)))
              user_data->roots_triggers[i] = 1;
            else
              user_data->roots_triggers[i] = -1;
        }

        else if (user_data->roots_operators[i] == 1)
        {
//            if (t_roots[i] > RCONST(0.0))
            if (rt_gt(t_roots[i], RCONST(0.0)))
              user_data->roots_triggers[i] = 1;
            else
              user_data->roots_triggers[i] = -1;
        }

        else if (user_data->roots_operators[i] == 2)
        {
//            if (t_roots[i] == RCONST(0.0))
            if (rt_eq(t_roots[i], RCONST(0.0)))
              user_data->roots_triggers[i] = 1;
            else
              user_data->roots_triggers[i] = -1;
        }

        else if (user_data->roots_operators[i] == 3)
        {
//            if (t_roots[i] != RCONST(0.0))
            if (rt_neq(t_roots[i], RCONST(0.0)))
              user_data->roots_triggers[i] = 1;
            else
              user_data->roots_triggers[i] = -1;
        }
    }
}


void updateRoots(IntegrationData * data, realtype * t_roots)
{
//    printf("We actually pass through update roots\n");
    int i;
    for (i=0; i < data->nb_roots; i++)
    {
        // If the operator is >=
        if (data->roots_operators[i] == 0)
        {
            // If the root was previously deactivated and the root pass strictly negative
//            if (data->roots_triggers[i] == 1 && t_roots[i] < 0 && data->roots_values[i] >= 0)
            if (data->roots_triggers[i] == 1 && rt_lt(t_roots[i], RCONST(0.0)) && rt_geq(data->roots_values[i], RCONST(0.0)))
                data->roots_triggers[i] = -1;

            // If the root was previously activated and the root pass positive
//            else if (data->roots_triggers[i] == -1 && t_roots[i] >= 0 && data->roots_values[i] <= 0)
            else if (data->roots_triggers[i] == -1 && rt_geq(t_roots[i], RCONST(0.0)) && rt_leq(data->roots_values[i], RCONST(0.0)))
              data->roots_triggers[i] = 1;
        }
        // If the operator is >
        else if (data->roots_operators[i] == 1)
        {
            // If the root was previously deactivated and the root pass negative
//            if (data->roots_triggers[i] == 1 && t_roots[i] <= 0 && data->roots_values[i] >= 0)
            if (data->roots_triggers[i] == 1 && rt_leq(t_roots[i], RCONST(0.0)) && rt_geq(data->roots_values[i], RCONST(0.0)))
              data->roots_triggers[i] = -1;

            // If the root was previously activated and the root pass strictly positive
//            else if (data->roots_triggers[i] == -1 && t_roots[i] > 0 && data->roots_values[i] <= 0)
            else if (data->roots_triggers[i] == -1 && rt_gt(t_roots[i], RCONST(0.0)) && rt_leq(data->roots_values[i], RCONST(0.0)))
              data->roots_triggers[i] = 1;
        }
        // If the operator is ==
        else if (data->roots_operators[i] == 2)
        {
//           if (data->roots_triggers[i] == 1 && t_roots[i] != 0 && data->roots_values[i] == 0)
           if (data->roots_triggers[i] == 1 && rt_neq(t_roots[i], RCONST(0.0)) && rt_eq(data->roots_values[i], RCONST(0.0)))
             data->roots_triggers[i] = -1;

//           else if (data->roots_triggers[i] == -1 && t_roots[i] == 0 && data->roots_values[i] != 0)
           else if (data->roots_triggers[i] == -1 && rt_eq(t_roots[i], RCONST(0.0)) && rt_neq(data->roots_values[i], RCONST(0.0)))
             data->roots_triggers[i] = 1;
        }

        // If the operator is !=
        else if (data->roots_operators[i] == 3)
        {
//          if (data->roots_triggers[i] == 1 && t_roots[i] == 0 && data->roots_values[i] != 0)
          if (data->roots_triggers[i] == 1 && rt_eq(t_roots[i], RCONST(0.0)) && rt_neq(data->roots_values[i], RCONST(0.0)))
             data->roots_triggers[i] = -1;

//           else if (data->roots_triggers[i] == -1 && t_roots[i] != 0 && data->roots_values[i] == 0)
           else if (data->roots_triggers[i] == -1 && rt_neq(t_roots[i], RCONST(0.0)) && rt_eq(data->roots_values[i], RCONST(0.0)))
             data->roots_triggers[i] = 1;
        }
    }
}


int getNbRoots(IntegrationData * data)
{
    return data->nb_roots + data->nb_timed_events;
}

int getNbEvents(IntegrationData * data)
{
    return data->nb_events + data->nb_timed_events;
}

int getNbTimedTreatments(IntegrationData * data)
{
    return data->nb_timed_treatments;
}

Events * getActivatedEvents(IntegrationData * data)
{
    int i;

    int nb_events_activated = 0;
    for (i=0; i < getNbEvents(data); i++)
        if (data->events_triggers[i] > 0)
            nb_events_activated++;

    Events * res = malloc(sizeof(res));
    res->len = nb_events_activated;

    if (nb_events_activated > 0)
    {
        int * list_events = calloc(nb_events_activated, sizeof(int));
        int i_event = 0;

        for (i=0; i < getNbEvents(data); i++)
            if (data->events_triggers[i] > 0)
            {
                list_events[i_event] = i;
                i_event++;
            }

        res->list = list_events;
    }

    return res;
}


realtype get_max_priority_activated_events(IntegrationData * data, realtype t, int * list_events, int nb_events_activated, int * executed_events)
{
    int i;
    // priority_wrapper(data, t);
    (*data->priorityEventsPtr)(t, data->derivative_variables, (void *) data);

    realtype min_priority = 1000;

    for (i=0; i < nb_events_activated; i++)
        if (data->events_has_priority[list_events[i]] == 1 && executed_events[i] == 0)
            min_priority = MIN(min_priority, *(data->events_priorities[list_events[i]]));

    for (i=0; i < nb_events_activated; i++)
        if (data->events_has_priority[list_events[i]] == 0 && executed_events[i] == 0)
            *(data->events_priorities[list_events[i]]) = (min_priority-1);

    realtype highest_priority = min_priority-1;

    for (i=0; i < nb_events_activated; i++)
        if (executed_events[i] == 0)
            highest_priority = MAX(highest_priority, *(data->events_priorities[list_events[i]]));

    return highest_priority;
}


Events * getNextConcurrentEvents(IntegrationData * data, Events * events_activated, int * executed_events, realtype t)
{
    int i;

    realtype max_priority = get_max_priority_activated_events(data, t, events_activated->list, events_activated->len, executed_events);

    int nb_concurrent_events = 0;

    for (i=0; i < events_activated->len; i++)
        if (*(data->events_priorities[events_activated->list[i]]) == max_priority)
            nb_concurrent_events++;

    int * list_concurrent_events = calloc(nb_concurrent_events, sizeof(int));
    int i_event = 0;

    for (i=0; i < events_activated->len; i++)
        if (*(data->events_priorities[events_activated->list[i]]) == max_priority)
        {
            list_concurrent_events[i_event] = events_activated->list[i];
            executed_events[i] = 1;
            i_event++;
        }

    Events * res = malloc(sizeof(Events));
    res->len = nb_concurrent_events;
    res->list = list_concurrent_events;


    return res;
}

void execute(IntegrationData * data, realtype t, int event_id)
{
    if (event_id < data->nb_events)
        assign_wrapper(data, t, event_id, NULL);

    else
    {
        int timed_event_ind = event_id-data->nb_events;

        assign_wrapper(data, t,
                        data->t_events_assignment[timed_event_ind],
                        data->t_events_memory[timed_event_ind]);
    }
}

void mark_executed(IntegrationData * data, int event_id)
{
    data->events_triggers[event_id] = MAX(data->events_triggers[event_id]-1, 0);
}


int roots_wrapper(IntegrationData * data, realtype t, realtype *gout)
{
  int i, ind;

  ind = data->nb_roots;
  for (i=0; i < data->nb_timed_events; i++)
      gout[ind+i] = t - data->t_events_time[i];

  ind += data->nb_timed_events;
  for (i=0; i < data->nb_timed_treatments; i++){
      gout[ind+i] = t - RCONST(data->timed_treatments[i]->t);
}
  return 0;
}


int activate_wrapper(IntegrationData * data, realtype t)
{
  if (data->nb_roots > 0)
    (*data->activateEventsPtr)(t, data->derivative_variables, (void *) data);

  int ind = data->nb_roots;
  int i;
  for (i=0; i < data->nb_timed_events; i++)
      if (data->roots_triggers[ind+i] == 1)
      {
        data->events_triggers[data->nb_events+i]++;
        data->roots_triggers[ind+i] = 0;
      }

  return 0;
}
//
// int priority_wrapper(IntegrationData * data, realtype t)
// {
//   if (data->nb_events > 0)
//     (*data->priorityEventsPtr)(t, data->derivative_variables, (void *) data);
//
//   return 0;
// }

int assign_wrapper(IntegrationData * data, realtype t, int assignment_id, realtype * memory)
{
  if (data->nb_events > 0)
    (*data->assignEventsPtr)(t, data->derivative_variables, (void *) data, assignment_id, memory);

  return 0;
}


void shuffle(Events * events)
{
    if (events->len > 1)
    {
        int i;
        for (i = 0; i < events->len - 1; i++)
        {
          int j = i + rand() / (RAND_MAX / (events->len - i) + 1);
          int t = events->list[j];
          events->list[j] = events->list[i];
          events->list[i] = t;
        }
    }

}

void freeEvents(Events * events)
{
  if (events->len > 0)
      free(events->list);

  free(events);
}

void executeTimedTreatments(IntegrationData * data)
{
    N_Vector y = data->derivative_variables;
    N_Vector cst = data->constant_variables;
    N_Vector ass = data->assignment_variables;

    int ind = getNbRoots(data);
    int i,j;
    for (i=0; i < data->nb_timed_treatments; i++) {
      //  printf(" root timed treatment %d = %g\n", i, data->roots_values[ind+i]);

        TimedTreatments * t_timed_treatments = data->timed_treatments[i];
        if (rt_eq(data->roots_values[ind+i], RCONST(0.0)))
        {
    //        data->roots_values[ind+i] = 0;

            for (j=0; j < t_timed_treatments->nb_treatments; j++) {
                // printf(" Executing treatment %d\n", j);
                Treatment * t_treatment = &(t_timed_treatments->treatments[j]);

                if (t_treatment->variable_type == 0) {
                  Ith(y, t_treatment->variable_ind + 1) = RCONST(t_treatment->value);
                } else if (t_treatment->variable_type == 1) {
                  Ith(ass, t_treatment->variable_ind + 1) = RCONST(t_treatment->value);
                }  else if (t_treatment->variable_type == 2) {
                  Ith(cst, t_treatment->variable_ind + 1) = RCONST(t_treatment->value);
                }
            }
        }
    }

}

//
// realtype * addTimedEvent(realtype t, int assignment, int memory_size, void * user_data)
// {
//     IntegrationData * data = (IntegrationData *) user_data;
//
//     data->nb_timed_events++;
//     realtype * t_times = realloc(data->t_events_time,
//                       sizeof(realtype)*data->nb_timed_events);
//     t_times[data->nb_timed_events-1] = t;
//     data->t_events_time = t_times;
//
//     data->t_events_assignment = realloc(data->t_events_assignment,
//                             sizeof(realtype)*data->nb_timed_events);
//     data->t_events_assignment[data->nb_timed_events-1] = assignment;
//
//     realtype ** t_events_memory = realloc(data->t_events_memory,
//                         sizeof(realtype *)*data->nb_timed_events);
//     t_events_memory[data->nb_timed_events-1] = malloc(sizeof(realtype)*memory_size);
//     data->t_events_memory = t_events_memory;
//
//     // Here we modify the global events objects that we need to activate
//     // the timed events with all the others
//     int * roots_triggers = realloc(data->roots_triggers,
//                           sizeof(int)*(data->nb_roots + data->nb_timed_events));
//     roots_triggers[data->nb_roots + data->nb_timed_events-1] = 0;
//     data->roots_triggers = roots_triggers;
//
//     realtype * roots_values = realloc(data->roots_values,
//                           sizeof(realtype)*(data->nb_roots + data->nb_timed_events));
//     roots_values[data->nb_roots + data->nb_timed_events-1] = 0;
//     data->roots_values = roots_values;
//
//
//     int nb_total_events = data->nb_events + data->nb_timed_events;
//
//     // - events_triggers
//     int * events_triggers = realloc(data->events_triggers,
//                               sizeof(int)*nb_total_events);
//     events_triggers[nb_total_events-1] = 0;
//     data->events_triggers = events_triggers;
//
//     // - events_has_priority
//     data->events_has_priority = realloc(data->events_has_priority,
//                                   sizeof(int)*nb_total_events);
//     data->events_has_priority[nb_total_events-1] = data->events_has_priority[assignment];
//     // data->events_has_priority = events_has_priority;
//
//     // - events_priorities
//     data->events_priorities = realloc(data->events_priorities,
//                                             sizeof(realtype *)*nb_total_events);
//
//     data->events_priorities[nb_total_events-1] = malloc(sizeof(realtype));
//
//     if (data->events_has_priority[assignment] == 1)
//       data->events_priorities[nb_total_events-1] = data->events_priorities[assignment];
//
//     data->events_nb_children[assignment]++;
//     data->events_children[assignment] = realloc(data->events_children[assignment],
//                                                   sizeof(int)*data->events_nb_children[assignment]);
//     data->events_children[assignment][data->events_nb_children[assignment]-1] = nb_total_events-1;
//
//     return t_events_memory[data->nb_timed_events-1];
// }
//
// void untrigger(IntegrationData * data, int event_id)
// {
//     data->events_triggers[event_id]--;
//     int i;
//     for (i=0; i < data->events_nb_children[event_id]; i++)
//       data->events_triggers[data->events_children[event_id][i]]--;
// }
