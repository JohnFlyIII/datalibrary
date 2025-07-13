---
url: "https://docs.superlinked.com/reference/components/index-6/topk_vector_database"
title: "Topk Vector Database | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-6/topk_vector_database\#classes)    Classes

`TopKVectorDatabase(api_key: str, region: str, https: bool = True, host: str = 'topk.io', default_query_limit: int = 10)`
: TopK implementation of the VectorDatabase.
This class provides a TopK-based vector database connector.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the TopKVectorDatabase.
Args:
    api_key (str): The API key for the TopK server.
    region (str): The region of the TopK server.
    https (bool): Whether to use HTTPS for the TopK server.
    host (str): The host of the TopK server.
    default_query_limit (int): Default vector search limit, set to TopK's default of 10.

### Ancestors (in MRO)

* superlinked.framework.dsl.storage.vector_database.VectorDatabase
* abc.ABC
* typing.Generic
```

[PreviousQdrant Vector Database](https://docs.superlinked.com/reference/components/index-6/qdrant_vector_database) [NextIn Memory Vector Database](https://docs.superlinked.com/reference/components/index-6/in_memory_vector_database)

Last updated 5 days ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject