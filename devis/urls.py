"""
Configuration des URLs de l'application devis.

Ce module définit toutes les routes URL pour l'application devis,
organisées par catégorie fonctionnelle. Chaque route est associée
à une vue spécifique qui gère la logique correspondante.
"""

from django.urls import path
from . import views

app_name = 'devis'

urlpatterns = [
    # Liste des devis
    # Affiche la liste de tous les devis
    path('', views.devis_list, name='devis_list'),
    # Affiche la liste des devis en cours (brouillon ou envoyé)
    path('en-cours/', views.devis_en_cours, name='devis_en_cours'),
    # Affiche la liste des devis terminés (acceptés ou refusés)
    path('termines/', views.devis_termines, name='devis_termines'),
    
    # Actions sur les devis
    # Création d'un nouveau devis
    path('nouveau/', views.devis_create, name='devis_create'),
    # Affichage des détails d'un devis spécifique
    path('<int:pk>/', views.devis_detail, name='devis_detail'),
    # Modification d'un devis existant
    path('<int:pk>/modifier/', views.devis_update, name='devis_update'),
    # Suppression d'un devis
    path('<int:pk>/supprimer/', views.devis_delete, name='devis_delete'),
    # Finalisation d'un devis (acceptation ou refus)
    path('<int:pk>/terminer/', views.devis_terminer, name='devis_terminer'),
    
    # Export des devis
    # Export d'un devis au format PDF
    path('<int:pk>/export/pdf/', views.devis_export_pdf, name='devis_export_pdf'),
    # Export d'un devis au format Excel
    path('<int:pk>/export/excel/', views.devis_export_excel, name='devis_export_excel'),
    # Export d'un devis au format Word
    path('<int:pk>/export/word/', views.devis_export_word, name='devis_export_word'),
    # Export de la liste des devis au format CSV
    path('export/csv/', views.devis_export_csv, name='devis_export_csv'),
]
