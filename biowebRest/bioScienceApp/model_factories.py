import factory

from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = "53326"
    clade = "E"
    genus = "Ancylostoma"
    species = "ceylanicum"

    class Meta:
        model = Taxonomy


class ProteinSanSeqFactory(factory.django.DjangoModelFactory):
    proteinId = 'A0A016S8J7'
    sequence = ''
    length = 101
    
    class Meta:
        model = Protein


class ProteinFactory(factory.django.DjangoModelFactory):
    protein_id = 'A0A016S8J7'
    sequence = 'MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA'
    length = 101
    taxonomy = factory.SubFactory(OrganismFactory)

    class Meta:
        model = Protein


class PfamFactory(factory.django.DjangoModelFactory):
    domain_id = 'PF01650'
    domain_description = 'PeptidaseC13family'

    class Meta:
        model = Pfam


class ProteinDomainLinkFactory(factory.django.DjangoModelFactory):
    protein = factory.SubFactory(ProteinFactory)
    pfam_id = factory.SubFactory(PfamFactory)
    description = 'Peptidase C13 legumain'
    start = 40
    stop = 94

    class Meta:
        model = ProteinDomainLink


class ProteinDomainLinkFactory2(factory.django.DjangoModelFactory):
    protein = factory.SubFactory(ProteinFactory)
    pfam_id = factory.SubFactory(PfamFactory)
    description = 'Neurotransmitter-gated ion-channel ligand-binding domain'
    start = 23
    stop = 39

    class Meta:
        model = ProteinDomainLink
