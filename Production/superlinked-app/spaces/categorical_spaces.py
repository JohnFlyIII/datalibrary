"""
Categorical Embedding Spaces

This module defines categorical similarity spaces for legal document classification.
These spaces enable filtering and organization by legal taxonomy.

Architecture:
- Hierarchical classification: Broad to specific categories
- Multi-label support: Documents can belong to multiple categories
- Extensible taxonomies: Easy to add new practice areas and jurisdictions
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Jurisdictional Classification Spaces

jurisdiction_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.jurisdiction,
    categories=[
        # Federal
        "federal",
        "supreme_court",
        "circuit_court", 
        "district_court",
        "federal_agency",
        
        # States - Major jurisdictions (expandable)
        "texas",
        "california", 
        "florida",
        "new_york",
        "illinois",
        "pennsylvania",
        "ohio",
        "georgia",
        "north_carolina",
        "michigan",
        
        # Local
        "municipal",
        "county",
        "local_government",
        
        # International (future expansion)
        "international",
        "treaty",
        "foreign_jurisdiction"
    ]
)

# Practice Area Classification Spaces

practice_areas_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.practice_areas,
    categories=[
        # Currently Implemented
        "employment",
        "personal_injury",
        "medical_malpractice",
        "civil_law",
        "tort_law",
        
        # Planned Expansions
        "corporate",
        "contract_law",
        "intellectual_property",
        "patents",
        "trademarks",
        "copyright",
        "family_law",
        "divorce",
        "child_custody",
        "criminal_law",
        "real_estate",
        "property_law",
        "tax_law",
        "immigration",
        "bankruptcy",
        "securities",
        "environmental",
        "healthcare",
        "insurance",
        "litigation",
        "arbitration",
        "compliance",
        "regulatory",
        "administrative",
        "constitutional",
        "civil_rights",
        "labor_law",
        "workers_compensation",
        "product_liability",
        "class_action",
        "antitrust",
        "merger_acquisition",
        "corporate_governance",
        "nonprofit",
        "estate_planning",
        "probate",
        "elder_law",
        "disability_law",
        "social_security",
        "veterans_law",
        "education_law",
        "sports_law",
        "entertainment",
        "media_law",
        "privacy",
        "data_protection",
        "cybersecurity",
        "telecommunications",
        "energy_law",
        "oil_gas",
        "mining",
        "agriculture",
        "transportation",
        "aviation",
        "maritime",
        "international_trade"
    ]
)

# Document Type Classification

content_type_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.content_type,
    categories=[
        # Primary Sources
        "statute",
        "case_law",
        "regulation",
        "constitutional",
        "treaty",
        "executive_order",
        "administrative_rule",
        
        # Secondary Sources  
        "commentary",
        "law_review",
        "practice_guide",
        "legal_encyclopedia",
        "treatise",
        "continuing_education",
        
        # Practice Documents
        "contract",
        "agreement",
        "brief",
        "pleading",
        "motion",
        "memorandum",
        "opinion_letter",
        "form",
        "template",
        
        # Business Documents
        "policy",
        "procedure",
        "handbook",
        "compliance_guide",
        "training_material",
        
        # Court Documents
        "court_order",
        "judgment",
        "injunction",
        "settlement",
        "discovery",
        
        # Administrative
        "agency_guidance",
        "interpretive_rule",
        "advisory_opinion",
        "enforcement_action",
        "consent_decree"
    ]
)

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

# Space Collections for Query Routing

# Legal Taxonomy Collection
LEGAL_TAXONOMY_SPACES = [
    jurisdiction_space,
    practice_areas_space,
    content_type_space,
    authority_level_space
]

# Content Organization Collection  
CONTENT_ORGANIZATION_SPACES = [
    target_audience_space,
    complexity_level_space,
    coverage_scope_space
]

# Administrative Collection
ADMINISTRATIVE_SPACES = [
    update_priority_space,
    authority_level_space
]

# Search Filtering Collection
SEARCH_FILTER_SPACES = [
    jurisdiction_space,
    practice_areas_space,
    content_type_space,
    target_audience_space,
    complexity_level_space
]