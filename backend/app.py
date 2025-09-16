from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, json, httpx
from cachetools import TTLCache
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Economic Indicators API", version="0.2.0")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = TTLCache(maxsize=256, ttl=1800)
WORLD_BANK_BASE = "https://api.worldbank.org/v2"

async def fetch_json(url, params=None):
    key = url + json.dumps(params or {}, sort_keys=True)
    if key in cache:
        return cache[key]
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    cache[key] = data
    return data

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

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
