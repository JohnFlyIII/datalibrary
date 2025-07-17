# Passage-Level Search Implementation for Legal Knowledge System

## Overview

This implementation enables users to find specific sections, sentences, and passages within large legal documents (700+ pages) rather than just getting document-level results. This is crucial for legal research where precise citations and quotes are needed.

## Key Features

### 1. Unlimited Document Size
- **Removed 50k character limit** from document ingestion
- Documents can now be ingested in their entirety
- Full-text search across complete documents

### 2. Automatic Document Chunking
- Documents are automatically split into manageable chunks (~2000 characters each)
- **200-character overlap** between chunks to maintain context
- Sentence-boundary aware chunking for better readability

### 3. Passage-Level Metadata
- **Character position tracking** for exact citation locations
- **Chunk context** for understanding surrounding content
- **Parent-child relationships** between full documents and chunks

### 4. Dual Search Modes
- **Document-level search**: Returns full documents (existing functionality)
- **Passage-level search**: Returns specific sections with exact positions

## Schema Enhancements

### New Fields Added to LegalDocument Schema

```python
# Passage-level fields (for chunked documents)
parent_document_id: sl.String         # ID of the parent document if this is a chunk
chunk_index: sl.Integer               # Position of this chunk in the document (0-based)
start_char: sl.Integer                # Character offset where this chunk starts in original document
end_char: sl.Integer                  # Character offset where this chunk ends in original document
chunk_context: sl.String             # Brief context around this chunk for citation purposes
is_chunk: sl.String                  # "true" if this is a chunk, "false" if full document
```

## Enhanced Ingestion Process

### 1. Full Document Ingestion
- Extracts complete text from PDF (no truncation)
- Creates parent document entry with full text
- Preserves all original metadata

### 2. Automatic Chunking
- Splits document into overlapping chunks
- Tracks character positions for each chunk
- Creates chunk context for citations
- Maintains relationship to parent document

### 3. Chunk Storage
- Each chunk is stored as a separate searchable entity
- Contains metadata pointing back to source document
- Includes character position information for precise citations

## New Query Capabilities

### Passage Search Query
```python
passage_search_query = (
    sl.Query(legal_research_index)
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .filter(legal_document.is_chunk == "true")  # Only return chunks
    .select_all()
    .limit(sl.Param("limit", default=50))
)
```

### API Endpoint
- **URL**: `/api/v1/search/passage_search`
- **Method**: POST
- **Purpose**: Find specific passages within documents

## Usage Examples

### 1. Document-Level Search (Existing)
```bash
curl -X POST 'http://localhost:8080/api/v1/search/legal_research' \
  --header 'Content-Type: application/json' \
  --data-raw '{"search_query": "medical malpractice", "limit": 10}'
```

### 2. Passage-Level Search (New)
```bash
curl -X POST 'http://localhost:8080/api/v1/search/passage_search' \
  --header 'Content-Type: application/json' \
  --data-raw '{"search_query": "medical malpractice", "limit": 20}'
```

## Benefits for Legal Research

### 1. Precise Citations
- Get exact character positions for quotes
- Reference specific sections and subsections
- Maintain proper legal citation format

### 2. Contextual Understanding
- See surrounding text for better comprehension
- Understand how passages relate to broader document
- Navigate between related sections

### 3. Efficient Research
- Find relevant passages without reading entire documents
- Compare similar provisions across multiple documents
- Build comprehensive legal arguments with precise references

## Implementation Details

### Chunking Strategy
- **Chunk Size**: 2000 characters (manageable for reading)
- **Overlap**: 400 characters (maintains context)
- **Boundary Detection**: Sentence-aware splitting
- **Context Window**: 100 characters before/after for citations

### Search Weighting
- **Content Weight**: 1.5 (higher for passage search)
- **Practice Area Weight**: 0.6
- **Authority Weight**: 0.7
- Optimized for finding relevant passages over document ranking

### Data Flow
1. **Ingestion**: PDF → Full Text → Chunks → Vector Storage
2. **Search**: Query → Vector Similarity → Chunk Results → Citation Info
3. **Display**: Passage Text + Context + Position + Parent Document

## Future Enhancements

### 1. UI Integration
- Display passage results with highlighting
- Show document navigation for full context
- Provide citation generation tools

### 2. Advanced Features
- Cross-reference detection between passages
- Automatic citation formatting
- Passage clustering by topic

### 3. Performance Optimization
- Caching for frequently accessed passages
- Incremental chunking for document updates
- Advanced ranking algorithms for passage relevance

## Migration Guide

### For Existing Documents
1. Re-ingest documents using `enhanced_chunked_ingester.py`
2. Existing full documents remain searchable
3. New chunk-based results will be available immediately

### For New Documents
1. Use enhanced ingester for all new documents
2. Both document and passage search will work automatically
3. No changes needed to existing API calls

## Technical Files Modified

1. **legal_superlinked_config/app.py**
   - Enhanced schema with passage-level fields
   - Added chunking to TextSimilaritySpace
   - Created passage_search_query
   - Added new REST endpoint

2. **enhanced_chunked_ingester.py** (New)
   - Unlimited document size support
   - Automatic chunking with position tracking
   - Dual ingestion (full document + chunks)

3. **Passage-Level Search Implementation.md** (This file)
   - Complete documentation and usage guide

## Conclusion

This implementation provides a complete solution for passage-level search in large legal documents, enabling precise citations and contextual understanding while maintaining backward compatibility with existing document-level search functionality.