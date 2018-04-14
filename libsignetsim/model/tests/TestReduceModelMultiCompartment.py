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

from libsignetsim import Model, KineticLaw

from unittest import TestCase


class TestReduceModel(TestCase):
	""" Tests high level functions """


	def testReduceModel(self):

		model = Model()
		cytosol = model.listOfCompartments.new("Cytosol")
		membrane = model.listOfCompartments.new("Membrane")

		ras_cytosol = model.listOfSpecies.new("Ras (cytosol)", cytosol, 200)
		ras_membrane = model.listOfSpecies.new("Ras (membrane)", membrane, 50)

		kf = model.listOfParameters.new("To cytosol")
		kr = model.listOfParameters.new("To membrane")

		r = model.listOfReactions.new("Ras transport")
		r.listOfReactants.add(ras_cytosol)
		r.listOfProducts.add(ras_membrane)

		r.setKineticLaw(KineticLaw.MASS_ACTION, reversible=True, parameters=[kf, kr])

		# print("> Model")
		model.build()
		# model.pprint()

		# print("\n> Stoichiometric matrix")
		model.stoichiometryMatrix.build()
		# model.stoichiometryMatrix.pprint()

		# print("\n> Conservation laws")
		model.listOfConservationLaws.build()
		# model.listOfConservationLaws.pprint()

		# print("\n> Reduced model")
		model.asymetricModel.build()
		# model.asymetricModel.pprint()

