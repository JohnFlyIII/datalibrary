---
url: "https://docs.superlinked.com/reference/components/index/index-1/rest_app"
title: "Rest App | Superlinked Docs"
---

## [Direct link to heading](https://docs.superlinked.com/reference/components/index/index-1/rest_app\#classes)    Classes

`RestApp(sources: Sequence[superlinked.framework.dsl.source.rest_source.RestSource | superlinked.framework.dsl.source.data_loader_source.DataLoaderSource], indices: Sequence[superlinked.framework.dsl.index.index.Index], queries: Sequence[superlinked.framework.dsl.executor.rest.rest_configuration.RestQuery], vector_database: superlinked.framework.dsl.storage.vector_database.VectorDatabase, context: superlinked.framework.common.dag.context.ExecutionContext, endpoint_configuration: superlinked.framework.dsl.executor.rest.rest_configuration.RestEndpointConfiguration, queue: superlinked.framework.queue.interface.queue.Queue[superlinked.framework.queue.interface.queue_message.MessageBody[dict]] | None = None, blob_handler: superlinked.framework.blob.blob_handler.BlobHandler | None = None)` : Rest implementation of the App class.

Copy

```inline-grid min-w-full grid-cols-[auto_1fr] [count-reset:line] print:whitespace-pre-wrap
Initialize the RestApp from a RestExecutor.

Args:
    sources (Sequence[RestSource | DataLoaderSource]): The list of sources, which can be either
        RestSource or DataLoaderSource.
    indices (Sequence[Index]): The list of indices to be used by the RestApp.
    queries (Sequence[RestQuery]): The list of queries to be executed by the RestApp.
    vector_database (VectorDatabase): The vector database instance to be used by the RestApp.
    context (ExecutionContext): The execution context for the RestApp.
    endpoint_configuration (RestEndpointConfiguration): The configuration for the REST endpoints.
    queue (Queue[dict] | None): a messaging queue persisting the ingested data; defaults to None.

### Ancestors (in MRO)

* superlinked.framework.dsl.app.online.online_app.OnlineApp
* superlinked.framework.dsl.app.app.App
* abc.ABC
* typing.Generic
* superlinked.framework.dsl.query.query_mixin.QueryMixin

### Instance variables

`data_loader_sources: Sequence[superlinked.framework.dsl.source.data_loader_source.DataLoaderSource]`
:   Property that returns the list of DataLoaderSource instances associated with the RestApp.

    Returns:
        Sequence[DataLoaderSource]: A sequence of DataLoaderSource instances.

`handler: superlinked.framework.dsl.executor.rest.rest_handler.RestHandler`
:   Property that returns the RestHandler instance associated with the RestApp.

    Returns:
        RestHandler: An instance of RestHandler.
```

[PreviousRest](https://docs.superlinked.com/reference/components/index/index-1) [NextOnline](https://docs.superlinked.com/reference/components/index/index-2)

Last updated 7 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject