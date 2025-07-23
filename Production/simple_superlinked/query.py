"""
Superlinked Query Configuration - Research Agent V2

Defines search queries for academic paper semantic search.
This follows the proper Superlinked server application structure.

Author: Research Agent V2
Last Modified: 2025-06-28
"""

from superlinked import framework as sl
from .index import (
    paper_index,
    paper_schema,
    title_space,
    abstract_space,
    content_space,
    author_space,
    subject_space,
    keyword_space,
    year_space,
    impact_space
)

# Semantic search query with weighted multi-modal search
semantic_search_query = (
    sl.Query(
        paper_index,
        weights={
            title_space: sl.Param("title_weight", 1.0),
            abstract_space: sl.Param("abstract_weight", 0.8),
            content_space: sl.Param("content_weight", 0.6),
            author_space: sl.Param("author_weight", 0.3),
            subject_space: sl.Param("subject_weight", 0.5),
            keyword_space: sl.Param("keyword_weight", 0.6),
            year_space: sl.Param("year_weight", 0.2),
            impact_space: sl.Param("impact_weight", 0.4)
        }
    )
    .find(paper_schema)
    .similar(title_space.text, sl.Param("query_text"))
    .limit(sl.Param("limit", 20))
)

# Author-focused search query
author_search_query = (
    sl.Query(
        paper_index,
        weights={
            author_space: sl.Param("author_weight", 1.0),
            title_space: sl.Param("title_weight", 0.5),
            impact_space: sl.Param("impact_weight", 0.3)
        }
    )
    .find(paper_schema)
    .similar(author_space.text, sl.Param("author_name"))
    .limit(sl.Param("limit", 20))
)

# Subject area search query
subject_search_query = (
    sl.Query(
        paper_index,
        weights={
            subject_space: sl.Param("subject_weight", 1.0),
            keyword_space: sl.Param("keyword_weight", 0.8),
            title_space: sl.Param("title_weight", 0.6)
        }
    )
    .find(paper_schema)
    .similar(subject_space.text, sl.Param("subject_area"))
    .limit(sl.Param("limit", 20))
)

# Recent papers query with year focus
recent_papers_query = (
    sl.Query(
        paper_index,
        weights={
            year_space: sl.Param("year_weight", 1.0),
            impact_space: sl.Param("impact_weight", 0.8),
            title_space: sl.Param("title_weight", 0.5)
        }
    )
    .find(paper_schema)
    .similar(title_space.text, sl.Param("query_text"))
    .limit(sl.Param("limit", 20))
)

# Export queries for API configuration
__all__ = [
    "semantic_search_query",
    "author_search_query", 
    "subject_search_query",
    "recent_papers_query"
]