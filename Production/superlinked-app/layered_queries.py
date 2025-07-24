"""
Three-Layer Query System for Advanced Legal Search
================================================

Implements progressive disclosure search patterns:
1. Discovery - broad search across document summaries 
2. Exploration - focused search within document types/jurisdictions
3. Deep Dive - precise chunk-level search for exact passages
"""

from superlinked import framework as sl
from .index import legal_document, index as document_index, content_space, document_type_space, jurisdiction_space
from .chunk_schema import chunk_schema, chunk_index, chunk_content_space, chunk_type_space, chunk_jurisdiction_space

# LAYER 1: DISCOVERY QUERIES
# Broad search across all documents for initial exploration

discovery_query = (
    sl.Query(document_index)
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=10))
)

discovery_by_type_query = (
    sl.Query(document_index)
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .similar(document_type_space, sl.Param("document_type"))
    .select_all()
    .limit(sl.Param("limit", default=10))
)

discovery_by_jurisdiction_query = (
    sl.Query(document_index)
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .similar(jurisdiction_space, sl.Param("jurisdiction"))
    .select_all()
    .limit(sl.Param("limit", default=10))
)

# LAYER 2: EXPLORATION QUERIES  
# Focused search with multiple filters for deeper investigation

exploration_query = (
    sl.Query(document_index)
    .find(legal_document)
    .similar(content_space.text, sl.Param("search_query"))
    .similar(document_type_space, sl.Param("document_type"))
    .similar(jurisdiction_space, sl.Param("jurisdiction"))
    .select_all()
    .limit(sl.Param("limit", default=5))
)

# LAYER 3: DEEP DIVE QUERIES
# Precise chunk-level search for exact text passages

deep_dive_query = (
    sl.Query(chunk_index)
    .find(chunk_schema)
    .similar(chunk_content_space.text, sl.Param("search_query"))
    .similar(chunk_type_space, sl.Param("document_type"))
    .similar(chunk_jurisdiction_space, sl.Param("jurisdiction"))
    .select_all()
    .limit(sl.Param("limit", default=20))
)

deep_dive_precise_query = (
    sl.Query(chunk_index)
    .find(chunk_schema)
    .similar(chunk_content_space.text, sl.Param("search_query"))
    .select_all()
    .limit(sl.Param("limit", default=10))
)

# COMBINED WORKFLOW QUERIES
# Multi-step search patterns for comprehensive research

def create_research_workflow_queries():
    """Create queries for comprehensive legal research workflow"""
    
    # Step 1: Initial discovery
    initial_discovery = (
        sl.Query(document_index)
        .find(legal_document)
        .similar(content_space.text, sl.Param("research_topic"))
        .select_all()
        .limit(sl.Param("discovery_limit", default=15))
    )
    
    # Step 2: Focused exploration by relevance
    focused_exploration = (
        sl.Query(document_index)
        .find(legal_document)
        .similar(content_space.text, sl.Param("refined_query"))
        .similar(document_type_space, sl.Param("preferred_type"))
        .similar(jurisdiction_space, sl.Param("target_jurisdiction"))
        .select_all()
        .limit(sl.Param("exploration_limit", default=8))
    )
    
    # Step 3: Deep dive for citations and details
    citation_deep_dive = (
        sl.Query(chunk_index)
        .find(chunk_schema)
        .similar(chunk_content_space.text, sl.Param("specific_terms"))
        .similar(chunk_type_space, sl.Param("source_type"))
        .select_all()
        .limit(sl.Param("deep_dive_limit", default=25))
    )
    
    return {
        "initial_discovery": initial_discovery,
        "focused_exploration": focused_exploration, 
        "citation_deep_dive": citation_deep_dive
    }

# Export layer queries
__all__ = [
    # Discovery layer
    "discovery_query",
    "discovery_by_type_query", 
    "discovery_by_jurisdiction_query",
    
    # Exploration layer
    "exploration_query",
    
    # Deep dive layer
    "deep_dive_query",
    "deep_dive_precise_query",
    
    # Workflow
    "create_research_workflow_queries"
]