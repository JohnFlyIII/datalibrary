# Curl Examples for Simple Superlinked Server

## 1. Health Check
```bash
curl http://localhost:8080/health
```
Expected response:
```json
{"message":"OK"}
```

## 2. Version Check
```bash
curl http://localhost:8080/version
```

## 3. Get OpenAPI Specification
```bash
curl http://localhost:8080/openapi.json | jq '.'
```

## 4. Ingest Car Data

### Single Car
```bash
curl -X POST http://localhost:8080/api/v1/ingest/car_schema \
  -H "Content-Type: application/json" \
  -d '[{"id": "1", "make": "Toyota", "model": "Camry"}]'
```

### Multiple Cars
```bash
curl -X POST http://localhost:8080/api/v1/ingest/car_schema \
  -H "Content-Type: application/json" \
  -d '[
    {"id": "1", "make": "Toyota", "model": "Camry"},
    {"id": "2", "make": "Honda", "model": "Accord"},
    {"id": "3", "make": "Toyota", "model": "Corolla"},
    {"id": "4", "make": "Ford", "model": "Mustang"},
    {"id": "5", "make": "Tesla", "model": "Model S"},
    {"id": "6", "make": "BMW", "model": "3 Series"},
    {"id": "7", "make": "Mercedes-Benz", "model": "C-Class"},
    {"id": "8", "make": "Audi", "model": "A4"},
    {"id": "9", "make": "Honda", "model": "Civic"},
    {"id": "10", "make": "Ford", "model": "F-150"}
  ]'
```

## 5. Search Queries

### Search by Make (Toyota)
```bash
curl -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Toyota",
    "model": "",
    "limit": 5
  }'
```

### Search by Model (Mustang)
```bash
curl -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "",
    "model": "Mustang",
    "limit": 3
  }'
```

### Combined Search (Honda Sedan)
```bash
curl -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Honda",
    "model": "sedan",
    "limit": 5
  }'
```

### Search for Luxury Cars
```bash
curl -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "luxury german",
    "model": "",
    "limit": 5
  }'
```

### Search Electric Vehicles
```bash
curl -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "electric",
    "model": "",
    "limit": 3
  }'
```

## 6. Response Format

### Successful Ingest Response
```
HTTP 202 Accepted
(Empty body or minimal response)
```

### Search Response Format
```json
{
  "entries": [
    {
      "id": "1",
      "fields": {},
      "metadata": {
        "score": 0.6128518,
        "partial_scores": [],
        "vector_parts": []
      }
    }
  ]
}
```

## 7. Testing Script

Save this as `test_api.sh`:
```bash
#!/bin/bash

echo "1. Checking health..."
curl -s http://localhost:8080/health | jq '.'
echo -e "\n"

echo "2. Ingesting test data..."
curl -s -X POST http://localhost:8080/api/v1/ingest/car_schema \
  -H "Content-Type: application/json" \
  -d '[
    {"id": "test1", "make": "Toyota", "model": "Camry"},
    {"id": "test2", "make": "Honda", "model": "Accord"},
    {"id": "test3", "make": "Tesla", "model": "Model 3"}
  ]'
echo -e "\nData ingested (202 response expected)\n"

sleep 2

echo "3. Searching for Toyota..."
curl -s -X POST http://localhost:8080/api/v1/search/query \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Toyota",
    "model": "",
    "limit": 3
  }' | jq '.'
```

## 8. Debugging Commands

### Check if services are running
```bash
docker compose ps
```

### View Superlinked logs
```bash
docker compose logs legal-superlinked --tail 50
```

### View Qdrant logs
```bash
docker compose logs qdrant --tail 50
```

### Check Qdrant collections
```bash
curl http://localhost:6333/collections
```