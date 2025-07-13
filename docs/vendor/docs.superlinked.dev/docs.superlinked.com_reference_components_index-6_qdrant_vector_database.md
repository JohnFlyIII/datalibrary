---
url: "https://docs.superlinked.com/reference/components/index-6/qdrant_vector_database"
title: "Qdrant Vector Database | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index-6/qdrant_vector_database\#classes)    Classes

`QdrantVectorDatabase(url: str, api_key: str, default_query_limit: int = 10, timeout: int | None = None, search_algorithm: superlinked.framework.common.storage.search_index.search_algorithm.SearchAlgorithm = SearchAlgorithm.FLAT, prefer_grpc: bool | None = None, **extra_params: Any)`
: Qdrant implementation of the VectorDatabase.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
This class provides a Qdrant-based vector database connector.

Initialize the QdrantVectorDatabase.

Args:
    url (str): The url of the Qdrant server.
    api_key (str): The api key of the Qdrant cluster.
    default_query_limit (int): Default vector search limit, set to Qdrant's default of 10.
    timeout (int | None): Timeout in seconds for Qdrant operations. Default is 5 seconds.
    prefer_grpc (bool | None): Whether to prefer gRPC for Qdrant operations. Default is False.
    **extra_params (Any): Additional parameters for the Qdrant connection.

### Ancestors (in MRO)

* superlinked.framework.dsl.storage.vector_database.VectorDatabase
* abc.ABC
* typing.Generic
```

[PreviousStorage](https://docs.superlinked.com/reference/components/index-6) [NextTopk Vector Database](https://docs.superlinked.com/reference/components/index-6/topk_vector_database)

Last updated 1 month ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject