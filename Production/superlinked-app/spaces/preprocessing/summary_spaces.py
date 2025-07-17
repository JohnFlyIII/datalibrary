"""
Summary and Executive Summary Spaces

Purpose:
- Enable search within AI-generated summaries
- Support different summary formats (executive, bullet points, conclusions)
- Facilitate quick document understanding

Usage:
- Quick overview searches
- Executive briefing preparation
- Key point extraction
- Conclusion-focused research

Human Note: Summaries are generated during preprocessing for quick access
AI Agent Note: Weight these spaces higher for overview/survey searches
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Executive Summary Space - One-page summaries
executive_summary_space = sl.TextSimilaritySpace(
    text=legal_document.executive_summary,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=300, chunk_overlap=75)
)

# Bullet Points Space - Key points in list format
summary_bullets_space = sl.TextSimilaritySpace(
    text=legal_document.summary_bullet_points,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Conclusion Space - Main takeaways
summary_conclusion_space = sl.TextSimilaritySpace(
    text=legal_document.summary_conclusion,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Original Summary Space - Detailed 1-2 page summaries
detailed_summary_space = sl.TextSimilaritySpace(
    text=legal_document.summary,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=500, chunk_overlap=100)
)

# Key Takeaways Space - For content strategy
key_takeaways_space = sl.TextSimilaritySpace(
    text=legal_document.key_takeaways,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Summary Collections
EXECUTIVE_SUMMARY_SPACES = [
    executive_summary_space,
    summary_bullets_space,
    summary_conclusion_space
]

DETAILED_SUMMARY_SPACES = [
    detailed_summary_space,
    key_takeaways_space
]

ALL_SUMMARY_SPACES = EXECUTIVE_SUMMARY_SPACES + DETAILED_SUMMARY_SPACES

# Export all spaces
__all__ = [
    'executive_summary_space',
    'summary_bullets_space',
    'summary_conclusion_space',
    'detailed_summary_space',
    'key_takeaways_space',
    'EXECUTIVE_SUMMARY_SPACES',
    'DETAILED_SUMMARY_SPACES',
    'ALL_SUMMARY_SPACES'
]

# Usage Examples:
"""
Summary-Based Query Patterns:

1. Quick Executive Overview:
   weights = {
       executive_summary_space: 3.0,
       summary_conclusion_space: 2.0,
       summary_bullets_space: 1.5
   }

2. Detailed Analysis Summary:
   weights = {
       detailed_summary_space: 3.0,
       key_takeaways_space: 2.0,
       executive_summary_space: 1.0
   }

3. Key Points Only:
   weights = {
       summary_bullets_space: 3.0,
       key_takeaways_space: 2.5,
       summary_conclusion_space: 2.0
   }

4. Conclusion-Focused:
   weights = {
       summary_conclusion_space: 3.0,
       key_takeaways_space: 2.0,
       executive_summary_space: 1.0
   }
"""