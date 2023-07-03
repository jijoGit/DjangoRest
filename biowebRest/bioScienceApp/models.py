'''
This data provides specific details about the protein, including its unique identifier (A0A014PQC0), 
the taxonomic ID of the organism it is found in (568076), its clade (E), 
the species (Metarhizium robertsii), 
and a description of the protein's function (Glyceraldehyde 3-phosphate dehydrogenase catalytic domain).
 The domain ID (PF02800) is a reference to a protein family or domain,
   and the start and stop positions (157 and 314) 
   indicate the positions within the protein sequence where this specific domain is located. 
The length (338) represents the total length of the protein sequence.

A single protein can have multiple domains, and each domain may have a different domain ID.

'''

from django.db import models

class Taxonomy(models.Model):
    taxa_id = models.CharField(max_length=256, null=False, blank=False)
    clade = models.CharField(max_length=256, null=False, blank=True)
    genus = models.CharField(max_length=256, null=False, blank=True)
    species = models.CharField(max_length=256, null=False, blank=True)
 
    def __str__(self):
        return self.taxa_id

    def get_proteins(self):
        return Protein.objects.filter(taxonomy=self)
    
    def get_pfams(self):
        return Pfam.objects.filter(proteindomainlink__protein__taxonomy=self)
    
class Protein(models.Model):
    protein_id = models.CharField(max_length=256, null=False, blank=False)
    sequence = models.CharField(max_length=256, blank=True)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING)
    length = models.IntegerField(null=False, blank=True)

    def get_taxonomy(self):
        return self.taxonomy.all()
    
        # That is Sum of the protein domain lengths (start-stop)/length of protein.
    def get_coverage(self):
        protein_domains = self.domain.all()
        print(protein_domains)
        if protein_domains.exists():
            domain_lengths = sum(domain.stop - domain.start for domain in protein_domains)
            return domain_lengths / self.length
        else:
            return 0


    def __str__(self):
        return self.protein_id
    

class Pfam(models.Model):
    domain_id = models.CharField(max_length=256, null=False, blank=False)
    domain_description = models.CharField(max_length=256, null=False, blank=True)

    def __str__(self):
        return self.domain_id
    

class ProteinDomainLink(models.Model):
    protein =  models.ForeignKey(Protein, on_delete=models.DO_NOTHING, related_name='domain')
    pfam_id = models.ForeignKey(Pfam, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=256, null=False, blank=True)
    start = models.IntegerField(null=False, blank=True)
    stop = models.IntegerField(null=False, blank=True)

    def get_protein(self):
        return self.protein.all()
    
    def get_pfam(self):
        return self.pfam_id.all()
    

    

    def __str__(self):
        return f"{self.protein.protein_id}_{self.pfam_id.domain_id[:8]}"



'''
Organism has one to many relation with Protein 
such as '2711','2880','3218'

Protein is associated with one or more Taxa_id 
such as U6M9K5, D2CJZ4, A0A1D5QV06, A0A1D6FYR9, A0A194WA83, A0A177U724, A0A177BX17, A0A1A8N5W2, A0A0P5IGI0,
A0A0V1IMU6, A0A0D9QY32, A0A016S8J7

Protien has one to many association 

'''  