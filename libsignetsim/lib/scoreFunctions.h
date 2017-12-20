/******************************************************************************
 *                                                                            *
 *   scoreFunctions.h                                                         *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   This file contains fuctions that are needed for computing                *
 *   diverses scores                                                          *
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

 #include <float.h>
#include "integrate/datas.h"
#include "integrate/models.h"
#include "plsa/types.h"

#include "integrate/integrate.h"

#define   MODEL_VS_DATA     1
#define   MODEL_VS_MODEL    2
#define   MAX_SCORE         DBL_MAX      /* the biggest possible score, ever */
#define   MAX_RECORD        256       /* max. length of lines read from file */


typedef struct
{
	double negative_penalty;               /* Penalty for negative numbers */


} ScoreSettings;

void      InitializeModelVsDataScoreFunction    (ModelDefinition * model,
                                                  Experiment * experiments,
                                                  int nb_experiments,
                                                  ScoreSettings * settings,
                                                  PArrPtr * my_plist);

void      FinalizeScoreFunction                 ();

double    computeScore                          ();
void      saveBestResult                        (char * path, int proc);
void      PrintReferenceData                    (char * path);

