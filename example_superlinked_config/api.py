"""
Superlinked API Configuration - Research Agent V2

Configures the REST executor and API endpoints for the Superlinked server.
This follows the proper Superlinked server application structure.

Author: Research Agent V2
Last Modified: 2025-06-28
"""

import os
from superlinked import framework as sl
from .index import paper_index, paper_schema
from .query import (
    semantic_search_query,
    author_search_query,
    subject_search_query,
    recent_papers_query
)

# Create REST source for data ingestion
paper_source = sl.RestSource(paper_schema)

# Create REST queries for different search types
semantic_query = sl.RestQuery(
    sl.RestDescriptor("semantic_search"), 
    semantic_search_query
)

author_query = sl.RestQuery(
    sl.RestDescriptor("author_search"),
    author_search_query
)

subject_query = sl.RestQuery(
    sl.RestDescriptor("subject_search"),
    subject_search_query
)

recent_query = sl.RestQuery(
    sl.RestDescriptor("recent_papers"),
    recent_papers_query
)

# Configure vector database connection for production
# Using QdrantVectorDatabase for persistent vector storage
vector_database = sl.QdrantVectorDatabase(
    url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None),  # No API key for local Qdrant
    default_query_limit=50
)

# Create and configure REST executor
executor = sl.RestExecutor(
    sources=[paper_source],
    indices=[paper_index],
    queries=[
        semantic_query,
        author_query,
        subject_query,
        recent_query
    ],
    vector_database=vector_database
)

# Register executor with Superlinked framework
sl.SuperlinkedRegistry.register(executor)

# Export for verification
__all__ = ["executor", "paper_source", "vector_database"]