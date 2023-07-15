# I wrote this code 
from django.shortcuts import render

from .models import * 

def index(request):
    proteins_all = Protein.objects.all()
    print(proteins_all[0]);
    return render(request, 'bioScienceApp/index.html', {'proteins': proteins_all})
#end of code I wrote 