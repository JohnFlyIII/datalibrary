# Superlinked App - Legal Knowledge System

## Current Status: Phase 1 Complete ✅

Successfully transitioned from car example to legal document search!

## Development Approach

1. **Start with Working Base** ✅
   - Copied from the simple car example that is confirmed working
   - Uses Qdrant vector database
   - Basic text similarity search

2. **Incremental Development Plan**
   - [x] Replace car schema with basic legal document schema ✅
   - [ ] Add document ingestion from JSON files
   - [ ] Implement hierarchical search (jurisdiction, practice areas)
   - [ ] Add temporal/recency scoring
   - [ ] Integrate preprocessing pipelines
   - [ ] Add advanced query patterns

## Current Implementation

The app implements legal document search with:
- Schema: `LegalDocument` with id, title, and content fields
- Two text similarity spaces:
  - `title_space` - searches document titles
  - `content_space` - searches document content
- REST API for ingestion and search
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
      "title": "Document Title",
      "content": "Full document content..."
    }
  ]'
```

### Search by Content
```bash
curl -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "medical malpractice",
    "title_query": "",
    "limit": 5
  }'
```

### Search by Title
```bash
curl -X POST http://localhost:8080/api/v1/search/search \
  -H "Content-Type: application/json" \
  -d '{
    "content_query": "",
    "title_query": "Texas",
    "limit": 3
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