"""
Temporal and Recency Spaces

Purpose:
- Enable time-based relevance and recency searches
- Support date-based filtering and ranking
- Facilitate finding recent changes or historical progression

Usage:
- Finding recently published laws
- Tracking effective dates for compliance
- Historical legal research
- Time-sensitive document discovery

Human Note: RecencySpace uses decay functions to prioritize newer/older content
AI Agent Note: Use positive weights for recent docs, negative for historical
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Published Date Recency - When document was published
published_recency_space = sl.RecencySpace(
    timestamp=legal_document.published_date,
    decay_rate=0.5,  # How quickly relevance decays (0-1)
    time_period=sl.Period.MONTHS  # Time unit for decay
)

# Effective Date Space - When laws/rules take effect
effective_date_space = sl.RecencySpace(
    timestamp=legal_document.effective_date,
    decay_rate=0.3,  # Slower decay for effective dates
    time_period=sl.Period.MONTHS
)

# Last Updated Space - Recent amendments/revisions
last_updated_space = sl.RecencySpace(
    timestamp=legal_document.last_updated,
    decay_rate=0.7,  # Faster decay for updates
    time_period=sl.Period.MONTHS
)

# Last Verified Space - Quality assurance recency
last_verified_space = sl.RecencySpace(
    timestamp=legal_document.last_verified,
    decay_rate=0.6,
    time_period=sl.Period.MONTHS
)

# Temporal Space Collections
TEMPORAL_SPACES = [
    published_recency_space,
    effective_date_space,
    last_updated_space,
    last_verified_space
]

# Document lifecycle spaces
LIFECYCLE_SPACES = [
    published_recency_space,
    effective_date_space,
    last_updated_space
]

# Quality assurance spaces
QA_TEMPORAL_SPACES = [
    last_verified_space,
    last_updated_space
]

# Export all spaces
__all__ = [
    'published_recency_space',
    'effective_date_space',
    'last_updated_space',
    'last_verified_space',
    'TEMPORAL_SPACES',
    'LIFECYCLE_SPACES',
    'QA_TEMPORAL_SPACES'
]

# Usage Examples:
"""
Temporal Query Patterns:

1. Recent Legal Changes (Last 6 months):
   weights = {
       published_recency_space: 3.0,
       last_updated_space: 2.5,
       effective_date_space: 2.0
   }

2. Upcoming Effective Dates:
   weights = {
       effective_date_space: 3.0,  # High weight for future dates
       published_recency_space: 1.0
   }

3. Historical Research (Older documents):
   weights = {
       published_recency_space: -2.0,  # Negative weight for older docs
       last_updated_space: -1.0
   }

4. Recently Verified Content:
   weights = {
       last_verified_space: 3.0,
       published_recency_space: 1.5
   }

5. Time-Sensitive Compliance:
   weights = {
       effective_date_space: 3.0,
       last_updated_space: 2.0,
       published_recency_space: 1.5
   }

Note on Decay Rates:
- 0.1-0.3: Slow decay - content remains relevant longer
- 0.4-0.6: Medium decay - balanced relevance over time
- 0.7-0.9: Fast decay - strong preference for very recent

Time Periods:
- sl.Period.DAYS: For rapidly changing content
- sl.Period.MONTHS: Standard legal document updates
- sl.Period.YEARS: For stable, long-term content
"""