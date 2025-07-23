from superlinked import framework as sl


@sl.schema
class LegalDocument:
    id: sl.IdField
    title: sl.String
    content: sl.String
    document_type: sl.String  # statute, case, regulation, etc.
    jurisdiction: sl.String  # federal, texas, california, etc.
    # publication_date: sl.Timestamp  # Will add in Phase 3


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
