from superlinked import framework as sl

from .index import title_space, content_space, legal_document, index

query = (
    sl.Query(index)
    .find(legal_document)
    .similar(title_space.text, sl.Param("title_query"))
    .similar(content_space.text, sl.Param("content_query"))
    .select_all()
    .limit(sl.Param("limit"))
)
