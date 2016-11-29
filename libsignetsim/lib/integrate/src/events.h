/******************************************************************************
 *                                                                          * *
 *   events.h                                                                 *
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
 
#include "types.h"

void            initRoots(IntegrationData * data, realtype * t_roots);
void            updateRoots(IntegrationData * data, realtype * t_roots);

int             getNbRoots(IntegrationData * data);
int             getNbEvents(IntegrationData * data);
int             getNbTimedTreatments(IntegrationData * data);

Events    *     getActivatedEvents(IntegrationData * data);
Events    *     getNextConcurrentEvents(IntegrationData * data, Events * events_activated, int * executed_events, realtype t);
void            executeTimedTreatments(IntegrationData * data);

void            execute(IntegrationData * data, realtype t, int event_id);
void            mark_executed(IntegrationData * data, int event_id);
// realtype *      addTimedEvent(realtype t, int assignment, int memory_size, void * user_data);
// void            untrigger(IntegrationData * data, int event_id);

int             roots_wrapper(IntegrationData * data, realtype t, realtype * gout);
int             activate_wrapper(IntegrationData * data, realtype t);
int             assign_wrapper(IntegrationData * data, realtype t, int assignment_id, realtype * memory);
// int             priority_wrapper(IntegrationData * data, realtype t);

void            shuffle(Events * events);
void            freeEvents(Events * events);
