import os
from dotenv import load_dotenv

load_dotenv()

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
# Add wildcard for development, but restrict in production
if os.getenv("ENVIRONMENT") == "development":
    CORS_ORIGINS.append("*")

# Cache Configuration
CACHE_MAX_SIZE = 256
CACHE_TTL = 1800  # 30 minutes

# App Configuration
APP_NAME = os.getenv("APP_NAME", "Generic API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
