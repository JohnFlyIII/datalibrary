"""
Spaces Module

This module aggregates all space types for the Legal Knowledge Platform:
- Hierarchical: Jurisdiction and practice area hierarchies
- Content: Discovery, exploration, and deep dive layers
- Preprocessing: Fact extraction and summaries
- Temporal: Time-based relevance
- Scoring: Numerical metrics
- Categorical: Classifications and filters
"""

# Import all space modules
from .hierarchical import *
from .content import *
from .preprocessing import *
from .temporal import *
from .scoring import *
from .categorical import *

# Aggregate all spaces by category
ALL_SPACES = {
    'hierarchical': ALL_HIERARCHICAL_SPACES,
    'content': ALL_CONTENT_SPACES,
    'preprocessing': ALL_PREPROCESSING_SPACES,
    'temporal': TEMPORAL_SPACES,
    'scoring': ALL_SCORING_SPACES,
    'categorical': ALL_CATEGORICAL_SPACES
}

# Progressive disclosure collections
PROGRESSIVE_DISCLOSURE = {
    'discovery': ALL_DISCOVERY_SPACES,
    'exploration': ALL_EXPLORATION_SPACES,
    'deep_dive': ALL_DEEP_DIVE_SPACES
}

# All spaces flat list
ALL_SPACES_LIST = (
    ALL_HIERARCHICAL_SPACES +
    ALL_CONTENT_SPACES +
    ALL_PREPROCESSING_SPACES +
    TEMPORAL_SPACES +
    ALL_SCORING_SPACES +
    ALL_CATEGORICAL_SPACES
)