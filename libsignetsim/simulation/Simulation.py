#!/usr/bin/env python
""" Simulation.py


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

from libsignetsim.simulation.CWriterSimulation import CWriterSimulation
from libsignetsim.simulation.SimulationException import SimulationException
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.settings.Settings import Settings
# from libsignetsim.model.Model import Model
from libsignetsim.model.SbmlDocument import SbmlDocument
from time import time, clock
from os import mkdir, setpgrp, getcwd
from os.path import join, isfile, exists, getsize
from subprocess import call
from shutil import rmtree


class Simulation(CWriterSimulation):


    SIM_SUCCESS         =    0
    SIM_FAILURE         =   -1

    SIM_DONE            =   10
    SIM_TODO            =   11


    def __init__ (self,
                    list_of_models=[],
                    list_of_initial_values=None,
                    experiment=None,
                    timeMin=Settings.simulationTimeMin,
                    timeMax=Settings.simulationTimeMax,
                    ech=Settings.simulationTimeEch,
                    abs_tol=Settings.defaultAbsTol,
                    rel_tol=Settings.defaultRelTol,
                    keep_files=Settings.simulationKeepFiles):

        self.keepFiles = keep_files#Settings.simulationKeepFiles
        self.sessionId = None
        self.simulationId = int(time()*1000)

        CWriterSimulation.__init__(self, list_of_models=list_of_models,
                        list_of_initial_values=list_of_initial_values,
                        experiment=experiment,
                        timeMin=timeMin,
                        timeMax=timeMax,
                        ech=ech,
                        abs_tol=abs_tol, rel_tol=rel_tol)
        self.listOfModels = list_of_models

        self.__simulationDone = self.SIM_TODO

        self.listOfData = None
        self.listOfData_v2 = None
        self.rawData = None

        self.nbConditions = 0
        # for experiment in self.listOfExperiments:
        if experiment is not None:
            self.nbConditions = len(experiment.listOfConditions)

    def restore(self, session_id, simulation_id):

        self.sessionId = session_id
        self.simulationId = simulation_id
        self.restoreModels()

    def restoreModels(self):

        if self.sessionId is not None and self.simulationId is not None:
            if isfile(join(self.getTempDirectory(), "model.sbml")):
                print "restoring single model"
                self.loadSbmlModel(join(self.getTempDirectory(), "model.sbml"))


            elif isfile(join(self.getTempDirectory(), "model_0.sbml")):
                print "restoring multiple model: not implemented yet"



    # def loadSbmlModel(self, filename):
    #
    #     document = SbmlDocument()
    #     document.readSbml(filename)
    #     self.listOfModels.append(document.model)


    def loadSbmlModel_v2(self, filename, modelDefinition=False):

        document = SbmlDocument()
        document.readSbml(filename)
        if modelDefinition:
            return document.model
        else:
            return document.getModelInstance()


    def getTempDirectory(self):
        if self.sessionId is None:
            return join(Settings.tempDirectory,
                                "simulation_%s/" % str(self.simulationId))
        else:
            return join(self.sessionId,
                                ("simulation_%s/" % str(self.simulationId)))


    def isDone(self):
        return self.__simulationDone == self.SIM_DONE


    def cleanTempDirectory(self):
        rmtree(self.getTempDirectory())


    def writeSimulationFiles(self):


        mkdir(self.getTempDirectory())
        # self.writeModelsFile()
        CWriterSimulation.writeSimulationFiles(self)

        res_path = join(self.getTempDirectory(),
                                # Settings.C_simulationDirectory,
                                Settings.C_simulationResultsDirectory)

        if not exists(res_path):
            mkdir(res_path)

    def writeModelsFile(self):
        if len(self.listOfModels) > 1:
            for i_model, model in enumerate(self.listOfModels):
                model.writeSbml(join(self.getTempDirectory(),
                                                "model_%d.sbml" % i_model))

        else:
            self.listOfModels[0].writeSbml(join(self.getTempDirectory(),
                                                        "model.sbml"))



    def __compile__(self, nb_procs=4):


        if self.nbConditions == 0 or nb_procs <= 1:
            cmd_comp = "make -C %s sim-serial" % self.getTempDirectory()
        else:
            cmd_comp = "make -C %s sim-parallel" % self.getTempDirectory()
        # else:
        #     cmd_comp = "make -C %s sim-serial" % self.getTempDirectory()

        res_comp = call(cmd_comp,
                        stdout=open("%sout_comp" % self.getTempDirectory(),"w"),
                        stderr=open("%serr_comp" % self.getTempDirectory(),"w"),
                        shell=True,preexec_fn=setpgrp,close_fds=True)

        if (res_comp != 0
            or getsize(self.getTempDirectory() + "err_comp") > 0):


            if Settings.verbose:
                print "-"*40 + "\n"
                print "> Error during file compilation :"
                f_err_comp = open(self.getTempDirectory() + "err_comp", 'r')
                for line in f_err_comp:
                    print line
                print "-"*40 + "\n"
                f_err_comp.close()

            raise SimulationException(
                SimulationException.COMP_ERROR,
                "Error during file simulation (%d)" % res_comp
            )
            return self.SIM_FAILURE

        else:
            return self.SIM_SUCCESS


    def __execute__(self, nb_procs=4, steady_states=False):

        present_dir = getcwd()

        flags = ""
        if steady_states:
            flags += "-s "


        if self.nbConditions == 0 or nb_procs <= 1:
            cmd_sim = "cd %s; ./sim-serial %s; cd %s" % (
                    self.getTempDirectory(),
                    flags, present_dir)

        else:
            cmd_sim = "cd %s; mpirun -np %d ./sim-parallel %s; cd %s" % (
                    self.getTempDirectory(),
                    nb_procs, flags,
                    present_dir)

        res_sim = call(cmd_sim,
                      stdout=open("%sout_sim" % self.getTempDirectory(),"w"),
                      stderr=open("%serr_sim" % self.getTempDirectory(),"w"),
                      shell=True,preexec_fn=setpgrp,close_fds=True)

        if res_sim != 0 or getsize(self.getTempDirectory() + "err_sim") > 0:

            raise SimulationException(
                        SimulationException.SIM_ERROR,
                        "Error during file simulation (%d, %d)" % (
                                res_sim,
                                getsize(self.getTempDirectory() + "err_sim")))

            if Settings.verbose:
                print "> Error during file simulation (%d, %d)" % (
                        res_sim,
                        getsize(self.getTempDirectory() + "err_sim"))

            return self.SIM_FAILURE

        else:
            if Settings.verbose:
                print "-"*40 + "\n"
                print "> Execution returned : \n"
                f_out_sim = open(self.getTempDirectory() + "out_sim", 'r')
                for line in f_out_sim:
                    print line
                print "-"*40 + "\n"
                f_out_sim.close()

            return self.SIM_SUCCESS


    def runSimulation(self, progress_signal=None, steady_states=False, nb_procs=4):

        start = clock()
        self.__compile__(nb_procs=nb_procs)

        mid = clock()

        if Settings.verbose:
            print ">> Compilation executed in %.2fs" % (mid-start)

        self.__execute__(nb_procs=nb_procs, steady_states=steady_states)
        end = clock()

        if Settings.verbose:
            print ">> Simulation executed in %.2fs" % (end-mid)


        self.__simulationDone = self.SIM_DONE
        return self.SIM_SUCCESS



    def loadSimulationResults(self):

        self.rawData = []
        t_filename = self.getTempDirectory() + Settings.C_simulationResultsDirectory + "results_0"
        t_filename_2 = t_filename + "_0"
        if isfile(t_filename):
            (t, y) = self.readResultFile(t_filename)
            self.rawData.append((t,y))

        elif isfile(t_filename_2):
            ind = 0
            while(isfile(t_filename + ("_%d" % ind))):
                (t, y) = self.readResultFile(t_filename + ("_%d" % ind))
                self.rawData.append((t,y))
                ind += 1

    def readResultFile(self, filename):

        resultsFile = open(filename, 'r')

        t = []
        trajs = {}
        for variable in self.listOfModels[0].listOfVariables.keys():
            trajs.update({variable:[]})

        for line in resultsFile:
            data = line.split()
            t.append(float(data[0]))

            for key, variable in self.listOfModels[0].listOfVariables.iteritems():
                t_sample = float(data[1+variable.getPos()])
                trajs[key].append(t_sample)

        resultsFile.close()

        # print self.listOfModels[0].listOfVariables.keys()
        # The simulations only deals with amounts, but some species are
        # Concentrations. So we need to transform them back
        for key, variable in self.listOfModels[0].listOfVariables.iteritems():
            if variable.isConcentration():
                # print "I'm a concentration !! %s" % variable.getSbmlId()
                t_traj = trajs[key]
                # print t_traj
                t_comp_traj = trajs[variable.getCompartment().getSbmlId()]
                res_traj = []

                for i, point in enumerate(t_traj):
                    # print t_comp_traj[i]
                    res_traj.append(point/t_comp_traj[i])
                trajs.update({key:res_traj})

        return (t, trajs)


    def getRawData(self):
        if self.__simulationDone == self.SIM_DONE:
            return self.rawData


    def writeOutput(self, output_file):

        if self.listOfData is not None:
            results_file = open(output_file, 'w')
            (traj_times, traj_species, traj_params, traj_compartments, _) = self.listOfData

            # Writing header
            line = "time"
            for species in self.listOfModels[0].listOfSpecies.values():
                line += ",%s" % species.sbmlId

            for compartment in self.listOfModels[0].listOfCompartments.values():
                line += ",%s" % compartment.sbmlId

            for parameter in self.listOfModels[0].listOfParameters.values():
                line += ",%s" % parameter.sbmlId



            results_file.write(line + "\n")


            # Writing content
            for i_t, t_time in enumerate(traj_times):
                line = "%.14f" % t_time

                for i_species, species in enumerate(self.listOfModels[0].listOfSpecies.values()):
                    line += ",%.14f" % traj_species[i_species][i_t]

                for i_compartment, compartment in enumerate(self.listOfModels[0].listOfCompartments.values()):
                    line += ",%.14f" % traj_compartments[i_compartment][i_t]

                for i_parameter, parameter in enumerate(self.listOfModels[0].listOfParameters.values()):
                    line += ",%.14f" % traj_params[i_parameter][i_t]


                results_file.write(line + "\n")

            results_file.close()
