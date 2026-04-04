# Multi-stage Dockerfile for Situation Room
# Stage 1: Build React frontend
# Stage 2: Serve with FastAPI (Python)

# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --production=false
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: Python Backend ----
FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY main.py .
COPY agents/ agents/
COPY db/ db/
COPY tools/ tools/
COPY mcp_servers/ mcp_servers/
COPY data/ data/

# Copy frontend build from stage 1
COPY --from=frontend-build /app/frontend/dist frontend/dist/

# Seed database
RUN python -m data.seed

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
