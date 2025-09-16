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
