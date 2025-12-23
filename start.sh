#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine paths based on environment (Docker vs Local)
if [ -d "$SCRIPT_DIR/backend" ]; then
    # Docker structure (flat)
    echo "Filesystem: Docker/Flat detected"
    BACKEND_DIR="$SCRIPT_DIR/backend"
    FRONTEND_DIR="$SCRIPT_DIR/frontend"
elif [ -d "$SCRIPT_DIR/Flux-Wallpaper-Web/backend" ]; then
    # Local structure (nested)
    echo "Filesystem: Local/Nested detected"
    BACKEND_DIR="$SCRIPT_DIR/Flux-Wallpaper-Web/backend"
    FRONTEND_DIR="$SCRIPT_DIR/Flux-Wallpaper-Web/frontend"
else
    echo "Error: Could not locate backend directory!"
    echo "Checked: $SCRIPT_DIR/backend and $SCRIPT_DIR/Flux-Wallpaper-Web/backend"
    exit 1
fi

# 1. Start Backend in Background (Port 8000)
echo "🚀 Starting FastAPI Backend on port 8000..."
cd "$BACKEND_DIR" || { echo "Backend dir not found"; exit 1; }

# Activate Virtual Environment (Local only)
if [ -f "../../.venv/bin/activate" ]; then
    source "../../.venv/bin/activate"
elif [ -f "../../venv/bin/activate" ]; then
    source "../../venv/bin/activate"
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
cd "$FRONTEND_DIR" || { echo "Frontend dir not found"; exit 1; }

# Check if we are in production mode (standalone build presence)
if [ -f "server.js" ]; then
    echo "🚀 Runtime: Production (Native Node)"
    # Start the standalone server
    # Port is handled by Next.js from PORT env var, Host from HOSTNAME
    node server.js
else
    echo "🚀 Runtime: Development (Next Dev)"
    # Use npm run dev for development
    npm run dev -- -H 0.0.0.0 -p 3000
fi

# Cleanup background process on exit
trap "kill $BACKEND_PID" EXIT
