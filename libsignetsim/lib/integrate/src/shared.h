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
 *   Shared fonctions for integrating models                                  *
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
#include <stdio.h>
#include "types.h"
#include "events.h"
#include "models.h"


int                   check_flag(void *flagvalue, char *funcname, int opt, FILE * errLog);

// IntegrationResult *   InitializeIntegrationResult(ModelDefinition * model, double * list_samples, int nb_samples);

IntegrationData *     InitializeIntegrationData(ModelDefinition * model,
                                                ExperimentalCondition * condition,
                                                FILE * errLog);

void                  FinalizeIntegrationData(ModelDefinition * model,
                                              IntegrationData * integration_data);

void                  WriteTrajectories(IntegrationResult * result,
                                        char * fileName);
void                  WriteSteadyStates(SteadyStatesIntegrationResult * integration_result,
                                        char * fileName);

void                  writeResultSample(ModelDefinition * model,
                                        IntegrationResult * result,
                                        IntegrationData * user_data,
                                        realtype t, int sample);
void                  writeResultSteadyState(ModelDefinition * model,
                                        SteadyStatesIntegrationResult * result,
                                        IntegrationData * user_data);
