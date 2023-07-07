
import csv
import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biowebRest.settings')
django.setup()

from collections import defaultdict
from bioScienceApp.models import *



class FileDataReader:
    '''

    Returns four dicts with data from files 

    initiation: 
    data_reader = FileDataReader(data_sequences_file='data_sequences.csv', assignment_data_set='assignment_data_set.csv', pfam_descriptions='pfam_descriptions.csv')

    usage: 
    proteins, organisms, protein_organism, domains = data_reader.read_data()
    

    '''
    def __init__(self, assignment_data_set):
        self.assignment_data_set = Path(assignment_data_set)
        self.proteins = defaultdict(list)
        self.organisms = defaultdict(list)
        self.protein_organism = defaultdict(list)
        self.pfams = defaultdict(dict)
        self.domains = defaultdict(list)


    def read_data(self):
        with open(self.assignment_data_set) as csv_file:
            csv_reader_assignment_data = csv.reader(csv_file, delimiter=',')
            for row in csv_reader_assignment_data:
                proteinId, taxaId, clade, genusSpecies, domainDesc, domainId, start, end, proteinLength = row

                self.proteins = self.add_proteins(proteinId, proteinLength, taxaId, self.proteins)
                self.organisms = self.add_organisms(taxaId, clade, genusSpecies, proteinId, self.organisms)
                self.protein_organism = self.add_protein_organisms(self.protein_organism, proteinId, taxaId)
                self.domains = self.add_domains(domainId, domainDesc, proteinId, start, end, self.domains)

        return self.proteins , self.organisms, self.protein_organism , self.domains
    
    def add_proteins(selc, protein_id,protein_length,taxa_id,container):
        if not taxa_id:
            taxa_id = ''
        # adding 'length' and organism. to proteins dict. 
        if protein_id in container:
            #since the protein is already there, lenght has to be appended to.
            # print('duplicate:', protein_id);
            if (len(container[protein_id]) == 1):
                container[protein_id].append(protein_length)
                container[protein_id].append(taxa_id)
            # else: same information not needed to add
        else:
            # as Protein Sequence is not there, it is substituted with empty string
            container[protein_id] = [protein_length,taxa_id]
                   
        return container
    
    def add_organisms(self, taxa_id, clade, genus_species, protein_id ,container):
        # split_list[1] is Organism TAXA ID
        if not taxa_id in container:
            genus, species = genus_species.split(' ',1)
            container[taxa_id] = [clade, genus, species, protein_id]
        else: #not likely 
            #is the Organism Clade Idenitifer and Genus Species different
            if not container[taxa_id][0] == clade:
                print( container[taxa_id] + ' clade is different ')
            elif not container[taxa_id][1] in genus_species:
                print( container[taxa_id] + ' specis is different ' + genus_species)

        return container
    

    def add_protein_organisms(self, container, protein_id, taxa_id=''):
        '''
        junction table to connect protein and organism as 
        "organisms are made of one or more cells. Each cell contains DNA and proteins. 
        Each protein has a biochemical function". 
        
        for case: Organisms can have more proteins 
        '''

        if taxa_id =='':
            print('protein_id dont have taxa id', protein_id)

        #keeping track of a protein connected to mmultiple taxa_id
        if protein_id in container:
            if not taxa_id in container[protein_id]:
                container[protein_id].append(taxa_id)
            #else do not do anything ignore 
        
        #otherwise just add it as first entry
        else:
            container[protein_id] = [taxa_id]

        return(container)
    
    def add_domains(self, domain_id, desc, protein_id, start, end, container):
        if domain_id not in container:
            container[domain_id] = {'desc': desc, 'start': start, 'end': end, 'protein_ids': {protein_id}}
        else:
            existing_values = container[domain_id]
            if existing_values['desc'] == desc and existing_values['start'] == start and existing_values['end'] == end:
                if protein_id in existing_values['protein_ids']:
                    raise ValueError(f"add_domains: domain_id and protein_id are not unique: {domain_id}, {protein_id}")
                else:
                    existing_values['protein_ids'].add(protein_id)
            else:
                existing_values['protein_ids'].add(protein_id)

        return container


class PfamDatabaseWriter:
    def __init__(self, pfam_descriptions):
        self.pfam_descriptions = Path(pfam_descriptions)
        self.pfam_rows = {}

    def add_pfam(self):
        with open(self.pfam_descriptions) as csv_file:
            csv_reader_pfam_descriptions = csv.reader(csv_file, delimiter='\n')
            for row in csv_reader_pfam_descriptions:
                split_list = row[0].split(',')
                domainId = split_list[0]
                domainFamDesc = split_list[1]

                pfam = Pfam(domainId=domainId, domain_description=domainFamDesc)
                pfam.save()

                self.pfam_rows[domainId] = pfam

        return self.pfam_rows
    

