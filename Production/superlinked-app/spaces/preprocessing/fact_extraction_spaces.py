"""
Fact Extraction Spaces

Purpose:
- Enable search within AI-extracted facts and findings
- Support citation-aware fact retrieval
- Facilitate fact-based legal research

Usage:
- Search for specific facts across documents
- Find documents with similar factual patterns
- Locate source citations for facts
- Analyze fact density and distribution

Human Note: Facts are extracted with APA 7th citations during preprocessing
AI Agent Note: Use these spaces for evidence-based searches and fact verification
"""

import superlinked as sl
from schema.base.legal_document import LegalDocument

# Initialize the legal document schema
legal_document = LegalDocument()

# Extracted Facts Space - Search within extracted facts
extracted_facts_space = sl.TextSimilaritySpace(
    text=legal_document.extracted_facts,
    model="sentence-transformers/all-mpnet-base-v2",
    chunking=sl.Chunking(chunk_size=200, chunk_overlap=50)
)

# Key Findings Space - Most important facts
key_findings_space = sl.TextSimilaritySpace(
    text=legal_document.key_findings,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Fact Locations Space - Find facts by location reference
fact_locations_space = sl.TextSimilaritySpace(
    text=legal_document.fact_locations,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Fact Density Space - Documents with many relevant facts
fact_count_space = sl.NumberSpace(
    number=legal_document.fact_count,
    min_value=0,
    max_value=1000,
    mode=sl.Mode.MAXIMUM
)

# Citation Space - APA formatted citations
citations_apa_space = sl.TextSimilaritySpace(
    text=legal_document.citations_apa7,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Internal Citations Space
internal_citations_space = sl.TextSimilaritySpace(
    text=legal_document.internal_citations,
    model="sentence-transformers/all-mpnet-base-v2"
)

# External Citations Space
external_citations_space = sl.TextSimilaritySpace(
    text=legal_document.external_citations,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Fact Extraction Collections
FACT_EXTRACTION_SPACES = [
    extracted_facts_space,
    key_findings_space,
    fact_locations_space,
    fact_count_space
]

CITATION_SPACES = [
    citations_apa_space,
    internal_citations_space,
    external_citations_space
]

ALL_FACT_SPACES = FACT_EXTRACTION_SPACES + CITATION_SPACES

# Export all spaces
__all__ = [
    'extracted_facts_space',
    'key_findings_space',
    'fact_locations_space',
    'fact_count_space',
    'citations_apa_space',
    'internal_citations_space',
    'external_citations_space',
    'FACT_EXTRACTION_SPACES',
    'CITATION_SPACES',
    'ALL_FACT_SPACES'
]

# Usage Examples:
"""
Fact-Based Query Patterns:

1. Find Specific Facts:
   weights = {
       extracted_facts_space: 3.0,
       key_findings_space: 2.0,
       fact_locations_space: 1.0
   }

2. High Fact Density Documents:
   weights = {
       fact_count_space: 3.0,
       extracted_facts_space: 2.0
   }

3. Citation Verification:
   weights = {
       citations_apa_space: 3.0,
       fact_locations_space: 2.0,
       extracted_facts_space: 1.5
   }

4. Cross-Reference Search:
   weights = {
       internal_citations_space: 2.5,
       external_citations_space: 2.5,
       citations_apa_space: 2.0
   }
"""