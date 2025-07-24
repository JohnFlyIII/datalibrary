"""
Chunk-based Schema and Spaces for Precise Document Retrieval
===========================================================

Separate schema for document chunks to enable precise location-based search.
Chunks provide exact text segments with character positions for accurate retrieval.
"""

from superlinked import framework as sl

@sl.schema
class DocumentChunk:
    """Schema for individual document chunks with precise location"""
    id: sl.IdField  # Format: {doc_id}_chunk_{chunk_index}
    parent_document_id: sl.String  # Links back to main document
    chunk_index: sl.Integer  # Position within document
    text: sl.String  # Actual chunk content
    start_char: sl.Integer  # Character position start
    end_char: sl.Integer  # Character position end
    
    # Inherited metadata from parent document
    document_type: sl.String  # statute, case, regulation, etc.
    jurisdiction: sl.String  # federal, texas, california, etc.

# Create chunk schema instance
chunk_schema = DocumentChunk()

# Text similarity space for chunk content - using same model for consistency
chunk_content_space = sl.TextSimilaritySpace(
    text=chunk_schema.text, 
    model="all-MiniLM-L6-v2"
)

# Categorical spaces for filtering chunks by metadata
chunk_type_space = sl.CategoricalSimilaritySpace(
    category_input=chunk_schema.document_type,
    categories=["statute", "case", "regulation", "guidance", "rule", "other"],
    negative_filter=-1.0,
    uncategorized_as_category=True
)

chunk_jurisdiction_space = sl.CategoricalSimilaritySpace(
    category_input=chunk_schema.jurisdiction,
    categories=["federal", "texas", "california", "new_york", "florida", "other"],
    negative_filter=-1.0,
    uncategorized_as_category=True
)

# Number space for chunk position (useful for finding specific sections)
chunk_position_space = sl.NumberSpace(
    number=chunk_schema.chunk_index,
    min_value=0,
    max_value=200,  # Most documents won't have more than 200 chunks
    mode=sl.Mode.MAXIMUM
)

# Create chunk index
chunk_index = sl.Index([
    chunk_content_space,
    chunk_type_space, 
    chunk_jurisdiction_space,
    chunk_position_space
])

# Export for use in other modules
__all__ = [
    "chunk_schema",
    "chunk_index",
    "chunk_content_space",
    "chunk_type_space",
    "chunk_jurisdiction_space", 
    "chunk_position_space"
]