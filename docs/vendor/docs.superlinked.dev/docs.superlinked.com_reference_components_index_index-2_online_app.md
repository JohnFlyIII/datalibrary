---
url: "https://docs.superlinked.com/reference/components/index/index-2/online_app"
title: "Online App | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index/index-2/online_app\#classes)    Classes

`OnlineApp(sources: Sequence[~OnlineSourceT], indices: Sequence[superlinked.framework.dsl.index.index.Index], vector_database: superlinked.framework.dsl.storage.vector_database.VectorDatabase, context: superlinked.framework.common.dag.context.ExecutionContext, init_search_indices: bool, queue: superlinked.framework.queue.interface.queue.Queue | None = None, blob_handler: superlinked.framework.blob.blob_handler.BlobHandler | None = None, query_result_converter: superlinked.framework.dsl.query.query_result_converter.query_result_converter.QueryResultConverter | None = None)` : Manages the execution environment for online sources and indices.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
This class extends the base App class and incorporates the QueryMixin to handle
query execution. It is designed to work with online sources and indices, providing
the necessary setup and management for efficient data processing and querying.

Initialize the OnlineApp with the given sources, indices, vector database, and execution context.

Args:
    sources (Sequence[OnlineSourceT]): A sequence of data sources to be used by the application.
    indices (Sequence[Index]): A sequence of indices for data retrieval and storage.
    vector_database (VectorDatabase): The vector database instance for managing vector data.
    context (ExecutionContext): The execution context providing necessary runtime information.
    source_to_queue_map (dict[OnlineSourceT, Queue] | None): a mapping from sources
        to messaging queues persisting the ingested data on the given source; defaults to None.

### Ancestors (in MRO)

* superlinked.framework.dsl.app.app.App
* abc.ABC
* typing.Generic
* superlinked.framework.dsl.query.query_mixin.QueryMixin

### Descendants

* superlinked.framework.dsl.app.interactive.interactive_app.InteractiveApp
* superlinked.framework.dsl.app.rest.rest_app.RestApp

### Class variables

`INGEST_MESSAGE_TYPE`
:
```

[PreviousOnline](https://docs.superlinked.com/reference/components/index/index-2) [NextInteractive](https://docs.superlinked.com/reference/components/index/index-3)

Last updated 5 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject