"""
Scoring Spaces Module

This module provides numerical scoring spaces for:
- Relevance and confidence scoring
- Quality metrics
- Usage analytics
"""

from .relevance_spaces import (
    client_relevance_score_space,
    confidence_score_space,
    readability_score_space,
    search_weight_space,
    access_frequency_space,
    search_performance_space,
    RELEVANCE_SCORING_SPACES,
    QUALITY_SCORING_SPACES,
    USAGE_SCORING_SPACES,
    ALL_SCORING_SPACES
)

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