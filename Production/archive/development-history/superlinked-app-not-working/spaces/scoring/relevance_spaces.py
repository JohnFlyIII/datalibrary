"""
Scoring and Relevance Spaces

Purpose:
- Enable numerical scoring and ranking of documents
- Support quality and relevance filtering
- Facilitate confidence-based searches

Usage:
- Finding highly relevant documents
- Quality threshold filtering
- Confidence-based research
- Performance optimization

Human Note: NumberSpace modes determine how scores are used in search
AI Agent Note: Use MAXIMUM for highest scores, SIMILAR for score ranges
"""

from superlinked import framework as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Client Relevance Score Space (0-10 scale)
client_relevance_score_space = sl.NumberSpace(
    number=legal_document.client_relevance_score,
    min_value=0,
    max_value=10,
    mode=sl.Mode.MAXIMUM  # Find highest relevance scores
)

# AI Confidence Score Space (0-100 scale)
confidence_score_space = sl.NumberSpace(
    number=legal_document.confidence_score,
    min_value=0,
    max_value=100,
    mode=sl.Mode.MAXIMUM  # Find highest confidence
)

# Readability Score Space (0-100 scale)
readability_score_space = sl.NumberSpace(
    number=legal_document.readability_score,
    min_value=0,
    max_value=100,
    mode=sl.Mode.MAXIMUM  # Prioritize higher readability scores
)

# Search Weight Space (0-10 scale)
search_weight_space = sl.NumberSpace(
    number=legal_document.search_weight,
    min_value=0,
    max_value=10,
    mode=sl.Mode.MAXIMUM  # Prioritize boosted documents
)

# Access Frequency Space
access_frequency_space = sl.NumberSpace(
    number=legal_document.access_frequency,
    min_value=0,
    max_value=10000,
    mode=sl.Mode.MAXIMUM  # Find most accessed documents
)

# Search Performance Space
search_performance_space = sl.NumberSpace(
    number=legal_document.search_performance,
    min_value=0,
    max_value=100,
    mode=sl.Mode.MAXIMUM  # Find best performing in search
)

# Scoring Space Collections
RELEVANCE_SCORING_SPACES = [
    client_relevance_score_space,
    confidence_score_space,
    search_weight_space
]

QUALITY_SCORING_SPACES = [
    confidence_score_space,
    readability_score_space
]

USAGE_SCORING_SPACES = [
    access_frequency_space,
    search_performance_space
]

ALL_SCORING_SPACES = (
    RELEVANCE_SCORING_SPACES + 
    QUALITY_SCORING_SPACES + 
    USAGE_SCORING_SPACES
)

# Export all spaces
__all__ = [
    'client_relevance_score_space',
    'confidence_score_space',
    'readability_score_space',
    'search_weight_space',
    'access_frequency_space',
    'search_performance_space',
    'RELEVANCE_SCORING_SPACES',
    'QUALITY_SCORING_SPACES',
    'USAGE_SCORING_SPACES',
    'ALL_SCORING_SPACES'
]

# Usage Examples:
"""
Scoring Query Patterns:

1. High Relevance Documents:
   weights = {
       client_relevance_score_space: 3.0,
       confidence_score_space: 2.0,
       search_weight_space: 1.5
   }

2. Quality Threshold Search:
   # First filter by minimum confidence
   .filter(legal_document.confidence_score >= 80)
   weights = {
       confidence_score_space: 2.5,
       readability_score_space: 1.5
   }

3. Popular Documents:
   weights = {
       access_frequency_space: 3.0,
       search_performance_space: 2.0,
       client_relevance_score_space: 1.5
   }

4. Easy-to-Read Content:
   weights = {
       readability_score_space: 3.0,  # Mode.SIMILAR with target ~70
       confidence_score_space: 1.5
   }

5. Boosted Search Results:
   weights = {
       search_weight_space: 2.5,
       client_relevance_score_space: 2.0,
       confidence_score_space: 1.5
   }

NumberSpace Modes:
- MAXIMUM: Find documents with highest scores
- MINIMUM: Find documents with lowest scores
- SIMILAR: Find documents with scores similar to query value

Example with SIMILAR mode:
query.with_vector({readability_score_space: 75})  # Find docs with readability ~75
"""