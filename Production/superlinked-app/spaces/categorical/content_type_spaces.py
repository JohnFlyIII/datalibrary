"""
Content Type Categorical Spaces

Purpose:
- Enable filtering by document type categories
- Support legal document classification
- Facilitate content type specific searches

Usage:
- Filter by primary sources (statutes, cases, regulations)
- Search within secondary sources (commentary, analysis)
- Find specific document types (contracts, briefs, etc.)
- Target practice documents vs. academic content

Human Note: Content type filtering is essential for legal research precision
AI Agent Note: Combine with authority level for comprehensive filtering
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Document Type Classification
content_type_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.content_type,
    categories=[
        # Primary Sources
        "statute",              # Legislative law
        "case_law",             # Court decisions
        "regulation",           # Administrative rules
        "constitutional",       # Constitutional provisions
        "treaty",               # International agreements
        "executive_order",      # Presidential/executive orders
        "administrative_rule",  # Agency rules
        
        # Secondary Sources  
        "commentary",           # Legal analysis and commentary
        "law_review",           # Academic articles
        "practice_guide",       # Practical guidance
        "legal_encyclopedia",   # Reference works
        "treatise",             # Comprehensive legal texts
        "continuing_education", # CLE materials
        "restatement",          # Restatements of law
        "annotation",           # Case annotations
        
        # Practice Documents
        "contract",             # Legal agreements
        "agreement",            # Various agreements
        "brief",                # Legal briefs
        "pleading",             # Court pleadings
        "motion",               # Legal motions
        "memorandum",           # Legal memos
        "opinion_letter",       # Legal opinions
        "form",                 # Legal forms
        "template",             # Document templates
        "checklist",            # Practice checklists
        
        # Business Documents
        "policy",               # Corporate policies
        "procedure",            # Standard procedures
        "handbook",             # Employee/policy handbooks
        "compliance_guide",     # Compliance documentation
        "training_material",    # Legal training content
        "code_of_conduct",      # Ethics codes
        
        # Court Documents
        "court_order",          # Judicial orders
        "judgment",             # Court judgments
        "injunction",           # Injunctive relief
        "settlement",           # Settlement agreements
        "discovery",            # Discovery documents
        "transcript",           # Court transcripts
        "docket",               # Court dockets
        
        # Administrative Documents
        "agency_guidance",      # Agency guidance docs
        "interpretive_rule",    # Interpretive rules
        "advisory_opinion",     # Advisory opinions
        "enforcement_action",   # Enforcement documents
        "consent_decree",       # Consent decrees
        "no_action_letter",     # Regulatory letters
        
        # Research Materials
        "research_memo",        # Research memoranda
        "case_summary",         # Case summaries
        "legal_update",         # Legal updates/alerts
        "client_alert",         # Client advisories
        "newsletter",           # Legal newsletters
        
        # Specialized Documents
        "patent",               # Patent documents
        "trademark",            # Trademark filings
        "copyright",            # Copyright registrations
        "license",              # License agreements
        "disclosure",           # Legal disclosures
    ]
)

# Simplified Type Categories (for broader filtering)
document_category_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.content_type,  # Maps to same field
    categories=[
        "primary_source",       # Binding legal authority
        "secondary_source",     # Commentary and analysis
        "practice_document",    # Practical legal documents
        "court_document",       # Court-related materials
        "business_document",    # Corporate/business docs
        "research_material",    # Research and analysis
        "form_template",        # Forms and templates
        "administrative"        # Administrative materials
    ]
)

# Document Purpose Classification
document_purpose_space = sl.CategoricalSimilaritySpace(
    category_list=legal_document.content_type,  # Maps to content type
    categories=[
        "informational",        # Provides information
        "transactional",        # Facilitates transactions
        "advocacy",             # Advocates positions
        "regulatory",           # Regulatory compliance
        "educational",          # Teaching/training
        "reference",            # Reference material
        "operational",          # Business operations
        "archival"              # Historical record
    ]
)

# Space Collections
CONTENT_TYPE_SPACES = [
    content_type_space,
    document_category_space,
    document_purpose_space
]

PRIMARY_SOURCE_TYPES = [
    "statute", "case_law", "regulation", "constitutional",
    "treaty", "executive_order", "administrative_rule"
]

SECONDARY_SOURCE_TYPES = [
    "commentary", "law_review", "practice_guide", "legal_encyclopedia",
    "treatise", "continuing_education", "restatement", "annotation"
]

PRACTICE_DOCUMENT_TYPES = [
    "contract", "agreement", "brief", "pleading", "motion",
    "memorandum", "opinion_letter", "form", "template"
]

# Export all
__all__ = [
    'content_type_space',
    'document_category_space',
    'document_purpose_space',
    'CONTENT_TYPE_SPACES',
    'PRIMARY_SOURCE_TYPES',
    'SECONDARY_SOURCE_TYPES',
    'PRACTICE_DOCUMENT_TYPES'
]

# Usage Examples:
"""
Content Type Query Patterns:

1. Primary Sources Only:
   .filter(legal_document.content_type.in_(PRIMARY_SOURCE_TYPES))
   weights = {
       content_type_space: 2.0,
       authority_level_space: 2.0,
       deep_dive_content_space: 3.0
   }

2. Case Law Research:
   .filter(legal_document.content_type == "case_law")
   weights = {
       content_type_space: 2.5,
       deep_dive_precedents_space: 3.0,
       deep_dive_citations_space: 2.5
   }

3. Practice Documents:
   .filter(legal_document.content_type.in_(PRACTICE_DOCUMENT_TYPES))
   weights = {
       content_type_space: 2.0,
       document_purpose_space: 1.5,
       exploration_provisions_space: 2.5
   }

4. Commentary and Analysis:
   .filter(legal_document.content_type.in_(["commentary", "law_review", "treatise"]))
   weights = {
       content_type_space: 2.0,
       exploration_concepts_space: 3.0,
       exploration_implications_space: 2.5
   }

5. Regulatory Materials:
   .filter(legal_document.content_type.in_(["regulation", "administrative_rule", "agency_guidance"]))
   weights = {
       content_type_space: 2.5,
       compliance_requirements_space: 3.0,
       effective_date_space: 2.0
   }

6. Forms and Templates:
   .filter(legal_document.content_type.in_(["form", "template", "checklist"]))
   weights = {
       content_type_space: 3.0,
       document_purpose_space: 2.0,
       target_audience_space: 1.5
   }
"""