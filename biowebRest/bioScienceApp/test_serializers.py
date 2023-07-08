import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *



class ProteinsSerializerTest(APITestCase):

    
    protein1 = None 
    proteinSerializer = None

    def setUp(self) -> None:
        self.protein1 = ProteinFactory.create(proteinId="A0A014PQC0")
        self.proteinsSerializer = ProteinSerializer(instance=self.protein1)

        self.validated_data = {
            'protein_id': 'A0A014PQC0',
            'sequence': 'SAMPLE_SEQUENCE',
            'length': 100
        }

       
    def tearDown(self) -> None:
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)

    def test_proteinsListSerializer(self):
        data = self.proteinsSerializer.data
        self.assertEqual(set(data.keys()), set(['protein_id', 'sequence', 'length']))

    def test_proteinSerializer_create(self):
        serializer = ProteinSerializer(data=self.validated_data)
        
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)
        self.assertTrue(is_valid)


class ProteinGetSerializerTest(APITestCase):
    '''
    Part of ProteinGetSerializerTest:
        ProteinGetSerializer
        TaxonomyProteinSerializer
        ProteinDomainLinkGetSerializer

    '''
    protein1 = None
    protein2 = None
    proteinSerializer = None
    domain1= None
    domain2=None
    domain_link1 = None
    domain_link2 = None 
    taxonomy = None
    taxaonmoylink1 = None
    taxaonmoylink2 = None

    def setUp(self):
                
        self.taxonomy = TaxonomyFactory.create(taxaId='55661')
        self.protein1 = ProteinFactory.create(proteinId='A0A014PQC0') 
        # self.protein2 = ProteinFactory.create(proteinId='A0A134567') 

        self.taxaonmoylink1 = TaxonomyProteinLinkFactory.create(protein=self.protein1, taxonomy=self.taxonomy)
        # self.taxaonmoylink2 = TaxonomyProteinLinkFactory.create(protein=self.protein2, taxonomy=self.taxonomy)

                 
        self.domain1 = PfamFactory(domainId='PF01650', domain_description='PeptidaseC13family')
        self.domain2 = PfamFactory(domainId='PF12345', domain_description='AnotherDomain')


        self.domain_link1 = ProteinDomainLinkFactory(protein=self.protein1, pfam=self.domain1)
        self.domain_link2 = ProteinDomainLinkFactory(protein=self.protein1, pfam=self.domain2)
        
        self.proteinSerializer = ProteinGetSerializer(self.protein1)

    def tearDown(self):
        Protein.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        TaxonomyProteinLink.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        ProteinDomainLinkFactory.reset_sequence(0)
        TaxonomyProteinLinkFactory.reset_sequence(0)

    def test_proteinGetSerializer(self):
        data = self.proteinSerializer.data
        self.assertEqual(set(data.keys()), set(['protein_id', 'sequence', 'taxonomy', 'length', 'domains']))

    def test_proteinGetSerializerHasCorrectData(self):
        data = self.proteinSerializer.data
        self.assertEqual(data['protein_id'], 'A0A014PQC0')

        # Additional assertions for the fields 'sequence', 'length', 'taxonomy', and 'domains'
        self.assertEqual(data['sequence'], self.protein1.sequence)
        self.assertEqual(data['length'], self.protein1.length)
        self.assertEqual(len(data['taxonomy']), 4)  
        self.assertEqual(len(data['domains']), 2)  # Assuming 2 domain entries for this protein

class TaxonomyProteinSerializerTest(TestCase):

    taxonomy_data = None

    def setUp(self):
        ''' not using factory boy, this serializer is part of create protein '''
        self.taxonomy_data = {
            'taxaId': '55661',
            'clade': 'Sample Clade',
            'genus': 'Sample Genus',
            'species': 'Sample Species'
        }



    def tearDown(self):
        Taxonomy.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        TaxonomyProteinLink.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        ProteinDomainLinkFactory.reset_sequence(0)
        TaxonomyProteinLinkFactory.reset_sequence(0)

    
    def test_taxonomyProteinSerializer(self):
       
        protein_data = {
            'taxonomy': self.taxonomy_data
        }

        serializer = TaxonomyProteinSerializer(protein_data)

        self.assertEqual(set(serializer.data.keys()), set(['taxa_id', 'clade', 'genus', 'species']))
        self.assertEqual(serializer.data['taxa_id'], '55661')
        self.assertEqual(serializer.data['clade'], 'Sample Clade')
        self.assertEqual(serializer.data['genus'], 'Sample Genus')
        self.assertEqual(serializer.data['species'], 'Sample Species')


