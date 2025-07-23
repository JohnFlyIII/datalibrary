from superlinked import framework as sl

from .index import title_space, content_space, document_type_space, jurisdiction_space, legal_document, index

query = (
    sl.Query(index)
    .find(legal_document)
    .similar(title_space.text, sl.Param("title_query"))
    .similar(content_space.text, sl.Param("content_query"))
    .similar(document_type_space, sl.Param("document_type"))
    .similar(jurisdiction_space, sl.Param("jurisdiction"))
    .select_all()
    .limit(sl.Param("limit"))
)
