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

	Testing the reading/writing of miriam annotations of the model

"""

from libsignetsim import SbmlDocument, Settings
from libsignetsim.uris.URI import URI

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir, getcwd


class TestAnnotation(TestCase):
	""" Tests high level functions """


	def testReadWriteModel(self):

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(testfiles_path, "BIOMD0000000001.xml"))
		sbml_doc.writeSbmlToFile(join(Settings.tempDirectory, "BIOMD0000000001.xml"))
		sbml_doc.readSbmlFromFile(join(testfiles_path, "BIOMD0000000001.xml"))

		sbml_model = sbml_doc.getModelInstance()

		self.assertEqual(sbml_model.modelHistory.getDateCreated(), "2005-02-02T14:56:11Z")
		creator = sbml_model.modelHistory.getListOfCreators()[0]
		self.assertEqual(creator.getEmail(), "lenov@ebi.ac.uk")
		self.assertEqual(creator.getGivenName(), "Nicolas")
		self.assertEqual(creator.getFamilyName(), "Le Novère")


		taxon_uri = URI()
		taxon_uri.setTaxonomy('7787')
		self.assertEqual(sbml_model.getAnnotation().getHasTaxon()[0], taxon_uri)
		self.assertEqual(sbml_model.getAnnotation().getHasTaxon()[0].getName(), "Tetronarce californica")

		self.assertEqual(sbml_model.getAnnotation().getHasProperty(), [])
		self.assertEqual(sbml_model.getAnnotation().getHasPart(), [])
		self.assertEqual(sbml_model.getAnnotation().getHasVersion(), [])
		self.assertEqual(sbml_model.getAnnotation().getIs(), [])
		self.assertEqual(sbml_model.getAnnotation().getIsDescribedBy(), [])
		self.assertEqual(sbml_model.getAnnotation().getIsEncodedBy(), [])
		self.assertEqual(sbml_model.getAnnotation().getIsHomologTo(), [])
		self.assertEqual(sbml_model.getAnnotation().getIsPartOf(), [])
		self.assertEqual(sbml_model.getAnnotation().getIsPropertyOf(), [])

		go_process1_uri = URI()
		go_process1_uri.setGO('GO:0007274')
		go_process2_uri = URI()
		go_process2_uri.setGO('GO:0007166')
		go_process3_uri = URI()
		go_process3_uri.setGO('GO:0019226')
		self.assertEqual(sbml_model.getAnnotation().getIsVersionOf()[0], go_process1_uri)
		self.assertEqual(sbml_model.getAnnotation().getIsVersionOf()[1], go_process2_uri)
		self.assertEqual(sbml_model.getAnnotation().getIsVersionOf()[2], go_process3_uri)

		self.assertEqual(sbml_model.getAnnotation().getOccursIn(), [])
		self.assertEqual(sbml_model.getAnnotation().getUnknown(), [])
		self.assertEqual(sbml_model.getAnnotation().getModelHasInstance(), [])

		biomodels_ref1_uri = URI()
		biomodels_ref1_uri.setBiomodels('MODEL6613849442')
		biomodels_ref2_uri = URI()
		biomodels_ref2_uri.setBiomodels('BIOMD0000000001')

		self.assertEqual(sbml_model.getAnnotation().getModelIs()[0], biomodels_ref1_uri)
		self.assertEqual(sbml_model.getAnnotation().getModelIs()[1], biomodels_ref2_uri)

		self.assertEqual(sbml_model.getAnnotation().getModelIsDerivedFrom(), [])

		publication_uri = URI()
		publication_uri.setPubmed('8983160')
		self.assertEqual(sbml_model.getAnnotation().getModelIsDescribedBy()[0], publication_uri)
		self.assertEqual(
			sbml_model.getAnnotation().getModelIsDescribedBy()[0].getName(),
			("Edelstein SJ(1), Schaad O, Henry E, Bertrand D, Changeux JP., "
				+ "A kinetic mechanism for nicotinic acetylcholine receptors based on multiple allosteric transitions., "
				+ "1. Biol Cybern. 1996 Nov;75(5):361-79.")
		)
		self.assertEqual(sbml_model.getAnnotation().getModelIsInstanceOf(), [])
		self.assertEqual(sbml_model.getAnnotation().getModelUnknown(), [])

		descriptions = [
			u'physical compartment', u'protein complex', u'protein complex', u'protein complex',
			u'multimer of macromolecules', u'protein complex', u'multimer of macromolecules', u'protein complex',
			u'multimer of macromolecules', u'protein complex', u'protein complex', u'multimer of macromolecules',
			u'protein complex', u'non-covalent binding', u'non-covalent binding', u'conformational transition',
			u'non-covalent binding', u'non-covalent binding', u'conformational transition',
			u'conformational transition', u'non-covalent binding', u'non-covalent binding',
			u'conformational transition', u'conformational transition', u'conformational transition',
			u'non-covalent binding', u'non-covalent binding', u'physical compartment', u'protein complex',
			u'protein complex', u'protein complex', u'multimer of macromolecules', u'protein complex',
			u'multimer of macromolecules', u'protein complex', u'multimer of macromolecules', u'protein complex',
			u'protein complex', u'multimer of macromolecules', u'protein complex', u'non-covalent binding',
			u'non-covalent binding', u'conformational transition', u'non-covalent binding', u'non-covalent binding',
			u'conformational transition', u'conformational transition', u'non-covalent binding',
			u'non-covalent binding', u'conformational transition', u'conformational transition',
			u'conformational transition', u'non-covalent binding', u'non-covalent binding'
		]

		resolved_descriptions = sbml_model.getListOfSBOTermsDescriptions()
		self.assertEqual(resolved_descriptions, descriptions)