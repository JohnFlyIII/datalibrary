# Legal Knowledge System Superlinked Server Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Superlinked server package
RUN pip install --upgrade pip
RUN pip install superlinked-server

# Create superlinked app directory
RUN mkdir -p superlinked_app

# Copy application configuration
COPY legal_superlinked_config/ superlinked_app/

# Set environment variables
ENV APP_MODULE_PATH=superlinked_app
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8080
ENV LOG_LEVEL=INFO
ENV TRANSFORMERS_CACHE=/app/model_cache

# Create model cache directory
RUN mkdir -p /app/model_cache

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/docs || exit 1

# Start Legal Knowledge Superlinked server
CMD ["python", "-m", "superlinked.server"]