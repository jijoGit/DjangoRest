
# I wrote this code 
from django.urls import path, re_path
from . import views
from . import api

urlpatterns = [

    path('api/protein/', api.CreateProteins.as_view(), name='createProteins_api'),
    path('api/protein/<str:protein_id>', api.GetProtein.as_view(), name='getProtein_api'),
    path('api/proteins/<str:taxa_id>', api.GetTaxonomy.as_view(), name='getTaxonomy_api'),
    path('api/pfam/<str:pfam_id>', api.GetPfam.as_view(), name='getPfam_api'),
    path('api/pfams/<int:taxa_id>', api.GetPfamOnTaxaId.as_view(), name='getPfamOnTaxaId_api'),  
    path('api/coverage/<str:protein_id>', api.GetCoverage.as_view(), name='getCoverage_api'),
]

#end of code I wrote 