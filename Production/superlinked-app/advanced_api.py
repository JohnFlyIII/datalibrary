"""
Advanced API Configuration with Document + Chunk Support
=======================================================

Provides multiple search endpoints:
1. Document-level search (summaries, metadata)
2. Chunk-level search (precise text segments)  
3. Multi-layered queries (discovery → exploration → deep dive)
"""

import os
from superlinked import framework as sl

# Import document-level components
from .index import legal_document, index as document_index
from .query import query as document_query

# Import chunk-level components  
from .chunk_schema import chunk_schema, chunk_index
from .chunk_queries import precise_chunk_query, section_search_query, document_chunks_query

# Create sources
document_source = sl.RestSource(legal_document)
chunk_source = sl.RestSource(chunk_schema)

# Create vector database connection
vector_database = sl.QdrantVectorDatabase(
    url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None),
)

# Create REST queries for document-level search
document_search_query = sl.RestQuery(
    sl.RestDescriptor("document_search"), 
    document_query
)

# Create REST queries for chunk-level search
precise_search_query = sl.RestQuery(
    sl.RestDescriptor("precise_search"),
    precise_chunk_query  
)

section_search_query_rest = sl.RestQuery(
    sl.RestDescriptor("section_search"),
    section_search_query
)

document_chunks_query_rest = sl.RestQuery(
    sl.RestDescriptor("document_chunks"),
    document_chunks_query
)

# Create and configure REST executor with multiple indices and queries
executor = sl.RestExecutor(
    sources=[document_source, chunk_source],
    indices=[document_index, chunk_index],
    queries=[
        # Document-level queries
        document_search_query,
        
        # Chunk-level queries
        precise_search_query,
        section_search_query_rest, 
        document_chunks_query_rest
    ],
    vector_database=vector_database,
)

# Register executor
sl.SuperlinkedRegistry.register(executor)

# Export for verification
__all__ = ["executor", "document_source", "chunk_source", "vector_database"]