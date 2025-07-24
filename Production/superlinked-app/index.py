from superlinked import framework as sl


@sl.schema
class LegalDocument:
    # Core fields (proven working)
    id: sl.IdField
    title: sl.String
    content: sl.String
    document_type: sl.String  # statute, case, regulation, etc.
    jurisdiction: sl.String  # federal, texas, california, etc.
    
    # PHASE 1 EXPANSION: AI Preprocessing Fields (using proven sl.String)
    # These fields are populated from our existing processed metadata
    extracted_facts: sl.String       # JSON array of facts with citations
    executive_summary: sl.String     # One-page executive summary  
    key_findings: sl.String          # Most important facts/findings
    key_takeaways: sl.String         # Plain-language explanations
    
    # PHASE 1 EXPANSION: Hierarchical Fields (using proven sl.String)
    jurisdiction_state: sl.String    # texas, california, etc.
    jurisdiction_city: sl.String     # houston, los_angeles, etc.
    practice_area_primary: sl.String # litigation, corporate, etc.
    practice_area_secondary: sl.String # personal_injury, medical_malpractice, etc.
    
    # PHASE 1 EXPANSION: Content Enhancement (using proven sl.String)  
    legal_topics: sl.String          # Specific legal concepts
    keywords: sl.String              # Important search terms
    
    # PHASE 2 EXPANSION: Testing new datatypes
    publication_date: sl.Timestamp      # Testing sl.Timestamp datatype ✅
    confidence_score: sl.Integer         # Testing sl.Integer datatype ✅
    
    # PHASE 1A: Document Metadata Fields (ready-to-use from existing metadata)
    source_filename: sl.String           # Original PDF filename
    file_size_bytes: sl.Integer          # Document file size
    total_pages: sl.Integer              # Number of pages in document
    total_chars: sl.Integer              # Total character count
    fact_count: sl.Integer               # Number of extracted facts
    
    # PHASE 1A: Enhanced Content Fields (ready-to-use from existing metadata)
    summary_bullet_points: sl.String    # Structured bullet point summary
    summary_conclusion: sl.String       # Final conclusion/takeaway
    
    # PHASE 1A: Processing Metadata Fields (ready-to-use from existing metadata)
    ai_model: sl.String                  # AI model used for processing
    preprocessing_version: sl.String     # Version of preprocessing pipeline


legal_document = LegalDocument()

# Core text similarity spaces for legal document search
title_space = sl.TextSimilaritySpace(text=legal_document.title, model="all-MiniLM-L6-v2")
content_space = sl.TextSimilaritySpace(text=legal_document.content, model="all-MiniLM-L6-v2")

# PHASE 3: AI Preprocessing Spaces
# High-quality spaces for AI-processed content with better model
executive_summary_space = sl.TextSimilaritySpace(
    text=legal_document.executive_summary, 
    model="sentence-transformers/all-mpnet-base-v2"
)

key_findings_space = sl.TextSimilaritySpace(
    text=legal_document.key_findings,
    model="sentence-transformers/all-mpnet-base-v2"
)

key_takeaways_space = sl.TextSimilaritySpace(
    text=legal_document.key_takeaways,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Extracted facts space for precise fact retrieval
extracted_facts_space = sl.TextSimilaritySpace(
    text=legal_document.extracted_facts,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Categorical space for document type filtering
document_type_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.document_type,
    categories=["statute", "case", "regulation", "guidance", "rule", "other"],
    negative_filter=-1.0,  # Penalize non-matching categories
    uncategorized_as_category=True  # Treat unknown types as "other"
)

# Categorical space for jurisdiction filtering
jurisdiction_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.jurisdiction,
    categories=["federal", "texas", "california", "new_york", "florida", "other"],
    negative_filter=-1.0,  # Penalize non-matching jurisdictions
    uncategorized_as_category=True  # Treat unknown jurisdictions as "other"
)

# PHASE 3: Hierarchical Jurisdiction Spaces
# Fine-grained jurisdiction filtering with state/city hierarchy
jurisdiction_state_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.jurisdiction_state,
    categories=["texas", "california", "new_york", "florida", "illinois", "other"],
    negative_filter=-1.0,
    uncategorized_as_category=True
)

jurisdiction_city_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.jurisdiction_city,
    categories=["houston", "dallas", "austin", "san_antonio", "los_angeles", "san_francisco", "chicago", "new_york", "other"],
    negative_filter=-1.0,
    uncategorized_as_category=True
)

# Practice Area Hierarchical Spaces
practice_area_primary_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_area_primary,
    categories=["litigation", "healthcare", "regulatory", "corporate", "criminal", "other"],
    negative_filter=-1.0,
    uncategorized_as_category=True
)

practice_area_secondary_space = sl.CategoricalSimilaritySpace(
    category_input=legal_document.practice_area_secondary,
    categories=["medical_malpractice", "personal_injury", "healthcare_compliance", "data_privacy", "general_litigation", "other"],
    negative_filter=-1.0,
    uncategorized_as_category=True
)

# PHASE 3: Content Enhancement Spaces
# Semantic spaces for legal topics and keywords
legal_topics_space = sl.TextSimilaritySpace(
    text=legal_document.legal_topics,
    model="sentence-transformers/all-mpnet-base-v2"
)

keywords_space = sl.TextSimilaritySpace(
    text=legal_document.keywords,
    model="sentence-transformers/all-mpnet-base-v2"
)

# PHASE 1A: Document Metrics Spaces
# Numerical spaces for document characteristics and quality metrics
total_pages_space = sl.NumberSpace(
    number=legal_document.total_pages,
    min_value=1,
    max_value=1000,
    mode=sl.Mode.MAXIMUM  # Prioritize longer documents when relevant
)

fact_count_space = sl.NumberSpace(
    number=legal_document.fact_count,
    min_value=0,
    max_value=100,
    mode=sl.Mode.MAXIMUM  # Prioritize documents with more facts
)

# Enhanced content spaces using the new summary fields
summary_bullet_points_space = sl.TextSimilaritySpace(
    text=legal_document.summary_bullet_points,
    model="sentence-transformers/all-mpnet-base-v2"
)

summary_conclusion_space = sl.TextSimilaritySpace(
    text=legal_document.summary_conclusion,
    model="sentence-transformers/all-mpnet-base-v2"
)

# Create index with Phase 1A enhanced comprehensive spaces
index = sl.Index([
    # Core spaces
    title_space, content_space, document_type_space, jurisdiction_space,
    
    # Phase 3: AI Preprocessing Spaces  
    executive_summary_space, key_findings_space, key_takeaways_space, extracted_facts_space,
    
    # Phase 3: Hierarchical Spaces
    jurisdiction_state_space, jurisdiction_city_space, 
    practice_area_primary_space, practice_area_secondary_space,
    
    # Phase 3: Content Enhancement Spaces for semantic search
    legal_topics_space, keywords_space,
    
    # Phase 1A: Document Metrics & Enhanced Summary Spaces
    total_pages_space, fact_count_space, summary_bullet_points_space, summary_conclusion_space
])
