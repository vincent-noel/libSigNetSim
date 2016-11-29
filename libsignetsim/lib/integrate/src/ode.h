/******************************************************************************
 *                                                                            *
 *   ode.h                                                                    *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Fonction for integrating ODE model with CVODE                            *
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
#include <stdio.h>

// Simulate model
IntegrationResult * simulateModelCVODE(ModelDefinition * model,
                                        ExperimentalCondition * condition,
                                        FILE * errLog,
                                        IntegrationResult * result);
SteadyStatesIntegrationResult * simulateModelCVODE_SteadyStates(ModelDefinition * model,
                                        ExperimentalCondition * condition,
                                        FILE * errLog,
                                        SteadyStatesIntegrationResult * result);
