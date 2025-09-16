from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, json, httpx, pandas as pd
from cachetools import TTLCache
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="Economic Indicators API", version="0.2.0")
# Allow local dev frontends (adjust via env)
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Simple in-memory cache (key -> JSON) for 30 minutes
cache = TTLCache(maxsize=256, ttl=1800)
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
WORLD_BANK_BASE = "https://api.worldbank.org/v2"
async def fetch_json(url, params=None):
    key = url + json.dumps(params or {}, sort_keys=True)
    if key in cache:
        return cache[key]
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
    try:
        data = r.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Upstream returned non-JSON")
    cache[key] = data
    return data
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
@app.get("/api/worldbank/indicator")
async def worldbank_indicator(country: str = "FRA", indicator: str = "NY.GDP.MKTP.CD", per_page: int = 100):
    url = f"{WORLD_BANK_BASE}/country/{country}/indicator/{indicator}"
    data = await fetch_json(url, params={"format": "json", "per_page": per_page})
    if not isinstance(data, list) or len(data) < 2:
        raise HTTPException(status_code=502, detail="Unexpected WB response")
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