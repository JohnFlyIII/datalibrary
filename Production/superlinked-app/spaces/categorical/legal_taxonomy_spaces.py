"""
Legal Taxonomy Categorical Spaces

Purpose:
- Enable filtering by legal classification categories
- Support document type and authority level filtering
- Facilitate audience and complexity targeting

Usage:
- Filter by document authority (primary, secondary, etc.)
- Target specific audiences (practitioners, clients, etc.)
- Filter by complexity level
- Search within specific document types

Human Note: These spaces enable precise categorical filtering
AI Agent Note: Use these for hard filters rather than weighted search
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Authority Level Classification
authority_level_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.authority_level,
    categories=[
        "primary",           # Statutes, cases, regulations
        "secondary",         # Commentary, treatises, law review
        "tertiary",          # Practice guides, forms
        "binding",           # Controlling authority in jurisdiction
        "persuasive",        # Influential but not binding
        "superseded",        # No longer valid/current
        "proposed",          # Draft legislation/rules
        "pending"            # Under consideration
    ]
)

# Target Audience Classification
target_audience_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.target_audience,
    categories=[
        "practitioners",     # Practicing attorneys
        "judges",           # Judicial officers
        "business_owners",  # Corporate executives, managers
        "compliance_officers", # Corporate compliance teams
        "hr_professionals", # Human resources staff
        "general_public",   # Citizens, consumers
        "clients",          # Legal services clients
        "students",         # Law students, paralegals
        "academics",        # Law professors, researchers
        "government",       # Government agencies, officials
        "nonprofit",        # Nonprofit organizations
        "small_business",   # Small business owners
        "corporations",     # Large corporate entities
        "law_enforcement",  # Police, prosecutors
        "healthcare",       # Healthcare providers
        "finance",          # Financial services industry
        "technology",       # Tech companies, IT professionals
        "real_estate",      # Real estate professionals
        "international"     # International organizations
    ]
)

# Complexity Level Classification
complexity_level_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.complexity_level,
    categories=[
        "basic",            # Foundational concepts
        "intermediate",     # Standard practice level
        "advanced",         # Complex legal analysis
        "expert",           # Specialized expertise required
        "academic",         # Scholarly/theoretical
        "practical",        # Hands-on application
        "introductory",     # New practitioner level
        "reference"         # Quick lookup/checklist
    ]
)

# Coverage Scope Classification
coverage_scope_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.coverage_scope,
    categories=[
        "narrow",           # Specific issue/provision
        "moderate",         # Topic area coverage
        "comprehensive",    # Broad subject coverage
        "complete",         # Exhaustive treatment
        "overview",         # High-level summary
        "detailed",         # In-depth analysis
        "focused",          # Targeted application
        "general"           # Broad applicability
    ]
)

# Update Priority Classification
update_priority_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.update_priority,
    categories=[
        "high",             # Critical updates needed
        "medium",           # Standard maintenance
        "low",              # Minor updates/improvements
        "urgent",           # Immediate attention required
        "scheduled",        # Regular review cycle
        "monitor",          # Watch for changes
        "stable",           # Unlikely to change
        "deprecated"        # No longer maintained
    ]
)

# Human Review Status
human_reviewed_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.human_reviewed,
    categories=[
        "true",             # Expert validated
        "false",            # Not yet reviewed
        "partial",          # Partially reviewed
        "pending"           # Review in progress
    ]
)

# Space Collections
LEGAL_TAXONOMY_SPACES = [
    authority_level_space,
    target_audience_space,
    complexity_level_space,
    coverage_scope_space
]

QUALITY_CONTROL_SPACES = [
    update_priority_space,
    human_reviewed_space,
    authority_level_space
]

CONTENT_ORGANIZATION_SPACES = [
    target_audience_space,
    complexity_level_space,
    coverage_scope_space
]

ALL_LEGAL_TAXONOMY_SPACES = (
    LEGAL_TAXONOMY_SPACES + 
    QUALITY_CONTROL_SPACES
)

# Export all spaces
__all__ = [
    'authority_level_space',
    'target_audience_space',
    'complexity_level_space',
    'coverage_scope_space',
    'update_priority_space',
    'human_reviewed_space',
    'LEGAL_TAXONOMY_SPACES',
    'QUALITY_CONTROL_SPACES',
    'CONTENT_ORGANIZATION_SPACES',
    'ALL_LEGAL_TAXONOMY_SPACES'
]

# Usage Examples:
"""
Legal Taxonomy Query Patterns:

1. Primary Authority Only:
   .filter(legal_document.authority_level == "primary")
   weights = {
       authority_level_space: 2.0,
       deep_dive_content_space: 3.0
   }

2. Practitioner-Focused Content:
   .filter(legal_document.target_audience.contains("practitioners"))
   weights = {
       target_audience_space: 2.0,
       complexity_level_space: 1.5,
       exploration_provisions_space: 3.0
   }

3. Basic Level for Clients:
   .filter(legal_document.complexity_level == "basic")
   .filter(legal_document.target_audience.contains("clients"))
   weights = {
       complexity_level_space: 2.0,
       target_audience_space: 2.0,
       client_takeaways_space: 3.0
   }

4. Comprehensive Coverage:
   .filter(legal_document.coverage_scope.in_(["comprehensive", "complete"]))
   weights = {
       coverage_scope_space: 2.0,
       deep_dive_content_space: 3.0
   }

5. Quality Assured Content:
   .filter(legal_document.human_reviewed == "true")
   .filter(legal_document.confidence_score >= 90)
   weights = {
       human_reviewed_space: 1.5,
       confidence_score_space: 2.0
   }
"""