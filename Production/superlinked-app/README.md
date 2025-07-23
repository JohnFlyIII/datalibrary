# Superlinked App - Legal Knowledge System

## Current Status: Starting Fresh from Working Example

This directory contains a new implementation of the legal knowledge system, starting from the proven working simple example and gradually building towards the full functionality.

## Development Approach

1. **Start with Working Base** ✅
   - Copied from the simple car example that is confirmed working
   - Uses Qdrant vector database
   - Basic text similarity search

2. **Incremental Development Plan**
   - [ ] Replace car schema with basic legal document schema
   - [ ] Add document ingestion from JSON files
   - [ ] Implement hierarchical search (jurisdiction, practice areas)
   - [ ] Add temporal/recency scoring
   - [ ] Integrate preprocessing pipelines
   - [ ] Add advanced query patterns

## Current Implementation

The app currently implements a simple car search example with:
- Schema: `CarSchema` with id, make, and model fields
- Two text similarity spaces for make and model
- REST API for ingestion and search
- Qdrant vector database integration

## Next Steps

1. Create a minimal `LegalDocument` schema with just id, title, and content
2. Test basic ingestion and search
3. Gradually add fields and complexity
4. Port functionality from `superlinked-app-not-working` piece by piece

## Files

- `index.py` - Schema and index definitions
- `api.py` - API configuration and database setup
- `query.py` - Query definitions
- `__init__.py` - Package initialization

## Testing

Always test each incremental change:
```bash
# Rebuild and restart
docker compose down
docker compose build legal-superlinked
docker compose up -d

# Wait for health
sleep 20 && curl http://localhost:8080/health

# Test with appropriate data for current schema
```