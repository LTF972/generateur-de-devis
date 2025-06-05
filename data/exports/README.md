# Générateur de Devis Professionnel

## Description
Application web moderne permettant la génération et la gestion de devis professionnels. Développée avec Django et React.js, cette solution offre une interface intuitive pour la création de devis, la gestion des clients et des produits.

## Technologies utilisées
- **Backend**: Python, Django
- **Frontend**: React.js
- **Base de données**: PostgreSQL
- **Autres**: API REST, HTML/CSS, JavaScript

## Fonctionnalités principales

### 1. Gestion des clients
- Création et modification de profils clients
- Historique des devis par client
- Informations de contact et adresses

### 2. Gestion des produits
- Catalogue de produits avec prix
- Catégorisation des produits
- Gestion des stocks

### 3. Génération de devis
- Interface de création intuitive
- Calcul automatique des totaux
- Gestion des taxes (TVA)
- Export en PDF et Excel

### 4. Interface utilisateur
- Design moderne et responsive
- Mode clair/sombre
- Navigation intuitive

## Structure du projet
```
generateur_de_devis/
├── backend/                 # Application Django
│   ├── devis/              # Application principale
│   ├── clients/            # Gestion des clients
│   └── products/           # Gestion des produits
├── frontend/               # Application React
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── pages/         # Pages de l'application
│   │   └── styles/        # Fichiers CSS
├── data/                   # Données et sauvegardes
└── docs/                   # Documentation
```

## Installation

### Prérequis
- Python 3.8+
- Node.js 14+
- PostgreSQL
- pip (gestionnaire de paquets Python)
- npm (gestionnaire de paquets Node.js)

### Étapes d'installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd generateur_de_devis
```

2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

3. Configurer la base de données PostgreSQL
- Créer une base de données
- Configurer les variables d'environnement dans le fichier .env

4. Lancer les migrations Django
```bash
python manage.py migrate
```

5. Installer les dépendances Node.js
```bash
cd frontend
npm install
```

6. Lancer l'application
```bash
# Backend (dans le dossier racine)
python manage.py runserver

# Frontend (dans le dossier frontend)
npm start
```

## Dépendances principales
- Django
- React.js
- PostgreSQL
- ReportLab (génération PDF)
- OpenPyXL (génération Excel)
- Python-docx (génération Word)

## Contribution
Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commiter vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pousser vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence
[À définir selon vos besoins]

## Contact
[Vos informations de contact] 