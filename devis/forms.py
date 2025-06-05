from django import forms
from .models import Devis

class DevisForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = [
            'client',
            'date_validite',
            'conditions_paiement',
            'notes',
            # Ajoutez ici d'autres champs du modèle Devis si nécessaire
        ]