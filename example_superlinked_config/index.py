"""
Superlinked Index Configuration - Research Agent V2

Defines the schema, spaces, and indexes for academic paper search.
This follows the proper Superlinked server application structure.

Author: Research Agent V2
Last Modified: 2025-06-28
"""

from superlinked import framework as sl

# Paper schema definition for academic papers
@sl.schema
class PaperSchema:
    """Schema for academic research papers with all relevant fields."""
    id: sl.IdField
    title: sl.String
    abstract: sl.String
    content: sl.String
    authors: sl.String  
    publication_year: sl.Integer
    journal: sl.String
    subject_areas: sl.String
    citations_count: sl.Integer
    doi: sl.String
    keywords: sl.String

# Create schema instance
paper_schema = PaperSchema()

# Define embedding model for production
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Lightweight but effective

# Define embedding spaces for multi-modal search
title_space = sl.TextSimilaritySpace(
    text=paper_schema.title,
    model=model_name
)

abstract_space = sl.TextSimilaritySpace(
    text=paper_schema.abstract,
    model=model_name
)

content_space = sl.TextSimilaritySpace(
    text=paper_schema.content,
    model=model_name
)

author_space = sl.TextSimilaritySpace(
    text=paper_schema.authors,
    model=model_name
)

subject_space = sl.TextSimilaritySpace(
    text=paper_schema.subject_areas,
    model=model_name
)

keyword_space = sl.TextSimilaritySpace(
    text=paper_schema.keywords,
    model=model_name
)

# Year space for publication year filtering
year_space = sl.NumberSpace(
    number=paper_schema.publication_year,
    min_value=1800,
    max_value=2030,
    mode=sl.Mode.MAXIMUM
)

# Number space for citation impact
impact_space = sl.NumberSpace(
    number=paper_schema.citations_count,
    min_value=0,
    max_value=10000,
    mode=sl.Mode.MAXIMUM
)

# Create comprehensive index with all spaces
paper_index = sl.Index([
    title_space,
    abstract_space,
    content_space,
    author_space, 
    subject_space,
    keyword_space,
    year_space,
    impact_space
])

# Export for use in other modules
__all__ = [
    "paper_schema",
    "paper_index", 
    "title_space",
    "abstract_space",
    "content_space",
    "author_space",
    "subject_space", 
    "keyword_space",
    "year_space",
    "impact_space"
]