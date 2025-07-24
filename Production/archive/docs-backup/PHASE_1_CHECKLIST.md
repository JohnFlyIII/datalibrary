# Phase 1 Checklist: Minimal Legal Document Schema

## Objective
Replace the car schema with the simplest possible legal document schema and verify it works.

## Pre-Implementation
- [ ] Backup current working state
  ```bash
  cp -r superlinked-app superlinked-app-backup-working-car
  ```
- [ ] Ensure docker containers are running
  ```bash
  docker compose ps
  ```

## Implementation Steps

### 1. Update Schema (index.py)
- [ ] Replace CarSchema with LegalDocument schema
- [ ] Change fields to: id, title, content
- [ ] Keep using @sl.schema decorator

### 2. Update Text Spaces (index.py)
- [ ] Create content_space for document content
- [ ] Create title_space for document title
- [ ] Use same model: "all-MiniLM-L6-v2"
- [ ] Update index to include both spaces

### 3. Update API (api.py)
- [ ] Change car_source to document_source
- [ ] Update schema reference
- [ ] Keep Qdrant configuration

### 4. Update Query (query.py)
- [ ] Create content search query
- [ ] Add parameters for content and title search
- [ ] Include limit parameter

## Testing Steps

### 1. Rebuild and Restart
```bash
docker compose down
docker compose build legal-superlinked
docker compose up -d
```

### 2. Wait and Check Health
```bash
sleep 20
curl http://localhost:8080/health
```

### 3. Check OpenAPI Spec
```bash
curl http://localhost:8080/openapi.json | jq '.paths'
```

### 4. Ingest Test Documents
```bash
curl -X POST http://localhost:8080/api/v1/ingest/legal_document \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "1",
      "title": "Texas Civil Practice and Remedies Code - Section 74",
      "content": "This section governs medical liability claims in Texas..."
    },
    {
      "id": "2", 
      "title": "California Consumer Privacy Act",
      "content": "The CCPA provides California residents with rights regarding their personal information..."
    },
    {
      "id": "3",
      "title": "Federal Rules of Civil Procedure - Rule 26",
      "content": "Parties must disclose witnesses and documents relevant to disputed facts..."
    }
  ]'
```

### 5. Test Search Queries
```bash
# Search by content
curl -X POST http://localhost:8080/api/v1/search/[query_name] \
  -H "Content-Type: application/json" \
  -d '{
    "content": "medical liability",
    "title": "",
    "limit": 5
  }'

# Search by title
curl -X POST http://localhost:8080/api/v1/search/[query_name] \
  -H "Content-Type: application/json" \
  -d '{
    "content": "",
    "title": "Texas",
    "limit": 5
  }'
```

## Validation Checklist
- [ ] Health endpoint returns OK
- [ ] OpenAPI spec shows new schema endpoints
- [ ] Ingestion returns 202 Accepted
- [ ] Search returns relevant results
- [ ] No errors in docker logs

## If Issues Occur
1. [ ] Check logs: `docker compose logs legal-superlinked --tail 50`
2. [ ] Verify schema field names match across all files
3. [ ] Ensure __init__.py exists in superlinked-app
4. [ ] Compare with working_simple_example structure
5. [ ] Try with single document first

## Documentation
- [ ] Update superlinked-app/README.md with new schema
- [ ] Save successful curl commands
- [ ] Note any configuration changes made

## Commit When Stable
```bash
git add -A
git commit -m "Phase 1: Implement minimal legal document schema

- Replaced car schema with legal document (id, title, content)
- Created content and title text similarity spaces  
- Updated queries for legal document search
- Tested with sample legal documents
- All tests passing"
```

## Next Phase Criteria
Only proceed to Phase 2 when:
- [ ] All test queries return expected results
- [ ] No errors in container logs
- [ ] Can consistently ingest and search documents
- [ ] Changes are committed to git