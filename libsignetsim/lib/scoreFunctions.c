/******************************************************************************
 *                                                                            *
 *   scoreFunctions.c                                                         *
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
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
// #include "../C_optimization/global.h"
#include "scoreFunctions.h"

#define MIN_PRECISION 1e-16

int       score_type;

ModelDefinition * sf_model;
Experiment * sf_experiments;
int nb_sf_experiments;
ScoreSettings * score_settings;
PArrPtr * sf_plist;

IntegrationResult *** sf_all_results;

IntegrationResult *** initializeIntegrationResults(ModelDefinition * model, Experiment * experiments, int nb_experiments)
{

   IntegrationResult *** all_results = malloc(sizeof(IntegrationResult **) * nb_experiments);

   int experiment_ind;
   for (experiment_ind = 0; experiment_ind < nb_experiments; experiment_ind++)
   {
	   all_results[experiment_ind] = malloc(sizeof(IntegrationResult *)*experiments[experiment_ind].nb_conditions);
	   int condition_ind;
	   for (condition_ind = 0; condition_ind < experiments[experiment_ind].nb_conditions; condition_ind ++)
	   {
		 ExperimentalCondition * t_condition = &(experiments[experiment_ind].conditions[condition_ind]);

		  if (t_condition->nb_observed_values > 0)
			all_results[experiment_ind][condition_ind] = InitializeIntegrationResult(model);

	   }
   }

   return all_results;
}


void terminateIntegrationResults(IntegrationResult *** all_results, Experiment * experiments, int nb_experiments)
{
  int experiment_ind;
  for (experiment_ind = 0; experiment_ind < nb_experiments; experiment_ind ++)
  {
	int condition_ind;
	for (condition_ind = 0; condition_ind < experiments[experiment_ind].nb_conditions; condition_ind ++)
	{
		ExperimentalCondition * t_condition = &(experiments[experiment_ind].conditions[condition_ind]);
		if (t_condition->nb_observed_values > 0)
		  FinalizeIntegrationResult(all_results[experiment_ind][condition_ind]);
	}
	free(all_results[experiment_ind]);
  }
  free(all_results);
}

void InitializeModelVsDataScoreFunction(ModelDefinition * model,
										Experiment * experiments,
										int nb_experiments,
										ScoreSettings * settings,
										PArrPtr * plist)
{
	score_type = MODEL_VS_DATA;
	sf_model = model;
	sf_experiments = experiments;
	nb_sf_experiments = nb_experiments;
	sf_all_results = initializeIntegrationResults(model, experiments, nb_experiments);
    score_settings = settings;
    sf_plist = plist;
}

void FinalizeScoreFunction()
{
	if (score_type == MODEL_VS_DATA)
	{
	  terminateIntegrationResults(sf_all_results, sf_experiments, nb_sf_experiments);
	}

}

int isAtSteadyState(double * y, int pos, double ech)
{
	double value = y[pos];
	double score = 0;
	double t_score;

	int pos_pt = (int) pos*1.1;
	// printf("> testing stability from %g to %g : %g\t", (double) pos, (double) pos_pt, value);
	int i;
	for (i=pos+1; i <= pos_pt; i++)
	{
		t_score = fabs(y[i]-value);
		// printf("%g\t", y[i]);
		if (value != 0)
			t_score /= value;
		else
			t_score /= MIN_PRECISION;
		score += t_score;
		//printf(" deviation: %g\n", t_score);
	}
	score /= (pos_pt-pos)*ech;
	// printf("> Average deviation : %g\n", score);
	// printf(":%g", score);

	if (score < 0.000001) return 1;
	else return 0;

}
int compare_doubles(const void* a, const void* b)
{
	 double double_a = * ( (double*) a );
	 double double_b = * ( (double*) b );

	 if ( double_a == double_b ) return 0;
	 else if ( double_a < double_b ) return -1;
	 else return 1;
}

//
// double ComputeScoreModelVsModel(IntegrationResult * result, IntegrationResult * result_reference, OptimMappingObservables * optim_mapping)
// {
//     double traj_score = 0;
//     int y;
//
//     for(y=0; y < optim_mapping->nbWorkingModelObservables; y++)
//     {
//         int working_model_id = optim_mapping->workingModelObservables[y].ind_variable;
//         if (optim_mapping->workingModelObservables[y].type_variable == VAR_ASSIGNMENT)
//             working_model_id += result->nb_derivative_variables;
//
//         int reference_model_id = optim_mapping->referenceModelObservables[optim_mapping->mappingObservables[y]].ind_variable;
//         if (optim_mapping->referenceModelObservables[optim_mapping->mappingObservables[y]].type_variable == VAR_ASSIGNMENT)
//             reference_model_id += result->nb_derivative_variables;
//
//         double t_score = 0;
//         int t;
//         for(t=0; t < result->nb_samples; t++)
//         {
//             if (result_reference->y[reference_model_id][t] != 0)
//                 t_score += fabs((result->y[working_model_id][t] - result_reference->y[reference_model_id][t])
//                                   / result_reference->y[reference_model_id][t]);
//             else
//                 t_score += fabs((result->y[working_model_id][t] - result_reference->y[reference_model_id][t])/MIN_PRECISION);
//         }
//         traj_score += t_score/result->nb_samples;
//     }
//
//     traj_score = traj_score/optim_mapping->nbWorkingModelObservables;
//     return traj_score;
// }
//




double ComputeScoreDataVsModel(IntegrationResult * result, ExperimentalObservation * observations, int nb_observations)
{
	//int debug=0;
	double score = 0;
	int i;
	double penalty = 0;
	for (i=0; i < (result->nb_derivative_variables + result->nb_assignment_variables); i++)
	{
		int t;
		for (t=0; t < result->nb_samples; t++)
		{
		  if (result->y[i][t] < -1e-8)
		  penalty += score_settings->negative_penalty;
		  // return -1;
		}

	}

	for (i=0; i < nb_observations; i++)
	{
		int t_ech_data = 0;
		while (t_ech_data < result->nb_samples && observations[i].t != result->list_samples[t_ech_data])
		    t_ech_data++;

		double model_ech, data_ech, ratio_ech,ratio_normalise_ech;
		double score_observed_value = 0;

		int ind = 0;
		if (observations[i].variable_type == 0)
			ind = observations[i].variable_ind;
		else if (observations[i].variable_type == 1)
			ind = result->nb_derivative_variables + observations[i].variable_ind;
		else if (observations[i].variable_type == 2)
			ind = result->nb_derivative_variables + result->nb_assignment_variables + observations[i].variable_ind;
		else printf("> Unknown type of variable !\n");

		model_ech = result->y[ind][t_ech_data];
		data_ech = observations[i].value;

		ratio_ech = data_ech-model_ech;

		// model : 2.4e+02, data : 12, score : 0.95

		if (data_ech < model_ech)
			if (data_ech != 0)
				ratio_normalise_ech = ratio_ech/data_ech;
			else
				ratio_normalise_ech = ratio_ech/MIN_PRECISION;
		else
		  if (model_ech != 0)
			  ratio_normalise_ech = ratio_ech/model_ech;
		  else
			  ratio_normalise_ech = ratio_ech/MIN_PRECISION;

//		double t_ech = result->t[1]-result->t[0];

		if (observations[i].isSteadyState == 0) {
		  score_observed_value = fabs(ratio_normalise_ech);
		  // printf("model : %.2g, data : %.2g, score : %.2g\n", model_ech, data_ech, score_observed_value);
		} /*else if (observations[i].isSteadyState == 1) {

		  int t_min_steady_state = (int) round(observations[i].min_steady_state/result->sampling_frequency);
		  int t_max_steady_state = (int) round(observations[i].max_steady_state/result->sampling_frequency);

		  if (isAtSteadyState(result->y[ind], t_min_steady_state, t_ech) == 0
			  && isAtSteadyState(result->y[ind], t_max_steady_state, t_ech) == 1) {

			  score_observed_value = fabs(ratio_normalise_ech);

		  } else score_observed_value = MAX_SCORE;
		} */
		else score_observed_value = MAX_SCORE;

		score += score_observed_value;
	}
	score /= nb_observations;

	return score+penalty;

}



