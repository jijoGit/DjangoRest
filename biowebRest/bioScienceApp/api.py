from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

from django.http import HttpResponse


class GetCoverage(APIView):
    
    # return the domain coverage for a given protein. 
    # That is Sum of the protein domain lengths (start-stop)/length of protein.
    def get(self, request, protein_id):

        protein = get_object_or_404(Protein.objects.all(), protein_id=protein_id)
        coverage = protein.get_coverage()
        return Response({'coverage': coverage}, status=status.HTTP_200_OK)

    


class GetPfamOnTaxaId(generics.GenericAPIView):
    serializer_class = GetPfamOnTaxaIdSerializer
    queryset = Taxonomy.objects.all()

    def get(self, request, taxa_id):
        taxonomy = get_object_or_404(Taxonomy, taxa_id=taxa_id)
        protein_domain_links = ProteinDomainLink.objects.filter(protein__taxonomy=taxonomy)

      
        pfam_data = self.serializer_class(protein_domain_links, many=True).data

        return Response(pfam_data, status=status.HTTP_200_OK)



class GetTaxonomy(generics.GenericAPIView):
    serializer_class = ProteinTaxaSerializer
    queryset = Taxonomy.objects.all()

    def get(self, request, taxa_id):
        taxonomy = get_object_or_404(self.get_queryset(), taxa_id=taxa_id)
        proteins = taxonomy.get_proteins()
        protein_data = self.serializer_class(proteins, many=True).data

        data = [
            {"id": taxa_id, "protein_id": protein["protein_id"]}
            for protein in protein_data
        ]

        return Response(data, status=status.HTTP_200_OK)

class GetPfam (generics.GenericAPIView):
    serializer_class = PfamSerializer
    
    def get(self, request, pfam_id):
        pfam = get_object_or_404(Pfam.objects.all(), domain_id=pfam_id)
        serializer = self.serializer_class(pfam)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetProtein(generics.GenericAPIView):

    serializer_class = ProteinGetSerializer

    def get(self, request, protein_id):
         protien = get_object_or_404(Protein.objects.all(), protein_id=protein_id)
         serializer = self.serializer_class(protien)
         return Response(serializer.data, status=status.HTTP_200_OK)
          

class CreateProteins(APIView):
    serializer_class = ProteinSerializer

    def post(self, request):
        
        domains = request.data.pop("domains", None)

        serializer = ProteinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        protein = serializer.save()

        self.create_domains(protein, domains)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
   

    def create_domains(self, protein, domains):

        domain_serialized = []

        for domain_data in domains:
            domain_data['protein'] = protein.id 
            domain_serialized.append(ProteinDomainLinkSerializer(data=domain_data))

        for domain_serializer in domain_serialized:
            domain_serializer.is_valid(raise_exception=True)
            domain_serializer.save()

        



