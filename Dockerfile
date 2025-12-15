# Copyright (c) 2025 dev-droid. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

FROM python:3.10-slim

LABEL maintainer="dev-droid"
LABEL description="AI-Powered Cron Job Generator with Web UI"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    curl \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY aicron ./aicron

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Expose Web UI port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AICRON_PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Default command: Start Web UI
CMD ["python", "-m", "aicron.main", "web", "--port", "8080"]
