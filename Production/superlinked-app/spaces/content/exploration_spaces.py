"""
Exploration Layer Content Spaces

Purpose:
- Enable focused analysis on specific aspects
- Support medium-precision filtering
- Facilitate concept and provision exploration

Usage:
- Second-pass searches after discovery
- Identifying relevant provisions and requirements
- Understanding legal concepts and implications
- Filtering by relevance and complexity

Human Note: Exploration spaces balance breadth and depth
AI Agent Note: Use these spaces to narrow down from discovery results
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument
# Import complexity_level_space to avoid duplication
from ..categorical.legal_taxonomy_spaces import complexity_level_space

# Initialize the legal document schema
legal_document = LegalDocument()

# Key Provisions Space - Critical legal requirements
exploration_provisions_space = sl.TextSimilaritySpace(
    text=legal_document.key_provisions,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=300, chunk_overlap=50)
)

# Legal Concepts Space - Semantic legal concepts
exploration_concepts_space = sl.TextSimilaritySpace(
    text=legal_document.legal_concepts,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Practical Implications Space - Real-world impact
exploration_implications_space = sl.TextSimilaritySpace(
    text=legal_document.practical_implications,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=400, chunk_overlap=75)
)

# Compliance Requirements Space - Specific actions needed
compliance_requirements_space = sl.TextSimilaritySpace(
    text=legal_document.compliance_requirements,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Client Relevance Scoring Space
relevance_score_space = sl.NumberSpace(
    number=legal_document.client_relevance_score,
    min_value=0,
    max_value=10,
    mode=sl.Mode.MAXIMUM  # Find most relevant
)

# Note: complexity_level_space is imported from categorical.legal_taxonomy_spaces
# to avoid duplicate definitions and ensure consistency

# Penalties and Consequences Space
penalties_space = sl.TextSimilaritySpace(
    text=legal_document.penalties_consequences,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Exceptions Space
exceptions_space = sl.TextSimilaritySpace(
    text=legal_document.exceptions_exclusions,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Common Questions Space - FAQ-style information
common_questions_space = sl.TextSimilaritySpace(
    text=legal_document.common_questions,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Exploration Collections
EXPLORATION_CONTENT_SPACES = [
    exploration_provisions_space,
    exploration_concepts_space,
    exploration_implications_space,
    compliance_requirements_space
]

EXPLORATION_FILTER_SPACES = [
    relevance_score_space,
    complexity_level_space
]

EXPLORATION_COMPLIANCE_SPACES = [
    compliance_requirements_space,
    penalties_space,
    exceptions_space
]

ALL_EXPLORATION_SPACES = (
    EXPLORATION_CONTENT_SPACES + 
    EXPLORATION_FILTER_SPACES + 
    EXPLORATION_COMPLIANCE_SPACES
)

# Export all spaces
__all__ = [
    'exploration_provisions_space',
    'exploration_concepts_space',
    'exploration_implications_space',
    'compliance_requirements_space',
    'relevance_score_space',
    'complexity_level_space',
    'penalties_space',
    'exceptions_space',
    'common_questions_space',
    'EXPLORATION_CONTENT_SPACES',
    'EXPLORATION_FILTER_SPACES',
    'EXPLORATION_COMPLIANCE_SPACES',
    'ALL_EXPLORATION_SPACES'
]

# Usage Examples:
"""
Exploration Query Patterns:

1. Key Provisions Focus:
   weights = {
       exploration_provisions_space: 3.0,
       compliance_requirements_space: 2.5,
       exploration_concepts_space: 2.0,
       relevance_score_space: 1.5
   }

2. Compliance Research:
   weights = {
       compliance_requirements_space: 3.0,
       penalties_space: 2.5,
       exceptions_space: 2.0,
       exploration_provisions_space: 2.0
   }

3. Concept Understanding:
   weights = {
       exploration_concepts_space: 3.0,
       exploration_implications_space: 2.5,
       complexity_level_space: 1.5
   }

4. High-Relevance Filtering:
   weights = {
       relevance_score_space: 3.0,
       exploration_provisions_space: 2.0,
       exploration_implications_space: 2.0
   }

5. Practical Impact Analysis:
   weights = {
       exploration_implications_space: 3.0,
       compliance_requirements_space: 2.5,
       penalties_space: 2.0,
       exceptions_space: 1.5
   }
"""