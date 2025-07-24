"""
Temporal Spaces Module

This module provides time-based relevance spaces for:
- Document recency and age
- Effective dates
- Update tracking
"""

from .recency_spaces import (
    published_recency_space,
    effective_date_space,
    last_updated_space,
    last_verified_space,
    TEMPORAL_SPACES,
    LIFECYCLE_SPACES,
    QA_TEMPORAL_SPACES
)

__all__ = [
    'published_recency_space',
    'effective_date_space',
    'last_updated_space',
    'last_verified_space',
    'TEMPORAL_SPACES',
    'LIFECYCLE_SPACES',
    'QA_TEMPORAL_SPACES'
]