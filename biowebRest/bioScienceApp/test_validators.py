# I wrote this code 

import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

class ProteinSerializerValidatorTest(TestCase):

    def test_protein_validation(self):
        data = {
            'protein_id': 'A0A014PQC0',
            'sequence': 'A0A014PQC0',
            'length': '100'
        }
        

        serializer = ProteinSerializer(data=data)
        
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)
        self.assertTrue(is_valid)

    def test_protein_validation_invalid_protein(self):
        data = {
            'protein_id': 'ABCD',
            'sequence': 'ABC@123',
            'length': '100'
        }
        serializer = ProteinSerializer(data=data)
        
        is_valid = serializer.is_valid()
        # if not is_valid:
        #     print(serializer.errors)
        self.assertFalse(is_valid)


    def test_protein_validation_invalid_length(self):
        data = {
            'protein_id': 'A0A014PQC0',
            'sequence': 'ABC123',
            'length': 'ABC'
        }
        serializer = ProteinSerializer(data=data)
        
        is_valid = serializer.is_valid()
        # if not is_valid:
        #     print(serializer.errors)
        self.assertFalse(is_valid)


    #end of code I wrote 