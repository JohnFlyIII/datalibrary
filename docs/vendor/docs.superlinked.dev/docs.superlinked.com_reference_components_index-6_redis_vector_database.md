---
url: "https://docs.superlinked.com/reference/components/index-6/redis_vector_database"
title: "Redis Vector Database | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-6/redis_vector_database\#classes)    Classes

`RedisVectorDatabase(host: str, port: int, default_query_limit: int = 10, search_algorithm: superlinked.framework.common.storage.search_index.search_algorithm.SearchAlgorithm = SearchAlgorithm.FLAT, **extra_params: Any)`
: Redis implementation of the VectorDatabase.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
This class provides a Redis-based vector database connector.

Initialize the RedisVectorDatabase.

Args:
    host (str): The hostname of the Redis server.
    port (int): The port number of the Redis server.
    default_query_limit (int): Default vector search limit, set to Redis's default of 10.
    search_algorithm (SearchAlgorithm): The algorithm to use for vector search. Defaults to FLAT.
    **extra_params (Any): Additional parameters for the Redis connection.

### Ancestors (in MRO)

* superlinked.framework.dsl.storage.vector_database.VectorDatabase
* abc.ABC
* typing.Generic
```

[PreviousIn Memory Vector Database](https://docs.superlinked.com/reference/components/index-6/in_memory_vector_database) [NextMongo Db Vector Database](https://docs.superlinked.com/reference/components/index-6/mongo_db_vector_database)

Last updated 2 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject