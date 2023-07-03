import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

json_data = '''
        {
            "protein_id": "A0A016S8J7",
            "sequence": "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA",
            "taxonomy": {
                "taxa_id": 53326,
                "clade": "E",
                "genus": "Ancylostoma",
                "species": "ceylanicum"
            },
            "length": 101,
            "domains": [
                {
                    "pfam_id": {
                        "domain_id": "PF01650",
                        "domain_description": "PeptidaseC13family"
                    },
                    "description": "Peptidase C13 legumain",
                    "start": 40,
                    "stop": 94
                },
                {
                    "pfam_id": {
                        "domain_id": "PF02931",
                        "domain_description": "Neurotransmitter-gatedion-channelligandbindingdomain"
                    },
                    "description": "Neurotransmitter-gated ion-channel ligand-binding domain",
                    "start": 23,
                    "stop": 39
                }
            ]
        }
        '''

class ProteinsListSerializerTest(APITestCase):

    def test_proteinsListSerializer(self):
        # JSON data
        
        json_obj = json.loads(json_data)
        serializer = ProteinSerializer(data=json_obj)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data
        self.assertEqual(serialized_data['taxonomy']['taxa_id'], str(json_obj['taxonomy']['taxa_id']))
        self.assertEqual(serialized_data['sequence'], json_obj['sequence'])
        self.assertEqual(serialized_data['taxonomy']['taxa_id'], str(json_obj['taxonomy']['taxa_id']))
        self.assertEqual(serialized_data['taxonomy']['clade'], json_obj['taxonomy']['clade'])
        self.assertEqual(serialized_data['taxonomy']['genus'], json_obj['taxonomy']['genus'])
        self.assertEqual(serialized_data['taxonomy']['species'], json_obj['taxonomy']['species'])
        self.assertEqual(serialized_data['length'], json_obj['length'])



    def test_protein_domain_link_get_serializer(self):
        # Sample data from JSON
        link_data_json = '''
        {
            "pfam_id": {
                "domain_id": "PF01650",
                "domain_description": "PeptidaseC13family"
            },
            "description": "Sample description",
            "start": 1,
            "stop": 10
        }
        '''

        # Deserialize the JSON data
        link_data = json.loads(link_data_json)

        # Create an instance of the ProteinDomainLink model
        link_serializer = ProteinDomainLinkGetSerializer(data=link_data)

        # Validate the serializer data
        self.assertTrue(link_serializer.is_valid())

        # Access the serialized data
        serialized_data = link_serializer.data

        # Assert the serialized data matches the input data
        self.assertEqual(serialized_data['description'], link_data['description'])
        self.assertEqual(serialized_data['start'], link_data['start'])
        self.assertEqual(serialized_data['stop'], link_data['stop'])
        self.assertEqual(serialized_data['pfam_id']['domain_id'], link_data['pfam_id']['domain_id'])
        self.assertEqual(serialized_data['pfam_id']['domain_description'], link_data['pfam_id']['domain_description'])
