# Multi-stage build for DocuGener
# Stage 1: Frontend build
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./

# Stage 2: Python backend
FROM python:3.11-slim

# Install system dependencies for screenshot and GUI libraries
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    gnupg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt ./backend/

# Install Python dependencies
# Note: pywin32 is Windows-specific, so we'll create a Linux-compatible requirements file
RUN sed '/pywin32/d' backend/requirements.txt > /tmp/requirements.txt && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Install supervisor for process management
RUN pip install --no-cache-dir supervisor

# Copy backend code
COPY backend/ ./backend/

# Copy frontend from builder stage
COPY --from=frontend-builder /app/frontend ./frontend

# Create directories for captures and database
RUN mkdir -p /app/backend/captures && \
    mkdir -p /app/data && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /etc/supervisor/conf.d

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV DISPLAY=:99

# Expose ports
# Backend API: 5000, Frontend: 5100
EXPOSE 5000 5100

# Create supervisor config
RUN echo '[supervisord]\n\
nodaemon=true\n\
logfile=/var/log/supervisor/supervisord.log\n\
pidfile=/var/run/supervisord.pid\n\
\n\
[program:xvfb]\n\
command=/usr/bin/Xvfb :99 -screen 0 1024x768x24\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/xvfb.err.log\n\
stdout_logfile=/var/log/xvfb.out.log\n\
\n\
[program:backend]\n\
command=python /app/backend/main.py\n\
directory=/app/backend\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/backend.err.log\n\
stdout_logfile=/var/log/backend.out.log\n\
environment=DISPLAY=":99",PYTHONUNBUFFERED="1"\n\
depends_on=xvfb\n\
\n\
[program:frontend]\n\
command=node /app/frontend/server.js\n\
directory=/app/frontend\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/frontend.err.log\n\
stdout_logfile=/var/log/frontend.out.log\n\
depends_on=backend\n\
' > /etc/supervisor/conf.d/docugener.conf

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
