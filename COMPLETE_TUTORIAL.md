# Economic Indicators Dashboard — Complete Tutorial (Enhanced V3)

**Date**: 2025-01-16  
**Stack**: Cursor • GitHub • Localhost • Render (FastAPI backend) • React (Vite) • Recharts  
**Enhanced with**: Modular architecture, production deployment, comprehensive error handling

## 🎯 How to Use This Guide

Each step has three parts:
1. **Do this now** (commands to paste)
2. **Paste this** (file contents) 
3. **What's happening** (plain-language explanation)

Copy blocks exactly as shown.

---

## 0) Prerequisites (macOS)

**Do this now:**
```bash
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11 node
```

**What's happening:**
- Xcode tools give you compilers and Git
- Homebrew installs Python 3.11 and Node
- This tutorial uses Render for backend deployment (no gcloud needed)

---

## 1) Project Skeleton

**Do this now:**
```bash
mkdir econ-indicators-dashboard && cd $_
git init
mkdir backend frontend scripts
```

**What's happening:**
- You create a mono-repo with backend (FastAPI) and frontend (Vite React)
- Git tracks your work so you can push to GitHub

---

## 2) Backend (FastAPI) - Enhanced Structure

**Do this now:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn[standard] httpx pandas python-dotenv cachetools fredapi
```

**Paste this into `backend/config.py` (create the file):**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
WORLD_BANK_BASE = "https://api.worldbank.org/v2"

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
# Add wildcard for development, but restrict in production
if os.getenv("ENVIRONMENT") == "development":
    CORS_ORIGINS.append("*")

# Cache Configuration
CACHE_MAX_SIZE = 256
CACHE_TTL = 1800  # 30 minutes
```

**Paste this into `backend/services.py` (create the file):**
```python
import json
import httpx
from cachetools import TTLCache
from fastapi import HTTPException
from config import CACHE_MAX_SIZE, CACHE_TTL

# Simple in-memory cache (key -> JSON) for 30 minutes
cache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL)

async def fetch_json(url, params=None):
    """Fetch JSON data with caching"""
    key = url + json.dumps(params or {}, sort_keys=True)
    if key in cache:
        return cache[key]
    
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    
    cache[key] = data
    return data
```

**Paste this into `backend/app.py` (create the file):**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS, FRED_API_KEY, WORLD_BANK_BASE
from services import fetch_json

app = FastAPI(title="Economic Indicators API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "economic-indicators-api"}

@app.get("/")
async def root():
    return {
        "message": "Economic Indicators API", 
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/healthz"
    }

@app.get("/api/worldbank/indicator")
async def worldbank_indicator(country: str = "FRA", indicator: str = "NY.GDP.MKTP.CD", per_page: int = 10000):
    url = f"{WORLD_BANK_BASE}/country/{country}/indicator/{indicator}"
    data = await fetch_json(url, params={"format": "json", "per_page": per_page})
    if not isinstance(data, list) or len(data) < 2:
        raise HTTPException(status_code=502, detail="Unexpected World Bank response")
    series = data[1]
    rows = []
    for item in series:
        year = item.get("date")
        value = item.get("value")
        if year is not None:
            try:
                yr = int(year)
            except Exception:
                continue
            rows.append({"year": yr, "value": value})
    rows = sorted(rows, key=lambda x: x["year"])
    return {"country": country, "indicator": indicator, "data": rows}

@app.get("/api/fred/series")
async def fred_series(series_id: str = "UNRATE", realtime_start: str = "1776-07-04", realtime_end: str = "9999-12-31"):
    if not FRED_API_KEY:
        raise HTTPException(status_code=400, detail="Set FRED_API_KEY in the environment to use FRED API")
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "realtime_start": realtime_start,
        "realtime_end": realtime_end
    }
    data = await fetch_json(url, params=params)
    obs = data.get("observations", [])
    rows = [{"date": o.get("date"), "value": None if (o.get("value") in ("", ".")) else float(o["value"])} for o in obs]
    return {"series_id": series_id, "data": rows}

@app.get("/api/oecd/raw")
async def oecd_raw(url: str):
    data = await fetch_json(url)
    return data

@app.get("/api/eurostat/raw")
async def eurostat_raw(url: str):
    data = await fetch_json(url)
    return data
