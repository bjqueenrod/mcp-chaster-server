
# Use Python 3.11 slim to optimize image size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment variables to optimize Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY *.py ./

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# Change file ownership
RUN chown -R appuser:appgroup /app
USER appuser

# Expose port
EXPOSE 3000

# Default environment variables
ENV PORT=3000

# Docker health check command
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Startup command
CMD ["python", "main.py"]

# Labels for documentation
LABEL maintainer="MCP Server Python"
LABEL version="1.0.0"
LABEL description="Chaster Locks MCP Server - Python FastAPI"
