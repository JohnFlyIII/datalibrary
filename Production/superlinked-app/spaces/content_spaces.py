"""
Content Embedding Spaces

This module defines text similarity spaces for different types of legal content.
Each space is optimized for specific search patterns and content types.

Architecture:
- Progressive disclosure: Discovery -> Exploration -> Deep Dive
- Content type specialization: Full text, summaries, provisions
- Performance optimization: Separate spaces for different use cases
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Progressive Disclosure Content Spaces

# Discovery Layer - Broad exploration and topic understanding
discovery_summary_space = sl.TextSimilaritySpace(
    text=legal_document.summary,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=500, chunk_overlap=100)
)

discovery_topics_space = sl.TextSimilaritySpace(
    text=legal_document.broad_topics,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Exploration Layer - Focused analysis and key information
exploration_provisions_space = sl.TextSimilaritySpace(
    text=legal_document.key_provisions,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=300, chunk_overlap=50)
)

exploration_concepts_space = sl.TextSimilaritySpace(
    text=legal_document.legal_concepts,
    model="sentence-transformers/all-mpnet-base-v2"
)

exploration_implications_space = sl.TextSimilaritySpace(
    text=legal_document.practical_implications,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=400, chunk_overlap=75)
)

# Deep Dive Layer - Detailed content and full analysis
deep_dive_content_space = sl.TextSimilaritySpace(
    text=legal_document.content_text,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=500, chunk_overlap=100)
)

deep_dive_precedents_space = sl.TextSimilaritySpace(
    text=legal_document.case_precedents,
    model="sentence-transformers/all-mpnet-base-v2"
)

deep_dive_citations_space = sl.TextSimilaritySpace(
    text=legal_document.citation_context,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Specialized Content Spaces

# Client Communication - Simplified explanations
client_takeaways_space = sl.TextSimilaritySpace(
    text=legal_document.key_takeaways,
    model="sentence-transformers/all-mpnet-base-v2"
)

client_questions_space = sl.TextSimilaritySpace(
    text=legal_document.common_questions,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Compliance & Practice - Action-oriented content
compliance_requirements_space = sl.TextSimilaritySpace(
    text=legal_document.compliance_requirements,
    model="sentence-transformers/all-mpnet-base-v2"
)

penalties_space = sl.TextSimilaritySpace(
    text=legal_document.penalties_consequences,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Search Enhancement - Keyword and terminology matching
keywords_space = sl.TextSimilaritySpace(
    text=legal_document.keywords,
    model="sentence-transformers/all-mpnet-base-v2"
)

synonyms_space = sl.TextSimilaritySpace(
    text=legal_document.synonyms,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Historical & Development - Context and background
legislative_history_space = sl.TextSimilaritySpace(
    text=legal_document.legislative_history,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=600, chunk_overlap=100)
)

# Relationship Content - Cross-document connections
related_documents_space = sl.TextSimilaritySpace(
    text=legal_document.related_documents,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Space Collections for Query Routing

# Discovery Layer Collection
DISCOVERY_SPACES = [
    discovery_summary_space,
    discovery_topics_space,
    client_takeaways_space
]

# Exploration Layer Collection  
EXPLORATION_SPACES = [
    exploration_provisions_space,
    exploration_concepts_space,
    exploration_implications_space,
    compliance_requirements_space
]

# Deep Dive Layer Collection
DEEP_DIVE_SPACES = [
    deep_dive_content_space,
    deep_dive_precedents_space,
    deep_dive_citations_space,
    legislative_history_space
]

# Specialized Collections
CLIENT_COMMUNICATION_SPACES = [
    client_takeaways_space,
    client_questions_space,
    exploration_implications_space
]

COMPLIANCE_SPACES = [
    compliance_requirements_space,
    penalties_space,
    exploration_provisions_space
]

RESEARCH_SPACES = [
    deep_dive_content_space,
    deep_dive_precedents_space,
    deep_dive_citations_space,
    related_documents_space
]

SEARCH_ENHANCEMENT_SPACES = [
    keywords_space,
    synonyms_space,
    discovery_summary_space
]