class TaxonomyProteinLinkSerializerTest(TestCase):

    def setUp(self):
        self.taxonomy = TaxonomyFactory.create(taxaId='55661')
        self.protein1 = ProteinFactory.create(proteinId='A0A014PQC0') 
        self.taxaonmoylink1 = TaxonomyProteinLinkFactory.create(protein=self.protein1, taxonomy=self.taxonomy)
        self.serializer = TaxonomyProteinLinkSerializer(instance=self.taxaonmoylink1)


    def tearDown(self):
        Taxonomy.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        TaxonomyProteinLink.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        ProteinDomainLinkFactory.reset_sequence(0)
        TaxonomyProteinLinkFactory.reset_sequence(0)
        

    def test_taxonomyProteinLinkSerializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['taxonomy', 'protein']))


class GetPfamOnTaxaIdSerializerTest(TestCase):

    def setUp(self):
        self.domain1 = PfamFactory(domainId='PF01650', domain_description='PeptidaseC13family')
        self.protein1 = ProteinFactory.create(proteinId='A0A04PQC0') 
        self.domain_link1 = ProteinDomainLinkFactory(protein=self.protein1, pfam=self.domain1)

        self.serializer = GetPfamOnTaxaIdSerializer(instance=self.domain_link1)

    def tearDown(self):
        Taxonomy.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        TaxonomyProteinLink.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        ProteinDomainLinkFactory.reset_sequence(0)
        TaxonomyProteinLinkFactory.reset_sequence(0)

    def test_getPfamOnTaxaIdSerializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'pfam_id']))
        self.assertEqual(data['id'], str(self.domain_link1.pk))
        self.assertEqual(data['pfam_id']['domain_id'], self.domain1.domainId)
        self.assertEqual(data['pfam_id']['domain_description'], self.domain1.domain_description)



class ProteinDomainLinkGetSerializerTest(TestCase):

    def setUp(self):
        self.domain1 = PfamFactory(domainId='PF01650', domain_description='PeptidaseC13family')
        self.protein1 = ProteinFactory(proteinId='A0A04PQC0')
        self.domain_link1 = ProteinDomainLinkFactory(protein=self.protein1, pfam=self.domain1)

        self.serializer = ProteinDomainLinkGetSerializer(instance=self.domain_link1)

    def tearDown(self):
        Taxonomy.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        TaxonomyProteinLink.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        ProteinDomainLinkFactory.reset_sequence(0)
        TaxonomyProteinLinkFactory.reset_sequence(0)
        

    def test_proteinDomainLinkGetSerializer(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['pfam_id', 'description', 'start', 'stop']))
        self.assertEqual(data['pfam_id']['domain_id'], self.domain1.domainId)
        self.assertEqual(data['pfam_id']['domain_description'], self.domain1.domain_description)


class ProteinDomainLinkSerializerTest(TestCase):

   
    def setUp(self):
        self.protein1 = ProteinFactory(proteinId='A0A04PQC0')
        self.data = {
            'protein': self.protein1.pk,
            'pfam_id': {
                'domain_id': 'PF01650',
                'domain_description': 'self.pfam.domain_description'
            },
            'description': 'Sample description',
            'start': 1,
            'stop': 10
        }
        self.serializer = ProteinDomainLinkSerializer(data=self.data)

    def tearDown(self):
        Taxonomy.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        TaxonomyProteinLink.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        ProteinDomainLinkFactory.reset_sequence(0)
        TaxonomyProteinLinkFactory.reset_sequence(0)
        

    def test_proteinDomainLinkSerializer_create(self):
        is_valid = self.serializer.is_valid()
        if not is_valid:
            print(self.serializer.errors)
        self.assertTrue(is_valid)

        link = self.serializer.save()

        self.assertEqual(link.protein, self.protein1)


class TaxonomySerializerTest(TestCase):

    def setUp(self):
        self.data = {
            'taxa_id': '55661',
            'clade': 'Sample Clade',
            'genus': 'Sample Genus',
            'species': 'Sample Species'
        }
        self.serializer = TaxonomySerializer(data=self.data)

    def tearDown(self):
        Taxonomy.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        TaxonomyProteinLink.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        ProteinDomainLinkFactory.reset_sequence(0)
        TaxonomyProteinLinkFactory.reset_sequence(0)
        

    def test_taxonomySerializer(self):
        self.assertTrue(self.serializer.is_valid())
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['taxa_id', 'clade', 'genus', 'species']))
        self.assertEqual(data['taxa_id'], '55661')
        self.assertEqual(data['clade'], 'Sample Clade')
        self.assertEqual(data['genus'], 'Sample Genus')
        self.assertEqual(data['species'], 'Sample Species')

