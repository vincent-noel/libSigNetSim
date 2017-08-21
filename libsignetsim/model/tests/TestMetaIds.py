#!/usr/bin/env python
""" TestMetaIds.py


	Testing the reading/writing of miriam annotations of the model


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

from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.uris.URI import URI
from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir, getcwd

from libsignetsim.settings.Settings import Settings

class TestMetaIds(TestCase):
	""" Tests high level functions """


	def testMetaIds(self):

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")

		sbml_doc = SbmlDocument()
		model = sbml_doc.getModelInstance()

		s1 = model.listOfSpecies.new("A")
		s2 = model.listOfSpecies.new("B")
		s3 = model.listOfSpecies.new("C")


		# Writing with defaults meta ids
		sbml_doc.writeSbmlToFile(join(testfiles_path, "test_meta_ids_1.xml"))

		# Forcing s2 to meta id '_meta_id_0_', which force the renaming of the existing one (the model)
		s2.setMetaId("_meta_id_0_", force=True)

		self.assertEqual(s2.getMetaId(), "_meta_id_0_")
		self.assertEqual(model.getMetaId(), "_meta_id_15_")

		# Now forcing the model to have no defined meta id.
		model.unsetMetaId()
		self.assertEqual(model.getMetaId(), None)

		sbml_doc.writeSbmlToFile(join(testfiles_path, "test_meta_ids_2.xml"))

		# During reading, compartment should get the default '_meta_id_0_' meta id. But when reading s2,
		# it should be renamed

		sbml_doc_2 = SbmlDocument()
		sbml_doc_2.readSbmlFromFile(join(testfiles_path, "test_meta_ids_2.xml"))
		model_2 = sbml_doc_2.getModelInstance()

		# for key, obj in model_2.listOfSbmlObjects.items():
		# 	print "%s:%s (%s)" % (key, obj.getMetaId(), type(obj))

		s2 = model_2.listOfSpecies.getByName("B")
		self.assertEqual(s2.getMetaId(), "_meta_id_0_")
		self.assertEqual(model_2.getMetaId(), "_meta_id_16_")

		sbml_doc_2.writeSbmlToFile(join(testfiles_path, "test_meta_ids_3.xml"))

		sbml_doc_3 = SbmlDocument()
		sbml_doc_3.readSbmlFromFile(join(testfiles_path, "test_meta_ids_3.xml"))
		model_3 = sbml_doc_3.getModelInstance()

		s2 = model_3.listOfSpecies.getByName("B")
		self.assertEqual(s2.getMetaId(), "_meta_id_0_")
		self.assertEqual(model_3.getMetaId(), "_meta_id_16_")
