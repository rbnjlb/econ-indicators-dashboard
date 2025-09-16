from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS, APP_NAME, APP_VERSION
from services import fetch_json

app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": APP_NAME.lower().replace(" ", "-")}

@app.get("/")
async def root():
    return {
        "message": APP_NAME, 
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/healthz"
    }

# Example API endpoints - customize these for your project
@app.get("/api/example/data")
async def get_example_data():
    """Example endpoint that returns sample data"""
    return {
        "message": "This is example data from your API",
        "data": [
            {"id": 1, "name": "Item 1", "value": 100},
            {"id": 2, "name": "Item 2", "value": 200},
            {"id": 3, "name": "Item 3", "value": 300}
        ]
    }

@app.get("/api/example/external")
async def get_external_data(url: str):
    """Example endpoint that fetches external data"""
    try:
        data = await fetch_json(url)
        return {"data": data, "source": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch data: {str(e)}")

@app.post("/api/example/process")
async def process_data(data: dict):
    """Example POST endpoint for data processing"""
    # Add your data processing logic here
    processed_data = {
        "original": data,
        "processed": True,
        "timestamp": "2025-01-16T10:00:00Z"
    }
    return processed_data