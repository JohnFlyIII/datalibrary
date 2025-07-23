# Legal Knowledge System - Production Superlinked Server Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for production
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel

# Install Superlinked server package (latest version)
RUN pip install superlinked-server==1.45.2

# Install additional production dependencies
RUN pip install \
    pandas \
    numpy \
    requests \
    python-dotenv \
    fastapi-cors

# Create application directories
RUN mkdir -p superlinked_app
RUN mkdir -p /app/model_cache
RUN mkdir -p /app/output
RUN mkdir -p /app/raw_data

# Copy the superlinked application
COPY superlinked-app/ superlinked-app/

# Set proper permissions
RUN chown -R nobody:nogroup /app
RUN chmod -R 755 /app

# Set environment variables for production
ENV APP_MODULE_PATH=superlinked-app
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8080
ENV LOG_LEVEL=INFO
ENV TRANSFORMERS_CACHE=/app/model_cache
ENV ENVIRONMENT=production
ENV PYTHONPATH=/app:/app/superlinked-app
ENV PYTHONUNBUFFERED=1
ENV HOME=/app
ENV HF_HOME=/app/model_cache
ENV SENTENCE_TRANSFORMERS_HOME=/app/model_cache

# Switch to non-root user for security
USER nobody

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start the Legal Knowledge Superlinked server
CMD ["python", "-m", "superlinked.server"]