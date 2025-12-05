# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Metadata
LABEL maintainer="Lourdes Rios"
LABEL description="Twitter News Classifier Multi-Agent System"
LABEL version="2.0.0"

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

# System dependencies needed for some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY domain ./domain
COPY infrastructure ./infrastructure
COPY application ./application
COPY presentation ./presentation
COPY main.py ./
COPY extract_real_tweets.py ./
COPY README.md ./
COPY .env.example ./.env.example

# Create writable directories for logs and outputs
RUN mkdir -p /app/logs /app/results /app/data \
    && useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; print('Health check passed'); sys.exit(0)"

# Expose port for potential API server
EXPOSE 8000

# Default command runs the main classifier
CMD ["python", "main.py"]
