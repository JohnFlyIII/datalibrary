import os
from superlinked import framework as sl

from .index import legal_document, index
from .query import query

document_source: sl.RestSource = sl.RestSource(legal_document)

# Use Qdrant for production
vector_database = sl.QdrantVectorDatabase(
    url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None),
)

executor = sl.RestExecutor(
    sources=[document_source],
    indices=[index],
    queries=[sl.RestQuery(sl.RestDescriptor("search"), query)],
    vector_database=vector_database,
)

sl.SuperlinkedRegistry.register(executor)
