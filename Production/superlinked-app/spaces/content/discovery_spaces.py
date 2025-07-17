"""
Discovery Layer Content Spaces

Purpose:
- Enable broad, exploratory searches
- Support initial research and topic understanding
- Facilitate knowledge landscape mapping

Usage:
- First-pass searches on new topics
- Understanding scope of available content
- Identifying relevant practice areas
- Building initial research queries

Human Note: Discovery spaces are optimized for breadth over depth
AI Agent Note: Use high weights on these spaces for initial exploration
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument
# Import coverage_scope_space to avoid duplication
from ..categorical.legal_taxonomy_spaces import coverage_scope_space

# Initialize the legal document schema
legal_document = LegalDocument()

# Broad Summary Space - High-level document overviews
discovery_summary_space = sl.TextSimilaritySpace(
    text=legal_document.summary,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=500, chunk_overlap=100)
)

# Topic Classification Space - Broad subject categories
discovery_topics_space = sl.TextSimilaritySpace(
    text=legal_document.broad_topics,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Content Density Space - How much content exists on topic
content_density_space = sl.NumberSpace(
    number=legal_document.content_density,
    min_value=0,
    max_value=100,
    mode=sl.Mode.SIMILAR  # Find similar density levels
)

# Note: coverage_scope_space is imported from categorical.legal_taxonomy_spaces
# to avoid duplicate definitions and ensure consistency

# Client Takeaways Space - Simplified explanations
client_takeaways_space = sl.TextSimilaritySpace(
    text=legal_document.key_takeaways,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Discovery Layer Collections
DISCOVERY_CONTENT_SPACES = [
    discovery_summary_space,
    discovery_topics_space,
    client_takeaways_space
]

DISCOVERY_METADATA_SPACES = [
    content_density_space,
    coverage_scope_space
]

ALL_DISCOVERY_SPACES = DISCOVERY_CONTENT_SPACES + DISCOVERY_METADATA_SPACES

# Export all spaces
__all__ = [
    'discovery_summary_space',
    'discovery_topics_space',
    'content_density_space',
    'coverage_scope_space',
    'client_takeaways_space',
    'DISCOVERY_CONTENT_SPACES',
    'DISCOVERY_METADATA_SPACES',
    'ALL_DISCOVERY_SPACES'
]

# Usage Examples:
"""
Discovery Query Patterns:

1. Initial Topic Exploration:
   weights = {
       discovery_topics_space: 3.0,
       discovery_summary_space: 2.5,
       coverage_scope_space: 1.5,
       content_density_space: 1.0
   }

2. Comprehensive Overview:
   weights = {
       discovery_summary_space: 3.0,
       client_takeaways_space: 2.0,
       discovery_topics_space: 2.0,
       coverage_scope_space: 1.5
   }

3. Content Availability Check:
   weights = {
       content_density_space: 3.0,
       coverage_scope_space: 2.5,
       discovery_topics_space: 2.0
   }

4. Client-Friendly Discovery:
   weights = {
       client_takeaways_space: 3.0,
       discovery_summary_space: 2.0,
       discovery_topics_space: 1.5
   }
"""