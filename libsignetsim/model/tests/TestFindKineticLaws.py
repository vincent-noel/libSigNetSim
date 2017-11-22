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

	Testing the research for conservation laws, and the subsequent reduction

"""

from libsignetsim import SbmlDocument, KineticLaw
from unittest import TestCase
from os.path import join, dirname
from os import getcwd


class TestFindKineticLaws(TestCase):
	""" Tests high level functions """


	def testFindKineticLaws(self):

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(testfiles_path, "modelqlzB7i.xml"))

		sbml_model = sbml_doc.getModelInstance()



		results_kinetic_law = [
			KineticLaw.MASS_ACTION, KineticLaw.MASS_ACTION, KineticLaw.MICHAELIS, KineticLaw.MICHAELIS,
			KineticLaw.MICHAELIS, KineticLaw.MICHAELIS, KineticLaw.MASS_ACTION, KineticLaw.MICHAELIS,
			KineticLaw.MASS_ACTION, KineticLaw.MICHAELIS, KineticLaw.MICHAELIS, KineticLaw.MICHAELIS,
			KineticLaw.MICHAELIS, KineticLaw.MICHAELIS, KineticLaw.MICHAELIS, KineticLaw.MICHAELIS,
			KineticLaw.MICHAELIS, KineticLaw.MICHAELIS, KineticLaw.MICHAELIS, KineticLaw.MICHAELIS,
			KineticLaw.MICHAELIS, KineticLaw.MASS_ACTION,
		]


		results_reversibility = [
			True, True, False, False, False, False, False, False, True, False, False, False, False, False,
			False, False, False, False, False, False, False, True,
		]

		for i, reaction in enumerate(sbml_model.listOfReactions.values()):
			self.assertEqual(reaction.getReactionType(), results_kinetic_law[i])
			self.assertEqual(reaction.kineticLaw.reversible, results_reversibility[i])


