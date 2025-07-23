from superlinked import framework as sl


@sl.schema
class LegalDocument:
    id: sl.IdField
    title: sl.String
    content: sl.String


legal_document = LegalDocument()

# Text similarity spaces for legal document search
title_space = sl.TextSimilaritySpace(text=legal_document.title, model="all-MiniLM-L6-v2")
content_space = sl.TextSimilaritySpace(text=legal_document.content, model="all-MiniLM-L6-v2")

# Create index with both title and content spaces
index = sl.Index([title_space, content_space])
