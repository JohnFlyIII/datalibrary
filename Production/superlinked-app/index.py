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
    confidence_score: sl.Integer         # Testing sl.Integer datatype


legal_document = LegalDocument()

# Text similarity spaces for legal document search
title_space = sl.TextSimilaritySpace(text=legal_document.title, model="all-MiniLM-L6-v2")
content_space = sl.TextSimilaritySpace(text=legal_document.content, model="all-MiniLM-L6-v2")

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

# Create index with current working spaces (will add recency in Phase 3)
index = sl.Index([title_space, content_space, document_type_space, jurisdiction_space])
