from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404

class TaxonomySerializer(serializers.ModelSerializer):

    taxa_id = serializers.CharField(source="taxaId")


    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']



class PfamSerializer(serializers.ModelSerializer):

    #renaming the field name to match the specification.
    domain_id = serializers.CharField(source="domainId")
    
    class Meta:
        model = Pfam
        fields = ["domain_id","domain_description"]


class ProteinDomainLinkSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer(source="pfam")
    # protein = serializers.CharField(source='protein')

    class Meta:
        model = ProteinDomainLink
        fields = ['protein', 'pfam_id', 'description', 'start', 'stop']


    def create(self, validated_data):
        print('validated_data', validated_data)
        pfam_data = validated_data.pop('pfam')
        pfam, _ = Pfam.objects.get_or_create(**pfam_data)

        # print('ProteinDomainLinkSerializer pfam', pfam)

        validated_data['pfam_id'] = pfam 

        link, _ = ProteinDomainLink.objects.get_or_create(
            protein=validated_data.get('protein'),
            pfam=pfam,
            description=validated_data['description'] ,
            start=validated_data['start'] ,
            stop=validated_data['stop'] 
        )

        print('ProteinDomainLinkSerializer link', link)
        return link


class ProteinDomainLinkGetSerializer(serializers.ModelSerializer):
    
    pfam_id = PfamSerializer(source="pfam")

    class Meta:
        model = ProteinDomainLink
        fields = ['pfam_id', 'description', 'start', 'stop']


class ProteinSerializer(serializers.ModelSerializer):
    ''' Serializer for the protein object'''

    protein_id = serializers.CharField(source='proteinId')
   
    class Meta:
        model = Protein
        fields = ['protein_id','sequence', 'length']

    def create(self, validated_data):
        
        protein, _ = Protein.objects.get_or_create(
            proteinId=validated_data.get('proteinId'),
            defaults={
                'sequence': validated_data.get('sequence'),
                'length': validated_data.get('length')
            }
        )
        return protein


class ProteinTaxaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxonomyProteinLink
        fields = ['proteinId']


class TaxonomyGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Taxonomy
        fields = ["taxaId"]


class GetPfamOnTaxaIdSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')
    pfam_id = PfamSerializer(source="pfam")

    class Meta:
        model = ProteinDomainLink
        fields = ['id', 'pfam_id']

class TaxonomyProteinLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxonomyProteinLink
        fields = ['taxonomy', 'protein']



class TaxonomyProteinLinkGetSerializer(serializers.ModelSerializer):
    taxonomy = TaxonomySerializer()

    class Meta:
        model = ProteinDomainLink
        fields = ['taxonomy']


class TaxonomyProteinSerializer(serializers.Serializer):
    '''not using model serailizer to control the return data'''
    taxa_id = serializers.CharField(source='taxonomy.taxaId')
    clade = serializers.CharField(source='taxonomy.clade')
    genus = serializers.CharField(source='taxonomy.genus')
    species = serializers.CharField(source='taxonomy.species')


class ProteinGetSerializer(serializers.ModelSerializer):
    ''' Serializer for the protein object'''
    taxonomy = serializers.SerializerMethodField()
    domains = serializers.SerializerMethodField()

    '''using proteinDomainlink'''
    def get_domains(self, obj):
        domains = ProteinDomainLink.objects.filter(protein=obj)
        serializer = ProteinDomainLinkGetSerializer(domains, many=True)
        return serializer.data
    
    def get_taxonomy(self, obj):
        taxonomyProtein_obj = TaxonomyProteinLink.objects.filter(protein=obj)
        
        '''to not to return a list if singlye object'''
        if len(taxonomyProtein_obj) == 1:
            taxonomyProtein_obj = TaxonomyProteinLink.objects.get(protein=obj)
            serializer = TaxonomyProteinSerializer(taxonomyProtein_obj)
            return serializer.data

        serializer = TaxonomyProteinSerializer(taxonomyProtein_obj, many=True)    
        return serializer.data

    
    class Meta:
        model = Protein
        fields = ('proteinId', 'sequence', 'taxonomy', 'length', 'domains')

