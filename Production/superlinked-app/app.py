"""
Legal Knowledge Platform - Enhanced Superlinked Application

Purpose:
- Main application combining all modular spaces
- Supports hierarchical search patterns
- Integrates preprocessing and fact extraction
- Provides multiple query patterns for different use cases

Architecture:
- Modular space imports for maintainability
- Hierarchical support for jurisdictions and practice areas
- Preprocessing integration for facts and summaries
- Progressive disclosure query patterns

Human Note: This is the main entry point - modify query weights for your use case
AI Agent Note: Consider space combinations based on search intent
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Import all space modules
from spaces.hierarchical import (
    # Jurisdiction spaces
    country_jurisdiction_space,
    state_jurisdiction_space,
    city_jurisdiction_space,
    jurisdiction_path_space,
    # Practice area spaces
    primary_practice_space,
    secondary_practice_space,
    specific_practice_space,
    practice_path_space,
    # Legacy spaces
    legacy_jurisdiction_space,
    legacy_practice_space,
    # Collections
    JURISDICTION_HIERARCHY_SPACES,
    PRACTICE_HIERARCHY_SPACES,
    ALL_HIERARCHICAL_SPACES
)

from spaces.content import (
    # Discovery spaces
    discovery_summary_space,
    discovery_topics_space,
    client_takeaways_space,
    # Exploration spaces
    exploration_provisions_space,
    exploration_concepts_space,
    exploration_implications_space,
    # Deep dive spaces
    deep_dive_content_space,
    deep_dive_precedents_space,
    deep_dive_citations_space,
    # Specialized spaces
    common_questions_space,
    compliance_requirements_space,
    penalties_space,
    exceptions_space,
    keywords_space,
    synonyms_space,
    legislative_history_space,
    related_documents_space,
    # Collections
    ALL_DISCOVERY_SPACES,
    ALL_EXPLORATION_SPACES,
    ALL_DEEP_DIVE_SPACES,
    ALL_CONTENT_SPACES
)

from spaces.preprocessing import (
    # Fact extraction spaces
    extracted_facts_space,
    key_findings_space,
    fact_locations_space,
    fact_count_space,
    citations_apa_space,
    # Summary spaces
    executive_summary_space,
    summary_bullets_space,
    summary_conclusion_space,
    # Collections
    FACT_EXTRACTION_SPACES,
    ALL_SUMMARY_SPACES,
    ALL_PREPROCESSING_SPACES
)

from spaces.temporal import (
    published_recency_space,
    effective_date_space,
    last_updated_space,
    TEMPORAL_SPACES
)

from spaces.scoring import (
    client_relevance_score_space,
    confidence_score_space,
    readability_score_space,
    search_weight_space,
    ALL_SCORING_SPACES
)

from spaces.categorical import (
    # Legal taxonomy spaces
    authority_level_space,
    target_audience_space,
    complexity_level_space,
    coverage_scope_space,
    update_priority_space,
    human_reviewed_space,
    # Content type spaces
    content_type_space,
    document_category_space,
    document_purpose_space,
    # Collections
    ALL_CATEGORICAL_SPACES
)

# Initialize the core schema
legal_document = LegalDocument()

# Define the Vector Database (Qdrant on AWS)
vector_db = sl.Qdrant("legal_knowledge", host="qdrant", port=6333)

# Create the Enhanced Index with All Spaces
legal_knowledge_index = sl.Index(
    spaces=[
        # Hierarchical Spaces
        country_jurisdiction_space,
        state_jurisdiction_space,
        city_jurisdiction_space,
        jurisdiction_path_space,
        primary_practice_space,
        secondary_practice_space,
        specific_practice_space,
        practice_path_space,
        
        # Progressive Disclosure Content Spaces
        discovery_summary_space,
        discovery_topics_space,
        exploration_provisions_space,
        exploration_concepts_space,
        exploration_implications_space,
        deep_dive_content_space,
        deep_dive_precedents_space,
        deep_dive_citations_space,
        
        # Preprocessing Spaces
        extracted_facts_space,
        key_findings_space,
        fact_locations_space,
        fact_count_space,
        executive_summary_space,
        summary_bullets_space,
        summary_conclusion_space,
        
        # Specialized Content Spaces
        client_takeaways_space,
        common_questions_space,
        compliance_requirements_space,
        penalties_space,
        keywords_space,
        synonyms_space,
        legislative_history_space,
        related_documents_space,
        
        # Temporal Spaces
        published_recency_space,
        effective_date_space,
        last_updated_space,
        
        # Scoring Spaces
        client_relevance_score_space,
        confidence_score_space,
        readability_score_space,
        search_weight_space,
        
        # Categorical Classification Spaces
        content_type_space,
        authority_level_space,
        target_audience_space,
        complexity_level_space,
        coverage_scope_space,
        update_priority_space,
        
        # Legacy compatibility spaces
        legacy_jurisdiction_space,
        legacy_practice_space
    ],
    fields=[
        # Core identification
        legal_document.id,
        legal_document.title,
        legal_document.content_text,
        
        # Preprocessing fields
        legal_document.extracted_facts,
        legal_document.fact_locations,
        legal_document.fact_count,
        legal_document.key_findings,
        legal_document.executive_summary,
        legal_document.summary_bullet_points,
        legal_document.summary_conclusion,
        
        # Hierarchical fields
        legal_document.jurisdiction_country,
        legal_document.jurisdiction_state,
        legal_document.jurisdiction_city,
        legal_document.jurisdiction_full_path,
        legal_document.practice_area_primary,
        legal_document.practice_area_secondary,
        legal_document.practice_area_specific,
        legal_document.practice_area_full_path,
        
        # Legacy fields
        legal_document.jurisdiction,
        legal_document.practice_areas,
        
        # Content structure
        legal_document.summary,
        legal_document.key_provisions,
        legal_document.practical_implications,
        
        # Document hierarchy
        legal_document.parent_document_id,
        legal_document.chunk_index,
        legal_document.start_char,
        legal_document.end_char,
        legal_document.chunk_context,
        legal_document.is_chunk,
        
        # Legal classification
        legal_document.legal_topics,
        legal_document.authority_level,
        legal_document.content_type,
        
        # Citation fields
        legal_document.citations_apa7,
        legal_document.internal_citations,
        legal_document.external_citations,
        legal_document.citation_format,
        
        # Temporal information
        legal_document.published_date,
        legal_document.effective_date,
        legal_document.last_updated,
        legal_document.last_verified,
        
        # Source information
        legal_document.source_url,
        legal_document.pdf_path,
        
        # Progressive disclosure fields
        legal_document.broad_topics,
        legal_document.content_density,
        legal_document.coverage_scope,
        legal_document.legal_concepts,
        legal_document.client_relevance_score,
        legal_document.complexity_level,
        legal_document.case_precedents,
        legal_document.citation_context,
        legal_document.legislative_history,
        
        # Relationship fields
        legal_document.cites_documents,
        legal_document.cited_by_documents,
        legal_document.related_documents,
        legal_document.superseded_by,
        
        # Content strategy fields
        legal_document.target_audience,
        legal_document.readability_score,
        legal_document.key_takeaways,
        legal_document.common_questions,
        
        # Legal practice fields
        legal_document.compliance_requirements,
        legal_document.deadlines_timeframes,
        legal_document.parties_affected,
        legal_document.penalties_consequences,
        legal_document.exceptions_exclusions,
        
        # Search enhancement
        legal_document.keywords,
        legal_document.synonyms,
        legal_document.acronyms_abbreviations,
        legal_document.search_weight,
        
        # Quality & validation
        legal_document.confidence_score,
        legal_document.human_reviewed,
        legal_document.notes_comments,
        legal_document.preprocessing_version,
        
        # Usage analytics
        legal_document.access_frequency,
        legal_document.user_ratings,
        legal_document.search_performance,
        legal_document.update_priority
    ]
)

# Enhanced Query Patterns

# 1. Hierarchical Jurisdiction Query
hierarchical_jurisdiction_query = sl.Query(
    legal_knowledge_index,
    weights={
        country_jurisdiction_space: 1.0,
        state_jurisdiction_space: 2.0,
        city_jurisdiction_space: 3.0,
        jurisdiction_path_space: 2.5,
        deep_dive_content_space: 2.0
    }
)

# 2. Hierarchical Practice Area Query
hierarchical_practice_query = sl.Query(
    legal_knowledge_index,
    weights={
        primary_practice_space: 1.5,
        secondary_practice_space: 2.5,
        specific_practice_space: 3.0,
        practice_path_space: 2.5,
        exploration_provisions_space: 2.0
    }
)

# 3. Fact-Based Research Query
fact_research_query = sl.Query(
    legal_knowledge_index,
    weights={
        extracted_facts_space: 3.0,
        key_findings_space: 2.5,
        fact_locations_space: 2.0,
        citations_apa_space: 2.0,
        deep_dive_content_space: 1.5
    }
)

# 4. Executive Briefing Query
executive_briefing_query = sl.Query(
    legal_knowledge_index,
    weights={
        executive_summary_space: 3.0,
        summary_bullets_space: 2.5,
        summary_conclusion_space: 2.5,
        key_takeaways_space: 2.0,
        client_relevance_score_space: 1.5
    }
)

# 5. Texas Employment Law Query (Combined Hierarchical)
texas_employment_query = sl.Query(
    legal_knowledge_index,
    weights={
        # Jurisdiction hierarchy
        country_jurisdiction_space: 0.5,    # US context
        state_jurisdiction_space: 3.0,      # Texas focus
        city_jurisdiction_space: 1.0,       # Include city ordinances
        
        # Practice hierarchy  
        primary_practice_space: 1.0,        # Labor/employment
        secondary_practice_space: 3.0,      # Specific employment issues
        specific_practice_space: 2.0,       # Ultra-specific topics
        
        # Content
        exploration_provisions_space: 2.5,
        compliance_requirements_space: 2.5,
        penalties_space: 2.0
    }
)

# 6. Time-Sensitive Compliance Query
time_sensitive_compliance_query = sl.Query(
    legal_knowledge_index,
    weights={
        compliance_requirements_space: 3.0,
        effective_date_space: 3.0,
        published_recency_space: 2.5,
        penalties_space: 2.5,
        update_priority_space: 2.0,
        exceptions_space: 1.5
    }
)

# Progressive Disclosure Queries

# Discovery Layer Query - Broad exploration
discovery_query = sl.Query(
    legal_knowledge_index,
    weights={
        discovery_summary_space: 3.0,
        discovery_topics_space: 2.0,
        client_takeaways_space: 1.5,
        primary_practice_space: 1.0,
        country_jurisdiction_space: 1.0,
        content_type_space: 1.0
    }
)

# Exploration Layer Query - Focused analysis
exploration_query = sl.Query(
    legal_knowledge_index,
    weights={
        exploration_provisions_space: 3.0,
        exploration_concepts_space: 2.5,
        exploration_implications_space: 2.0,
        compliance_requirements_space: 2.0,
        authority_level_space: 1.5,
        complexity_level_space: 1.0
    }
)

# Deep Dive Query - Detailed research
deep_dive_query = sl.Query(
    legal_knowledge_index,
    weights={
        deep_dive_content_space: 3.0,
        deep_dive_precedents_space: 2.5,
        deep_dive_citations_space: 2.0,
        legislative_history_space: 1.5,
        related_documents_space: 1.0,
        keywords_space: 1.0
    }
)

# Specialized Query Patterns

# Client Communication Query - Simplified explanations
client_communication_query = sl.Query(
    legal_knowledge_index,
    weights={
        client_takeaways_space: 3.0,
        summary_bullets_space: 2.5,
        exploration_implications_space: 2.0,
        discovery_summary_space: 1.5,
        target_audience_space: 1.0
    }
)

# Compliance Query - Action-oriented research
compliance_query = sl.Query(
    legal_knowledge_index,
    weights={
        compliance_requirements_space: 3.0,
        penalties_space: 2.5,
        exploration_provisions_space: 2.0,
        authority_level_space: 2.0,
        state_jurisdiction_space: 1.5
    }
)

# Legal Research Query - Comprehensive analysis
legal_research_query = sl.Query(
    legal_knowledge_index,
    weights={
        deep_dive_content_space: 2.5,
        deep_dive_precedents_space: 2.5,
        exploration_provisions_space: 2.0,
        authority_level_space: 2.0,
        state_jurisdiction_space: 1.5,
        content_type_space: 1.5
    }
)

# Passage-Level Query - Chunk-specific search
passage_query = sl.Query(
    legal_knowledge_index,
    weights={
        deep_dive_content_space: 3.0,
        exploration_provisions_space: 2.0,
        keywords_space: 1.5,
        synonyms_space: 1.0
    }
)

# Create the Superlinked App
app = sl.SuperlinkedApp(
    "legal_knowledge_platform",
    vector_db,
    [legal_knowledge_index]
)

# Export Query Patterns
QUERY_PATTERNS = {
    # Progressive Disclosure
    "discovery": discovery_query,
    "exploration": exploration_query,
    "deep_dive": deep_dive_query,
    
    # Hierarchical
    "hierarchical_jurisdiction": hierarchical_jurisdiction_query,
    "hierarchical_practice": hierarchical_practice_query,
    "texas_employment": texas_employment_query,
    
    # Preprocessing-based
    "fact_research": fact_research_query,
    "executive_briefing": executive_briefing_query,
    
    # Specialized
    "client_communication": client_communication_query,
    "compliance": compliance_query,
    "legal_research": legal_research_query,
    "time_sensitive": time_sensitive_compliance_query,
    "passage": passage_query
}

# Export Space Collections
SPACE_COLLECTIONS = {
    # Hierarchical
    "jurisdiction_hierarchy": JURISDICTION_HIERARCHY_SPACES,
    "practice_hierarchy": PRACTICE_HIERARCHY_SPACES,
    
    # Content Layers
    "discovery": ALL_DISCOVERY_SPACES,
    "exploration": ALL_EXPLORATION_SPACES,
    "deep_dive": ALL_DEEP_DIVE_SPACES,
    
    # Preprocessing
    "fact_extraction": FACT_EXTRACTION_SPACES,
    "summaries": ALL_SUMMARY_SPACES,
    
    # Other categories
    "temporal": TEMPORAL_SPACES,
    "scoring": ALL_SCORING_SPACES,
    "categorical": ALL_CATEGORICAL_SPACES
}

if __name__ == "__main__":
    print("Enhanced Legal Knowledge Platform - Superlinked Application")
    print("="*60)
    print(f"Schema: {legal_document.__class__.__name__}")
    print(f"Vector DB: {vector_db}")
    print(f"Total Spaces: {len(legal_knowledge_index.spaces)}")
    print(f"Total Fields: {len(legal_knowledge_index.fields)}")
    print(f"Query Patterns: {list(QUERY_PATTERNS.keys())}")
    print(f"Space Collections: {list(SPACE_COLLECTIONS.keys())}")
    print("\nKey Features:")
    print("- Hierarchical jurisdiction support (Country → State → City)")
    print("- Hierarchical practice area support")
    print("- AI preprocessing integration (facts + summaries)")
    print("- Progressive disclosure architecture")
    print("- Time-sensitive search capabilities")
    print("="*60)