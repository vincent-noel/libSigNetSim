#!/usr/bin/env python
""" SteadyStatesSimulation.py


    This file ...


    Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from libsignetsim.simulation.Simulation import Simulation

from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ExperimentalData import ExperimentalData
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.Experiment import Experiment as Experiment

from libsignetsim.settings.Settings import Settings

from os.path import join, isfile
from time import clock


class SteadyStatesSimulation(Simulation):

    SIM_DONE            =   10
    SIM_TODO            =   11

    def __init__(self,
                 list_of_models=[],
                 species_input=None,
                 list_of_initial_values=[],
                 time_max=Settings.steadyStatesMaxTime,
                 keep_files=Settings.simulationKeepFiles):

        self.listOfInitialValues = list_of_initial_values
        self.experiment = None
        self.generateExperiment(species_input, list_of_initial_values)

        Simulation.__init__(self,
            list_of_models=list_of_models,
            time_min=0,
            list_samples=[0.0, time_max*1.1],
            experiment=self.experiment,
            keep_files=keep_files
        )

    def generateExperiment(self, species_input, list_of_initial_values):

        if len(list_of_initial_values) > 0:

            self.experiment = Experiment()
            self.experiment.name = "SteadyState"
            for initial_value in list_of_initial_values:

                t_condition = ExperimentalCondition()
                list_of_experimental_data = ListOfExperimentalData()
                list_of_input_data = ListOfExperimentalData()

                t_experimental_data = ExperimentalData()

                t_experimental_data.name = species_input.getSbmlId()
                t_experimental_data.t = 0
                t_experimental_data.value = initial_value

                list_of_input_data.add(t_experimental_data)

                t_condition.read(list_of_input_data, list_of_experimental_data)

                self.experiment.addCondition(t_condition)

    def run(self):

        start = clock()
        self.writeSimulationFiles()
        mid = clock()

        if Settings.verboseTiming >= 1:
            print "> Files written in %.2fs" % (mid-start)

        self.runSimulation(steady_states=True)
        self.loadSimulationResults()

        if not self.keepFiles:
            self.cleanTempDirectory()

        stop = clock()

        if Settings.verboseTiming >= 1:
            print "> Simulation executed in %.2fs" % (stop-start)

    def loadSimulationResults(self):

        t_model = self.listOfModels[0]
        self.rawData = {}

        for variable in t_model.listOfVariables.values():
            self.rawData.update({variable.getSbmlId(): []})

        if len(self.listOfInitialValues) > 0:

            for i_initial_values, _ in enumerate(self.listOfInitialValues):

                t_file = join(
                    self.getTempDirectory(),
                    Settings.C_simulationResultsDirectory,
                    "results_0_%d" % i_initial_values
                )

                if isfile(t_file):

                    resultsFile = open(t_file, "r")

                    for line in resultsFile:
                        data = line.split()

                        for variable in t_model.listOfVariables.values():
                            t_array = self.rawData[variable.getSbmlId()]
                            t_array.append(float(data[variable.getPos()]))
                            self.rawData.update({variable.getSbmlId(): t_array})

                    resultsFile.close()

        else:
            t_file = join(
                self.getTempDirectory(),
                Settings.C_simulationResultsDirectory,
                "results_0"
            )

            if isfile(t_file):

                resultsFile = open(t_file, "r")

                for line in resultsFile:
                    data = line.split()

                    for variable in t_model.listOfVariables.values():
                        t_array = self.rawData[variable.getSbmlId()]
                        t_array.append(float(data[variable.getPos()]))
                        self.rawData.update({variable.getSbmlId(): t_array})

                resultsFile.close()
