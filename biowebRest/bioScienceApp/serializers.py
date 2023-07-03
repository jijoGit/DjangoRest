from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']



class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ["domain_id","domain_description"]


class ProteinDomainLinkSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()

    class Meta:
        model = ProteinDomainLink
        fields = '__all__'


    def create(self, validated_data):
        pfam_data = validated_data.pop('pfam_id')
        pfam, _ = Pfam.objects.get_or_create(**pfam_data)

        print('ProteinDomainLinkSerializer pfam', pfam)

        validated_data['pfam_id'] = pfam 

        link, _ = ProteinDomainLink.objects.get_or_create(
            protein=validated_data.get('protein'),
            pfam_id=pfam,
            description=validated_data['description'] ,
            start=validated_data['start'] ,
            stop=validated_data['stop'] 
        )

        print('ProteinDomainLinkSerializer link', link)
        return link


class ProteinSerializer(serializers.ModelSerializer):
    ''' Serializer for the protein object'''
    taxonomy = TaxonomySerializer()
    lookup_field = 'protein_id'
    
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length']

    def create(self, validated_data):

        taxonomy_data = validated_data.pop('taxonomy')
    
        taxonomy, _ = Taxonomy.objects.get_or_create(**taxonomy_data)
        
        protein, _ = Protein.objects.get_or_create(
            protein_id=validated_data.get('protein_id'),
            defaults={
                'sequence': validated_data.get('sequence'),
                'taxonomy': taxonomy,
                'length': validated_data.get('length')
            }
        )
        return protein


class ProteinDomainLinkGetSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()

    class Meta:
        model = ProteinDomainLink
        fields = ['pfam_id', 'description', 'start', 'stop']


class ProteinGetSerializer(serializers.ModelSerializer):
    ''' Serializer for the protein object'''
    taxonomy = TaxonomySerializer()

    domains = serializers.SerializerMethodField()

    '''using proteinDomainlink i can pfams'''
    def get_domains(self, obj):
        domains = ProteinDomainLink.objects.filter(protein=obj)
        print('domain***********', domains)
        for domain in domains:
            print(domain)
        serializer = ProteinDomainLinkGetSerializer(domains, many=True)
        return serializer.data

       
    class Meta:
        model = Protein
        fields = ('protein_id', 'sequence', 'taxonomy', 'length', 'domains')


class ProteinTaxaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ['protein_id']


class TaxonomyGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Taxonomy
        fields = ["taxa_id"]


class GetPfamOnTaxaIdSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')
    pfam_id = PfamSerializer()

    class Meta:
        model = ProteinDomainLink
        fields = ['id', 'pfam_id']