```

**Paste this into `backend/requirements.txt` (create the file):**
```txt
fastapi==0.116.1
uvicorn[standard]==0.35.0
httpx==0.27.0
pandas==2.2.2
python-dotenv==1.0.1
cachetools==5.3.3
fredapi==0.5.1
gunicorn==23.0.0
```

**Paste this into `backend/.env.example` (create the file):**
```bash
FRED_API_KEY=your_fred_api_key_here
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
ENVIRONMENT=development
```

**Run locally:**
```bash
uvicorn app:app --reload --port 8000
```

**What's happening:**
- FastAPI defines HTTP endpoints; Uvicorn runs the server
- Modular structure: `config.py` for settings, `services.py` for business logic, `app.py` for routes
- `/api/worldbank/indicator` fetches GDP, inflation, etc. from the World Bank
- `/api/fred/series` fetches FRED series when you provide an API key
- CORS is configured for both development and production
- Enhanced error handling and health checks

---

## 3) Frontend (Vite React + Recharts) - Enhanced Structure

**Do this now:**
```bash
cd ../frontend
npm create vite@latest . -- --template react
npm install
npm install recharts
```

**Paste this into `frontend/src/components/Chart.jsx` (create the file):**
```jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function Chart({ data, title, dataKey = "value", xAxisKey = "year" }) {
  return (
    <div style={{ width: "100%", height: 420 }}>
      <h3>{title}</h3>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey={dataKey} dot={false} stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

**Paste this into `frontend/src/services/api.js` (create the file):**
```javascript
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export const api = {
  async getWorldBankIndicator(country = "FRA", indicator = "NY.GDP.MKTP.CD") {
    const response = await fetch(
      `${API_BASE}/api/worldbank/indicator?country=${country}&indicator=${indicator}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  async getFredSeries(seriesId = "UNRATE") {
    const response = await fetch(
      `${API_BASE}/api/fred/series?series_id=${seriesId}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  async healthCheck() {
    const response = await fetch(`${API_BASE}/healthz`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }
};
```

**Paste this into `frontend/src/App.jsx` (overwrite the Vite starter content):**
```jsx
import { useEffect, useState } from "react";
import Chart from "./components/Chart";
import { api } from "./services/api";

export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const result = await api.getWorldBankIndicator("FRA", "NY.GDP.MKTP.CD");
        setData(result.data || []);
      } catch (e) {
        setError(String(e));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <p>Loading…</p>;
  if (error) return <p style={{ color: "crimson" }}>Error: {error}</p>;

  return (
    <div style={{ fontFamily: "Inter, system-ui, sans-serif", padding: 24 }}>
      <h1>Economic Indicators Dashboard</h1>
      <Chart 
        data={data} 
        title="GDP (current US$) — World Bank (FRA)"
        dataKey="value"
        xAxisKey="year"
      />
    </div>
  );
}
```

**Paste this into `frontend/.env.local` (create the file):**
```bash
VITE_API_BASE=http://127.0.0.1:8000
```

**Run locally:**
```bash
npm run dev # open the printed URL (e.g., http://127.0.0.1:5173)
```

**What's happening:**
- Vite scaffolds a modern React app
- Recharts draws the line chart
- Modular structure: `Chart.jsx` for reusable components, `api.js` for API calls
- `VITE_API_BASE` points your app at the local FastAPI server in dev
- Better error handling and loading states

---

## 4) Development Scripts

**Paste this into `scripts/start-dev.sh` (create the file):**
```bash
#!/bin/bash

# Start development environment
echo "Starting Economic Indicators Dashboard..."

# Start backend
echo "Starting backend server..."
cd backend
source .venv/bin/activate
uvicorn app:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend running on http://127.0.0.1:8000"
echo "Frontend running on http://localhost:5173"
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
```

**Make it executable:**
```bash
chmod +x scripts/start-dev.sh
```

**Run both servers:**
```bash
./scripts/start-dev.sh
```

**What's happening:**
- One command starts both backend and frontend
- Backend serves data at http://127.0.0.1:8000
- Frontend runs at http://127.0.0.1:5173 and fetches data from the backend

---

## 5) Push to GitHub

**Do this now (from project root):**
```bash
# Set environment variables for git setup
export BACKEND_DIR="backend"
export FRONTEND_DIR="frontend" 
export PROJECT_REPO="econ-indicators-dashboard"

# Create .gitignore
printf ".env\n$BACKEND_DIR/.venv/\n$FRONTEND_DIR/node_modules/\n.DS_Store\n" >> .gitignore

# Git setup
git add .
git commit -m "chore: initial commit (enhanced backend FastAPI + frontend React)"
git branch -M main
git remote add origin https://github.com/<your-username>/econ-indicators-dashboard.git
git push -u origin main
```

**What's happening:**
- Your code is versioned online
- If prompted for credentials, use a Personal Access Token as your Git password

---

## 6) Deploy Backend to Render

**Paste this into `render.yaml` (create the file):**
```yaml
services:
  - type: web
    name: econ-indicators-api
    env: python
    plan: free
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: FRED_API_KEY
        sync: false  # You'll set this in Render dashboard
      - key: CORS_ORIGINS
        value: https://your-frontend-domain.onrender.com,http://localhost:5173
      - key: ENVIRONMENT
        value: production
      - key: PYTHON_VERSION
        value: 3.11.0
```

**Paste this into `backend/start.sh` (create the file):**
```bash
#!/bin/bash

# Production startup script for Render
echo "Starting Economic Indicators API..."

# Install dependencies
pip install -r requirements.txt

# Start the application
uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1
```

**Make it executable:**
```bash
chmod +x backend/start.sh
```

**Deploy to Render:**
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect and use the `render.yaml` configuration
5. Set environment variables in Render dashboard:
   - `FRED_API_KEY`: Your FRED API key (get from [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html))
   - `CORS_ORIGINS`: `https://your-frontend-domain.onrender.com,http://localhost:5173`
   - `ENVIRONMENT`: `production`

**Test deployment:**
```bash
# After deployment, test your API
curl -s https://your-app-name.onrender.com/healthz
curl -s "https://your-app-name.onrender.com/api/worldbank/indicator?country=FRA&indicator=NY.GDP.MKTP.CD"
```

**What's happening:**
- Render builds and runs your FastAPI as a container automatically
- `render.yaml` provides automated deployment configuration
- Environment variables are securely managed in Render dashboard
- Your API is now publicly accessible

---

## 7) Update Frontend for Production

**Update `frontend/.env.local` for production:**
```bash
# For production, update this to your Render URL
VITE_API_BASE=https://your-app-name.onrender.com
```

**Build and test:**
```bash
cd frontend
npm run build
npm run preview  # Test the production build locally
```

**What's happening:**
- Frontend now points to your deployed Render API
- Production build is optimized and ready for deployment

---

## 8) Project Documentation

**Paste this into `README.md` (create the file):**
```markdown
# Economic Indicators Dashboard

A full-stack application for visualizing economic indicators from various data sources including World Bank, FRED, OECD, and Eurostat.

## Architecture

- **Backend**: FastAPI (Python) - provides REST API endpoints
- **Frontend**: React + Vite - interactive dashboard with charts
- **Data Sources**: World Bank, FRED, OECD, Eurostat APIs

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env  # Edit with your API keys
uvicorn app:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Start Both (Development)
```bash
./scripts/start-dev.sh
```

## API Endpoints

- `GET /healthz` - Health check
- `GET /api/worldbank/indicator` - World Bank economic indicators
- `GET /api/fred/series` - FRED economic data series
- `GET /api/oecd/raw` - OECD data
- `GET /api/eurostat/raw` - Eurostat data

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `FRED_API_KEY`: Your FRED API key (get from https://fred.stlouisfed.org/docs/api/api_key.html)
- `CORS_ORIGINS`: Allowed frontend origins
- `VITE_API_BASE`: Backend API URL

## Deployment

Backend is deployed to Render automatically via `render.yaml` configuration.
```

---

## 9) Troubleshooting

### Common Issues and Solutions:

**"uvicorn: command not found"**
```bash
# Solution: Activate virtual environment first
cd backend
source .venv/bin/activate
uvicorn app:app --reload --port 8000
```

**"CORS error in browser"**
```bash
# Solution: Check CORS_ORIGINS in backend/.env
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**"Module not found" errors**
```bash
# Solution: Install dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**Render deployment fails**
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify environment variables are set

**Git commands hanging**
```bash
# Solution: Set environment variables first
export BACKEND_DIR="backend"
export FRONTEND_DIR="frontend" 
export PROJECT_REPO="econ-indicators-dashboard"
```

---

## 10) API Examples

### World Bank Common Codes:
- GDP (current US$): `NY.GDP.MKTP.CD`
- Inflation, CPI (%): `FP.CPI.TOTL.ZG`
- Unemployment (%): `SL.UEM.TOTL.ZS`

### Local API Calls:
```bash
# Health check
curl -s http://127.0.0.1:8000/healthz

# World Bank data
curl -s "http://127.0.0.1:8000/api/worldbank/indicator?country=FRA&indicator=NY.GDP.MKTP.CD"

# FRED data (requires FRED_API_KEY)
curl -s "http://127.0.0.1:8000/api/fred/series?series_id=UNRATE"
```

### Production (Render):
```bash
# Replace with your actual Render URL
curl -s "https://your-app-name.onrender.com/api/worldbank/indicator?country=FRA&indicator=NY.GDP.MKTP.CD"
```

---

## 🎯 Summary

This enhanced tutorial provides:

✅ **Modular Architecture**: Clean separation of concerns  
✅ **Production Ready**: Automated deployment with Render  
✅ **Development Experience**: One-command startup scripts  
✅ **Error Handling**: Comprehensive error management  
✅ **Documentation**: Complete setup and usage guide  
✅ **Best Practices**: Following Python and React standards  

The result is a professional-grade economic indicators dashboard that's easy to develop, deploy, and maintain.

---

## 🚀 Next Steps

1. **Add TypeScript** for better type safety
2. **Implement Testing** (unit tests for both frontend and backend)
3. **Add Docker** for containerized deployment
4. **Set up CI/CD** with GitHub Actions
5. **Add Database** for persistent caching
6. **Implement Logging** for production monitoring
7. **Add API Rate Limiting** for production security
