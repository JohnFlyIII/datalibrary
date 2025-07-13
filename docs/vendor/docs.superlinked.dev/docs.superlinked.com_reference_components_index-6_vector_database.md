---
url: "https://docs.superlinked.com/reference/components/index-6/vector_database"
title: "Vector Database | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-6/vector_database\#classes)    Classes

`VectorDatabase()`
: Abstract base class for a Vector Database.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
This class serves as a blueprint for vector databases, ensuring that any concrete implementation
provides a connector to the vector database.

Attributes:
    _vdb_connector (VDBConnectorT): An abstract property that should return an instance of a VDBConnector.

### Ancestors (in MRO)

* abc.ABC
* typing.Generic

### Descendants

* superlinked.framework.dsl.storage.in_memory_vector_database.InMemoryVectorDatabase
* superlinked.framework.dsl.storage.mongo_db_vector_database.MongoDBVectorDatabase
* superlinked.framework.dsl.storage.qdrant_vector_database.QdrantVectorDatabase
* superlinked.framework.dsl.storage.redis_vector_database.RedisVectorDatabase
* superlinked.framework.dsl.storage.topk_vector_database.TopKVectorDatabase
```

[PreviousMongo Db Vector Database](https://docs.superlinked.com/reference/components/index-6/mongo_db_vector_database) [NextIndex](https://docs.superlinked.com/reference/components/index-7)

Last updated 5 days ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject