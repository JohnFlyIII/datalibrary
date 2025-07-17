"""
Hierarchical Spaces Module

This module provides hierarchical navigation spaces for:
- Jurisdiction hierarchies (Country -> State -> City)
- Practice area hierarchies (Primary -> Secondary -> Specific)
"""

from .jurisdiction_hierarchy import (
    country_jurisdiction_space,
    state_jurisdiction_space,
    city_jurisdiction_space,
    jurisdiction_path_space,
    legacy_jurisdiction_space,
    JURISDICTION_HIERARCHY_SPACES
)

from .practice_area_hierarchy import (
    primary_practice_space,
    secondary_practice_space,
    specific_practice_space,
    practice_path_space,
    legacy_practice_space,
    PRACTICE_HIERARCHY_SPACES
)

# Combined hierarchical spaces
ALL_HIERARCHICAL_SPACES = JURISDICTION_HIERARCHY_SPACES + PRACTICE_HIERARCHY_SPACES

__all__ = [
    # Jurisdiction
    'country_jurisdiction_space',
    'state_jurisdiction_space',
    'city_jurisdiction_space',
    'jurisdiction_path_space',
    'legacy_jurisdiction_space',
    'JURISDICTION_HIERARCHY_SPACES',
    
    # Practice Areas
    'primary_practice_space',
    'secondary_practice_space',
    'specific_practice_space',
    'practice_path_space',
    'legacy_practice_space',
    'PRACTICE_HIERARCHY_SPACES',
    
    # Combined
    'ALL_HIERARCHICAL_SPACES'
]