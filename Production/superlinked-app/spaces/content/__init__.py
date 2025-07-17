"""
Content Spaces Module

This module provides text-based content spaces organized by progressive disclosure:
- Discovery: Broad exploration and topic understanding
- Exploration: Focused analysis and filtering
- Deep Dive: Detailed research and full context
"""

from .discovery_spaces import (
    discovery_summary_space,
    discovery_topics_space,
    content_density_space,
    coverage_scope_space,
    client_takeaways_space,
    DISCOVERY_CONTENT_SPACES,
    DISCOVERY_METADATA_SPACES,
    ALL_DISCOVERY_SPACES
)

from .exploration_spaces import (
    exploration_provisions_space,
    exploration_concepts_space,
    exploration_implications_space,
    compliance_requirements_space,
    relevance_score_space,
    complexity_level_space,
    penalties_space,
    exceptions_space,
    common_questions_space,
    EXPLORATION_CONTENT_SPACES,
    EXPLORATION_FILTER_SPACES,
    EXPLORATION_COMPLIANCE_SPACES,
    ALL_EXPLORATION_SPACES
)

from .deep_dive_spaces import (
    deep_dive_content_space,
    deep_dive_precedents_space,
    deep_dive_citations_space,
    legislative_history_space,
    related_documents_space,
    legal_topics_space,
    keywords_space,
    synonyms_space,
    chunk_context_space,
    acronyms_space,
    DEEP_DIVE_CONTENT_SPACES,
    DEEP_DIVE_REFERENCE_SPACES,
    DEEP_DIVE_SEARCH_SPACES,
    ALL_DEEP_DIVE_SPACES
)

# Combined content spaces by layer
PROGRESSIVE_DISCLOSURE_SPACES = {
    'discovery': ALL_DISCOVERY_SPACES,
    'exploration': ALL_EXPLORATION_SPACES,
    'deep_dive': ALL_DEEP_DIVE_SPACES
}

# All content spaces combined
ALL_CONTENT_SPACES = (
    ALL_DISCOVERY_SPACES + 
    ALL_EXPLORATION_SPACES + 
    ALL_DEEP_DIVE_SPACES
)

__all__ = [
    # Discovery
    'discovery_summary_space',
    'discovery_topics_space',
    'content_density_space',
    'coverage_scope_space',
    'client_takeaways_space',
    
    # Exploration
    'exploration_provisions_space',
    'exploration_concepts_space',
    'exploration_implications_space',
    'compliance_requirements_space',
    'relevance_score_space',
    'complexity_level_space',
    'penalties_space',
    'exceptions_space',
    'common_questions_space',
    
    # Deep Dive
    'deep_dive_content_space',
    'deep_dive_precedents_space',
    'deep_dive_citations_space',
    'legislative_history_space',
    'related_documents_space',
    'legal_topics_space',
    'keywords_space',
    'synonyms_space',
    'chunk_context_space',
    'acronyms_space',
    
    # Collections
    'PROGRESSIVE_DISCLOSURE_SPACES',
    'ALL_CONTENT_SPACES'
]