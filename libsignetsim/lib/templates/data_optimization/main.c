/******************************************************************************
 *                                                                            *
 *   main.c                                                                   *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Data optimization template                                               *
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
#ifdef MPI
#include <mpi.h>
#endif

//#include "scoreFunctions.h"
#include "optim.h"
#include "model.h"
#include "data.h"

int main(int argc, char **argv )
{


#ifdef MPI
	// MPI initialization steps
	int nnodes, myid;

	int rc = MPI_Init(NULL, NULL); 	     /* initializes the MPI environment */
	if (rc != MPI_SUCCESS)
		printf (" > Error starting MPI program. \n");

	MPI_Comm_size(MPI_COMM_WORLD, &nnodes);        /* number of processors? */
	MPI_Comm_rank(MPI_COMM_WORLD, &myid);         /* ID of local processor? */



#endif	// define the optimization settings

	// Initializing the scoring function
	// First, the model
	init_models();
	list_of_models * t_models = getListOfModels();
	ModelDefinition * working_model = t_models->models[0];

	// Then, the data
	init_data();
	Experiment * experiments = getListOfExperiments();
	int nb_experiments = getNbExperiments();

    ScoreSettings * score_settings = init_score_settings();

    // define the optimization parameters
	init_params(working_model);

	// Finally, we initialize the data and print the reference
	InitializeModelVsDataScoreFunction(working_model, experiments, nb_experiments, score_settings, getOptimParameters());

#ifdef MPI
	SAType * settings = InitPLSA(nnodes, myid);

#else
	SAType * settings = InitPLSA();

#endif


	// define the optimization settings
    init_settings(settings);

	settings->scoreFunction = &computeScore;
	settings->printFunction = &saveBestResult;
	settings->logs->best_score = 1;
	settings->logs->best_res = 1;
	settings->logs->params = 1;
	settings->logs->res = 1;
	settings->logs->score = 1;
	settings->logs->pid = 1;

	// Needs to be called now since we call getLogDir()
	InitializeLogs(settings->logs);



#ifdef MPI
	if (myid == 0)
	{
#endif

	PrintReferenceData(getLogDir());

#ifdef MPI
	}
#endif

	// Running the optimization
	runPLSA();


	FinalizeScoreFunction();
	finalize_data();
	finalize_models();

#ifdef MPI
	// terminates MPI execution environment
	MPI_Finalize();
#endif

	return 0;
}
