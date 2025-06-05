from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Client(models.Model):
    """
    Modèle représentant un client dans le système.
    
    Ce modèle stocke toutes les informations relatives à un client,
    y compris ses coordonnées et son historique d'interactions.
    
    Attributs:
        nom (str): Nom du client (personne ou entreprise)
        email (str): Adresse email de contact
        téléphone (str): Numéro de téléphone
        adresse (str): Adresse postale complète (optionnelle)
        notes (str): Notes additionnelles sur le client (optionnelles)
        date_creation (DateTimeField): Date et heure d'ajout du client
        cree_par (ForeignKey): Utilisateur ayant créé le client
    """
    
    # Champs obligatoires
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Nom complet du client ou de l'entreprise"
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Adresse email de contact principale"
    )
    téléphone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
        help_text="Numéro de téléphone de contact"
    )
    
    # Champs optionnels
    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Adresse",
        help_text="Adresse postale complète"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes",
        help_text="Notes additionnelles sur le client"
    )
    
    # Champs système
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
        help_text="Date et heure de création du client"
    )
    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Créé par",
        help_text="Utilisateur ayant créé le client"
    )
    
    class Meta:
        """Métadonnées du modèle"""
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom']  # Tri alphabétique par nom
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        """Représentation textuelle du client"""
        return self.nom
    
    def get_absolute_url(self):
        """
        Retourne l'URL pour accéder aux détails du client.
        Utilisé par Django pour la redirection après création/modification.
        """
        return reverse('clients:client_detail', args=[str(self.id)])
    
    @property
    def nombre_devis(self):
        """
        Retourne le nombre total de devis associés à ce client.
        Propriété calculée à la volée.
        """
        return self.devis.count()
    
    @property
    def devis_actifs(self):
        """
        Retourne le nombre de devis en cours (brouillon ou envoyé).
        Propriété calculée à la volée.
        """
        return self.devis.filter(statut__in=['brouillon', 'envoye']).count()
    
    @property
    def devis_acceptes(self):
        """
        Retourne le nombre de devis acceptés.
        Propriété calculée à la volée.
        """
        return self.devis.filter(statut='accepte').count()
    
    @property
    def montant_total_devis(self):
        """
        Retourne le montant total des devis acceptés.
        Propriété calculée à la volée.
        """
        return sum(devis.montant_ttc for devis in self.devis.filter(statut='accepte'))
    
    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour ajouter des validations
        ou des traitements supplémentaires si nécessaire.
        """
        # Validation supplémentaire si nécessaire
        if not self.nom:
            raise ValueError("Le nom du client est obligatoire")
        
        super().save(*args, **kwargs)
