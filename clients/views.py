"""
Vues de l'application clients.

Ce module contient toutes les vues nécessaires pour la gestion des clients,
incluant la création, la modification, la suppression et l'affichage des clients.
Chaque vue est protégée par le décorateur @login_required pour assurer
que seuls les utilisateurs authentifiés peuvent y accéder.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import Client
from devis.models import Devis
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
import csv
from datetime import datetime

@login_required
def home_client(request):
    """
    Vue principale pour la gestion des clients.
    
    Cette vue affiche la page d'accueil de la section clients avec
    les différentes options de navigation disponibles.
    
    Args:
        request: La requête HTTP
        
    Returns:
        HttpResponse: La page d'accueil des clients
    """
    return render(request, 'clients/index.html')

@login_required
def client_list(request):
    """
    Vue pour afficher la liste de tous les clients.
    
    Cette vue gère l'affichage paginé de tous les clients dans le système.
    Les clients sont triés par nom et affichés 10 par page.
    
    Args:
        request: La requête HTTP
        
    Returns:
        HttpResponse: La page HTML avec la liste paginée des clients
    """
    clients = Client.objects.all().order_by('nom')
    paginator = Paginator(clients, 10)  # 10 clients par page
    page = request.GET.get('page')
    clients = paginator.get_page(page)
    return render(request, 'clients/client_list.html', {'clients': clients})

@login_required
def client_detail(request, pk):
    """
    Vue pour afficher les détails d'un client spécifique.
    
    Cette vue affiche toutes les informations d'un client, y compris
    son historique de devis et des statistiques sur ses devis.
    
    Args:
        request: La requête HTTP
        pk: L'identifiant unique du client
        
    Returns:
        HttpResponse: La page HTML avec les détails du client
    """
    client = get_object_or_404(Client, pk=pk)
    devis = Devis.objects.filter(client=client).order_by('-date_creation')
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'devis': devis
    })

@login_required
def client_create(request):
    """
    Vue pour créer un nouveau client.
    
    Cette vue gère le processus de création d'un nouveau client :
    1. Affiche le formulaire de création si la méthode est GET
    2. Traite les données soumises si la méthode est POST
    3. Crée le client et redirige vers sa page de détails
    
    Args:
        request: La requête HTTP
        
    Returns:
        HttpResponse: Le formulaire de création ou redirection vers le détail
    """
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        notes = request.POST.get('notes')
        
        # Création du client
        client = Client.objects.create(
            nom=nom,
            email=email,
            téléphone=telephone,
            adresse=adresse,
            notes=notes,
            cree_par=request.user
        )
        
        messages.success(request, 'Client créé avec succès!')
        return redirect('clients:client_detail', pk=client.pk)
    
    return render(request, 'clients/client_form.html')

@login_required
def client_update(request, pk):
    """
    Vue pour modifier un client existant.
    
    Cette vue gère le processus de modification d'un client :
    1. Affiche le formulaire pré-rempli si la méthode est GET
    2. Traite les données soumises si la méthode est POST
    3. Met à jour le client et redirige vers sa page de détails
    
    Args:
        request: La requête HTTP
        pk: L'identifiant unique du client à modifier
        
    Returns:
        HttpResponse: Le formulaire de modification ou redirection vers le détail
    """
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        # Mise à jour des données du client
        client.nom = request.POST.get('nom')
        client.email = request.POST.get('email')
        client.telephone = request.POST.get('telephone')
        client.adresse = request.POST.get('adresse')
        client.notes = request.POST.get('notes')
        client.save()
        
        messages.success(request, 'Client mis à jour avec succès!')
        return redirect('clients:client_detail', pk=client.pk)
    
    return render(request, 'clients/client_form.html', {'client': client})

@login_required
def client_delete(request, pk):
    """
    Vue pour supprimer un client.
    
    Cette vue gère le processus de suppression d'un client :
    1. Vérifie qu'aucun devis n'est associé au client
    2. Affiche une page de confirmation si la méthode est GET
    3. Supprime le client si la méthode est POST
    
    Args:
        request: La requête HTTP
        pk: L'identifiant unique du client à supprimer
        
    Returns:
        HttpResponse: La page de confirmation ou redirection vers la liste
    """
    client = get_object_or_404(Client, pk=pk)
    
    # Vérification de l'existence de devis associés
    if Devis.objects.filter(client=client).exists():
        messages.error(request, 'Impossible de supprimer ce client car il a des devis associés.')
        return redirect('clients:client_detail', pk=client.pk)
    
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé avec succès!')
        return redirect('clients:client_list')
    
    return render(request, 'clients/client_confirm_delete.html', {'client': client})

@login_required
def client_export_csv(request):
    """
    Exporte la liste des clients en format CSV.
    
    Cette vue génère un fichier CSV contenant toutes les informations
    des clients, y compris leurs statistiques de devis.
    
    Args:
        request: La requête HTTP
        
    Returns:
        HttpResponse: Le fichier CSV généré avec les en-têtes appropriés
    """
    # Configuration de la réponse HTTP
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="clients_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    # En-têtes du CSV
    writer.writerow([
        'Nom', 'Email', 'Téléphone', 'Adresse',
        'Nombre total de devis', 'Devis acceptés',
        'Montant total des devis acceptés'
    ])
    
    # Écriture des données des clients
    clients = Client.objects.all().order_by('nom')
    for client in clients:
        writer.writerow([
            client.nom,
            client.email,
            client.telephone,
            client.adresse,
            client.nombre_devis(),
            client.nombre_devis_acceptes(),
            f"{client.montant_total_devis_acceptes():.2f} €"
        ])
    
    return response

def register(request):
    """
    Vue pour l'inscription des nouveaux utilisateurs.
    
    Cette vue gère le processus d'inscription des nouveaux utilisateurs :
    1. Affiche le formulaire d'inscription si la méthode est GET
    2. Traite les données soumises si la méthode est POST
    3. Crée le compte et redirige vers la page de connexion
    
    Args:
        request: La requête HTTP
        
    Returns:
        HttpResponse: Le formulaire d'inscription ou redirection vers la connexion
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé avec succès pour {username}! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    """
    Vue personnalisée pour la déconnexion.
    
    Cette vue gère le processus de déconnexion des utilisateurs :
    1. Déconnecte l'utilisateur
    2. Affiche un message de confirmation
    3. Redirige vers la page de connexion
    
    Args:
        request: La requête HTTP
        
    Returns:
        HttpResponse: Redirection vers la page de connexion
    """
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')
