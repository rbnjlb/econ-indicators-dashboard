# 🚀 Template Générique Full-Stack - Guide d'Adaptation

Ce projet est maintenant un **template générique** que vous pouvez utiliser comme base pour différents projets. Voici comment l'adapter à vos besoins.

## 📁 Structure du Template

```
econ-indicators-dashboard/
├── backend/                    # API FastAPI
│   ├── app.py                 # Routes principales
│   ├── config.py              # Configuration
│   ├── services.py            # Logique métier
│   ├── requirements.txt       # Dépendances Python
│   ├── .env.example          # Variables d'environnement
│   └── start.sh              # Script de démarrage
├── frontend/                   # Interface React
│   ├── src/
│   │   ├── components/        # Composants réutilisables
│   │   │   ├── Chart.jsx     # Graphiques (ligne/barre)
│   │   │   └── DataTable.jsx # Tableaux de données
│   │   ├── services/         # Appels API
│   │   │   └── api.js        # Service API centralisé
│   │   └── App.jsx           # Composant principal
│   └── package.json
├── scripts/
│   └── start-dev.sh          # Démarrage développement
├── render.yaml               # Configuration déploiement
└── README.md                 # Documentation
```

## 🔧 Comment Adapter le Template

### 1. **Personnaliser le Backend**

#### Modifier `backend/config.py` :
```python
# Changer le nom de l'application
APP_NAME = os.getenv("APP_NAME", "Mon Projet API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Ajouter vos variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL", "")
API_KEY = os.getenv("API_KEY", "")
```

#### Modifier `backend/app.py` :
```python
# Remplacer les endpoints d'exemple par vos routes
@app.get("/api/users")
async def get_users():
    # Votre logique ici
    return {"users": []}

@app.post("/api/users")
async def create_user(user_data: dict):
    # Votre logique ici
    return {"message": "User created", "user": user_data}
```

#### Ajouter des dépendances dans `backend/requirements.txt` :
```txt
# Ajouter selon vos besoins
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
redis==4.5.0
```

### 2. **Personnaliser le Frontend**

#### Modifier `frontend/src/services/api.js` :
```javascript
export const api = {
  // Remplacer par vos appels API
  async getUsers() {
    const response = await fetch(`${API_BASE}/api/users`);
    return response.json();
  },

  async createUser(userData) {
    const response = await fetch(`${API_BASE}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    return response.json();
  }
};
```

#### Modifier `frontend/src/App.jsx` :
```jsx
export default function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    async function loadUsers() {
      const result = await api.getUsers();
      setUsers(result.users || []);
    }
    loadUsers();
  }, []);

  return (
    <div>
      <h1>Mon Application</h1>
      <DataTable data={users} title="Liste des Utilisateurs" />
    </div>
  );
}
```

### 3. **Ajouter de Nouveaux Composants**

#### Créer `frontend/src/components/UserForm.jsx` :
```jsx
import { useState } from 'react';
import { api } from '../services/api';

export default function UserForm({ onUserCreated }) {
  const [formData, setFormData] = useState({ name: '', email: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createUser(formData);
      onUserCreated();
      setFormData({ name: '', email: '' });
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Nom"
        value={formData.name}
        onChange={(e) => setFormData({...formData, name: e.target.value})}
      />
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({...formData, email: e.target.value})}
      />
      <button type="submit">Créer Utilisateur</button>
    </form>
  );
}
```

### 4. **Configuration des Variables d'Environnement**

#### `backend/.env.example` :
```bash
# Configuration de l'application
APP_NAME=Mon Projet API
APP_VERSION=1.0.0

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# APIs externes
EXTERNAL_API_KEY=your_api_key_here

# CORS
CORS_ORIGINS=http://localhost:5173,https://mon-domaine.com

# Environment
ENVIRONMENT=development
```

#### `frontend/.env.local` :
```bash
VITE_API_BASE=http://127.0.0.1:8000
VITE_APP_NAME=Mon Application
```

### 5. **Déploiement**

#### Modifier `render.yaml` :
```yaml
services:
  - type: web
    name: mon-projet-api
    env: python
    plan: free
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: APP_NAME
        value: Mon Projet API
      - key: DATABASE_URL
        sync: false  # À configurer dans Render
      - key: EXTERNAL_API_KEY
        sync: false  # À configurer dans Render
```

## 🎯 Exemples d'Adaptation

### **E-commerce**
- Backend : Gestion produits, commandes, utilisateurs
- Frontend : Catalogue, panier, profil utilisateur
- Composants : ProductCard, ShoppingCart, UserProfile

### **Blog/News**
- Backend : Articles, commentaires, catégories
- Frontend : Liste articles, article détaillé, formulaire commentaire
- Composants : ArticleCard, CommentForm, CategoryFilter

### **Dashboard Analytics**
- Backend : Collecte données, calculs statistiques
- Frontend : Graphiques, métriques, filtres
- Composants : MetricCard, FilterPanel, DateRangePicker

### **Gestion de Tâches**
- Backend : CRUD tâches, utilisateurs, projets
- Frontend : Liste tâches, formulaire création, filtres
- Composants : TaskItem, TaskForm, ProjectSelector

## 🚀 Commandes de Démarrage

```bash
# Développement
./scripts/start-dev.sh

# Backend seul
cd backend && source .venv/bin/activate && uvicorn app:app --reload --port 8000

# Frontend seul
cd frontend && npm run dev

# Test API
curl http://127.0.0.1:8000/healthz
```

## 📝 Checklist d'Adaptation

- [ ] Modifier `APP_NAME` dans `config.py`
- [ ] Remplacer les endpoints d'exemple dans `app.py`
- [ ] Adapter les appels API dans `api.js`
- [ ] Personnaliser l'interface dans `App.jsx`
- [ ] Ajouter vos dépendances dans `requirements.txt`
- [ ] Configurer les variables d'environnement
- [ ] Mettre à jour `render.yaml` pour le déploiement
- [ ] Tester localement avec `./scripts/start-dev.sh`
- [ ] Déployer sur Render

## 🎨 Personnalisation Avancée

### **Ajouter une Base de Données**
```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# backend/models.py
from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

### **Ajouter l'Authentification**
```python
# backend/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # Votre logique d'authentification
    return user
```

### **Ajouter des Tests**
```python
# backend/test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
```

Ce template vous donne une base solide et modulaire pour créer rapidement des applications full-stack modernes ! 🚀
