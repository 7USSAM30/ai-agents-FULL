# Multi-Agent AI System - Unified Next.js Application
# This Dockerfile creates a single Next.js application with integrated AI agents

FROM node:18-alpine AS base

# Install Python 3.11 and system dependencies for AI processing
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    gcc \
    g++ \
    curl \
    make \
    libc-dev \
    linux-headers \
    && ln -sf python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip

# Set working directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000 \
    NEXT_TELEMETRY_DISABLED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY frontend/ ./

# Copy backend agents to be used by Next.js API routes
COPY backend/agents/ ./lib/agents/
COPY backend/requirements.txt ./

# Install Python dependencies for AI processing
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p cache docs

# Build the Next.js application
RUN npm run build

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=base /app/public ./public
COPY --from=base --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=base --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["node", "server.js"]
