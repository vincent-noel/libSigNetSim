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
#ifdef MPI
#include <mpi.h>
#endif

#include "plsa/sa.h"
#include "plsa/config.h"
#include "scoreFunctions.h"

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

#endif


    // Initializing the scoring function
    // First, the model
    init_models();
    list_of_models * t_models = getListOfModels();
    ModelDefinition * working_model = t_models->models[0];
    // Integration * integration = getIntegration();
    // Then, the data
    init_data();
    Experiment * experiments = getListOfExperiments();
    int nb_experiments = getNbExperiments();

    // Finally, we initialize the data and print the reference
    InitializeModelVsDataScoreFunction(working_model, experiments, nb_experiments);












  	// define the optimization settings
#ifdef MPI
  	SAType * settings = InitPLSA(nnodes, myid);
#else
  	SAType * settings = InitPLSA();
#endif


  // setLogDir("logs");




  // // Initializing the optimization parameters
  // init_settings();
  init_params(working_model);




  settings->scoreFunction = &computeScore;
  settings->printFunction = &saveBestResult;

  PArrPtr * params = getOptimParameters();

  PrintReferenceData(getLogDir());
  // Running the optimization
  runPLSA(params);

  // finalize_settings();
  // finalize_params();
  FinalizeScoreFunction();
  finalize_data();
  finalize_models();
  // print final parameter value and score
#ifdef MPI
//   if (myid == 0)
//   {
// #endif
// 	  printf("final value : %10.7f\n", param);
// 	  printf("final score : %g\n", final_score);
// #ifdef MPI
//   }


  // terminates MPI execution environment
  MPI_Finalize();
#endif
  return 0;
}
