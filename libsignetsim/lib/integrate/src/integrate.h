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
#include "models.h"
#define   MAX_RECORD            256   /* max. length of lines read from file */


// Simulate model
IntegrationResult * simulateModel(ModelDefinition * model,
                                    ExperimentalCondition * condition,
                                    IntegrationResult * result);


SteadyStatesIntegrationResult * simulateModelSteadyStates(ModelDefinition * model,
                                  ExperimentalCondition * condition,
                                  SteadyStatesIntegrationResult * result);
// Free IntegrationResult object
IntegrationResult * InitializeIntegrationResult(
                                  ModelDefinition * model);
void FinalizeIntegrationResult(IntegrationResult * integration_result);

SteadyStatesIntegrationResult * InitializeSteadyStatesIntegrationResult(
                                  ModelDefinition * model,
                                  double * list_samples,
                                  int nb_samples);

void FinalizeSteadyStatesIntegrationResult(
                            SteadyStatesIntegrationResult * integration_result);

// Write integration results to a file
void WriteTrajectories(IntegrationResult * integration_result, char * fileName);
void WriteSteadyStates(SteadyStatesIntegrationResult * integration_result, char * fileName);


// Logging functions
// Integration duration logging
// [Des]Activate integration duration logging
void setIntegrationDurationLog(int mode);

// Modify integration duration log filename
void setIntegrationDurationLogFilename(char * filename);

// Error logging
// [Des]Activate error logging
void setIntegrationErrorsLog(int mode);

// Modify error log filename
void setIntegrationErrorsLogFilename(char * filename);

void setWorkingDirectory(char * directory);

realtype * addTimedEvent(realtype t, int assignment, int memory_size, void * user_data);
void untriggerChildren(IntegrationData * data, int event_id);
void retriggerChildren(IntegrationData * data, int event_id);
