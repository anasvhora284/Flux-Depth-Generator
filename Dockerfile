# ==========================================
# Phase 1: Build Frontend (Next.js)
# ==========================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Install dependencies
COPY Flux-Wallpaper-Web/frontend/package*.json ./
RUN npm ci

# Copy source code
COPY Flux-Wallpaper-Web/frontend/ .

# Build with standalone output
# WE SET API URL TO EMPTY because we use relative path /api via Next.js rewrites
ENV NEXT_PUBLIC_API_URL=""
RUN npm run build

# ==========================================
# Phase 2: Setup Unified Runtime (Python + Node)
# ==========================================
FROM python:3.11-slim-bookworm AS runtime

# Install System Dependencies & Node.js 20
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ==========================================
# Phase 3: Setup Backend
# ==========================================
WORKDIR /app/backend

# Install Python Dependencies
COPY Flux-Wallpaper-Web/backend/requirements.txt .
# Install CPU-only torch first
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY Flux-Wallpaper-Web/backend/ .

# Create uploads folder
RUN mkdir -p uploads

# Download Models (cached in image)
RUN python download_models.py

# ==========================================
# Phase 4: Setup Frontend (Copy Build)
# ==========================================
WORKDIR /app/frontend

# Copy Next.js Standalone Build
COPY --from=frontend-builder /app/frontend/.next/standalone ./
COPY --from=frontend-builder /app/frontend/.next/static ./.next/static
COPY --from=frontend-builder /app/frontend/public ./public

# ==========================================
# Phase 5: Final Startup Config
# ==========================================
WORKDIR /app

# Copy Startup Script
COPY start.sh .
RUN chmod +x start.sh

# Environment Variables
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV PYTHONUNBUFFERED=1

EXPOSE 3000

CMD ["./start.sh"]
