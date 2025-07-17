"""
Base Legal Document Schema

This module defines the core LegalDocument class that serves as the foundation
for all legal document types in the knowledge platform.

Design Principles:
- Extensible base class for all legal documents
- Support for passage-level chunking and full documents
- Progressive disclosure architecture (discovery/exploration/deep-dive)
- Comprehensive metadata for legal research and compliance
"""

import superlinked as sl
from typing import Optional


@sl.schema
class LegalDocument:
    """
    Base schema for all legal documents in the knowledge platform.
    
    This class provides the foundational structure that can be extended
    for specific document types (statutes, cases, regulations, contracts)
    and specialized practice areas.
    """
    
    # Core Identification Fields
    id: sl.IdField
    title: sl.String
    content_text: sl.String
    
    # Content Structure Fields
    summary: sl.String                      # AI-generated summary (1-2 pages)
    key_provisions: sl.String               # Critical legal requirements
    practical_implications: sl.String       # Real-world impact and meaning
    
    # Document Hierarchy & Chunking
    parent_document_id: sl.String           # Links chunks to parent document  
    chunk_index: sl.Integer                 # Position within document (0-based)
    start_char: sl.Integer                  # Character offset start
    end_char: sl.Integer                    # Character offset end
    chunk_context: sl.String                # Surrounding text for proper citation
    is_chunk: sl.String                     # "true" for chunks, "false" for full docs
    
    # Legal Classification
    jurisdiction: sl.String                 # federal, texas, california, etc.
    practice_areas: sl.String               # employment,personal_injury,corporate
    legal_topics: sl.String                 # specific legal concepts
    authority_level: sl.String              # primary, secondary, tertiary
    content_type: sl.String                 # statute, case_law, regulation, commentary
    
    # Temporal Information  
    published_date: sl.String               # When document was published
    effective_date: sl.String               # When law/rule takes effect
    last_updated: sl.String                 # Most recent amendment/revision
    
    # Source & Access Information
    source_url: sl.String                   # Official source URL
    pdf_path: sl.String                     # Local file path
    citation_format: sl.String              # Proper legal citation format
    
    # Progressive Disclosure Layers
    
    # Discovery Layer - High-level exploration
    broad_topics: sl.String                 # High-level categorization
    content_density: sl.Integer             # Content amount on topic (0-100)
    coverage_scope: sl.String               # narrow, moderate, comprehensive
    
    # Exploration Layer - Focused analysis  
    legal_concepts: sl.String               # Semantic legal concepts
    client_relevance_score: sl.Integer      # Relevance to client work (0-10)
    complexity_level: sl.String             # basic, intermediate, advanced
    
    # Deep Dive Layer - Detailed research
    case_precedents: sl.String              # Related case law references
    citation_context: sl.String             # Cross-document connections
    legislative_history: sl.String          # Background and development
    
    # Relationship Fields
    cites_documents: sl.String              # Documents this one cites
    cited_by_documents: sl.String           # Documents that cite this one
    related_documents: sl.String            # Conceptually related content
    superseded_by: sl.String                # Newer versions or amendments
    
    # Content Strategy Fields
    target_audience: sl.String              # practitioners, business_owners, clients
    readability_score: sl.Integer           # Reading difficulty (0-100)
    key_takeaways: sl.String                # Main points for content creation
    common_questions: sl.String             # FAQ-style information
    
    # Legal Practice Fields
    compliance_requirements: sl.String      # Specific actions required
    deadlines_timeframes: sl.String         # Important dates and periods
    parties_affected: sl.String             # Who must comply/is protected
    penalties_consequences: sl.String       # Results of non-compliance
    exceptions_exclusions: sl.String        # When rules don't apply
    
    # Search Enhancement Fields
    keywords: sl.String                     # Important search terms
    synonyms: sl.String                     # Alternative terminology
    acronyms_abbreviations: sl.String       # Legal shorthand and acronyms
    search_weight: sl.Integer               # Boost factor for search (0-10)
    
    # Quality & Validation Fields
    confidence_score: sl.Integer            # AI confidence in analysis (0-100)
    human_reviewed: sl.String               # "true" if expert-validated
    last_verified: sl.String                # Date of last accuracy check
    notes_comments: sl.String               # Internal annotations
    
    # Usage Analytics Fields  
    access_frequency: sl.Integer            # How often accessed
    user_ratings: sl.String                 # User feedback scores
    search_performance: sl.Integer          # Search result effectiveness
    update_priority: sl.String              # high, medium, low