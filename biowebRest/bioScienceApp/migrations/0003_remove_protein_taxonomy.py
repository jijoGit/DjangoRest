# Generated by Django 4.0.6 on 2023-07-03 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bioScienceApp', '0002_alter_pfam_domain_id_alter_protein_protein_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protein',
            name='taxonomy',
        ),
    ]
