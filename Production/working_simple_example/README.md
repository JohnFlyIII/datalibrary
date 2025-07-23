# Working Simple Example - Superlinked Server

This directory contains a **FULLY WORKING** simple example of a Superlinked server with vector search capabilities.

## Status: ✅ WORKING

This example has been tested and confirmed working on 2025-07-23 with:
- superlinked-server==1.45.2 (latest)
- Qdrant as vector database
- Simple car schema with make/model search

## Directory Structure

```
working_simple_example/
├── docker-compose.yml              # Docker compose configuration
├── production-superlinked.Dockerfile # Dockerfile for Superlinked server
├── simple_example/                 # Python application code
│   ├── __init__.py
│   ├── api.py                     # API configuration with Qdrant
│   ├── index.py                   # Schema and index definition
│   └── query.py                   # Query definition
├── openapi.json                   # OpenAPI specification
└── README.md                      # This file
```

## Quick Start

1. Start the services:
```bash
docker compose up -d
```

2. Wait for services to be healthy (about 20-30 seconds):
```bash
# Check health
curl http://localhost:8080/health
# Expected: {"message":"OK"}
```

3. Ingest sample data:
```bash
curl -X POST http://localhost:8080/api/v1/ingest/car_schema \
  -H "Content-Type: application/json" \
  -d '[
    {"id": "1", "make": "Toyota", "model": "Camry"},
    {"id": "2", "make": "Honda", "model": "Accord"},
    {"id": "3", "make": "Toyota", "model": "Corolla"},
    {"id": "4", "make": "Ford", "model": "Mustang"},
    {"id": "5", "make": "Tesla", "model": "Model S"}
  ]'
```

4. Search for cars:
```bash
# Search for Toyota cars
curl -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Toyota",
    "model": "",
    "limit": 5
  }'

# Search by model
curl -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "",
    "model": "Mustang",
    "limit": 3
  }'
```

## API Endpoints

### Health Check
```bash
GET http://localhost:8080/health
```

### Version Info
```bash
GET http://localhost:8080/version
```

### Ingest Data
```bash
POST http://localhost:8080/api/v1/ingest/car_schema
Content-Type: application/json

# Body: Array of objects with schema fields
[
  {"id": "unique_id", "make": "Brand", "model": "Model"}
]
```

### Search Query
```bash
POST http://localhost:8080/api/v1/search/query
Content-Type: application/json

# Body: Query parameters
{
  "make": "search term for make",
  "model": "search term for model",
  "limit": 10
}
```

## Schema Definition

The car schema (in `simple_example/index.py`):
```python
@sl.schema
class CarSchema:
    id: sl.IdField
    make: sl.String
    model: sl.String
```

## Text Similarity Spaces

- **car_make_text_space**: Searches by car manufacturer/brand
- **car_model_text_space**: Searches by car model name
- Both use the `all-MiniLM-L6-v2` sentence transformer model

## Important Configuration

### Environment Variables (in docker-compose.yml)
- `SERVER_HOST=0.0.0.0`
- `SERVER_PORT=8080`
- `QDRANT_URL=http://qdrant:6333`
- `APP_MODULE_PATH=simple_example`
- `TRANSFORMERS_CACHE=/app/model_cache`
- `HOME=/app` (Required for model downloads)
- `HF_HOME=/app/model_cache`
- `SENTENCE_TRANSFORMERS_HOME=/app/model_cache`

### Key Fixes Applied
1. Changed from `InMemoryVectorDatabase` to `QdrantVectorDatabase` for persistence
2. Added HOME environment variables to fix permission errors when downloading models
3. Proper Python module structure with `__init__.py`

## Troubleshooting

### Permission Errors
If you see `Permission denied: '/nonexistent'`, ensure the Dockerfile includes:
```dockerfile
ENV HOME=/app
ENV HF_HOME=/app/model_cache
ENV SENTENCE_TRANSFORMERS_HOME=/app/model_cache
```

### Vector Dimension Mismatch
If you see vector collision errors, stop containers and remove volumes:
```bash
docker compose down -v
docker compose up -d
```

### Check Logs
```bash
docker compose logs legal-superlinked --tail 50
docker compose logs qdrant --tail 50
```

## OpenAPI Specification

The full OpenAPI spec is saved in `openapi.json`. Key endpoints:
- `/health` - Health check
- `/version` - Version information
- `/api/v1/ingest/car_schema` - Data ingestion
- `/api/v1/search/query` - Search queries

## Next Steps

This working example can be extended by:
1. Adding more fields to the schema
2. Creating additional text spaces for other search dimensions
3. Adding categorical, numerical, or temporal spaces
4. Implementing more complex query patterns
5. Adding data loaders for batch processing