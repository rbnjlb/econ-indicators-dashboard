# 🚀 Template Full-Stack Générique

Un template complet et modulaire pour créer rapidement des applications full-stack modernes avec FastAPI (backend) et React (frontend).

## 🏗️ Architecture

- **Backend**: FastAPI (Python) - API REST modulaire et extensible
- **Frontend**: React + Vite - Interface moderne avec composants réutilisables
- **Déploiement**: Render - Configuration automatique
- **Structure**: Modulaire et facilement adaptable

## ⚡ Démarrage Rapide

### Installation
```bash
# Cloner le template
git clone <votre-repo>
cd econ-indicators-dashboard

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Personnaliser selon vos besoins

# Frontend
cd ../frontend
npm install
```

### Développement
```bash
# Démarrer les deux serveurs d'un coup
./scripts/start-dev.sh

# Ou séparément :
# Backend: cd backend && source .venv/bin/activate && uvicorn app:app --reload --port 8000
# Frontend: cd frontend && npm run dev
```

## 🎯 Fonctionnalités

### Backend (FastAPI)
- ✅ Structure modulaire (`config.py`, `services.py`, `app.py`)
- ✅ Gestion des erreurs et cache
- ✅ CORS configuré pour développement et production
- ✅ Endpoints d'exemple prêts à personnaliser
- ✅ Health checks et monitoring

### Frontend (React)
- ✅ Composants réutilisables (`Chart`, `DataTable`)
- ✅ Service API centralisé
- ✅ Gestion d'état et erreurs
- ✅ Interface responsive
- ✅ Graphiques (ligne et barre)

### Déploiement
- ✅ Configuration Render automatique
- ✅ Variables d'environnement sécurisées
- ✅ Scripts de production

## 📚 Documentation

- **[Guide d'Adaptation](TEMPLATE_GUIDE.md)** - Comment personnaliser le template
- **[Tutoriel Complet](COMPLETE_TUTORIAL.md)** - Guide détaillé de création
- **[Améliorations](PROJECT_IMPROVEMENTS_SUMMARY.md)** - Historique des optimisations

## 🔧 API Endpoints (Exemple)

- `GET /healthz` - Vérification de santé
- `GET /api/example/data` - Données d'exemple
- `GET /api/example/external?url=...` - Récupération de données externes
- `POST /api/example/process` - Traitement de données

## 🌍 Variables d'Environnement

### Backend (`.env`)
```bash
APP_NAME=Mon Projet API
APP_VERSION=1.0.0
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
ENVIRONMENT=development
```

### Frontend (`.env.local`)
```bash
VITE_API_BASE=http://127.0.0.1:8000
```

## 🚀 Déploiement

Le backend se déploie automatiquement sur Render via `render.yaml` :

1. Connecter votre repo GitHub à Render
2. Configurer les variables d'environnement
3. Déployer automatiquement via Git push

## 🎨 Exemples d'Adaptation

Ce template peut être adapté pour :
- **E-commerce** : Gestion produits, commandes, utilisateurs
- **Blog/News** : Articles, commentaires, catégories  
- **Dashboard** : Analytics, métriques, graphiques
- **Gestion** : Tâches, projets, équipes
- **API** : Microservices, intégrations

## 📝 Prochaines Étapes

1. Lire le [Guide d'Adaptation](TEMPLATE_GUIDE.md)
2. Personnaliser selon vos besoins
3. Ajouter vos fonctionnalités
4. Déployer en production

---

**Template créé pour être facilement adaptable et réutilisable ! 🎯**