# Superlinked App - Legal Knowledge System

## Current Status: Phase 2 Complete ✅

Successfully added metadata filtering with categorical spaces!

## Development Approach

1. **Start with Working Base** ✅
   - Copied from the simple car example that is confirmed working
   - Uses Qdrant vector database
   - Basic text similarity search

2. **Incremental Development Plan**
   - [x] Replace car schema with basic legal document schema ✅
   - [x] Add document_type and jurisdiction metadata filtering ✅
   - [ ] Add document ingestion from JSON files
   - [ ] Add temporal/recency scoring
   - [ ] Implement hierarchical search (jurisdiction, practice areas)
   - [ ] Integrate preprocessing pipelines
   - [ ] Add advanced query patterns

## Current Implementation

The app implements advanced legal document search with:
- Schema: `LegalDocument` with id, title, content, document_type, and jurisdiction fields
- Multiple similarity spaces:
  - `title_space` - searches document titles
  - `content_space` - searches document content
  - `document_type_space` - filters by document type (statute, case, regulation, etc.)
  - `jurisdiction_space` - filters by jurisdiction (federal, texas, california, etc.)
- REST API for ingestion and search with categorical filtering
- Qdrant vector database integration

## API Endpoints

- **Ingest**: `POST /api/v1/ingest/legal_document`
- **Search**: `POST /api/v1/search/search`
- **Health**: `GET /health`

## Example Usage

### Ingest Documents
```bash
curl -X POST http://localhost:8080/api/v1/ingest/legal_document \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "1",
      "title": "Texas Medical Malpractice Act",
      "content": "Full document content...",
      "document_type": "statute",
      "jurisdiction": "texas"
    }
  ]'
```

### Search by Content and Type
```bash
curl -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "medical malpractice",
    "title_query": "",
    "document_type": "case",
    "jurisdiction": "",
    "limit": 5
  }'
```

### Filter by Jurisdiction Only
```bash
curl -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "",
    "title_query": "",
    "document_type": "",
    "jurisdiction": "texas",
    "limit": 10
  }'
```

### Combined Filtering
```bash
curl -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "privacy",
    "title_query": "",
    "document_type": "regulation",
    "jurisdiction": "federal",
    "limit": 5
  }'
```

## Next Steps

1. Add document metadata fields (jurisdiction, document_type)
2. Integrate with existing JSON data in output/metadata/
3. Add hierarchical search capabilities
4. Implement temporal/recency scoring

## Files

- `index.py` - Schema and index definitions
- `api.py` - API configuration and database setup
- `query.py` - Query definitions
- `__init__.py` - Package initialization