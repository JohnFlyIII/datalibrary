"""
Categorical Spaces Module

This module provides categorical filtering spaces for:
- Legal taxonomy and classification
- Document types and purposes
- Authority levels and audiences
"""

from .legal_taxonomy_spaces import (
    authority_level_space,
    target_audience_space,
    complexity_level_space,
    coverage_scope_space,
    update_priority_space,
    human_reviewed_space,
    LEGAL_TAXONOMY_SPACES,
    QUALITY_CONTROL_SPACES,
    CONTENT_ORGANIZATION_SPACES,
    ALL_LEGAL_TAXONOMY_SPACES
)

from .content_type_spaces import (
    content_type_space,
    document_category_space,
    document_purpose_space,
    CONTENT_TYPE_SPACES,
    PRIMARY_SOURCE_TYPES,
    SECONDARY_SOURCE_TYPES,
    PRACTICE_DOCUMENT_TYPES
)

# Combined categorical spaces
ALL_CATEGORICAL_SPACES = ALL_LEGAL_TAXONOMY_SPACES + CONTENT_TYPE_SPACES

# Search filter collections
SEARCH_FILTER_SPACES = [
    content_type_space,
    authority_level_space,
    target_audience_space,
    complexity_level_space
]

__all__ = [
    # Legal Taxonomy
    'authority_level_space',
    'target_audience_space',
    'complexity_level_space',
    'coverage_scope_space',
    'update_priority_space',
    'human_reviewed_space',
    
    # Content Types
    'content_type_space',
    'document_category_space',
    'document_purpose_space',
    
    # Collections
    'ALL_CATEGORICAL_SPACES',
    'SEARCH_FILTER_SPACES',
    'LEGAL_TAXONOMY_SPACES',
    'CONTENT_TYPE_SPACES',
    
    # Type Lists
    'PRIMARY_SOURCE_TYPES',
    'SECONDARY_SOURCE_TYPES',
    'PRACTICE_DOCUMENT_TYPES'
]