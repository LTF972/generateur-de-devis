# clients/signals.py
import csv
import os
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client
from django.conf import settings

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Client)
def enregistrer_client_csv(sender, instance, created, **kwargs):
    if created:
        try:
            # Chemin du fichier CSV (configurable via settings)
            file_path = getattr(settings, 'CLIENTS_CSV_PATH', 
                              os.path.join(settings.BASE_DIR, 'clients_data.csv'))

            # Vérifie si le fichier existe
            file_exists = os.path.isfile(file_path)

            # Vérifie si les données sont valides
            if not instance.nom or not instance.email:
                logger.warning(f"Données client invalides: nom={instance.nom}, email={instance.email}")
                return

            # Ouvre le fichier en mode ajout
            with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Écrit l'en-tête si le fichier est nouveau
                if not file_exists:
                    writer.writerow(['Nom', 'Email'])

                # Écrit les données du nouveau client
                writer.writerow([instance.nom, instance.email])
                
            logger.info(f"Client {instance.nom} enregistré avec succès dans le fichier CSV")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement du client dans le CSV: {str(e)}")
