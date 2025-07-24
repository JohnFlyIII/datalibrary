"""
Layered API Configuration with Three-Layer Query System
======================================================

Provides progressive disclosure search endpoints:
- Discovery: broad search across documents
- Exploration: focused multi-filter search  
- Deep Dive: precise chunk-level search
"""

import os
from superlinked import framework as sl

# Import existing components
from .index import legal_document, index as document_index
from .query import query as basic_document_query
from .chunk_schema import chunk_schema, chunk_index
from .chunk_queries import precise_chunk_query

# Import layered queries
from .layered_queries import (
    discovery_query, discovery_by_type_query, discovery_by_jurisdiction_query,
    exploration_query, deep_dive_query, deep_dive_precise_query
)

# Create sources
document_source = sl.RestSource(legal_document)
chunk_source = sl.RestSource(chunk_schema)

# Create vector database connection
vector_database = sl.QdrantVectorDatabase(
    url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None),
)

# DISCOVERY LAYER ENDPOINTS
discovery_search_query = sl.RestQuery(
    sl.RestDescriptor("discovery_search"), 
    discovery_query
)

discovery_by_type_query_rest = sl.RestQuery(
    sl.RestDescriptor("discovery_by_type"),
    discovery_by_type_query
)

discovery_by_jurisdiction_query_rest = sl.RestQuery(
    sl.RestDescriptor("discovery_by_jurisdiction"),
    discovery_by_jurisdiction_query
)

# EXPLORATION LAYER ENDPOINTS  
exploration_search_query = sl.RestQuery(
    sl.RestDescriptor("exploration_search"),
    exploration_query
)

# DEEP DIVE LAYER ENDPOINTS
deep_dive_search_query = sl.RestQuery(
    sl.RestDescriptor("deep_dive_search"),
    deep_dive_query
)

deep_dive_precise_search_query = sl.RestQuery(
    sl.RestDescriptor("deep_dive_precise"),
    deep_dive_precise_query
)

# LEGACY ENDPOINTS (for backward compatibility)
basic_document_search_query = sl.RestQuery(
    sl.RestDescriptor("document_search"), 
    basic_document_query
)

basic_chunk_search_query = sl.RestQuery(
    sl.RestDescriptor("precise_search"),
    precise_chunk_query  
)

# Create and configure REST executor with layered queries
executor = sl.RestExecutor(
    sources=[document_source, chunk_source],
    indices=[document_index, chunk_index],
    queries=[
        # Discovery layer queries
        discovery_search_query,
        discovery_by_type_query_rest,
        discovery_by_jurisdiction_query_rest,
        
        # Exploration layer queries
        exploration_search_query,
        
        # Deep dive layer queries
        deep_dive_search_query,
        deep_dive_precise_search_query,
        
        # Legacy queries for backward compatibility
        basic_document_search_query,
        basic_chunk_search_query
    ],
    vector_database=vector_database,
)

# Register executor
sl.SuperlinkedRegistry.register(executor)

# Export for verification
__all__ = ["executor", "document_source", "chunk_source", "vector_database"]