# Generated by Django 5.2.1 on 2025-05-26 18:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_client_options_client_adresse_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20, unique=True, verbose_name='Numéro de devis')),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de création')),
                ('date_validite', models.DateField(verbose_name='Date de validité')),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Montant total')),
                ('statut', models.CharField(choices=[('en_cours', 'En cours'), ('termine', 'Terminé'), ('annule', 'Annulé')], default='en_cours', max_length=20, verbose_name='Statut')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients_devis', to='clients.client', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Devis',
                'verbose_name_plural': 'Devis',
                'ordering': ['-date_creation'],
            },
        ),
    ]
