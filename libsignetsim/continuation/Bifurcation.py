#!/usr/bin/env python
""" Bifurcation.py


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

from PyDSTool import args, Generator, ContClass
from libsignetsim.model.math.sympy_shortcuts import SympySymbol
from time import time
import mpld3


class Bifurcation(object):

    def __init__ (self, model):

        self.model = model
        self.modelInstance = model.parentDoc.getModelInstance()

        self.systemParameters = None
        self.system = None

        self.continuation = None
        self.continuationParameters = None


    def build(self):

        self.modelInstance.build()
        self.buildDS()
        self.buildCont()
        self.executeCont()
        self.plotCont()

    def makeSubs(self, formula):

        t_atoms = formula.atoms(SympySymbol)
        t_subs = {}
        for atom in t_atoms:
            t_var = self.modelInstance.listOfVariables.getBySbmlId(str(atom))
            t_value = t_var.value.getInternalMathFormula()
            if len(t_value.atoms(SympySymbol)) > 0:
                t_value = self.makeSubs(t_value)
            t_subs.update({atom:t_value})

        return formula.subs(t_subs)


    def buildDS(self):


        parameters = {}
        variables = {}
        odes = {}
        for variable in self.modelInstance.listOfVariables.values():
            if variable.isConstant():
                t_symbol = str(variable.symbol.getInternalMathFormula())

                t_raw_value = variable.value.getInternalMathFormula()
                if len(t_raw_value.atoms(SympySymbol)) > 0:
                    t_raw_value = self.makeSubs(t_raw_value)
                t_value = float(t_raw_value)

                parameters.update({t_symbol:t_value})

            if variable.isDerivative():
                t_symbol = variable.symbol.getInternalMathFormula()

                t_raw_value = variable.value.getInternalMathFormula()
                if len(t_raw_value.atoms(SympySymbol)) > 0:
                    t_raw_value = self.makeSubs(t_raw_value)
                t_value = float(t_raw_value)

                variables.update({str(t_symbol):t_value})

                t_vars = [var.getInternalMathFormula() for var in self.modelInstance.ODE_vars]
                t_index = t_vars.index(variable.symbol.getInternalMathFormula())
                t_ode = self.modelInstance.ODEs[t_index].getInternalMathFormula()
                odes.update({str(t_symbol):str(t_ode)})
                # print [var.getInternalMathFormula() for var in self.modelInstance.ODE_vars]

        print parameters
        print variables
        print odes

        self.systemParameters = args(name=self.modelInstance.getSbmlId())
        self.systemParameters.pars = parameters
        self.systemParameters.varspecs = odes
        self.systemParameters.ics = variables
        self.system = Generator.Vode_ODEsystem(self.systemParameters)



        # pars = {'k1': 0.00018, 'd1': 3, 'k2': 0.00017, 'd2': 0.4, 'kcat3': 2, 'K3m': 1640, 'kcat4': 0.003, 'K4m': 9120, 'kcat5': 0.1, 'K5m': 107, 'kcat6': 0.01, 'K6m': 0.0051, 'k7': 0, 'd7': 1, 'y1': 100, 'y3': 100, 'tras': 1000, 'tsos': 200}
        #
        # icdict = {'u5': 988.1112, 'RasGTP': 11.8888, 'u9': 0, 'u11': 0}
        #
        # # Set up model
        # u5str =  '-k1*u11*u5 + d1*(tras-u5-RasGTP-u9) - kcat3*(u9*u5)/(K3m+u5) - kcat4*((tras-u5-RasGTP-u9)*u5)/(K4m+u5) + kcat5*(y1*RasGTP)/(K5m+RasGTP) - kcat6*(y3*u5)/(K6m+u5)'
        # #u6str =   'k1*u11*u5 - d1*u6' u6=(tras-u5-RasGTP-u9)
        # RasGTPstr =  '-k2*u11*RasGTP + d2*u9 + kcat3*(u9*u5)/(K3m+u5) + kcat4*((tras-u5-RasGTP-u9)*u5)/(K4m+u5) - kcat5*(y1*RasGTP)/(K5m+RasGTP) + kcat6*(y3*u5)/(K6m+u5)'
        # u9str =   'k2*u11*RasGTP - d2*u9'
        # u11str = '-k1*u11*u5 + d1*(tras-u5-RasGTP-u9) - k2*u11*RasGTP + d2*u9 - d7*u11 + k7*(tsos-u11-(tras-u5-RasGTP-u9)-u9)'
        # #u12str =  'd7*u11-k7*u12' u12=(tsos-u11-u6-u9)
        #
        # DSargs = args(name='SOSGEFRas')
        # DSargs.pars = pars
        # #DSargs.varspecs = {'u5': u5str, 'u6': u6str, 'RasGTP': RasGTPstr, 'u9': u9str, 'u11': u11str, 'u12': u12str}
        # DSargs.varspecs = {'u5': u5str, 'RasGTP': RasGTPstr, 'u9': u9str, 'u11': u11str}
        # DSargs.ics = icdict
        # testDS = Generator.Vode_ODEsystem(DSargs)
        #


    def buildCont(self):

        self.continuation = ContClass(self.system)

        self.continuationParameters = args(name='EQ1', type='EP-C')
        self.continuationParameters.freepars = ['ras_activation_by_gef_cat']
        self.continuationParameters.StepSize = 0.001
        self.continuationParameters.MaxNumPoints = 1500
        self.continuationParameters.MaxStepSize = 1
        self.continuationParameters.MinStepSize = 0.00001
        self.continuationParameters.LocBifPoints = 'All'
        self.continuationParameters.verbosity = 1
        self.continuationParameters.SaveEigen = True

        self.continuation.newCurve(self.continuationParameters)

        # # Set up continuation class
        # PyCont = ContClass(testDS)
        #
        # PCargs = args(name='EQ1', type='EP-C')
        # PCargs.freepars = ['k7']
        # PCargs.StepSize = 0.1
        # PCargs.MaxNumPoints = 1500
        # PCargs.MaxStepSize = 1
        # PCargs.MinStepSize = 0.01
        # PCargs.LocBifPoints = 'All'
        # PCargs.verbosity = 2
        # PCargs.SaveEigen = True
        # PyCont.newCurve(PCargs)
        #


    def executeCont(self):

        print('Computing curve...')
        start = time()
        self.continuation['EQ1'].forward()
        print('done in %.3f seconds!' % (time()-start))

        # PyCont['EQ1'].forward()
        #


    def plotCont(self):

        # Plot
        self.continuation.plot.setLabels('')
        self.continuation.plot.toggleLabels(visible="on")
        self.continuation.display(('ras_activation_by_gef_cat','ras_gtp'), stability=True)
        #PyCont.plot.setLegends('HAHAHA')
        #PyCont.plot.toggleLegends(visible="on")
        #plt.show()
        #plt.savefig('foo.png')
        mpld3.show()
        # print mpld3.save_html()
        #
        # # Plot
        # PyCont.plot.setLabels('')
        # PyCont.plot.toggleLabels(visible="on")
        # PyCont.display(('k7','RasGTP'), stability=True)
        # #PyCont.plot.setLegends('HAHAHA')
        # #PyCont.plot.toggleLegends(visible="on")
        # #plt.show()
        # #plt.savefig('foo.png')
        # mpld3.show()
