#!/usr/bin/env python
""" __main__.py


    This file is made to be called by the SBML Test Suite


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

from libsignetsim.simulation.SbmlTestCaseSimulation import SbmlTestCaseSimulation
from libsignetsim.model.ModelException import ModelException
from libsignetsim.simulation.SimulationException import SimulationException

from libsignetsim.settings.Settings import Settings

from sys import argv
from optparse import OptionParser

import traceback

class __main__():

    def __init__(self):

        if len(argv) > 1:
            self.readArgs(argv)


    def readArgs(self, argv):

        parser = OptionParser()

        parser.add_option("-v", "--verbose", dest="verbose", help="Verbose mode", nargs=0)

        parser.add_option("-k", "--keepfiles", dest="keep_files", help="Keep temporary files", nargs=0)

        parser.add_option("-c", "--test-conformity", dest="test_conformity", nargs=3,
                          help="Generate output for specified case. To use with Sbml Test Suite", metavar="CASE LEVEL VERSION")

        parser.add_option("-e", "--test-export", dest="test_export", nargs=3,
                          help="Test sbml output for specified case. To use with Sbml Test Suite", metavar="CASE LEVEL VERSION")

        (options, _) = parser.parse_args()

        if options.verbose is not None:
            Settings.verbose = 1

        if options.keep_files is not None:
            Setting.simulationKeepFiles = True


        if options.test_conformity is not None:

            try:
                simulation = SbmlTestCaseSimulation(
                                options.test_conformity[0],
                                options.test_conformity[1],
                                options.test_conformity[2],
                                test_export=False)

                simulation.run()

            except ModelException as e:
                print "Caught %s" % str(type(e))
                print "> %s" % e.message
                traceback.print_exc()

            except SimulationException as e:
                print "Caught %s" % str(type(e))
                print "> %s" % e.message
                traceback.print_exc()


        elif options.test_export is not None:

            try:
                simulation = SbmlTestCaseSimulation(
                                options.test_export[0],
                                options.test_export[1],
                                options.test_export[2],
                                test_export=True)
                simulation.run()

            except ModelException as e:
                print "Caught %s" % str(type(e))
                print "> %s" % e.message
                traceback.print_exc()

            except SimulationException as e:
                print "Caught %s" % str(type(e))
                print "> %s" % e.message
                traceback.print_exc()



if __name__ == "__main__":
    __main__()
