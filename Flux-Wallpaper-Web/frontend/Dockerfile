# Frontend Build Stage
FROM node:20-alpine as builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Build Next.js app
# Note: We need NEXT_PUBLIC_API_URL at build time for static pages, 
# but mostly it's used client-side. We can set a placeholder or use env vars.
ENV NEXT_PUBLIC_API_URL=PLACEHOLDER_URL
RUN npm run build

# Runner Stage
FROM node:20-alpine as runner

WORKDIR /app

ENV NODE_ENV=production

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
