"""
Django settings for generateur_de_devis project.

Ce fichier contient toutes les configurations du projet Django.
Il définit les paramètres de base de données, les applications installées,
les middlewares, les templates, et d'autres configurations essentielles.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
# Ces variables contiennent des informations sensibles comme les clés secrètes
# et les identifiants de base de données
load_dotenv()

# Définition du chemin de base du projet
# Ce chemin est utilisé pour construire les chemins relatifs dans le projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuration de sécurité
# Ces paramètres sont critiques pour la sécurité de l'application
SECRET_KEY = os.getenv('SECRET_KEY')  # Clé secrète pour le chiffrement
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Mode debug (désactivé en production)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')  # Hôtes autorisés

# Liste des applications installées
# Inclut les applications Django par défaut et nos applications personnalisées
INSTALLED_APPS = [   
    'clients',  # Application de gestion des clients
    'devis',    # Application de gestion des devis
    'django.contrib.admin',  # Interface d'administration
    'django.contrib.auth',   # Système d'authentification
    'django.contrib.contenttypes',  # Framework de types de contenu
    'django.contrib.sessions',  # Gestion des sessions
    'django.contrib.messages',  # Système de messages
    'django.contrib.staticfiles',  # Gestion des fichiers statiques
    'crispy_forms',  # Amélioration des formulaires
    'crispy_bootstrap5',  # Intégration Bootstrap 5
]

# Middleware
# Ces composants sont exécutés dans l'ordre pour chaque requête
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Sécurité
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sessions
    'django.middleware.common.CommonMiddleware',  # Fonctionnalités communes
    'django.middleware.csrf.CsrfViewMiddleware',  # Protection CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentification
    'django.contrib.messages.middleware.MessageMiddleware',  # Messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protection clickjacking
]

# Configuration des URLs
ROOT_URLCONF = 'generateur_de_devis.urls'

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'clients.context_processors.clients_list',  # Liste des clients pour tous les templates
            ],
        },
    },
]

# Configuration WSGI
WSGI_APPLICATION = 'generateur_de_devis.wsgi.application'

# Configuration de la base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),      # Nom de la base de données
        'USER': os.getenv('DB_USER'),      # Utilisateur
        'PASSWORD': os.getenv('DB_PASSWORD'),  # Mot de passe
        'HOST': os.getenv('DB_HOST'),      # Hôte
        'PORT': os.getenv('DB_PORT'),      # Port
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuration de l'internationalisation
LANGUAGE_CODE = 'fr-fr'  # Langue par défaut
TIME_ZONE = 'Europe/Paris'  # Fuseau horaire
USE_I18N = True  # Internationalisation
USE_TZ = True  # Support des fuseaux horaires

# Configuration des fichiers statiques
STATIC_URL = 'static/'  # URL pour les fichiers statiques
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Dossier des fichiers statiques
]

# Configuration des fichiers média
MEDIA_URL = '/media/'  # URL pour les fichiers média
MEDIA_ROOT = BASE_DIR / 'media'  # Dossier des fichiers média

# Configuration du champ clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration des redirections d'authentification
LOGIN_URL = '/accounts/login/'  # URL de connexion
LOGIN_REDIRECT_URL = '/clients/'  # Redirection après connexion
LOGOUT_REDIRECT_URL = '/accounts/login/'  # Redirection après déconnexion

# Configuration de Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # Pack de templates autorisé
CRISPY_TEMPLATE_PACK = "bootstrap5"  # Pack de templates par défaut

# Configuration de l'envoi d'emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Backend SMTP
EMAIL_HOST = os.getenv('EMAIL_HOST')  # Serveur SMTP
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # Port SMTP
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'  # Utilisation de TLS
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Utilisateur SMTP
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Mot de passe SMTP
