from django.urls import path, re_path
from . import views
from . import api

urlpatterns = [
    # //http://127.0.0.1:8000/api/pfam/[PFAM ID]
    path('api/protein/', api.CreateProteins.as_view()),
    path('api/protein/<str:protein_id>', api.GetProtein.as_view()),

    path('api/proteins/<str:taxa_id>', api.GetTaxonomy.as_view()),

    path('api/pfam/<str:pfam_id>', api.GetPfam.as_view()),

    path('api/pfams/<int:taxa_id>', api.GetPfamOnTaxaId.as_view()),

    path('api/coverage/<str:protein_id>', api.GetCoverage.as_view()),

  

# GET  http://127.0.0.1:8000/api/coverage/[PROTEIN ID] - return the domain coverage for a given protein. That is Sum of the protein domain lengths (start-stop)/length of protein.
# http://127.0.0.1:8000/api/coverage/A0A016S8J7 returns
# coverage:	0.693069306930693

    
# GET  http://127.0.0.1:8000/api/pfams/[TAXA ID] 
]
