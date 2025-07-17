"""
Preprocessing Spaces Module

This module provides spaces for AI-preprocessed content:
- Fact extraction with citations
- Summary generation in multiple formats
"""

from .fact_extraction_spaces import (
    extracted_facts_space,
    key_findings_space,
    fact_locations_space,
    fact_count_space,
    citations_apa_space,
    internal_citations_space,
    external_citations_space,
    FACT_EXTRACTION_SPACES,
    CITATION_SPACES,
    ALL_FACT_SPACES
)

from .summary_spaces import (
    executive_summary_space,
    summary_bullets_space,
    summary_conclusion_space,
    detailed_summary_space,
    key_takeaways_space,
    EXECUTIVE_SUMMARY_SPACES,
    DETAILED_SUMMARY_SPACES,
    ALL_SUMMARY_SPACES
)

# Combined preprocessing spaces
ALL_PREPROCESSING_SPACES = ALL_FACT_SPACES + ALL_SUMMARY_SPACES

__all__ = [
    # Fact Extraction
    'extracted_facts_space',
    'key_findings_space',
    'fact_locations_space',
    'fact_count_space',
    'citations_apa_space',
    'internal_citations_space',
    'external_citations_space',
    
    # Summaries
    'executive_summary_space',
    'summary_bullets_space',
    'summary_conclusion_space',
    'detailed_summary_space',
    'key_takeaways_space',
    
    # Collections
    'FACT_EXTRACTION_SPACES',
    'CITATION_SPACES',
    'ALL_FACT_SPACES',
    'EXECUTIVE_SUMMARY_SPACES',
    'DETAILED_SUMMARY_SPACES',
    'ALL_SUMMARY_SPACES',
    'ALL_PREPROCESSING_SPACES'
]