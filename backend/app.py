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
