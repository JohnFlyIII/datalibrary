import os
from superlinked import framework as sl

from .index import car_schema, index
from .query import query

car_source: sl.RestSource = sl.RestSource(car_schema)

# Use Qdrant for production
vector_database = sl.QdrantVectorDatabase(
    url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None),
)

executor = sl.RestExecutor(
    sources=[car_source],
    indices=[index],
    queries=[sl.RestQuery(sl.RestDescriptor("query"), query)],
    vector_database=vector_database,
)

sl.SuperlinkedRegistry.register(executor)
