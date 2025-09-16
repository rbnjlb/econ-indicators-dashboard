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