double computeScoreData(IntegrationResult *** all_results, ModelDefinition * model, Experiment * experiments, int nb_experiments)
{
	double score = 0;
	int experiment_ind;
	for (experiment_ind = 0; experiment_ind < nb_experiments; experiment_ind++)
	{
		double score_experiment = 0;
		int condition_ind;
		for (condition_ind = 0; condition_ind < experiments[experiment_ind].nb_conditions; condition_ind++)
		{
			// Code for one condition
			ExperimentalCondition * t_condition = &(experiments[experiment_ind].conditions[condition_ind]);

			if (t_condition->nb_observed_values > 0)
			{

				IntegrationResult * result = all_results[experiment_ind][condition_ind];
				// IntegrationResult * result = InitializeIntegrationResult(model, NULL, 0);
				result->return_code = -1;
				simulateModel(model, t_condition, result);

				// all_results[experiment_ind][condition_ind] = result;

				// Computing scores
				double score_condition = MAX_SCORE/experiments[experiment_ind].nb_conditions;
				if (result->return_code >= 0)
				{
					score_condition = ComputeScoreDataVsModel(result, t_condition->observed_values, t_condition->nb_observed_values);

					if (score_condition >= 0)
						score_condition = score_condition/experiments[experiment_ind].nb_conditions;

					else
						score_condition = MAX_SCORE/experiments[experiment_ind].nb_conditions;
				}

				score_experiment += score_condition;
			}
		}
		score_experiment = score_experiment/nb_experiments;
		score += score_experiment;
	}

	return score;
}


