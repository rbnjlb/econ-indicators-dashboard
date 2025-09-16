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
