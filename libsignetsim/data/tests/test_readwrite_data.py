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

	This file is a test for writing the SigNetSim data structure into a NuML document

"""

from libsignetsim import Settings, Experiment

from unittest import TestCase
from os.path import join


class TestReadWriteData(TestCase):
	""" Tests high level functions """

	def testReadWriteData(self):

		# Initializing data structure
		experiment = Experiment("Ras-GTP, ERK1-2 quantifications")
		experiment.notes = "Elisa quantifications for RAS-GTP, Western blot quanfitication for ERK1-2"
		condition_0 = experiment.createCondition("Starved")

		condition_0.addInitialCondition(0, "FGF2", 0)
		condition_0.notes = "starved cells for 48h"
		condition_0.addObservation(0, "Total Ras-GTP", 40)
		condition_0.addObservation(60, "Total Ras-GTP", 40)
		condition_0.addObservation(180, "Total Ras-GTP", 40)
		condition_0.addObservation(300, "Total Ras-GTP", 40)
		condition_0.addObservation(900, "Total Ras-GTP", 40)
		condition_0.addObservation(1800, "Total Ras-GTP", 40)
		condition_0.addObservation(3600, "Total Ras-GTP", 40)

		condition_1 = experiment.createCondition("FGF2")
		condition_1.notes = "FGF2 treatment"
		condition_1.addInitialCondition(0, "FGF2", 333)

		condition_1.addObservation(0, "Total Ras-GTP", 40)
		condition_1.addObservation(60, "Total Ras-GTP", 92)
		condition_1.addObservation(180, "Total Ras-GTP", 77)
		condition_1.addObservation(300, "Total Ras-GTP", 333)
		condition_1.addObservation(900, "Total Ras-GTP", 222)
		condition_1.addObservation(1800, "Total Ras-GTP", 68)
		condition_1.addObservation(3600, "Total Ras-GTP", 60)

		experiment.writeNuMLToFile(join(Settings.tempDirectory, "data.xml"))

		experiment_imported = Experiment()
		experiment_imported.readNuMLFromFile(join(Settings.tempDirectory, "data.xml"))

		self.assertEqual(experiment_imported.getMaxTime(), 3600.0)
		self.assertEqual(experiment_imported.getTimes(), [0.0, 900.0, 1800.0, 300.0, 3600.0, 180.0, 60.0])
		self.assertEqual(experiment_imported.getTreatedVariables(), ['FGF2'])

		experiment_imported.writeNuMLToFile(join(Settings.tempDirectory, "data_copy.xml"))

	def testAttribute(self):

		experiment = Experiment("Ras-GTP, ERK1-2 quantifications")
		experiment.notes = "Elisa quantifications for RAS-GTP, Western blot quanfitication for ERK1-2"
		condition_0 = experiment.createCondition("Starved")

		condition_0.addInitialCondition(0, "fgf2", 0, name_attribute="id")
		condition_0.notes = "starved cells for 48h"
		condition_0.addObservation(0, "total_ras_gtp", 40, name_attribute="id")
		condition_0.addObservation(60, "total_ras_gtp", 40, name_attribute="id")
		condition_0.addObservation(180, "total_ras_gtp", 40, name_attribute="id")
		condition_0.addObservation(300, "total_ras_gtp", 40, name_attribute="id")
		condition_0.addObservation(900, "total_ras_gtp", 40, name_attribute="id")
		condition_0.addObservation(1800, "total_ras_gtp", 40, name_attribute="id")
		condition_0.addObservation(3600, "total_ras_gtp", 40, name_attribute="id")

		condition_1 = experiment.createCondition("fgf2")
		condition_1.notes = "FGF2 treatment"
		condition_1.addInitialCondition(0, "fgf2", 333, name_attribute="id")

		condition_1.addObservation(0, "total_ras_gtp", 40, name_attribute="id")
		condition_1.addObservation(60, "total_ras_gtp", 92, name_attribute="id")
		condition_1.addObservation(180, "total_ras_gtp", 77, name_attribute="id")
		condition_1.addObservation(300, "total_ras_gtp", 333, name_attribute="id")
		condition_1.addObservation(900, "total_ras_gtp", 222, name_attribute="id")
		condition_1.addObservation(1800, "total_ras_gtp", 68, name_attribute="id")
		condition_1.addObservation(3600, "total_ras_gtp", 60, name_attribute="id")

		experiment.writeNuMLToFile(join(Settings.tempDirectory, "data_with_ids.xml"))

		experiment_imported = Experiment()
		experiment_imported.readNuMLFromFile(join(Settings.tempDirectory, "data_with_ids.xml"))

		self.assertEqual(experiment_imported.getMaxTime(), 3600.0)
		self.assertEqual(experiment_imported.getTimes(), [0.0, 900.0, 1800.0, 300.0, 3600.0, 180.0, 60.0])
		self.assertEqual(experiment_imported.getTreatedVariables(), ['fgf2'])

		experiment_imported.writeNuMLToFile(join(Settings.tempDirectory, "data_with_ids_copy.xml"))
