from django.db import models


class Organism(models.Model):
    taxaId = models.CharField(max_length=256, null=False, blank=False)
    clade = models.CharField(max_length=256, null=False, blank=True)
    genus = models.CharField(max_length=256, null=False, blank=True)
    species = models.CharField(max_length=256, null=False, blank=True)

    def __str__(self):
        return self.taxaId

'''
Protein is associated with one or more Taxa_id 
such as U6M9K5, D2CJZ4, A0A1D5QV06, A0A1D6FYR9, A0A194WA83, A0A177U724, A0A177BX17, A0A1A8N5W2, A0A0P5IGI0,
 A0A0V1IMU6, A0A0D9QY32, A0A016S8J7

 Protien has one to many association 
'''   
class Protein(models.Model):
    proteinId = models.CharField(max_length=256, null=False, blank=False)
    sequence = models.CharField(max_length=256, blank=True)
    length = models.IntegerField(null=False, blank=True)

    organism = models.ForeignKey(Organism, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.proteinId


class Domain(models.Model):
    domainId = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=256, null=False, blank=True)
    
    protien = models.ForeignKey("Protein", blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.domainId


class ProteinOrganismLink(models.Model):
    protein =  models.ForeignKey(Protein, on_delete=models.DO_NOTHING)
    organism = models.ForeignKey(Organism, on_delete=models.DO_NOTHING)
    start = models.IntegerField(null=False, blank=True)
    stop = models.IntegerField(null=False, blank=True)

    def __str__(self):
        return f"{self.protein.proteinId}_{self.organism.taxaId[:4]}"


class Pfam(models.Model):
    domainId = models.CharField(max_length=256, null=False, blank=False)
    domainFamDesc = models.CharField(max_length=256, null=False, blank=True)

    def __str__(self):
        return self.domainId
