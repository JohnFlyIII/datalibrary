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

from datetime import timedelta
from superlinked import framework as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Published Date Recency - When document was published
published_recency_space = sl.RecencySpace(
    timestamp=legal_document.published_date,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), 1.0),    # Very recent: full weight
        sl.PeriodTime(timedelta(days=365), 0.8),   # Recent: high weight  
        sl.PeriodTime(timedelta(days=1825), 0.5),  # 5 years: medium weight
        sl.PeriodTime(timedelta(days=3650), 0.2),  # 10 years: low weight
    ],
    negative_filter=-0.2
)

# Effective Date Space - When laws/rules take effect
effective_date_space = sl.RecencySpace(
    timestamp=legal_document.effective_date,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), 1.0),    # Brand new laws: full weight
        sl.PeriodTime(timedelta(days=180), 0.9),   # Recent laws: very high weight
        sl.PeriodTime(timedelta(days=365), 0.7),   # Year old: high weight
        sl.PeriodTime(timedelta(days=1825), 0.4),  # 5 years: moderate weight
        sl.PeriodTime(timedelta(days=3650), 0.2),  # 10 years: low weight
    ],
    negative_filter=-0.3  # Slower decay for effective dates
)

# Last Updated Space - Recent amendments/revisions
last_updated_space = sl.RecencySpace(
    timestamp=legal_document.last_updated,
    period_time_list=[
        sl.PeriodTime(timedelta(days=7), 1.0),     # Updated this week: full weight
        sl.PeriodTime(timedelta(days=30), 0.8),    # Updated this month: high weight
        sl.PeriodTime(timedelta(days=90), 0.5),    # Updated this quarter: medium weight
        sl.PeriodTime(timedelta(days=365), 0.2),   # Updated this year: low weight
        sl.PeriodTime(timedelta(days=730), 0.1),   # 2+ years: very low weight
    ],
    negative_filter=-0.7  # Faster decay for updates
)

# Last Verified Space - Quality assurance recency
last_verified_space = sl.RecencySpace(
    timestamp=legal_document.last_verified,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), 1.0),    # Verified this month: full weight
        sl.PeriodTime(timedelta(days=90), 0.8),    # Verified this quarter: high weight
        sl.PeriodTime(timedelta(days=180), 0.6),   # Verified 6 months ago: medium weight
        sl.PeriodTime(timedelta(days=365), 0.3),   # Verified this year: low weight
        sl.PeriodTime(timedelta(days=730), 0.1),   # 2+ years: needs re-verification
    ],
    negative_filter=-0.6  # Moderate decay for verification
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