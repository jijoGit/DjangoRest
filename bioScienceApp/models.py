# I wrote this code 

'''
TA single protein can have multiple domains, and each domain may have a different domain ID.

'''

from django.db import models

class Taxonomy(models.Model):
    taxaId = models.CharField(max_length=256, unique=True, null=False, blank=False)
    clade = models.CharField(max_length=256, null=False, blank=True)
    genus = models.CharField(max_length=256, null=False, blank=True)
    species = models.CharField(max_length=256, null=False, blank=True)
 
    def __str__(self):
        return self.taxaId

  
class Protein(models.Model):
    proteinId = models.CharField(max_length=256, unique=True, null=False, blank=False)
    sequence = models.CharField(max_length=256, blank=True)
    length = models.IntegerField(null=False, blank=True)

       
    def get_coverage(self):
        
        protein_domains = self.domain.all()
        if protein_domains.exists():
            domain_lengths = sum(domain.stop - domain.start for domain in protein_domains)
            return domain_lengths / self.length
        else:
            return 0


    def __str__(self):
        return self.proteinId
    
class TaxonomyProteinLink(models.Model):
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE)
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('taxonomy', 'protein')

    def __str__(self):
        return f"{self.protein.proteinId}_{self.taxonomy.taxaId}"


class Pfam(models.Model):
    domainId = models.CharField(max_length=256, unique=True, null=False, blank=False)
    domain_description = models.CharField(max_length=256, null=False, blank=True)

    def __str__(self):
        return self.domainId
    

class ProteinDomainLink(models.Model):
    protein =  models.ForeignKey(Protein, on_delete=models.DO_NOTHING, related_name='domain')
    pfam = models.ForeignKey(Pfam, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=256, null=False, blank=True)
    start = models.IntegerField(null=False, blank=True)
    stop = models.IntegerField(null=False, blank=True)

    # def get_protein(self):
    #     return self.protein.all()
    
    # def get_pfam(self):
    #     return self.pfam.all()

    def __str__(self):
        return f"{self.protein.proteinId}_{self.pfam.domainId[:8]}"



'''
Organism has one to many relation with Protein 
such as '2711','2880','3218'

Protein is associated with one or more Taxa_id 
such as U6M9K5, D2CJZ4, A0A1D5QV06, A0A1D6FYR9, A0A194WA83, A0A177U724, A0A177BX17, A0A1A8N5W2, A0A0P5IGI0,
A0A0V1IMU6, A0A0D9QY32, A0A016S8J7

Protien has one to many association 

'''  

#end of code I wrote 