#!/usr/bin/env python
""" SbmlTestCaseSimulation.py


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

from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.settings.Settings import Settings
from libsignetsim.model.math.MathFormula import MathFormula

from os.path import join, expanduser

class SbmlTestCaseSimulation(TimeseriesSimulation):

    def __init__ (self, case_id, sbml_level, sbml_version, test_export=False, keep_files=Settings.simulationKeepFiles):

        self.caseId = case_id
        self.sbmlLevel = sbml_level
        self.sbmlVersion = sbml_version
        self.testExport = test_export
        self.model = None
        self.absTol = 1e-8
        self.relTol = 1e-6
        self.sbmlIdToPlot = []
        self.sbmlIdToPlotAmount = []
        self.sbmlIdToPlotConcentrations = []

        self.loadSBMLTestSuiteSettings()
        self.loadTestCaseModel()

        TimeseriesSimulation.__init__(self,
                                        list_of_models=[self.model],
                                        time_min=self.timeMin,
                                        time_max=self.timeMax,
                                        time_ech=self.timeEch,
                                        abs_tol=self.absTol,
                                        rel_tol=self.relTol,
                                        keep_files=keep_files)


    def run(self):

        TimeseriesSimulation.run(self)
        self.writeSbmlTestOutput()



    def loadTestCaseModel(self):


        if self.testExport:
            self.model = self.loadSbmlModel_v2(self.getModelFilename(), modelDefinition=True)
            t_filename = self.getTemporaryModelFilename()
            # t_document = SbmlDocument(self.model)
            # t_document.writeSbml(t_filename)
            t_document = self.model.parentDoc
            t_document.writeSbml(t_filename)

            self.model = self.loadSbmlModel_v2(t_filename)
        else:
            self.model = self.loadSbmlModel_v2(self.getModelFilename())



    def getModelFolder(self):

        return join(
            expanduser('~'),
            ".test-suite/cases/semantic/%s/" % (self.caseId)
        )



    def getModelFilename(self):

        return join(
            expanduser('~'),
            ".test-suite/cases/semantic/%s/%s-sbml-l%sv%s.xml" % (
                self.caseId, self.caseId, self.sbmlLevel, self.sbmlVersion)
        )


    def getSettingsFilename(self):

        return join(
            expanduser('~'),
            ".test-suite/cases/semantic/%s/%s-settings.txt" % (
                self.caseId, self.caseId)
        )


    def getResultsFilename(self):
        return join(expanduser('~'), ".test-suite/test-suite-results/%s.csv" % self.caseId)

    def getTemporaryModelFilename(self):
        return join(expanduser('~'), ".test-suite/test-suite-results/%s.xml" % self.caseId)


    def loadSBMLTestSuiteSettings(self):

        settings = open(self.getSettingsFilename(), 'r')

        for line in settings:

            if line.startswith("start:"):
                res_split = line.split(":", 2)
                self.timeMin = float(res_split[1].strip())

            if line.startswith("duration:"):
                res_split = line.split(":", 2)
                self.timeMax = float(res_split[1].strip()) + self.timeMin

            if line.startswith("steps:"):
                res_split = line.split(":", 2)
                self.timeEch = (self.timeMax - self.timeMin)/int(res_split[1].strip())

            if line.startswith("variables:"):
                res_split = line.split(":", 2)
                if len(res_split[1].strip()) > 0:
                    res_split = res_split[1].strip().split(",")
                    for t_var in res_split:
                        self.sbmlIdToPlot.append(t_var.strip())

            if line.startswith("amount:"):
                res_split = line.split(":", 2)
                if len(res_split[1].strip()) > 0:
                    res_split = res_split[1].strip().split(",")
                    for t_var in res_split:
                        self.sbmlIdToPlotAmount.append(t_var.strip())

            if line.startswith("concentration:"):
                res_split = line.split(":", 2)
                if len(res_split[1].strip()) > 0:
                    res_split = res_split[1].strip().split(",")
                    for t_var in res_split:
                        self.sbmlIdToPlotConcentrations.append(t_var.strip())

            if line.startswith("absolute:"):
                res_split = line.split(":", 2)
                self.absTol = min(float(res_split[1].strip())/1000, 1e-8)

            if line.startswith("relative:"):
                res_split = line.split(":", 2)
                self.relTol = min(float(res_split[1].strip())/1000, 1e-6)


    def writeSbmlTestOutput(self,):

        # print "sbml id to plot"
        # print self.sbmlIdToPlot
        #
        # print "\nsbml id to plot concentrations"
        # print self.sbmlIdToPlotConcentrations
        #
        # print "\nsbml id to plot amount"
        # print self.sbmlIdToPlotAmount


        if self.rawData is not None:
            results_file = open(self.getResultsFilename(), 'w')
            (traj_times, trajs) = self.rawData[0]

            # Writing header
            line = "time"

            for sbml_id in self.sbmlIdToPlot:
                if sbml_id in self.listOfModels[0].listOfVariables.keys():
                    t_var = self.listOfModels[0].listOfVariables[sbml_id]
                    line += ",%s" % t_var.getSbmlId()

            results_file.write(line + "\n")

            for i_t, t_time in enumerate(traj_times):
                line = "%.14f" % t_time

                for sbml_id in self.sbmlIdToPlot:
                    if sbml_id in self.listOfModels[0].listOfVariables.keys():
                        t_var = self.listOfModels[0].listOfVariables[sbml_id]
                        if t_var.isSpecies():

                            t_compartment = t_var.getCompartment()
                            # Here we ask for the concentration but it's declared an amount
                            if t_var.getSbmlId() in self.sbmlIdToPlotConcentrations and t_var.hasOnlySubstanceUnits:
                                line += ",%.14f" % (trajs[t_var.getSbmlId()][i_t]/trajs[t_compartment.getSbmlId()][i_t])

                            # Here we ask for an amout but it's declared a concentration
                            elif t_var.getSbmlId() in self.sbmlIdToPlotAmount and not t_var.hasOnlySubstanceUnits:
                                # print "Yeah we need to plot the amount (%s)= %.5g" % (t_var.getSbmlId(),(trajs[t_var.getSbmlId()][i_t]*trajs[t_compartment.getSbmlId()][i_t]) )
                                line += ",%.14f" % (trajs[t_var.getSbmlId()][i_t]*trajs[t_compartment.getSbmlId()][i_t])

                            else:
                                line += ",%.14f" % trajs[t_var.getSbmlId()][i_t]
                        else:
                            line += ",%.14f" % trajs[t_var.getSbmlId()][i_t]

                results_file.write(line + "\n")

            results_file.close()
