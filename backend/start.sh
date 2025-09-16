#!/bin/bash

# Production startup script for Render
echo "Starting Economic Indicators API..."

# Install dependencies
pip install -r requirements.txt

# Start the application
uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1