double computeScore()
{

  double score=0;

  if (score_type == MODEL_VS_DATA)
	  score = computeScoreData(sf_all_results, sf_model, sf_experiments, nb_sf_experiments);

  return score;
}


void PrintReferenceData(char * path)
{

	int i, j, k;

    char t_variables_filename[MAX_RECORD];
	sprintf(t_variables_filename,"%s/variables", path);
	remove(t_variables_filename);
	FILE * t_variables_file = fopen(t_variables_filename, "a");

	for (i=0; i < nb_sf_experiments; i++)
	{
		char t_summary_filename[MAX_RECORD];
		sprintf(t_summary_filename,"%s/summary_exp_%d", path, i);
		remove(t_summary_filename);
		FILE * t_summary_file = fopen(t_summary_filename, "a");




		Experiment * t_experiment = &(sf_experiments[i]);
		for (j=0; j < t_experiment->nb_conditions; j++)
		{
			ExperimentalCondition * t_condition = &(t_experiment->conditions[j]);

			// Here we just removed the old file
			for (k=0; k < t_condition->nb_observed_values; k++)
			{
				ExperimentalObservation * t_observation = &(t_condition->observed_values[k]);
				char t_filename[MAX_RECORD];
				sprintf(t_filename,"%s/exp_%d_cond_%d_var_%d", path, i, j, t_observation->variable_pos);
				remove(t_filename);
			}

			for (k=0; k < t_condition->nb_observed_values; k++)
			{
				ExperimentalObservation * t_observation = &(t_condition->observed_values[k]);

				char t_filename[MAX_RECORD];
				sprintf(t_filename,"%s/exp_%d_cond_%d_var_%d", path, i, j, t_observation->variable_pos);
				FILE * t_file = fopen(t_filename,"a");
				fprintf(t_file, "%.12g\t%.12g\t%.12g\n", t_observation->t, t_observation->value, t_observation->value_dev);
				fclose(t_file);

				if (t_observation->isSteadyState == 1)
				  fprintf(t_summary_file, "%d\t%d\t%d\t%s\n", j, k, t_observation->variable_pos, t_condition->name);

				fprintf(t_variables_file, "%d\t%d\t%d\t%s\n", i, j, k, t_observation->variable_name);

			}



		}
		fclose(t_summary_file);
	}
    fclose(t_variables_file);

}



void saveBestParams(char * path, int proc)
{
    char parameters_output[MAX_RECORD];
	sprintf(parameters_output, "%s/parameters_%d", path, proc);

	FILE * parameters = fopen(parameters_output,"w");

	int ii;
	for (ii=0; ii < sf_plist->size; ii++)
		fprintf(parameters, "%s : %.16g\n",
					sf_plist->array[ii].name,
					*(sf_plist->array[ii].param));

	fclose(parameters);
}

void saveBestTimecourse(char * path, int proc)
{
	int i_exp;
	for (i_exp = 0; i_exp < nb_sf_experiments; i_exp++)
	{
		Experiment * t_exp = &(sf_experiments[i_exp]);
		int i_cond;
		for (i_cond = 0; i_cond < t_exp->nb_conditions; i_cond++)
		{

			// Writing individual trajectories from OptimMappingObservables
			ExperimentalCondition * t_cond = &(t_exp->conditions[i_cond]);
			if (t_cond->nb_observed_values > 0)
			{
				IntegrationResult * t_res = sf_all_results[i_exp][i_cond];

				int i_obs;
				for (i_obs = 0; i_obs < t_cond->nb_observed_values; i_obs++)
				{

					char t_filename[MAX_RECORD];
					sprintf(t_filename,"%s/model_exp_%d_cond_%d_var_%d_proc_%d", path, i_exp, i_cond, t_cond->observed_values[i_obs].variable_pos, proc);
					remove(t_filename);

				}
				for (i_obs = 0; i_obs < t_cond->nb_observed_values; i_obs++)
				{
					char t_filename[MAX_RECORD];
					sprintf(t_filename,"%s/model_exp_%d_cond_%d_var_%d_proc_%d", path, i_exp, i_cond, t_cond->observed_values[i_obs].variable_pos, proc);

					FILE * f_res = fopen(t_filename,"r");
					if (f_res == NULL)
					{
						FILE * f_res = fopen(t_filename,"w");

						int t_obs;
						for (t_obs = 0; t_obs < t_res->nb_samples; t_obs++)
							fprintf(f_res, "%g\t%g\n", t_res->t[t_obs], t_res->y[t_cond->observed_values[i_obs].variable_id][t_obs]);

						fclose(f_res);
					} else fclose(f_res);
				}
			}
		}
	}
}


void saveBestResult(char * path, int proc)
{
	saveBestTimecourse(path, proc);
	saveBestParams(path, proc);
}