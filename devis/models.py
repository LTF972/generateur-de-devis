from django.db import models
from django.conf import settings
from clients.models import Client
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal

def get_default_date_validite():
    """
    Retourne la date de validité par défaut (30 jours à partir d'aujourd'hui).
    Utilisé comme valeur par défaut pour le champ date_validite du modèle Devis.
    """
    return timezone.now().date() + timedelta(days=30)

def get_default_numero():
    """
    Génère un numéro de devis par défaut au format DEV-YYYYMM-0001.
    Utilisé comme valeur par défaut pour le champ numero du modèle Devis.
    """
    year_month = timezone.now().strftime('%Y%m')
    return f'DEV-{year_month}-0001'

class Devis(models.Model):
    """
    Modèle représentant un devis dans le système.
    
    Un devis est un document commercial qui détaille les produits/services proposés,
    leurs prix, et les conditions de vente. Il est lié à un client et peut avoir
    plusieurs lignes de devis.
    
    Attributs:
        numero (str): Numéro unique du devis, généré automatiquement
        client (ForeignKey): Référence au client concerné
        date_creation (DateTimeField): Date et heure de création du devis
        date_validite (DateField): Date jusqu'à laquelle le devis est valable
        montant_ht (DecimalField): Montant total hors taxes
        conditions_paiement (TextField): Conditions de paiement spécifiées
        notes (TextField): Notes additionnelles sur le devis
        statut (CharField): État du devis (brouillon, envoyé, accepté, refusé)
        cree_par (ForeignKey): Utilisateur ayant créé le devis
    """
    
    # Choix possibles pour le statut du devis
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyé'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]
    
    # Champs principaux
    numero = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Numéro",
        help_text="Numéro unique du devis"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='devis',
        verbose_name="Client",
        help_text="Client concerné par le devis"
    )
    
    # Champs de dates
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
        help_text="Date et heure de création du devis"
    )
    date_validite = models.DateField(
        default=get_default_date_validite,
        verbose_name="Date de validité",
        help_text="Date jusqu'à laquelle le devis est valable"
    )
    
    # Champs financiers
    montant_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Montant HT",
        help_text="Montant total hors taxes"
    )
    
    # Champs de texte
    conditions_paiement = models.TextField(
        verbose_name="Conditions de paiement",
        help_text="Conditions de paiement spécifiées"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes",
        help_text="Notes additionnelles sur le devis"
    )
    
    # Champs système
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='brouillon',
        verbose_name="Statut",
        help_text="État actuel du devis"
    )
    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Créé par",
        help_text="Utilisateur ayant créé le devis"
    )
    
    class Meta:
        """Métadonnées du modèle"""
        verbose_name = "Devis"
        verbose_name_plural = "Devis"
        ordering = ['-date_creation']  # Tri par date de création décroissante
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['date_creation']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        """Représentation textuelle du devis"""
        return f"Devis {self.numero} - {self.client.nom}"
    
    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour générer automatiquement le numéro de devis
        si celui-ci n'existe pas encore.
        """
        if not self.numero:
            # Format: DEV-YYYYMM-XXXX où XXXX est un numéro séquentiel
            year_month = timezone.now().strftime('%Y%m')
            last_devis = Devis.objects.filter(
                numero__startswith=f'DEV-{year_month}'
            ).order_by('-numero').first()
            
            if last_devis:
                last_num = int(last_devis.numero.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
                
            self.numero = f'DEV-{year_month}-{new_num:04d}'
        
        super().save(*args, **kwargs)
    
    @property
    def montant_ttc(self):
        """
        Calcule le montant TTC du devis (HT + TVA 20%).
        Propriété calculée à la volée.
        """
        return self.montant_ht * Decimal('1.20')

class LigneDevis(models.Model):
    """
    Modèle représentant une ligne dans un devis.
    
    Une ligne de devis détaille un produit ou service spécifique,
    avec sa description, quantité, prix unitaire et montant total.
    
    Attributs:
        devis (ForeignKey): Référence au devis parent
        description (TextField): Description détaillée du produit/service
        quantite (IntegerField): Quantité commandée
        prix_unitaire (DecimalField): Prix unitaire hors taxes
        montant (DecimalField): Montant total de la ligne (quantité * prix unitaire)
    """
    
    # Relations
    devis = models.ForeignKey(
        Devis,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name="Devis",
        help_text="Devis parent"
    )
    
    # Champs de description
    description = models.TextField(
        verbose_name="Description",
        help_text="Description détaillée du produit ou service"
    )
    
    # Champs numériques
    quantite = models.PositiveIntegerField(
        verbose_name="Quantité",
        help_text="Quantité commandée"
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire",
        help_text="Prix unitaire hors taxes"
    )
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name="Montant",
        help_text="Montant total de la ligne (calculé automatiquement)"
    )
    
    class Meta:
        """Métadonnées du modèle"""
        verbose_name = "Ligne de devis"
        verbose_name_plural = "Lignes de devis"
        ordering = ['id']  # Tri par ordre d'ajout
    
    def __str__(self):
        """Représentation textuelle de la ligne de devis"""
        return f"{self.description} - {self.quantite} x {self.prix_unitaire}€"
    
    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour calculer automatiquement le montant
        de la ligne et mettre à jour le montant total du devis.
        """
        # Calcul du montant de la ligne
        self.montant = self.quantite * self.prix_unitaire
        
        # Sauvegarde de la ligne
        super().save(*args, **kwargs)
        
        # Mise à jour du montant total du devis
        self.devis.montant_ht = sum(ligne.montant for ligne in self.devis.lignes.all())
        self.devis.save()
