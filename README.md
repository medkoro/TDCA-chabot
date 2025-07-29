<div align="center">

# 🤖 Chatbot Alten - Gestion des Demandes

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Un système intelligent de gestion des demandes avec interface chatbot*

[📋 Fonctionnalités](#-fonctionnalités) • [🚀 Installation](#-installation) • [📖 Documentation](#-documentation) • [🤝 Contribution](#-contribution)

</div>

---

## 📋 Description

> **Chatbot Alten** est une application web moderne qui révolutionne la gestion des demandes techniques grâce à un système de suivi intelligent, d'audit automatisé et d'évaluation de satisfaction en temps réel. Doté d'un chatbot conversationnel, il simplifie l'interaction entre les utilisateurs et le système de gestion.

### ✨ Fonctionnalités principales

- 🎯 **Gestion intelligente des demandes** - Suivi complet du cycle de vie
- 🔄 **Transferts automatisés** - Routage intelligent entre experts
- 📊 **Audit en temps réel** - Contrôle qualité automatique
- 💬 **Chatbot conversationnel** - Interface naturelle et intuitive
- 📈 **Tableau de bord** - Métriques et analytics avancés
- 🔔 **Notifications** - Alertes en temps réel
- 📱 **Interface responsive** - Compatible mobile et desktop

---

## 🛠️ Stack Technique

<table>
<tr>
<td align="center"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="40" height="40"/><br><b>Python 3.8+</b></td>
<td align="center"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" width="40" height="40"/><br><b>Django</b></td>
<td align="center"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" width="40" height="40"/><br><b>PostgreSQL</b></td>
<td align="center"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" width="40" height="40"/><br><b>HTML5</b></td>
<td align="center"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" width="40" height="40"/><br><b>CSS3</b></td>
</tr>
</table>

---

## 🚀 Installation

### Prérequis

Assurez-vous d'avoir installé :
- 🐍 Python 3.8 ou supérieur
- 🐘 PostgreSQL 13+
- 📦 pip (gestionnaire de paquets Python)
- 🌐 Git

### Installation rapide

1. **📥 Cloner le dépôt**
   ```bash
   git clone https://github.com/medkoro/TDCA-chabot.git
   cd TDCA-chabot
   ```

2. **🔧 Créer l'environnement virtuel**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **📦 Installer les dépendances**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### 🗄️ Configuration de la base de données

<details>
<summary>🔽 Cliquez pour voir la configuration détaillée</summary>

1. **Créer la base de données PostgreSQL**
   ```sql
   CREATE DATABASE chatbotalten;
   CREATE USER postgres WITH PASSWORD 'moha.2003.';
   GRANT ALL PRIVILEGES ON DATABASE chatbotalten TO postgres;
   ```

2. **Variables d'environnement** (recommandé)
   
   Créez un fichier `.env` à la racine du projet :
   ```env
   DEBUG=True
   SECRET_KEY=votre-clé-secrète-ici
   DB_NAME=chatbotalten
   DB_USER=postgres
   DB_PASSWORD=moha.2003.
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. **Appliquer les migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

</details>

### 🏃‍♂️ Démarrage

```bash
python manage.py runserver
```

🎉 **Votre application est maintenant accessible à** : http://127.0.0.1:8000/

---

## 📊 Architecture de la base de données

<details>
<summary>🔽 Voir le schéma complet de la base de données</summary>

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Responsable   │    │   Application   │    │    Demande      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • ID (PK)       │    │ • Nom           │◄───┤ • Référence(PK) │
│ • Nom           │    │ • Périmètre     │    │ • Date ouvert.  │
│ • Prénom        │    └─────────────────┘    │ • Date ferm.    │
└─────────────────┘                           │ • Catégorie     │
         ▲                                    │ • Commentaire   │
         │                                    │ • Demandeur(FK) │
         └────────────────────────────────────┤ • Orientation   │
                                              └─────────────────┘
                                                       ▲
                  ┌─────────────────┐                  │
                  │    Transfert    │──────────────────┘
                  ├─────────────────┤
                  │ • Demande (FK)  │
                  │ • Expert (FK)   │
                  │ • Support (FK)  │
                  │ • Date          │
                  └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Audit       │    │  Satisfaction   │    │   Historique    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Demande (FK)  │    │ • Demande (FK)  │    │ • Requête       │
│ • Résultat      │    │ • Score         │    │ • Réponse       │
│ • Auditeur(FK)  │    └─────────────────┘    │ • Date          │
│ • Date          │                           │ • ID conversat. │
└─────────────────┘                           └─────────────────┘
```

### Modèles détaillés

1. **🔑 Responsable**
   - Identifiant (PK)
   - Nom
   - Prénom

2. **📱 Application**
   - Nom de l'application
   - Périmètre

3. **📋 Demande**
   - Référence (PK)
   - Application (FK)
   - Dates d'ouverture/fermeture
   - Catégorie
   - Commentaire
   - Demandeur (FK vers Responsable)
   - Orientation

4. **🔄 Transfert**
   - Référence de la demande (FK)
   - Expert (FK vers Responsable)
   - Support (FK vers Responsable)
   - Date de transfert

5. **🔍 Audit**
   - Demande (FK)
   - Résultat de l'audit
   - Auditeur (FK vers Responsable)
   - Date d'audit

6. **⭐ Satisfaction**
   - Demande (FK)
   - Score

7. **📜 Historique**
   - Requête
   - Réponse
   - Date de la requête
   - ID de conversation

</details>

---

## 🤖 Fonctionnalités du Chatbot

<table>
<tr>
<td width="50%">

### 💬 **Interface conversationnelle**
- Traitement du langage naturel avec **LangChain**
- Réponses contextuelles intelligentes
- Historique des conversations persistant
- Support multilingue (FR/EN)

</td>
<td width="50%">

### 🎯 **Gestion intelligente**
- Création automatique de demandes
- Routage intelligent vers experts
- Suivi en temps réel des statuts
- Notifications proactives

</td>
</tr>
<tr>
<td>

### 📊 **Analytics & Reporting**
- Métriques de performance en temps réel
- Rapports d'audit automatiques
- Tableaux de bord personnalisés
- Export des données (CSV, Excel)

</td>
<td>

### 🔧 **Administration**
- Interface d'administration Django à `/admin`
- Gestion des utilisateurs et permissions
- Configuration des workflows
- Logs détaillés et monitoring

</td>
</tr>
</table>

---

## 🎨 Interface utilisateur

<details>
<summary>🔽 Voir les captures d'écran</summary>

### 🏠 **Page d'accueil**
![Dashboard](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Dashboard+Preview)

### 💬 **Interface Chatbot**
![Chatbot](https://via.placeholder.com/800x400/7ED321/FFFFFF?text=Chatbot+Interface)

### 📊 **Tableau de bord Analytics**
![Analytics](https://via.placeholder.com/800x400/F5A623/FFFFFF?text=Analytics+Dashboard)

</details>

---

## 🔒 Sécurité & Variables d'environnement

Pour des raisons de sécurité, il est **fortement recommandé** de déplacer les informations sensibles dans des variables d'environnement.

### 🛡️ **Mesures de sécurité implémentées**
- 🔐 **Authentification sécurisée** - Sessions chiffrées
- 🛡️ **Protection CSRF** - Tokens anti-forgery
- 🚫 **Validation des entrées** - Sanitisation automatique
- 📝 **Logs d'audit** - Traçabilité complète
- 🔑 **Gestion des permissions** - Contrôle d'accès granulaire

### ⚙️ **Configuration des variables d'environnement**

Créez un fichier `.env` :
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DB_NAME=chatbotalten
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

---

## 🚀 Déploiement

### 🌐 **Production**

```bash
# Variables d'environnement pour la production
export DEBUG=False
export ALLOWED_HOSTS=votre-domaine.com
export DATABASE_URL=postgresql://user:pass@host:port/db

# Collecte des fichiers statiques
python manage.py collectstatic --noinput

# Migration en production
python manage.py migrate --no-input
```

### 🐳 **Docker** (optionnel)

```dockerfile
# Dockerfile inclus pour le déploiement containerisé
docker build -t chatbot-alten .
docker run -p 8000:8000 chatbot-alten
```

---

## 📖 Documentation

<details>
<summary>🔽 Guides détaillés</summary>

### 🎯 **Guide utilisateur**
- [Configuration initiale](docs/setup.md)
- [Utilisation du chatbot](docs/chatbot-guide.md)
- [Gestion des demandes](docs/requests-management.md)

### 👨‍💻 **Guide développeur**
- [Architecture du projet](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Tests et déploiement](docs/deployment.md)

### 🔧 **Administration**
- [Configuration avancée](docs/admin-config.md)
- [Monitoring et logs](docs/monitoring.md)
- [Backup et restauration](docs/backup.md)

</details>

---

## 🤝 Contribution

Nous accueillons avec plaisir les contributions ! 

### 🔄 **Processus de contribution**

1. 🍴 **Fork** le projet
2. 🌿 **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. ✅ **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. 📤 **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. 📬 **Ouvrir** une Pull Request

### 📋 **Guidelines**
- ✍️ Code documenté et commenté
- 🧪 Tests unitaires inclus
- 📝 Respect des conventions PEP 8
- 🔍 Code review obligatoire

---

## 📞 Support & Contact

<div align="center">

### 🆘 **Besoin d'aide ?**

[![Issues](https://img.shields.io/badge/🐛_Bugs-GitHub_Issues-red.svg)](https://github.com/medkoro/TDCA-chabot/issues)
[![Questions](https://img.shields.io/badge/❓_Questions-Discussions-blue.svg)](https://github.com/medkoro/TDCA-chabot/discussions)
[![Email](https://img.shields.io/badge/📧_Email-support@alten.com-green.svg)](mailto:support@alten.com)

</div>

---

## 📋 Roadmap

- [ ] 🌍 **Internationalisation** complète
- [ ] 📱 **Application mobile** native
- [ ] 🤖 **IA avancée** avec GPT integration
- [ ] 📊 **Dashboard analytics** temps réel
- [ ] 🔌 **API REST** complète
- [ ] 📧 **Notifications email** automatiques
- [ ] 🔄 **Workflow designer** visuel

---

## 📝 Notes techniques

- 🧠 **LangChain** : Intégration avec des modèles de langage pour le traitement NLP
- 🔧 **Django Admin** : Interface d'administration complète disponible à `/admin`
- 🗄️ **PostgreSQL** : Base de données relationnelle robuste pour le stockage des données
- 🚀 **Performance** : Optimisé pour gérer de gros volumes de demandes
- 🔄 **Scalabilité** : Architecture modulaire permettant l'extension

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

### 🌟 **Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile !** ⭐

**Développé avec ❤️ par l'équipe Alten**

[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/medkoro)
[![Built with Python](https://img.shields.io/badge/Built%20with-🐍%20Python-blue.svg)](https://python.org)
[![Powered by Django](https://img.shields.io/badge/Powered%20by-🎸%20Django-green.svg)](https://djangoproject.com)

</div>
