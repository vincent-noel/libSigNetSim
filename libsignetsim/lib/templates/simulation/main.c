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
 *   Simulation template                                                      *
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
#include <math.h>
#include <string.h>
#include <stdlib.h>

#include <cvode/cvode.h>             /* prototypes for CVODE fcts., consts. */
#include <cvode/cvode_dense.h>       /* prototype for CVDense */

#include "model.h"
// #include "../C_generated/initial_values.h"
#include "data.h"
#include "integrate/integrate.h"

#define NV_Ith_S(v,i) ( NV_DATA_S(v)[i] )
#define Ith(v,i)    NV_Ith_S(v,i-1)       /* Ith numbers components 1..NEQ */
#define IJth(A,i,j) DENSE_ELEM(A,i-1,j-1) /* IJth numbers rows,cols 1..NEQ */

#ifdef MPI
#include <mpi.h>
int nb_procs;
int my_proc;
#endif
double steady_states = 0;

list_of_models            *    t_models;
// ListOfInitialValues       *    t_initial_values;
Experiment * experiments;
int nb_experiments;

void init_data();
void initializeModels()
{
    init_models();
    t_models = getListOfModels();

    init_data();
    experiments = getListOfExperiments();
    nb_experiments = getNbExperiments();
}

#ifdef MPI
int simulate_model(int model_id, char * folder)
{


    ModelDefinition * t_model = t_models->models[model_id];
    int return_code = 0;

    if (folder != NULL)
        setWorkingDirectory(folder);

    if (nb_experiments > 0) {

        int nb_conditions = 0;
        int experiment_ind;
        int condition_ind;
        for (experiment_ind = 0; experiment_ind < nb_experiments; experiment_ind++)
            for (condition_ind = 0; condition_ind < experiments[experiment_ind].nb_conditions; condition_ind++)
                nb_conditions++;

        ExperimentalCondition ** list_conditions = malloc(sizeof(ExperimentalCondition *)*nb_conditions);
        int * inds_experiments = malloc(sizeof(int)*nb_conditions);
        int * inds_conditions = malloc(sizeof(int)*nb_conditions);

        int i_condition = 0;
        for (experiment_ind = 0; experiment_ind < nb_experiments; experiment_ind++)
            for (condition_ind = 0; condition_ind < experiments[experiment_ind].nb_conditions; condition_ind++)
            {
                list_conditions[i_condition] = &(experiments[experiment_ind].conditions[condition_ind]);
                inds_experiments[i_condition] = experiment_ind;
                inds_conditions[i_condition] = condition_ind;

                i_condition++;
            }

        int nb_runs = nb_conditions/nb_procs;
        if (nb_conditions%nb_procs > 0)
          nb_runs++;

        int i_run;
        for (i_run = 0; i_run <= nb_runs; i_run++)
        {
            int indice_condition = i_run*nb_procs + my_proc;
            if (indice_condition < nb_conditions)
            {

              printf("run #%d on proc %d (%d/%d)\n", i_run, my_proc, indice_condition, nb_conditions);

                ExperimentalCondition * t_condition = list_conditions[indice_condition];
            
                if (steady_states == 0)
                {

                  IntegrationResult * result;
                  result = simulateModel(t_model, t_condition, NULL);//, 0);

                  if (result->return_code >= 0)
                  {
                      char out_name[200];
                      if (folder != NULL)
                          sprintf(out_name, "%s/results/results_%d_%d", folder,
                                    inds_experiments[indice_condition],
                                    inds_conditions[indice_condition]);

                      else
                          sprintf(out_name, "results/results_%d_%d",
                                    inds_experiments[indice_condition],
                                    inds_conditions[indice_condition]);

                      WriteTrajectories(result, out_name);
                      return_code &= result->return_code;

                      FinalizeIntegrationResult(result);
                  }
                }
                else
                {
                    SteadyStatesIntegrationResult * result;
                    result = simulateModelSteadyStates(t_model, t_condition, NULL);//, 0);

                    if (result->return_code >= 0)
                    {
                        char out_name[200];
                        if (folder != NULL)
                            sprintf(out_name, "%s/results/results_%d_%d", folder,
                                      inds_experiments[indice_condition],
                                      inds_conditions[indice_condition]);

                        else
                            sprintf(out_name, "results/results_%d_%d",
                                      inds_experiments[indice_condition],
                                      inds_conditions[indice_condition]);


                        WriteSteadyStates(result, out_name);
                    }
                    return_code &= result->return_code;


                    FinalizeSteadyStatesIntegrationResult(result);
                }
            }
            printf("run #%d on proc %d done !\n", i_run, my_proc);

        }
    }

    return return_code;
}

#else

