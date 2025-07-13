---
url: "https://docs.superlinked.com/reference/components/index-6/in_memory_vector_database"
title: "In Memory Vector Database | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-6/in_memory_vector_database\#classes)    Classes

`InMemoryVectorDatabase(default_query_limit: int = -1)` : In-memory implementation of the VectorDatabase.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
This class provides an in-memory vector database connector, which is useful for testing
and development purposes.

Initialize the InMemoryVectorDatabase.

Args:
    default_query_limit (int): The default limit for query results. A value of -1 indicates no limit.

Sets up an in-memory vector DB connector for testing and development.

### Ancestors (in MRO)

* superlinked.framework.dsl.storage.vector_database.VectorDatabase
* abc.ABC
* typing.Generic
```

[PreviousTopk Vector Database](https://docs.superlinked.com/reference/components/index-6/topk_vector_database) [NextRedis Vector Database](https://docs.superlinked.com/reference/components/index-6/redis_vector_database)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject