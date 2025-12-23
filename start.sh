#!/bin/bash

# Get project root (relative to this script)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/Flux-Wallpaper-Web"

# 1. Start Backend in Background (Port 8000)
echo "🚀 Starting FastAPI Backend on port 8000..."
cd "$PROJECT_DIR/backend" || { echo "Backend dir not found"; exit 1; }

# Activate Virtual Environment
if [ -f "../.venv/bin/activate" ]; then
    source "../.venv/bin/activate"
elif [ -f "../venv/bin/activate" ]; then
    source "../venv/bin/activate"
fi

# Run Uvicorn (Ensure app module is importable)
# Python path implicitly includes current dir
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 2. Wait for Backend to initialize
echo "Waiting for Backend to initialize..."
sleep 5

# 3. Start Frontend in Foreground
echo "🚀 Starting Next.js Frontend..."
cd "$PROJECT_DIR/frontend" || { echo "Frontend dir not found"; exit 1; }

# Use npm run dev for development
# -H 0.0.0.0 binds to all network interfaces
npm run dev -- -H 0.0.0.0 -p 3000

# Cleanup background process on exit
trap "kill $BACKEND_PID" EXIT
