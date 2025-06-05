"""
Configuration des URLs de l'application clients.

Ce module définit toutes les routes URL pour l'application clients,
organisées par catégorie fonctionnelle. Chaque route est associée
à une vue spécifique qui gère la logique correspondante.
"""

from django.urls import path
from . import views

app_name = 'clients'

# Configuration des URLs de l'application clients
urlpatterns = [
    # Liste des clients
    # Affiche la liste paginée de tous les clients
    path('', views.client_list, name='client_list'),
    
    # Actions sur les clients
    # Création d'un nouveau client
    path('nouveau/', views.client_create, name='client_create'),
    # Affichage des détails d'un client spécifique
    path('<int:pk>/', views.client_detail, name='client_detail'),
    # Modification d'un client existant
    path('<int:pk>/modifier/', views.client_update, name='client_update'),
    # Suppression d'un client
    path('<int:pk>/supprimer/', views.client_delete, name='client_delete'),
    
    # Export des clients
    # Export de la liste des clients au format CSV
    path('export/csv/', views.client_export_csv, name='client_export_csv'),
    
    # Authentification
    # Inscription d'un nouvel utilisateur
    path('register/', views.register, name='register'),
]