int simulate_model(int model_id, char * folder)
{

    ModelDefinition * t_model = t_models->models[model_id];
    int return_code = 0;

    if (folder != NULL)
        setWorkingDirectory(folder);

    if (nb_experiments > 0) {

        int experiment_ind;
        for (experiment_ind = 0; experiment_ind < nb_experiments; experiment_ind++)
        {

            int condition_ind;
            for (condition_ind = 0; condition_ind < experiments[experiment_ind].nb_conditions; condition_ind++)
            {
                // Code for one condition
                ExperimentalCondition * t_condition = &(experiments[experiment_ind].conditions[condition_ind]);

                // Simulating
                //IntegrationResult * result = InitializeIntegrationResult(model, NULL, 0);
                if (steady_states == 0)
                {

                  IntegrationResult * result;
                  result = simulateModel(t_model, t_condition, NULL);//, 0);

                  if (result->return_code >= 0)
                  {
                      char out_name[200];
                      if (folder != NULL)
                          sprintf(out_name, "%s/results/results_%d_%d", folder,
                                    experiment_ind, condition_ind);

                      else
                          sprintf(out_name, "results/results_%d_%d",
                                    experiment_ind, condition_ind);


                      WriteTrajectories(result, out_name);
                      return_code &= result->return_code;

                      FinalizeIntegrationResult(result);
                  }
                }
                else
                {
                    SteadyStatesIntegrationResult * result;
                    result = simulateModelSteadyStates(t_model, t_condition, NULL);//, 0);

                    if (result->return_code >= 0)
                    {
                        char out_name[200];
                        if (folder != NULL)
                            sprintf(out_name, "%s/results/results_%d_%d", folder,
                                        experiment_ind, condition_ind);


                        else
                            sprintf(out_name, "results/results_%d_%d",
                                        experiment_ind, condition_ind);



                        WriteSteadyStates(result, out_name);
                    }
                    return_code &= result->return_code;


                    FinalizeSteadyStatesIntegrationResult(result);
                }

            }
        }


    } else {


        if (steady_states == 0)
        {

          IntegrationResult * result;
          result = simulateModel(t_model, NULL, NULL);//, 0);

          if (result->return_code >= 0)
          {
              char out_name[200];
              if (folder != NULL)
                sprintf(out_name, "%s/results/results_0_%d", folder, model_id);

              else
                sprintf(out_name, "results/results_0_%d", model_id);

              WriteTrajectories(result, out_name);
              return_code &= result->return_code;

              FinalizeIntegrationResult(result);
          }
        }
        else
        {
            SteadyStatesIntegrationResult * result;
            result = simulateModelSteadyStates(t_model, NULL, NULL);//, 0);

            if (result->return_code >= 0)
            {
                char out_name[200];
                if (folder != NULL)
                  sprintf(out_name, "%s/results/results_%d", folder, model_id);

                else
                  sprintf(out_name, "results/results_%d", model_id);

                WriteSteadyStates(result, out_name);
            }

            return_code &= result->return_code;

            FinalizeSteadyStatesIntegrationResult(result);
        }
    }

    return return_code;
}

#endif

int simulate_models(char * filename)
{
    int i, t_res, res;
    res = 0;

    for (i=0; i < t_models->nb_models; i++)
    {
        t_res = simulate_model(i, filename);
        res = (res < 0 || t_res < 0)?-1:0;
    }
    return res;
}


int main (int argc, char * argv[])
{

#ifdef MPI

    MPI_Init (&argc, &argv);	/* starts MPI */
    MPI_Comm_rank (MPI_COMM_WORLD, &my_proc);	/* get current process id */
    MPI_Comm_size (MPI_COMM_WORLD, &nb_procs);	/* get number of processes */

#endif

    int res;
    initializeModels();

    char * folder = NULL;
    int model_id = -1;
    int i_arg = 1;

    // double time_max = CONV_TIME;
    steady_states = 0;

    while(i_arg < argc)
    {
        //printf("%s\n", argv[i_arg]);

        if (strcmp(argv[i_arg],"-o") == 0)
        {
            folder = argv[i_arg+1];
            i_arg += 2;
        }

        else if (strcmp(argv[i_arg], "-m") == 0)
        {
            model_id = atoi(argv[i_arg+1]);
            if (model_id >= t_models->nb_models)
            {
                printf("! Model id #%d doesn't exist !\n", model_id);
                return EXIT_FAILURE;
            }
            i_arg += 2;
        }

        // else if (strcmp(argv[i_arg], "-t") == 0)
        // {
        //     time_max = atof(argv[i_arg+1]);
        //     i_arg += 2;
        // }

        else if (strcmp(argv[i_arg], "-s") == 0)
        {
            steady_states = 1;
            i_arg += 1;
        }

    }

    // if (steady_states == 1)
    // ;
    //     // res = look_steady_states(model_id, time_max, folder);
    //
    // else
    // {
    if (model_id >= 0)
        res = simulate_model(model_id, folder);
    else
        res = simulate_models(folder);
    // }



    finalize_models();

#ifdef MPI
    MPI_Finalize();
#endif

    if (res == -1) return EXIT_FAILURE;
    else
    {
        //printf("%d\n", useJacobian);
        return EXIT_SUCCESS;
    }
}
