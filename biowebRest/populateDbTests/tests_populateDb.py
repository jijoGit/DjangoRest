#this is based on https://stackoverflow.com/questions/18867747/how-to-use-mock-open-with-patch-object-in-test-annotation

# I wrote this code 
import unittest
from unittest.mock import mock_open, patch
from django.test import TestCase

from populateDb import FileDataReader


class FileDataReaderTestCase(TestCase):
    csv = 'protein1,taxa1,clade1,genus1 species1,desc1,domain1,1,10,100\nprotein2,taxa2,clade2,genus2 species2,desc2,domain2,11,20,200\n'

    def setUp(self):
        self.file_data_reader = FileDataReader(assignment_data_set='csv/assignment_data_set.csv')

    @patch('builtins.open', new_callable=mock_open, read_data=csv)
    def test_read_data(self, mock_open):
        proteins, organisms, protein_organism, domains = self.file_data_reader.read_data()

        print(protein_organism)
        self.assertEqual(len(proteins), 2)
        self.assertEqual(len(organisms), 2)
        self.assertEqual(len(protein_organism), 2)
        self.assertEqual(len(domains), 2)

        expected_domains = {
            'domain1': {'desc': 'desc1', 'start': '1', 'end': '10', 'protein_ids': {'protein1'}},
            'domain2': {'desc': 'desc2', 'start': '11', 'end': '20', 'protein_ids': {'protein2'}}
        }

        expected_protein_organism = {
            'protein1': ('taxa1',),
            'protein2': ('taxa2',)
        }

        expected_organisms = {
             'taxa1': ['clade1', 'genus1', 'species1', 'protein1'],
             'taxa2': ['clade2', 'genus2', 'species2', 'protein2']
        }

        
        expected_proteins = {
             'protein1': ['100', 'taxa1'],
             'protein2': ['200', 'taxa2']
             }
        
        converted_organisms = dict(organisms)
        converted_proteins = dict(proteins)
        converted_protein_organism = {k: tuple(v) for k, v in protein_organism.items()}

        self.assertDictEqual(converted_proteins, expected_proteins)

        self.assertDictEqual(converted_organisms, expected_organisms)

        self.assertDictEqual(converted_protein_organism, expected_protein_organism)

        self.assertDictEqual(domains, expected_domains)
        

if __name__ == '__main__':
    unittest.main()
#end of code I wrote 