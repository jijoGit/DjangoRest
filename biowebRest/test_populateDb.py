#code is based on below answer for the question about mock opening file.
#https://stackoverflow.com/questions/18867747/how-to-use-mock-open-with-patch-object-in-test-annotation


import unittest
from unittest.mock import mock_open, patch
from collections import defaultdict
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from populateDb import FileDataReader

from bioScienceApp.models import Protein, Taxonomy, Pfam, TaxonomyProteinLink, ProteinDomainLink


class FileDataReaderTestCase(TestCase):
    def setUp(self):
        # test data
        self.assignment_data = [
            ['protein1', 'taxa1', 'clade1', 'genus1 species1', 'desc1', 'domain1', '1', '10', '100'],
            ['protein2', 'taxa2', 'clade2', 'genus2 species2', 'desc2', 'domain2', '11', '20', '200'],
        ]
      
        self.file_data_reader = FileDataReader(assignment_data_set='assignment_data_set.csv')

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_read_data(self, mock_open):
        
        mock_file = mock_open.return_value
        mock_file.readlines.return_value = [','.join(row) + '\n' for row in self.assignment_data]

        
        proteins, organisms, protein_organism, domains = self.file_data_reader.read_data()
        print(proteins)

        self.assertEqual(len(proteins), 2)


if __name__ == '__main__':
    unittest.main()