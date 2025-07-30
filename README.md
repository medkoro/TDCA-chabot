# Chatbot Alten - Gestion des Demandes

Un système de gestion des demandes avec interface chatbot, développé avec Django et PostgreSQL.

## 📋 Description

Ce projet est une application web qui permet de gérer les demandes techniques avec un système de suivi, d'audit et d'évaluation de satisfaction. Il inclut un chatbot pour faciliter l'interaction avec le système.

## 🛠️ Prérequis

- Python 3.8 ou supérieur
- PostgreSQL
- pip (gestionnaire de paquets Python)

## 🚀 Installation

1. **Cloner le dépôt**
   ```bash
   git clone [URL_DU_REPO]
   cd TDCA-chabot
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Sur Windows
   # ou
   source .venv/bin/activate  # Sur macOS/Linux
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🗄️ Configuration de la base de données

1. **Créer une base de données PostgreSQL**
   - Nom: `chatbotalten`
   - Utilisateur: `postgres`
   - Mot de passe: `moha.2003.`
   - Hôte: `localhost`
   - Port: `5432`

   Ou modifier ces paramètres dans `ChatbotAlten/settings.py` selon votre configuration.

2. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

3. **Créer un superutilisateur (admin)**
   ```bash
   python manage.py createsuperuser
   ```

## 🏃‍♂️ Lancer l'application

```bash
python manage.py runserver
```

Accédez à l'application à l'adresse : http://127.0.0.1:8000/

## 📊 Structure de la base de données

### Modèles principaux

1. **Responsable**
   - Identifiant (PK)
   - Nom
   - Prénom

2. **Application**
   - Nom de l'application
   - Périmètre

3. **Demande**
   - Référence (PK)
   - Application (FK)
   - Dates d'ouverture/fermeture
   - Catégorie
   - Commentaire
   - Demandeur (FK vers Responsable)
   - Orientation

4. **Transfert**
   - Référence de la demande (FK)
   - Expert (FK vers Responsable)
   - Support (FK vers Responsable)
   - Date de transfert

5. **Audit**
   - Demande (FK)
   - Résultat de l'audit
   - Auditeur (FK vers Responsable)
   - Date d'audit

6. **Satisfaction**
   - Demande (FK)
   - Score

7. **Historique**
   - Requête
   - Réponse
   - Date de la requête
   - ID de conversation

## 🔒 Variables d'environnement

Pour des raisons de sécurité, il est recommandé de déplacer les informations sensibles (comme les mots de passe) dans des variables d'environnement.

## 🤖 Fonctionnalités du Chatbot

- Gestion des demandes techniques
- Suivi des transferts entre experts
- Évaluation de la satisfaction
- Historique des conversations
- Génération de graphiques et statistiques sur les demandes (via commandes du chatbot ou API)

## 🛡️ Gestion et administration des données

- **Toutes les données (demandes, applications, responsables, etc.) peuvent être ajoutées, modifiées ou supprimées via l'interface Django admin** :
  - Accédez à l'administration à l'adresse : http://127.0.0.1:8000/admin/
  - Connectez-vous avec votre superutilisateur
  - Tous les modèles sont disponibles pour une gestion complète

## 📈 Visualisation et statistiques

- Les graphiques ne sont plus affichés en permanence dans l'interface principale.
- Pour obtenir des statistiques ou des graphiques, utilisez les commandes du chatbot (ex : "Montre-moi les demandes par catégorie") ou accédez aux endpoints API (voir `views.py`).
- Les résultats s'affichent dans le chat ou peuvent être intégrés dans d'autres interfaces selon vos besoins.

## 🛠️ Dépannage courant

- **Aucune donnée dans les graphiques/statistiques ?**
  - Vérifiez que vous avez bien ajouté des "Demandes" et autres objets via l'admin.
  - Rafraîchissez la page après modification des données.

- **Impossible d'accéder à l'admin ?**
  - Utilisez : http://127.0.0.1:8000/admin/
  - Si besoin, créez un superutilisateur :
    ```bash
    python manage.py createsuperuser
    ```

- **Problème d'affichage ou bug ?**
  - Vérifiez la console du navigateur et les logs du serveur Django pour plus d'informations.

## 📝 Notes supplémentaires

- Le projet utilise LangChain pour l'intégration avec des modèles de langage
- L'interface d'administration Django est disponible à `/admin`
- Les données sont stockées dans une base PostgreSQL

## 📄 Licence

[À spécifier]
