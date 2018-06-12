#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)
#
# This file is part of libSigNetSim.
#
# libSigNetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libSigNetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libSigNetSim.  If not, see <http://www.gnu.org/licenses/>.

"""

    This file ...

"""
from __future__ import print_function

from libsignetsim.simulation.Simulation import Simulation
from libsignetsim.data.Experiment import Experiment

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

                t_condition = self.experiment.createCondition()
                t_condition.addInitialCondition(
                    t=0, name=species_input.getSbmlId(),
                    value=initial_value, name_attribute="id"
                )

    def run(self, timeout=None):

        start = clock()
        self.writeSimulationFiles()
        mid = clock()

        if Settings.verboseTiming >= 1:
            print("> Files written in %.2fs" % (mid-start))

        self.runSimulation(steady_states=True, timeout=timeout)
        self.loadSimulationResults()

        if not self.keepFiles:
            self.cleanTempDirectory()

        stop = clock()

        if Settings.verboseTiming >= 1:
            print("> Simulation executed in %.2fs" % (stop-start))

    def loadSimulationResults(self):

        t_model = self.listOfModels[0]
        self.rawData = {}

        for variable in t_model.listOfVariables:
            self.rawData.update({variable.getSbmlId(): []})

        if len(self.listOfInitialValues) > 1:

            for i_initial_values, _ in enumerate(self.listOfInitialValues):

                t_file = join(
                    self.getTempDirectory(),
                    Settings.C_simulationResultsDirectory,
                    "results_0_%d" % i_initial_values
                )

                if isfile(t_file):
                    self.readFile(t_file)

        else:
            t_file = join(
                self.getTempDirectory(),
                Settings.C_simulationResultsDirectory,
                "results_0"
            )

            if isfile(t_file):
                self.readFile(t_file)

    def readFile(self, filename):
        resultsFile = open(filename, "r")
        variables = []
        for i, line in enumerate(resultsFile):
            data = line.split()

            if i == 0:
                variables = data
            else:
                for i_value, value in enumerate(data):
                    f_value = float(value)
                    array = self.rawData[variables[i_value]]
                    array.append(f_value)
                    self.rawData.update({variables[i_value]: array})

        resultsFile.close()
