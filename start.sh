#!/bin/bash

# 1. Start Backend in Background (Port 8000)
echo "🚀 Starting FastAPI Backend on port 8000..."
cd /app/backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 &

# 2. Wait for Backend (optional, but good practice)
# We just give it a second to initialize
sleep 5

# 3. Start Frontend in Foreground (Port $PORT)
echo "🚀 Starting Next.js Frontend on port $PORT..."
cd /app/frontend
node server.js
