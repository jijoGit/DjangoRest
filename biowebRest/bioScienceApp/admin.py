from django.contrib import admin
from .models import *

class ProteinDomainLinkAdmin(admin.ModelAdmin):
    model = ProteinDomainLink

class ProteinAdmin(admin.ModelAdmin):
    model = Protein

class TaxonomyAdmin(admin.ModelAdmin):
    model = Taxonomy

class PfamAdmin(admin.ModelAdmin):
    model = Pfam


admin.site.register(ProteinDomainLink, ProteinDomainLinkAdmin)
admin.site.register(Protein, ProteinAdmin)
admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Pfam, PfamAdmin)


# admin.site.register(ProteinOrganismLink, ProteinOrganismLinkInline)