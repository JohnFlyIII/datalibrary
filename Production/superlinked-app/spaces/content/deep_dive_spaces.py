"""
Deep Dive Layer Content Spaces

Purpose:
- Enable detailed, full-precision searches
- Support comprehensive legal research
- Facilitate citation and precedent analysis

Usage:
- Final-stage detailed research
- Full-text searches with context
- Citation network exploration
- Precedent and case law analysis

Human Note: Deep dive spaces provide maximum detail and precision
AI Agent Note: Use these spaces for thorough analysis after exploration
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Full Content Space - Complete document text
deep_dive_content_space = sl.TextSimilaritySpace(
    text=legal_document.content_text,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=500, chunk_overlap=100)
)

# Case Precedents Space - Related case law
deep_dive_precedents_space = sl.TextSimilaritySpace(
    text=legal_document.case_precedents,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Citation Context Space - Cross-document connections
deep_dive_citations_space = sl.TextSimilaritySpace(
    text=legal_document.citation_context,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Legislative History Space - Background and development
legislative_history_space = sl.TextSimilaritySpace(
    text=legal_document.legislative_history,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=600, chunk_overlap=100)
)

# Related Documents Space - Conceptual connections
related_documents_space = sl.TextSimilaritySpace(
    text=legal_document.related_documents,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Legal Topics Space - Detailed concept matching
legal_topics_space = sl.TextSimilaritySpace(
    text=legal_document.legal_topics,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Keywords Space - Important search terms
keywords_space = sl.TextSimilaritySpace(
    text=legal_document.keywords,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Synonyms Space - Alternative terminology
synonyms_space = sl.TextSimilaritySpace(
    text=legal_document.synonyms,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Chunk Context Space - For precise citation
chunk_context_space = sl.TextSimilaritySpace(
    text=legal_document.chunk_context,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Acronyms and Abbreviations Space
acronyms_space = sl.TextSimilaritySpace(
    text=legal_document.acronyms_abbreviations,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Deep Dive Collections
DEEP_DIVE_CONTENT_SPACES = [
    deep_dive_content_space,
    deep_dive_precedents_space,
    deep_dive_citations_space,
    legislative_history_space
]

DEEP_DIVE_REFERENCE_SPACES = [
    related_documents_space,
    legal_topics_space,
    chunk_context_space
]

DEEP_DIVE_SEARCH_SPACES = [
    keywords_space,
    synonyms_space,
    acronyms_space,
    legal_topics_space
]

ALL_DEEP_DIVE_SPACES = (
    DEEP_DIVE_CONTENT_SPACES + 
    DEEP_DIVE_REFERENCE_SPACES + 
    DEEP_DIVE_SEARCH_SPACES
)

# Export all spaces
__all__ = [
    'deep_dive_content_space',
    'deep_dive_precedents_space',
    'deep_dive_citations_space',
    'legislative_history_space',
    'related_documents_space',
    'legal_topics_space',
    'keywords_space',
    'synonyms_space',
    'chunk_context_space',
    'acronyms_space',
    'DEEP_DIVE_CONTENT_SPACES',
    'DEEP_DIVE_REFERENCE_SPACES',
    'DEEP_DIVE_SEARCH_SPACES',
    'ALL_DEEP_DIVE_SPACES'
]

# Usage Examples:
"""
Deep Dive Query Patterns:

1. Full Text Research:
   weights = {
       deep_dive_content_space: 3.0,
       keywords_space: 2.0,
       synonyms_space: 1.5,
       legal_topics_space: 2.0
   }

2. Precedent Analysis:
   weights = {
       deep_dive_precedents_space: 3.0,
       deep_dive_citations_space: 2.5,
       related_documents_space: 2.0,
       legislative_history_space: 1.5
   }

3. Citation Network:
   weights = {
       deep_dive_citations_space: 3.0,
       chunk_context_space: 2.5,
       related_documents_space: 2.0,
       deep_dive_content_space: 1.5
   }

4. Historical Context:
   weights = {
       legislative_history_space: 3.0,
       deep_dive_precedents_space: 2.0,
       deep_dive_citations_space: 2.0,
       deep_dive_content_space: 1.5
   }

5. Comprehensive Analysis:
   weights = {
       deep_dive_content_space: 2.5,
       deep_dive_precedents_space: 2.5,
       deep_dive_citations_space: 2.0,
       legislative_history_space: 2.0,
       related_documents_space: 1.5,
       legal_topics_space: 1.5
   }
"""