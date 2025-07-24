"""
Chunk-based Query Definitions
============================

Advanced query patterns for precise document chunk retrieval.
Enables finding exact text segments within documents.
"""

from superlinked import framework as sl
from .chunk_schema import (
    chunk_schema, chunk_index, chunk_content_space, 
    chunk_type_space, chunk_jurisdiction_space, chunk_position_space
)

# Precise chunk search - finds exact text segments
precise_chunk_query = (
    sl.Query(chunk_index)
    .find(chunk_schema)
    .similar(chunk_content_space.text, sl.Param("content_query"))
    .similar(chunk_type_space, sl.Param("document_type"))
    .similar(chunk_jurisdiction_space, sl.Param("jurisdiction"))
    .select_all()
    .limit(sl.Param("limit"))
)

# Position-based search - finds chunks in specific document sections  
section_search_query = (
    sl.Query(chunk_index)
    .find(chunk_schema)
    .similar(chunk_content_space.text, sl.Param("content_query"))
    .similar(chunk_type_space, sl.Param("document_type"))
    .similar(chunk_jurisdiction_space, sl.Param("jurisdiction"))
    .select_all()
    .limit(sl.Param("limit"))
)

# Document-specific chunk search - all chunks from specific document
document_chunks_query = (
    sl.Query(chunk_index)
    .find(chunk_schema)
    .similar(chunk_content_space.text, sl.Param("content_query"))
    .select_all()
    .limit(sl.Param("limit"))
)

# Export queries
__all__ = [
    "precise_chunk_query",
    "section_search_query", 
    "document_chunks_query"
]