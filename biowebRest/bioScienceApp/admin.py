# I wrote this code 
from django.contrib import admin
from .models import *

class TaxonomyProteinLinkAdmin(admin.ModelAdmin):
    model = TaxonomyProteinLink


class ProteinDomainLinkAdmin(admin.ModelAdmin):
    model = ProteinDomainLink

class ProteinAdmin(admin.ModelAdmin):
    model = Protein

class TaxonomyAdmin(admin.ModelAdmin):
    model = Taxonomy

class PfamAdmin(admin.ModelAdmin):
    model = Pfam


admin.site.register(TaxonomyProteinLink, TaxonomyProteinLinkAdmin)
admin.site.register(ProteinDomainLink, ProteinDomainLinkAdmin)
admin.site.register(Protein, ProteinAdmin)
admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Pfam, PfamAdmin)


#end of code I wrote 