class SequenceDBWriter:
    def __init__(self, data_sequences_file):
        self.data_sequences_file = Path(data_sequences_file)

    def add_sequence(self):
        with open(self.data_sequences_file) as csv_file:
            csv_reader_data_sequences = csv.reader(csv_file, delimiter='\n')
            for row in csv_reader_data_sequences:
                tupple = row[0].split(',')
                proteinId = tupple[0]
                sequence = tupple[1]

                try:
                    protein = Protein.objects.get(proteinId=proteinId)
                    protein.sequence = sequence
                    protein.save()
                except Protein.DoesNotExist:
                    print(f"Protein with ID {proteinId} does not exist.")

        print('Done Sequence table ') 



class DatabaseWriter:
    def __init__(self, proteins, organisms, protein_organisms, domains, pfam_read_writer, sequence_read_writer):
        self.pfam_read_writer = pfam_read_writer
        self.proteins= proteins
        self.organisms = organisms
        self.protein_organisms = protein_organisms
        self.domains = domains 
        self.sequence_read_writer = sequence_read_writer

    def populate_organisms_table(self):
        organism_rows = {}

        for organism_id in self.organisms:
            content_list = self.organisms[organism_id]
            if len(content_list)==4:
                row = Taxonomy.objects.create(taxaId=organism_id, clade=content_list[0], genus=content_list[1], species=content_list[2])           
                row.save()
            else: 
                print('error: populate_db, length is not = 3 for organism_id')

            organism_rows[organism_id]=row

        print('Done organisms table ')
        return organism_rows


    def populate_protein_table(self):
        protein_rows = {}
        for protein_id in self.proteins:
            content_list = self.proteins[protein_id]
            row = Protein.objects.create(proteinId=protein_id, length=content_list[1])
            row.save()
            protein_rows[protein_id] = row
            
        print('Done Protein table ')
        return protein_rows

    
    def populate_taxonomy_Protein_table(self, organism_rows, protein_rows):

        organism_protein_rows = {}

        for protein, org_list in self.protein_organisms.items():
            for taxa_id in org_list:
                # print(taxa_id)
                row = TaxonomyProteinLink.objects.create(taxonomy=organism_rows[taxa_id],
                                                         protein=protein_rows[protein])
                row_name = f"{protein}_{taxa_id}"
                organism_protein_rows[row_name] = row
        print('Done taxonomy_Protein table ')  
        return organism_protein_rows
    
    def populate_pfam_table(self):
        pfam_rows = self.pfam_read_writer.add_pfam()
        print('Done Pfam table ') 
        return pfam_rows
    
    def populate_Protein_domainLink_table(self, protein_rows, domains, pfam_rows):
        '''PF02800 domain is connected with {'A0A014PQC0', 'B2CK99', 'A0A1B2CT05'} '''
        domain_rows = {}
        for domain_id, domain_list in self.domains.items():
            for protein_id in domain_list['protein_ids']:
                row = ProteinDomainLink.objects.create(
                    protein = protein_rows[protein_id],
                    description = domain_list['desc'],
                    pfam = pfam_rows[domain_id],
                    start = domain_list['start'],
                    stop = domain_list['end'])
                row.save()
                domain_rows[domain_id] = row
        
        print('Done Domain table ')       
        return domain_rows
    
    def delete_all_tables(self):
        TaxonomyProteinLink.objects.all().delete()
        ProteinDomainLink.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()
        Pfam.objects.all().delete()

        print('tables deleted')

    def populate_tables(self):
        self.delete_all_tables()
        organism_rows = self.populate_organisms_table()
        protein_rows = self.populate_protein_table()
        organism_protein_rows = self.populate_taxonomy_Protein_table(organism_rows, protein_rows)
        pfam_rows = self.populate_pfam_table()
        domain_rows = self.populate_Protein_domainLink_table(protein_rows, self.domains, pfam_rows)
        self.sequence_read_writer.add_sequence()


if __name__ == '__main__':

    data_reader = FileDataReader(assignment_data_set='./csv/assignment_data_set.csv')
    proteins, organisms, protein_organisms, domains = data_reader.read_data()
    pfam_read_writer = PfamDatabaseWriter(pfam_descriptions='./csv/pfam_descriptions.csv')
    sequence_read_writer = SequenceDBWriter(data_sequences_file='./csv/assignment_data_sequences.csv')

    db_writer = DatabaseWriter(proteins, organisms, protein_organisms, domains, pfam_read_writer, sequence_read_writer)
    db_writer.populate_tables()
    print('script completed.')


    # def delete_all_tables():
    #     TaxonomyProteinLink.objects.all().delete()
    #     ProteinDomainLink.objects.all().delete()
    #     Taxonomy.objects.all().delete()
    #     Protein.objects.all().delete()
    #     Pfam.objects.all().delete()

    #     print('tables deleted')

    
    # delete_all_tables()