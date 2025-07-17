"""
Legal Knowledge Platform - Superlinked Application

This is the main Superlinked application that combines all schema components
and embedding spaces for the legal knowledge platform.

Architecture:
- Modular schema design for extensibility
- Progressive disclosure query patterns
- Comprehensive embedding space coverage
- Production-ready configuration
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument
from spaces.content_spaces import *
from spaces.categorical_spaces import *

# Initialize the core schema
legal_document = LegalDocument()

# Define the Vector Database
vector_db = sl.Qdrant("legal_knowledge", host="qdrant", port=6333)

# Create the Index with Progressive Disclosure Architecture
legal_knowledge_index = sl.Index(
    spaces=[
        # Progressive Disclosure Content Spaces
        discovery_summary_space,
        discovery_topics_space,
        exploration_provisions_space,
        exploration_concepts_space,
        exploration_implications_space,
        deep_dive_content_space,
        deep_dive_precedents_space,
        deep_dive_citations_space,
        
        # Specialized Content Spaces
        client_takeaways_space,
        client_questions_space,
        compliance_requirements_space,
        penalties_space,
        keywords_space,
        synonyms_space,
        legislative_history_space,
        related_documents_space,
        
        # Categorical Classification Spaces
        jurisdiction_space,
        practice_areas_space,
        content_type_space,
        authority_level_space,
        target_audience_space,
        complexity_level_space,
        coverage_scope_space,
        update_priority_space
    ],
    fields=[
        # Core identification
        legal_document.id,
        legal_document.title,
        
        # Content structure
        legal_document.content_text,
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
        legal_document.jurisdiction,
        legal_document.practice_areas,
        legal_document.legal_topics,
        legal_document.authority_level,
        legal_document.content_type,
        
        # Temporal information
        legal_document.published_date,
        legal_document.effective_date,
        legal_document.last_updated,
        
        # Source information
        legal_document.source_url,
        legal_document.pdf_path,
        legal_document.citation_format,
        
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
        legal_document.last_verified,
        legal_document.notes_comments,
        
        # Usage analytics
        legal_document.access_frequency,
        legal_document.user_ratings,
        legal_document.search_performance,
        legal_document.update_priority
    ]
)

# Query Definitions for Progressive Disclosure

# Discovery Layer Query - Broad exploration
discovery_query = sl.Query(
    legal_knowledge_index,
    weights={
        discovery_summary_space: 3.0,
        discovery_topics_space: 2.0,
        client_takeaways_space: 1.5,
        jurisdiction_space: 1.0,
        practice_areas_space: 2.0,
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
        client_questions_space: 2.5,
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
        jurisdiction_space: 1.5
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
        jurisdiction_space: 1.5,
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

# Export query patterns for external use
QUERY_PATTERNS = {
    "discovery": discovery_query,
    "exploration": exploration_query,
    "deep_dive": deep_dive_query,
    "client_communication": client_communication_query,
    "compliance": compliance_query,
    "legal_research": legal_research_query,
    "passage": passage_query
}

# Export space collections for dynamic querying
SPACE_COLLECTIONS = {
    "discovery": DISCOVERY_SPACES,
    "exploration": EXPLORATION_SPACES,
    "deep_dive": DEEP_DIVE_SPACES,
    "client_communication": CLIENT_COMMUNICATION_SPACES,
    "compliance": COMPLIANCE_SPACES,
    "research": RESEARCH_SPACES,
    "search_enhancement": SEARCH_ENHANCEMENT_SPACES,
    "legal_taxonomy": LEGAL_TAXONOMY_SPACES,
    "content_organization": CONTENT_ORGANIZATION_SPACES,
    "administrative": ADMINISTRATIVE_SPACES,
    "search_filter": SEARCH_FILTER_SPACES
}

if __name__ == "__main__":
    print("Legal Knowledge Platform - Superlinked Application")
    print("="*50)
    print(f"Schema: {legal_document.__class__.__name__}")
    print(f"Vector DB: {vector_db.name}")
    print(f"Index: {legal_knowledge_index}")
    print(f"Query Patterns: {list(QUERY_PATTERNS.keys())}")
    print(f"Space Collections: {list(SPACE_COLLECTIONS.keys())}")
    print("="*50)