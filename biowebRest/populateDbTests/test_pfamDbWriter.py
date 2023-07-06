
#python manage.py test populateDbTests.test_pfamDbWriter

import unittest
from unittest.mock import mock_open, patch
from django.test import TestCase
from bioScienceApp.models import *
from bioScienceApp.model_factories import *

from populateDb import PfamDatabaseWriter, SequenceDBWriter, DatabaseWriter

class PfamDatabaseWriterTestCase(TestCase):
    csv = 'CoiledCoil,coil prediction\nLowComplexity,low complexity prediction'

    def setUp(self):
        self.file_data_reader = PfamDatabaseWriter(pfam_descriptions='./csv/pfam_descriptions.csv')

    @patch('builtins.open', new_callable=mock_open, read_data=csv)
    def test_add_pfam(self, mock_file):

        pfam_rows = self.file_data_reader.add_pfam()
        # print(pfam_rows)

        self.assertEqual(len(pfam_rows), 2)
        self.assertIsInstance(pfam_rows['CoiledCoil'], Pfam)
        self.assertIsInstance(pfam_rows['LowComplexity'], Pfam)
        self.assertEqual(pfam_rows['CoiledCoil'].domainId, 'CoiledCoil')
        self.assertEqual(pfam_rows['CoiledCoil'].domain_description, 'coil prediction')
        
class SequenceWriterTestCase(TestCase):
    csv = 'A0A016S8J7,sequence1 \nprotein2, sequence2'

    def setUp(self):
        self.sequence_db_writer = SequenceDBWriter(data_sequences_file='./csv/assignment_data_sequences.csv')

    @patch('builtins.open', new_callable=mock_open, read_data=csv)
    def test_add_sequence(self, mock_file):
        protein_id = ProteinSanSeqFactory.create()

        self.sequence_db_writer.add_sequence()

        protein1 = Protein.objects.get(proteinId='A0A016S8J7')
   
        self.assertEqual(protein1.sequence.strip(), 'sequence1')

class DatabaseWriterTestCase(TestCase):
   
    def setUp(self):
        self.database_writer = DatabaseWriter(
            proteins='',
            organisms=None,
            protein_organisms=None,
            domains=None,
            pfam_read_writer=None,
            sequence_read_writer=None
        )
